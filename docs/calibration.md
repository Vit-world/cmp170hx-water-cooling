# CMP 170HX water-loop calibration

**English** (summary: [Русский](#по-русски-кратко)) · [← back](../README.md)

Measured data and tools from one CMP 170HX on a custom water loop, run from motherboard fan headers on Linux:
**how much does more pump speed or more radiator-fan speed actually lower the temperature, and where does it stop paying off?**

Single machine, single loop, single tester: treat the numbers as one report, not as a rule.
The same findings are proposed for the community wiki ([Consensus-Protocol/cmp170hx](https://github.com/Consensus-Protocol/cmp170hx), `docs/operations/cooling.md`); see [`wiki-pr/`](../wiki-pr/).

## TL;DR (250 W, `gpu_burn` FP32, plateau = median of the last 2 min)

| Finding | Number |
|---|---|
| Radiator fans: 100 % duty (2900 rpm) vs 50 % (1660 rpm) | 53 / 58 C vs 55 / 59.5 C (core / HBM). The extra ~1250 rpm buys about 2 C |
| Radiator fans down to 25 % (~1000 rpm) | 59 / 62 C (first run, loop not fully heat-soaked, so probably 1-2 C optimistic); 15 % (740 rpm) was still climbing at 64 / 66 C |
| Pump: 100 % (4070 rpm) vs 20 % (2480 rpm) at radiator 50 % | core 56 vs 56, HBM 61 vs 61 C; across all pump steps core 55-56 / HBM 59-61 C |
| Lowest HBM temperature seen | idle 44-46 C whatever the cooling; under load 51 C (~157 W) / 52 C (250 W), both with a not-yet-soaked loop; 58 C at 250 W with a soaked loop and radiator at 100 % |

So: one radiator fan duty around 50 % is the knee, the pump can sit near its minimum, and HBM does not get colder with more cooling.

## Setup

| | |
|---|---|
| Card | NVIDIA CMP 170HX, PCI ID `10de:20c2` (8 GB variant), unlocked to 64 GB; link Gen2 x4; power limit 250 W |
| Software | Linux 6.8, NVIDIA open kernel module 610.43.03 (community unlock), `gpu_burn` ([wilicc/gpu-burn](https://github.com/wilicc/gpu-burn)) FP32 `-m 90%` |
| Host | Intel Core i5-12400, ASUS TUF GAMING B760M-PLUS WIFI D4 (BIOS 1604), 2x 32 GB Kingston DDR4-2400; Corsair FRAME 4000D case |
| Fan / pump control | Nuvoton NCT6798 via the `nct6775` hwmon driver. Pump on the `AIO_PUMP` header (`pwm6` / `fan6`); three radiator fans, each on its own header `CHA_FAN1/2/3` (`pwm1,4,5` / `fan1,4,5`), driven with one common duty. `CPU_OPT` has no PWM of its own (follows `CPU_FAN`) |
| Water block | Bykski N-TESLA-A100-40G-SR |
| Radiator | Bykski CR-RD360RC-TN-V2, 360 mm, black (thickness not recorded) |
| Radiator fans | 3x ARCTIC P12 Pro Reverse A-RGB Black (120 mm, PWM, reverse-blade), each on its own header. Duty to rpm: 5 % 460, 15 % 730, 30 % 1110, 50 % 1660, 70 % 2190, 100 % 2900 |
| Pump | Bykski B-UL-D5-X-V4 (D5 pump with 150 mm reservoir), PWM from the `AIO_PUMP` header. Duty to rpm: 20 % 2480, 30 % 2820, 40 % 3125, 55 % 3500, 70 % 3750, 100 % 4070 |
| Ambient | 23 C room temperature during the tests |
| Date | 2026-10-11 / 2026-10-12 |

## Method

1. `gpu_burn` runs for the whole experiment. Warm-up 5-8 min at pump 55 %, radiator 50 %.
2. Steps (5-6 min each): **A** pump 55 %, radiator 100 / 70 / 50 / 35 / 25 / 15 %; **B** radiator 50 %, pump 100 / 70 / 40 / 30 / 20 %.
3. Every 5 s: core and HBM temperature (`nvidia-smi`), power, SM clock, fan and pump rpm. Plateau = median of the last 120 s of the step; slope = least-squares core slope over the same window.
4. The duty is set through a manual override that the cooling daemon honours for 90 s after each refresh (a crashed script cannot leave the loop under-cooled). The daemon's emergency threshold (core 72 / HBM 82 C to 100 %) stays active. A step reaching core 68 / HBM 76 C is cut short.

**Known flaw:** the first run started with a cold loop, so its first points (radiator 100 / 70 %, ~2 C) read too low. A second run on a warm loop re-measured 100 / 70 / 50 / 15 % and the pump at 20 % (folder `02-rerun-warm-loop`); use those where they exist. The 35 % and 25 % radiator points exist only from the first run (a few tenths of a degree to ~2 C optimistic).

## Results

### Radiator fan duty (pump 55 %)

| Radiator duty | Radiator rpm (mean of 3) | Core C | HBM C | Power W | Source |
|---|---|---|---|---|---|
| 100 % | 2897 | 53 | 58 | 249 | warm re-run |
| 70 % | 2198 | 54 | 59 | 246 | warm re-run |
| 50 % | 1661 | 55 | 59.5 | 246 | warm re-run |
| 35 % | 1271 | 56 | 59 | 246 | first run, loop not fully soaked |
| 25 % | 1010 | 59 | 62 | 248 | first run, loop not fully soaked |
| 15 % | 743 | 64 | 66 | 243 | warm re-run, **not settled** (+0.7 C/min after 8 min) |

### Pump duty (radiator 50 %, ~1665 rpm)

| Pump duty | Pump rpm | Core C | HBM C | Source |
|---|---|---|---|---|
| 100 % | 4066 | 56 | 61 | first run |
| 70 % | 3750 | 55 | 59 | first run |
| 55 % | 3479 | 55 | 59.5 | warm re-run |
| 40 % | 3125 | 55 | 59 | first run |
| 30 % | 2818 | 55 | 60 | first run |
| 20 % | 2481 | 56 | 61 | warm re-run |

### HBM temperature floor

- Idle (card at ~30 W, memory at its full clock): **44-46 C** at every fan and pump setting tried, including radiator fans at 100 %.
- Under load, lowest readings: **51 C** at about 157 W (`03-power-limited-partial`, radiator 100 %, core 41 C) and **52 C** at 250 W (first run, radiator 50-100 %, core 46 C). Both were taken while the loop was still cold; with a heat-soaked loop and the radiator at 100 % the same 250 W gave HBM 58 C / core 53 C (`02-rerun-warm-loop`).
- HBM sits about 15 C above the core at idle and 5-12 C above it under load, in every run. Cooling the core harder (core 39 C vs 64 C across runs) moves HBM less than one-for-one, which suggests HBM temperature is limited by the package and its contact rather than by loop capacity. One loop only; the HBM sensor's absolute accuracy is unknown, and this has not been reproduced.

### Subjective noise (one listener, computer in a quiet room; listening distance not recorded)

| Radiator fans (3x) | Verdict |
|---|---|
| off to 20 % | no difference from off |
| 30 % (~1100 rpm) | very quiet, practically inaudible at night |
| 40 % (~1400 rpm) | quiet |
| 50 % (~1660 rpm) | starting to be audible |
| 70 % (~2190 rpm) | clearly audible, uncomfortable in a room (tolerable briefly) |

| Pump | Verdict |
|---|---|
| 20 % vs 30 % | no difference |
| 40 % (~3125 rpm) | thin whine audible when sitting next to the PC |
| 55 % (~3500 rpm) | audible across the room |

Combined: fans 30 % + pump 30 % is inaudible at night; fans 40 % + pump 40 % is audible at night but quiet in the daytime.

### Two fan-curve profiles built from this (validated with 10-minute `gpu_burn` runs, 250 W)

| Profile | Plateau core / HBM | Radiator / pump rpm | Performance |
|---|---|---|---|
| `quiet` (<= 30 % until core ~60 / HBM ~66 C) | 59 / 62 C | 1097 / 2872 | 12647 Gflop/s, 0 errors |
| `cold` (radiator up to ~50 %, pump 40-50 %) | 55 / 60 C | 1663 / 3400 | 12651 Gflop/s, 0 errors |

The difference between the profiles is about 4 C. Raw data in `04-profile-validation/`.

## Files

| Path | What |
|---|---|
| `scripts/cmp_cooling_daemon.py` | closed-loop daemon: pump and N radiator fans from core / HBM temperature, emergency threshold, stall watchdog, override file |
| `scripts/cooling_cal.py` | the calibration run (needs the daemon, or replace `set_override()`) |
| `data/01-sweep-first-run/` | first sweeps A and B (`summary.json`, 5-s `samples.csv`, `burn.log`) |
| `data/02-rerun-warm-loop/` | warm-loop re-measurement of 100 / 70 / 50 / 15 % and pump 20 % |
| `data/03-power-limited-partial/` | partial run at ~157 W (stopped early) |
| `data/04-profile-validation/` | the two profile runs |
| `wiki-pr/` | text proposed for the community wiki |

To use the scripts on your own board, edit the CONFIG block at the top of the daemon (hwmon chip name, which `pwmN` / `fanN` is the pump and which are radiator fans) and the same constants in `cooling_cal.py`. Find the mapping by driving each `pwmN` to 100 % and watching which `fanN` reports rpm.

## Licence

**CC0 1.0 Universal** (public-domain dedication) for everything in this repository: code, data and text. Use, copy, change, redistribute and build on any of it for any purpose, commercial or not, without asking and without attribution. See [LICENSE](../LICENSE).

---

## По-русски (кратко)

Измерения на одной CMP 170HX с водяным охлаждением и управлением вентиляторами/помпой от материнской платы (Linux). Итог при 250 Вт: колено вентиляторов радиатора около 50 % (~1660 об/мин), дальше +1250 об/мин дают всего ~2 °C; помпу можно держать на минимуме (20–100 % отличаются на ~1,5 °C); температура HBM не опускается ниже 44–46 °C в простое и ~51–52 °C под нагрузкой при любом охлаждении. Один стенд, одна петля: это отчёт одного испытателя, не правило.
