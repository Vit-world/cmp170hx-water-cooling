#!/usr/bin/env python3
"""Closed-loop cooling daemon for a CMP 170HX on a water loop, driven from motherboard fan headers.

Reads the card's core and HBM temperature from nvidia-smi and sets the PWM of
  * the pump (AIO_PUMP header) and
  * N radiator fans (one PWM channel each, same duty on all)
through the Nuvoton NCT6798 hwmon driver (kernel module nct6775). Pump and fan curves are
temperature -> duty tables taken from the calibration in this repository (see README.md).

Safety behaviour
  * any error, card missing from nvidia-smi, SIGTERM/SIGINT -> pump and radiator fans to 100 %
  * emergency threshold (core >= PANIC_CORE or HBM >= PANIC_MEM) -> 100 % on everything, whatever the profile or override
  * stall watchdog: a radiator fan reporting 0 rpm for 15 s at duty >= ~8 % is logged and the other fans
    are raised to at least FAULT_RAD_PCT
  * manual override (used by cooling_cal.py): a JSON file {"pump": %, "rad": %, "until": unix_time
    [, "max_core": C, "max_mem": C]} is honoured only while "until" is in the future (the writer must keep
    refreshing it) and, if given, only while the card is cooler than max_core / max_mem.

Everything hardware-specific is in the CONFIG block below; adapt the pwm/fan numbers to your board
(`grep . /sys/class/hwmon/hwmon*/name`, then drive each pwmN to 100 % and watch which fanN reports rpm).
Run as root. Linux only.
"""
import glob, json, signal, subprocess, sys, time

# ---------------------------------------------------------------- CONFIG
HWMON_CHIP = "nct6798"                    # name of the hwmon device with the fan headers
PUMP = "pwm6"                             # pump header (AIO_PUMP on the tested board)
RADS = ("pwm1", "pwm4", "pwm5")           # radiator fan headers (CHA_FAN1/2/3 on the tested board)
TACH = {"pwm1": "fan1", "pwm4": "fan4", "pwm5": "fan5"}   # tach input of each radiator channel
PROFILE_FILE = "/etc/cmp-cooling/profile"           # contains "quiet" or "cold"; missing file -> quiet
OVERRIDE_FILE = "/etc/cmp-cooling/override.json"    # manual override, see docstring
PANIC_CORE, PANIC_MEM = 72, 82                      # deg C, everything to 100 % at or above these
PERIOD = 3                                          # seconds between control ticks
DOWN = 10                                           # max PWM decrease per tick (0..255); increases are immediate
STALL_TICKS, STALL_MIN_PWM, FAULT_RAD_PCT = 5, 20, 70
GPU_NAME_HINTS = ("CMP", "Graphics Device")         # nvidia-smi name of the card (the unlocked card reports "Graphics Device")

# (temperature deg C, duty %) curves; the final duty is the max over the core curve and the HBM curve.
#   quiet: pump and fans stay at <= 30 % until the core is ~60 C / HBM ~66 C. Plateau at 250 W: ~59 / 62 C
#   cold : fans up to ~50 %, pump 40-50 %.                                  Plateau at 250 W: ~55 / 60 C
PROFILES = {
    "quiet": dict(
        pump_core=[(50, 30), (62, 30), (70, 45)], pump_mem=[(58, 30), (66, 30), (74, 45)],
        rad_core=[(40, 15), (50, 20), (60, 30), (64, 35), (68, 55), (72, 85), (74, 100)],
        rad_mem=[(55, 15), (62, 25), (66, 30), (70, 40), (75, 65), (80, 90), (82, 100)]),
    "cold": dict(
        pump_core=[(40, 40), (52, 50)], pump_mem=[(52, 40), (62, 50)],
        rad_core=[(35, 30), (45, 40), (55, 50), (60, 70), (64, 100)],
        rad_mem=[(50, 30), (58, 45), (64, 60), (70, 85), (74, 100)]),
}
ALL = (PUMP,) + RADS
# ------------------------------------------------------------------------


def log(msg):
    print(msg, file=sys.stderr, flush=True)


def find_hwmon(name):
    for h in glob.glob("/sys/class/hwmon/hwmon*"):
        try:
            if open(h + "/name").read().strip() == name:
                return h
        except OSError:
            pass
    return None


def interp(curve, t):
    if t <= curve[0][0]:
        return curve[0][1]
    if t >= curve[-1][0]:
        return curve[-1][1]
    for (t1, p1), (t2, p2) in zip(curve, curve[1:]):
        if t1 <= t <= t2:
            return p1 + (p2 - p1) * (t - t1) / (t2 - t1)
    return curve[-1][1]


def profile():
    try:
        name = open(PROFILE_FILE).read().strip()
    except OSError:
        name = ""
    return name if name in PROFILES else "quiet"


def override(core, mem):
    try:
        d = json.load(open(OVERRIDE_FILE))
        if "max_core" in d and (core >= float(d["max_core"]) or mem >= float(d.get("max_mem", 999))):
            return None
        if float(d["until"]) > time.time():
            return max(0.0, min(100.0, float(d["pump"]))), max(0.0, min(100.0, float(d["rad"])))
    except Exception:
        pass
    return None


def gpu_temps():
    """(core, hbm) of the CMP, or (None, None)."""
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=name,temperature.gpu,temperature.memory",
                              "--format=csv,noheader,nounits"], capture_output=True, text=True, timeout=5).stdout
        for line in out.splitlines():
            v = [x.strip() for x in line.split(",")]
            if any(h in v[0] for h in GPU_NAME_HINTS):
                return int(v[1]), (int(v[2]) if v[2].isdigit() else 0)
    except Exception:
        pass
    return None, None


H = find_hwmon(HWMON_CHIP)
if not H:
    log(f"hwmon chip '{HWMON_CHIP}' not found (modprobe nct6775?)")
    sys.exit(1)


def write(ch, val):
    open(f"{H}/{ch}", "w").write(str(int(val)))


def full_blast(*_):
    for ch in ALL:
        try:
            open(f"{H}/{ch}_enable", "w").write("1")
            write(ch, 255)
        except OSError:
            pass
    sys.exit(0)


signal.signal(signal.SIGTERM, full_blast)
signal.signal(signal.SIGINT, full_blast)

for ch in ALL:
    open(f"{H}/{ch}_enable", "w").write("1")        # manual PWM mode
    write(ch, 255)                                  # start at 100 %, ramp down by curve
cur = {ch: 255 for ch in ALL}
stall = {ch: 0 for ch in RADS}
faulty, manual, missing, active = set(), False, 0, None

while True:
    core, mem = gpu_temps()
    if core is None:
        missing += 1
        if missing in (1, 20):
            log("card not visible in nvidia-smi: pump and radiator at 100 %")
        tgt = {ch: 255 for ch in ALL}
    else:
        if missing:
            log("card visible again, back to curves")
        missing = 0
        name = profile()
        if name != active:
            log(f"cooling profile: {name}")
            active = name
        P = PROFILES[name]
        pump = max(interp(P["pump_core"], core), interp(P["pump_mem"], mem))
        rad = max(interp(P["rad_core"], core), interp(P["rad_mem"], mem))
        ov = override(core, mem)
        if ov:
            pump, rad = ov
        if (ov is not None) != manual:
            manual = ov is not None
            log("manual override " + (f"on: pump {pump:.0f} %, radiator {rad:.0f} %" if manual else "off, curves"))
        if core >= PANIC_CORE or mem >= PANIC_MEM:
            pump = rad = 100
        if faulty:
            rad = max(rad, FAULT_RAD_PCT)
        tgt = {PUMP: round(pump * 2.55)}
        tgt.update({r: round(rad * 2.55) for r in RADS})
    for ch in ALL:
        t = tgt[ch]
        cur[ch] = t if t > cur[ch] else max(t, cur[ch] - DOWN)
        try:
            write(ch, cur[ch])
        except OSError:
            full_blast()
    for ch in RADS:                                 # stall watchdog
        try:
            rpm = int(open(f"{H}/{TACH[ch]}_input").read())
        except (OSError, ValueError):
            continue
        if cur[ch] >= STALL_MIN_PWM and rpm == 0:
            stall[ch] += 1
            if stall[ch] == STALL_TICKS and ch not in faulty:
                faulty.add(ch)
                log(f"radiator fan {ch}/{TACH[ch]} stalled at duty {round(cur[ch] / 2.55)} %: others raised to >= {FAULT_RAD_PCT} %")
        else:
            stall[ch] = 0
            if rpm > 0 and ch in faulty:
                faulty.discard(ch)
                log(f"radiator fan {ch}/{TACH[ch]} running again")
    time.sleep(PERIOD)
