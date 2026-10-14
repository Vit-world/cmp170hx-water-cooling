<!--
Proposed changes to docs/operations/cooling.md, section "Water cooling". Three insertions:

 A. one new row at the end of the table of blocks (after the Bykski N-TESLA-A100-X-V2 row);
 B. two new subsections (H3) right after the "Open problem: HBM temperature on water" note and before the "---" line;
 C. one new paragraph at the end of that same note.
-->

<!-- ===================== A. new table row ===================== -->

| **Bykski N-TESLA-A100-40G-SR** + Bykski 360 mm radiator, three 120 mm PWM fans, D5 pump | **53 C core / 58 C memory at 250 W** (`gpu_burn`, radiator fans 100 %, pump 55 %, heat-soaked loop, 23 C room); **55 / 59.5 C** with the radiator fans at 50 % (about 1660 rpm) | One report. Fits, but needed hand-made fixes at two spots (see the first subsection below). Pump speed barely matters: 20 % to 100 % moved the result by 1 to 2 C. |

<!-- ===================== B. two subsections ===================== -->

### Fitting the Bykski N-TESLA-A100-40G-SR (one build)

One tester fitted this 40 GB-family PCIe block, which comes with a manual, to an 8 GB 170HX (unlocked to 64 GB), and reported that it fits almost perfectly, but that **two components were not reached by the contact surface as delivered** and that the block has more raised bosses than the manual covers. A test fit showed where (thermal pads on the chips, block lowered and removed again; a pad that stuck to the block shows contact, a pad that stayed on its chip with no mark on the block shows a gap):

- **Spot 1, a pocket above a component.** A component between two inductors on the PCIe-connector side of the GPU sits under a large recess in the block, so a pad alone leaves a gap. Fix used: a 15 x 7 mm rectangular aluminium spacer cut from an old heatsink, with a thermal pad on each side (pad, spacer, pad). The spacer was 5.5 mm tall, with the kit's 1.7 mm pads above and below it. The tester found the height by 3D-printing 15 x 7 mm blanks in 0.5 mm steps and test-fitting each.
- **Spot 2, a flat area with no boss.** A small IC near the power-connector end of the board faces a flat surface of the block, so the gap is simply the missing height. Fix used: two of the kit's 1.7 mm pads glued together.
- **Extra bosses.** The block has further raised pads, beside the capacitors on the left and the right of the GPU, that the manual does not say to pad. The tester matched them to components and fitted pads there as well.
- **Capacitor insulation.** After reading about components touching the block, the tester covered two areas of the block, where the capacitors seemed able to touch it, with Kapton (polyimide) tape. A precaution by eye, not measured.
- **Soft pads.** The kit's pads (1.7 mm) were very soft and looked like the card's factory pads (both cards opened had intact factory seals). A stiffer set bought separately was not used: a soft pad can be pressed down with light force, so a gap that is wrong by a fraction of a millimetre still gives contact without bending the card or straining the PCB.

> [!CAUTION]
> **The aluminium spacer conducts.** It must be insulated on both faces by pads that are larger than the spacer and do not conduct electricity, with no overhang or burr touching anything else. Check for shorts before powering up. Stacked pads also conduct heat worse than a single pad, and the chips involved have no temperature readout (unknown), so there is no number for them; in this build the card ran `gpu_burn` at 250 W without errors or throttling.

### Pump and radiator-fan duty on a water loop (one measured loop)

One tester measured pump duty and radiator-fan duty against temperature on a 250 W-limited unlocked 8 GB card (`10de:20c2`, 64 GB) with `gpu_burn` FP32 on a custom loop: Bykski N-TESLA-A100-40G-SR block, Bykski 360 mm radiator, Bykski D5 pump with a 150 mm reservoir, three 120 mm ARCTIC P12 Pro PWM radiator fans, 23 C room. The pump sits on a motherboard `AIO_PUMP` header and each radiator fan on its own chassis header (one common duty), all driven through the Nuvoton NCT6798 hwmon driver. Each step ran 5 to 6 minutes after a warm-up; the plateau is the median of the last 2 minutes.

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

- Radiator fans: going from 50 % (about 1660 rpm) to 100 % (about 2900 rpm) lowered the core by about 2 °C and HBM by about 1.5 °C. Below 35 % the temperature rises quickly.
- Pump: across 20 % to 100 % (2480 to 4070 rpm) the spread was 1 °C on the core and 2 °C on HBM. Pump speed above its minimum bought nothing measurable.
- Two fan curves built from this were validated with 10-minute 250 W runs: radiator and pump at 30 % until the core reached about 60 °C gave 59 / 62 °C at about 1100 rpm radiator and 2870 rpm pump; radiator up to 50 % and pump 40 to 50 % gave 55 / 60 °C. No compute errors in either run.
- Noise (one listener, quiet room): the three fans were indistinguishable from off up to 20 % duty, almost inaudible at 30 % (about 1100 rpm), quiet at 40 %, audible from 50 %, and uncomfortable at 70 % (about 2200 rpm). The pump was indistinguishable between 20 % and 30 % (about 2500 to 2800 rpm), audible as a thin whine up close at 40 %, and audible across the room at 55 %.

HBM temperature in this loop: never below 44 to 46 °C at idle, whatever the fan and pump speed, and never below 51 °C under load (about 157 W, loop not yet heat-soaked) or 52 °C at 250 W; with a heat-soaked loop and the radiator fans at 100 % it was 58 °C. HBM sat about 15 °C above the core at idle and 5 to 12 °C above it under load in every run.

<!-- ===================== C. paragraph appended to the "Open problem: HBM temperature on water" note ===================== -->

> One tester's loop (see the last subsection below) reports HBM never below 44 to 46 °C at idle and 51 to 52 °C under load whatever the fan and pump speed, and 58 °C at 250 W once heat-soaked, close to the 58 °C reported above for the budget block. That suggests the floor is set by the package and its contact rather than by the loop, but it is two loops and has not been reproduced; the absolute accuracy of the HBM sensor is unknown.
