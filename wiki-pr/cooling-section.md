<!-- Proposed addition to docs/operations/cooling.md, under "Water cooling". Heading level assumes the section is an H2. -->

### Pump and radiator-fan duty on a water loop (one measured loop)

The page above lists pump duty versus temperature and radiator-fan duty versus temperature at 250 W as unmeasured.
One tester measured both on a 250 W-limited, unlocked 8 GB card (`10de:20c2`, 64 GB) with `gpu_burn` FP32 on a
custom loop (Bykski N-TESLA-A100-40G-SR block, Bykski 360 mm radiator, Bykski D5 pump with 150 mm reservoir, 23 °C room). Pump on a motherboard `AIO_PUMP` header, three 120 mm ARCTIC P12 Pro PWM radiator fans on separate chassis headers (one common duty), both
driven through the Nuvoton NCT6798 hwmon driver.
Each step ran 5 to 6 minutes after a warm-up; the plateau is the median of the last 2 minutes.

| Radiator fan duty | Radiator rpm | Core / HBM °C | Evidence | Conditions |
|---|---|---|---|---|
| 100 % | 2900 | 53 / 58 | one report | pump 55 %, 249 W, heat-soaked loop |
| 70 % | 2200 | 54 / 59 | one report | same |
| 50 % | 1660 | 55 / 59.5 | one report | same |
| 35 % | 1270 | 56 / 59 | one report | loop not fully heat-soaked, perhaps 1 to 2 °C optimistic |
| 25 % | 1010 | 59 / 62 | one report | same |
| 15 % | 740 | 64 / 66, still rising 0.7 °C/min | one report | not settled after 8 minutes |

| Pump duty | Pump rpm | Core / HBM °C | Evidence | Conditions |
|---|---|---|---|---|
| 100 % | 4070 | 56 / 61 | one report | radiator fans 50 % (about 1660 rpm), about 245 W |
| 70 % | 3750 | 55 / 59 | one report | same |
| 55 % | 3480 | 55 / 59.5 | one report | same |
| 40 % | 3125 | 55 / 59 | one report | same |
| 30 % | 2820 | 55 / 60 | one report | same |
| 20 % | 2480 | 56 / 61 | one report | same |

What the numbers say, for this loop:

- Radiator fans: going from 50 % (about 1660 rpm) to 100 % (about 2900 rpm) lowered the core by about 2 °C and HBM by about 1.5 °C. Below 35 %
  the temperature rises quickly.
- Pump: across 20 % to 100 % (2480 to 4070 rpm) the spread was 1 °C on the core and 2 °C on HBM. Pump speed above its minimum bought nothing measurable.
- Two fan curves built from this were validated with 10-minute 250 W runs: radiator and pump at 30 % until the core reached about 60 °C gave 59 / 62 °C
  at 1100 rpm radiator and 2870 rpm pump; radiator up to 50 % and pump 40 to 50 % gave 55 / 60 °C. No compute errors in either run.
- Noise (one listener, quiet room): the three fans were indistinguishable from off up to 20 % duty, almost inaudible at 30 %
  (about 1100 rpm), quiet at 40 %, audible from 50 %, and uncomfortable at 70 % (about 2200 rpm). The pump was
  indistinguishable between 20 % and 30 % (about 2500 to 2800 rpm), audible as a thin whine up close at 40 %, and audible across the room at 55 %.

HBM temperature on water: in this loop HBM was never below 44 to 46 °C at idle, whatever the fan and pump speed, and never below
51 °C under load (about 157 W, loop not yet heat-soaked) or 52 °C at 250 W; with a heat-soaked loop and the radiator at 100 % it was 58 °C. HBM sat
about 15 °C above the core at idle and 5 to 12 °C above it under load in every run.

> [!NOTE]
> **Open problem.** The HBM temperature floor above is one loop and one sensor. It suggests the memory temperature is limited by the package and its
> contact rather than by the loop, but this has not been reproduced, and the absolute accuracy of the HBM sensor is unknown.
