#!/usr/bin/env python3
"""Water-loop calibration for a CMP 170HX: how much does more pump / radiator-fan speed actually buy?

Runs gpu_burn on the card and steps pump and radiator-fan duty through a table of set points. At each step it
logs core / HBM temperature, power, SM clock and fan / pump rpm every 5 s and reports the plateau
(median of the last 120 s of the step) and the core-temperature slope over that window (deg C / min).

It does NOT take over the PWM channels itself: it writes the requested duty to an override file that
cmp_cooling_daemon.py honours (and that the daemon ignores 90 s after the last refresh, so a crashed
script is harmless; the daemon's emergency threshold stays active). If you drive your fans some other way,
replace set_override() / clear_override().

  cooling_cal.py --burn-dir /path/to/gpu-burn [--hold 360] [--warmup 300] [--out DIR]
  cooling_cal.py --burn-dir ... --custom 55:100:300,55:70:300,20:50:360     # pump:radiator:seconds

Default sweeps: A) pump 55 %, radiator 100 -> 70 -> 50 -> 35 -> 25 -> 15 %;  B) radiator 50 %, pump 100 -> 70 -> 40 -> 30 -> 20 %.
A step that reaches core >= 68 C or HBM >= 76 C is cut short and the remaining (hotter) steps of that sweep are skipped.
Run on an idle card: the script refuses if utilisation is > 10 %. Needs nvidia-smi and the gpu-burn tool.
Results: samples.csv, summary.json, burn.log in a time-stamped folder under --out.
"""
import argparse, csv, glob, json, os, signal, statistics, subprocess, sys, time

OVERRIDE = "/etc/cmp-cooling/override.json"        # same file the daemon reads
HWMON_CHIP = "nct6798"
RAD_TACHS = ("fan1", "fan4", "fan5")               # radiator fan tach inputs
PUMP_TACH = "fan6"
GPU_NAME_HINTS = ("CMP", "Graphics Device")
LIM_CORE, LIM_HBM = 68, 76                         # cut a step short
ABORT_CORE, ABORT_HBM = 70, 80                     # abort the whole run (daemon panics at 72 / 82)
SAMPLE = 5
RAD_SWEEP = [100, 70, 50, 35, 25, 15]
PUMP_SWEEP = [100, 70, 40, 30, 20]
PUMP_FIXED, RAD_FIXED = 55, 50


def sh(cmd, timeout=15):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def find_gpu():
    out = sh(["nvidia-smi", "--query-gpu=index,name,uuid", "--format=csv,noheader"]).stdout
    for line in out.splitlines():
        i, name, uuid = [x.strip() for x in line.split(",")]
        if any(h in name for h in GPU_NAME_HINTS):
            return int(i), uuid
    sys.exit("CMP not found in nvidia-smi")


def find_hwmon():
    for h in glob.glob("/sys/class/hwmon/hwmon*"):
        if open(h + "/name").read().strip() == HWMON_CHIP:
            return h
    sys.exit(f"hwmon chip {HWMON_CHIP} not found")


H, (GPU, UUID) = find_hwmon(), find_gpu()


def rd(name):
    try:
        return int(open(f"{H}/{name}").read())
    except Exception:
        return None


def sample():
    v = [x.strip() for x in sh(["nvidia-smi", "-i", str(GPU), "--query-gpu=temperature.gpu,temperature.memory,power.draw,clocks.sm,utilization.gpu",
                                "--format=csv,noheader,nounits"]).stdout.strip().split(",")]
    f = lambda x, t=float: t(x) if x.replace(".", "", 1).isdigit() else None
    rads = [rd(f"{n}_input") or 0 for n in RAD_TACHS]
    return dict(core=f(v[0], int), hbm=f(v[1], int), power=f(v[2]), sm=f(v[3], int), util=f(v[4], int),
                rad_rpm=round(sum(rads) / len(rads)), rad_min=min(rads), pump_rpm=rd(f"{PUMP_TACH}_input"))


def set_override(pump, rad):
    os.makedirs(os.path.dirname(OVERRIDE), exist_ok=True)
    tmp = OVERRIDE + ".tmp"
    open(tmp, "w").write(json.dumps({"pump": pump, "rad": rad, "until": time.time() + 90}))
    os.replace(tmp, OVERRIDE)


def clear_override():
    try:
        os.remove(OVERRIDE)
    except OSError:
        pass


def slope_per_min(pts):
    if len(pts) < 4:
        return None
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    mx, my = statistics.mean(xs), statistics.mean(ys)
    den = sum((x - mx) ** 2 for x in xs)
    return 60 * sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den if den else None


class Run:
    def __init__(self, out, burn_dir, hold, warmup, custom):
        self.burn_dir, self.hold, self.warmup, self.custom = burn_dir, hold, warmup, custom
        self.dir = f"{out}/{time.strftime('%Y%m%d-%H%M%S')}"
        os.makedirs(self.dir, exist_ok=True)
        self.csv = open(f"{self.dir}/samples.csv", "w", newline="")
        self.w = csv.writer(self.csv)
        self.w.writerow(["t", "label", "pump_set", "rad_set", "core", "hbm", "power", "sm", "rad_rpm", "rad_min", "pump_rpm"])
        self.t0, self.burn, self.results, self.aborted = time.time(), None, [], None

    def log(self, s):
        print(time.strftime("%H:%M:%S ") + s, flush=True)

    def hold_point(self, label, pump, rad, seconds):
        end, pts, last_ov, hit = time.time() + seconds, [], 0, None
        while time.time() < end:
            if time.time() - last_ov > 30:
                set_override(pump, rad)
                last_ov = time.time()
            s = sample()
            now = time.time() - self.t0
            self.w.writerow([round(now), label, pump, rad, s["core"], s["hbm"], s["power"], s["sm"], s["rad_rpm"], s["rad_min"], s["pump_rpm"]])
            self.csv.flush()
            if s["core"] is None:
                time.sleep(SAMPLE)
                continue
            pts.append((now, s))
            if self.burn is not None and self.burn.poll() is not None:
                self.aborted = "gpu_burn exited early"
                break
            if s["core"] >= ABORT_CORE or (s["hbm"] or 0) >= ABORT_HBM:
                self.aborted = f"abort threshold: core {s['core']} / HBM {s['hbm']}"
                break
            if label != "warmup" and (s["core"] >= LIM_CORE or (s["hbm"] or 0) >= LIM_HBM):
                hit = f"step limit: core {s['core']} / HBM {s['hbm']}"
                break
            time.sleep(SAMPLE)
        tail = [(t, s) for t, s in pts if t >= pts[-1][0] - 120] if pts else []
        med = lambda k: round(statistics.median([s[k] for _, s in tail if s[k] is not None]), 1) if tail else None
        sl = slope_per_min([(t, s["core"]) for t, s in tail]) if tail else None
        return dict(label=label, pump_set=pump, rad_set=rad, core=med("core"), hbm=med("hbm"), power=med("power"), sm=med("sm"),
                    rad_rpm=med("rad_rpm"), rad_min=med("rad_min"), pump_rpm=med("pump_rpm"),
                    slope_core=round(sl, 2) if sl is not None else None, limit=hit)

    def report(self, r):
        self.log(f"   core {r['core']} / HBM {r['hbm']} C, {r['power']} W, radiator {r['rad_rpm']} rpm (min {r['rad_min']}), "
                 f"pump {r['pump_rpm']} rpm, slope {r['slope_core']} C/min" + (f"  [{r['limit']}]" if r["limit"] else ""))

    def sweep(self, name, points):
        skipped = False
        for pump, rad in points:
            label = f"{name}: pump {pump}% rad {rad}%"
            if skipped:
                self.results.append(dict(label=label, pump_set=pump, rad_set=rad, skipped="skipped: previous step hit the limit"))
                continue
            self.log(f"-> {label}")
            r = self.hold_point(label, pump, rad, self.hold)
            r["sweep"] = name
            self.results.append(r)
            self.report(r)
            skipped = bool(r["limit"])
            if self.aborted:
                return

    def run_custom(self):
        for pump, rad, secs in self.custom:
            label = f"C: pump {pump}% rad {rad}%"
            self.log(f"-> {label} ({secs} s)")
            r = self.hold_point(label, pump, rad, secs)
            r["sweep"] = "C"
            self.results.append(r)
            self.report(r)
            if r["limit"] or self.aborted:
                return

    def run(self):
        total = self.warmup + 180 + (sum(x[2] for x in self.custom) if self.custom else self.hold * (len(RAD_SWEEP) + len(PUMP_SWEEP)))
        self.log(f"step {self.hold} s, warm-up {self.warmup} s, about {round(total / 60)} min; output {self.dir}")
        env = dict(os.environ, CUDA_VISIBLE_DEVICES=UUID)
        self.burnlog = open(f"{self.dir}/burn.log", "w")
        self.burn = subprocess.Popen([f"{self.burn_dir}/gpu_burn", "-stts", "2", "-i", "0", "-m", "90%", str(int(total))],
                                     stdout=self.burnlog, stderr=subprocess.STDOUT, cwd=self.burn_dir, env=env, start_new_session=True)
        time.sleep(20)
        self.log("-> warm-up (pump 55 %, radiator 50 %)")
        r = self.hold_point("warmup", PUMP_FIXED, RAD_FIXED, self.warmup)
        self.log(f"   after warm-up: core {r['core']} / HBM {r['hbm']} C")
        if self.aborted:
            return
        if self.custom:
            self.run_custom()
        else:
            self.sweep("A", [(PUMP_FIXED, x) for x in RAD_SWEEP])
            if not self.aborted:
                self.sweep("B", [(p, RAD_FIXED) for p in PUMP_SWEEP])

    def stop_burn(self):
        p = self.burn
        if not p:
            return

        def alive():
            p.poll()
            try:
                os.killpg(p.pid, 0)
                return True
            except ProcessLookupError:
                return False
            except PermissionError:
                return True
        for sig, tries in ((signal.SIGTERM, 40), (signal.SIGKILL, 40)):
            if not alive():
                return
            try:
                os.killpg(p.pid, sig)
            except OSError:
                pass
            for _ in range(tries):
                if not alive():
                    return
                time.sleep(0.25)

    def finish(self):
        clear_override()
        self.stop_burn()
        tail = []
        try:
            tail = [l for l in open(f"{self.dir}/burn.log").read().splitlines() if "errors" in l.lower()][-1:]
        except Exception:
            pass
        json.dump(dict(aborted=self.aborted, burn_tail=tail, results=self.results), open(f"{self.dir}/summary.json", "w"), indent=1)
        self.log("=== SUMMARY ===" + (f"  (aborted: {self.aborted})" if self.aborted else ""))
        print(f"{'step':28} {'core':>5} {'HBM':>5} {'W':>5} {'rad rpm':>8} {'pump rpm':>9} {'dT/min':>7}")
        for r in self.results:
            if r.get("skipped"):
                print(f"{r['label']:28} - {r['skipped']}")
            else:
                print(f"{r['label']:28} {r['core']:>5} {r['hbm']:>5} {r['power']:>5} {r['rad_rpm']:>8} {r['pump_rpm']:>9} {str(r['slope_core']):>7}"
                      + ("  LIMIT" if r["limit"] else ""))
        print("burn:", tail)
        self.csv.close()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--burn-dir", required=True, help="directory containing the gpu_burn binary")
    ap.add_argument("--out", default="./results")
    ap.add_argument("--hold", type=int, default=360, help="seconds per step (default 360)")
    ap.add_argument("--warmup", type=int, default=300)
    ap.add_argument("--custom", help="explicit steps pump:radiator:seconds, comma separated")
    a = ap.parse_args()
    custom = [tuple(int(x) for x in t.split(":")) for t in a.custom.split(",")] if a.custom else None
    util = float(sh(["nvidia-smi", "-i", str(GPU), "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"]).stdout.strip())
    if util > 10:
        sys.exit(f"card busy (utilisation {util} %): run the calibration on an idle card")
    run = Run(a.out, a.burn_dir, a.hold, a.warmup, custom)

    def bail(*_):
        run.aborted = "stopped by signal"
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, bail)
    try:
        run.run()
    except KeyboardInterrupt:
        pass
    finally:
        run.finish()


if __name__ == "__main__":
    main()
