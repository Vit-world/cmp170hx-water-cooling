# Water-cooling the NVIDIA CMP 170HX

**English** · [Русский](README.ru.md)

A working water-cooling build for the **CMP 170HX** (GA100) using a **Bykski N-TESLA-A100-40G-SR** block: what fits, the spots where the block needs help, how the fans and pump are controlled, and the temperatures and noise you get. One build, one tester, documented with photos and raw data.

**At the time of writing: room temperature 23 °C, card idle, GPU core 27 °C, memory 45 °C, card power draw 33 W. Fans at 15 % (750 rpm), pump at 30 % (2842 rpm).**

## Photos

Click a photo to jump to its explanation.

<table>
<tr><td align="center" valign="top"><a href="docs/fitment.md#background-the-air-cooled-phase"><img src="images/01-air-cooling-intake-shroud.jpg" width="230" alt="Air cooling: intake fan with a 3D-printed adapter"></a><br><sub>1. Air cooling: intake fan with a 3D-printed adapter</sub></td><td align="center" valign="top"><a href="docs/fitment.md#background-the-air-cooled-phase"><img src="images/02-air-cooling-rear-exhaust.jpg" width="230" alt="Air cooling: rear exhaust fan on the case"></a><br><sub>2. Air cooling: rear exhaust fan on the case</sub></td><td align="center" valign="top"><a href="docs/fitment.md#test-fit-where-the-water-block-does-not-touch-the-cards-chips"><img src="images/03-block-test-fit-overview.jpg" width="230" alt="Test fit: block and card side by side"></a><br><sub>3. Test fit: block and card side by side</sub></td><td align="center" valign="top"><a href="docs/fitment.md#spot-1-a-pocket-in-the-block-above-a-component"><img src="images/04-block-pocket-closeup.jpg" width="230" alt="A pocket in the block above a component"></a><br><sub>4. A pocket in the block above a component</sub></td></tr>
<tr><td align="center" valign="top"><a href="docs/fitment.md#spot-1-a-pocket-in-the-block-above-a-component"><img src="images/06-aluminium-spacer-in-pocket.jpg" width="230" alt="The aluminium spacer in the pocket"></a><br><sub>5. The aluminium spacer in the pocket</sub></td><td align="center" valign="top"><a href="docs/fitment.md#spot-2-a-small-ic-near-the-power-connector-end-of-the-board"><img src="images/08-spot2-flat-area-over-small-ic.jpg" width="230" alt="Spot 2: a small IC and the flat area above it"></a><br><sub>6. Spot 2: a small IC and the flat area above it</sub></td><td align="center" valign="top"><a href="docs/fitment.md#map-matching-the-pads-on-the-card-with-the-bosses-on-the-block"><img src="images/05-pad-to-boss-map.jpg" width="230" alt="Map: pads on the card and bosses on the block"></a><br><sub>7. Map: pads on the card and bosses on the block</sub></td><td align="center" valign="top"><a href="docs/fitment.md#insulating-the-capacitors-with-kapton-tape"><img src="images/07-kapton-insulation-areas.jpg" width="230" alt="Kapton insulation on the block"></a><br><sub>8. Kapton insulation on the block</sub></td></tr>
</table>

| Guide | Status |
|---|---|
| [Fitting the block: two spots it does not reach, a map of every pad, plus extra bosses](docs/fitment.md) | written, more photos to come |
| Step-by-step install (disassembly, paste, screw order, loop, leak test) | in progress |
| [Calibration: pump and radiator-fan duty vs temperature, HBM floor, noise](docs/calibration.md) | written |
| [3D-printable spacer blanks: 15 x 7 mm, 3.0 to 6.5 mm in 0.5 mm steps](stl/) | written |
| [Scripts: cooling daemon and calibration runner](scripts/) | written |
| [Raw measurement data](data/) | written |

## Parts used

| Part | Model |
|---|---|
| Card | NVIDIA CMP 170HX (`10de:20c2`, 8 GB variant unlocked to 64 GB) |
| Water block | Bykski N-TESLA-A100-40G-SR |
| Radiator | Bykski CR-RD360RC-TN-V2, 360 mm |
| Pump | Bykski B-UL-D5-X-V4 (D5 pump with 150 mm reservoir) |
| Fans | 3x ARCTIC P12 Pro Reverse A-RGB Black, 120 mm, PWM |
| Case | Corsair FRAME 4000D |
| Board / CPU | ASUS TUF GAMING B760M-PLUS WIFI D4, Intel Core i5-12400 |

## Results at a glance (250 W, `gpu_burn` test)

The hottest part of this card is the memory chips (HBM); they are always hotter than the GPU core. Under full load the card gave:

- Radiator fans: 50 % (1660 rpm). Spinning them up to 100 % only makes it about 2 C colder (core 53 vs 55 C).
- The pump can sit near its minimum: 20 % to 100 % changes core and HBM by 1 to 2 C.
- Two fan curves: `quiet` 59 / 62 C (core / HBM) with fans and pump at about 30 %, practically inaudible at night; `cold` 55 / 60 C with fans up to about 50 %.
- HBM did not go below 44 to 46 C at idle or 51 to 52 C under load, whatever the cooling (at maximum pump and fan speeds). The memory on this card always runs at its maximum clock, even at idle.

Details and caveats in [docs/calibration.md](docs/calibration.md).

## Honest limits

All measurements and tests were made at a room temperature of 23 C. Nothing here is a general rule, and some numbers are unknown or unreproduced; each page says so where it matters. Corrections, other builds' data and translation fixes are welcome as issues or pull requests.

The same cooling measurements are also proposed for the community wiki, [Consensus-Protocol/cmp170hx](https://github.com/Consensus-Protocol/cmp170hx).

## Licence

**CC0 1.0 Universal**: everything here (text, data, code) is dedicated to the public domain. Use it for anything, commercial or not, without asking or crediting. See [LICENSE](LICENSE).
