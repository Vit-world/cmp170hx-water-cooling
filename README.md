# Water-cooling the NVIDIA CMP 170HX

**English** · [Русский](README.ru.md)

A working water-cooling build for the **CMP 170HX** (GA100) using a **Bykski N-TESLA-A100-40G-SR** block: what fits, the spots where the block needs help, how the fans and pump are controlled, and the temperatures and noise you get. One build, one tester, documented with photos and raw data.

## Photos

Click a photo to jump to its explanation.

<table>
<tr><td align="center" valign="top"><a href="docs/fitment.md#background-the-air-cooled-phase"><img src="images/01-air-cooling-intake-shroud.jpg" width="230" alt="Air-cooled phase: intake fan with a 3D-printed adapter"></a><br><sub>1. Air-cooled phase: intake fan with a 3D-printed adapter</sub></td><td align="center" valign="top"><a href="docs/fitment.md#background-the-air-cooled-phase"><img src="images/02-air-cooling-rear-exhaust.jpg" width="230" alt="Air-cooled phase: rear exhaust fan on the case"></a><br><sub>2. Air-cooled phase: rear exhaust fan on the case</sub></td><td align="center" valign="top"><a href="docs/fitment.md#test-fit-where-the-block-does-not-touch"><img src="images/03-block-test-fit-overview.jpg" width="230" alt="Test fit: block and card side by side"></a><br><sub>3. Test fit: block and card side by side</sub></td><td align="center" valign="top"><a href="docs/fitment.md#spot-1-red-a-pocket-in-the-block-above-a-component"><img src="images/04-block-pocket-closeup.jpg" width="230" alt="A pocket in the block above a component"></a><br><sub>4. A pocket in the block above a component</sub></td></tr>
<tr><td align="center" valign="top"><a href="docs/fitment.md#spot-1-red-a-pocket-in-the-block-above-a-component"><img src="images/06-aluminium-spacer-in-pocket.jpg" width="230" alt="The aluminium spacer in the pocket"></a><br><sub>5. The aluminium spacer in the pocket</sub></td><td align="center" valign="top"><a href="docs/fitment.md#map-which-pad-on-the-card-meets-which-boss-on-the-block"><img src="images/05-pad-to-boss-map.jpg" width="230" alt="Map: which pad meets which boss"></a><br><sub>6. Map: which pad meets which boss</sub></td><td align="center" valign="top"><a href="docs/fitment.md#insulating-the-capacitors-with-kapton-tape"><img src="images/07-kapton-insulation-areas.jpg" width="230" alt="Kapton insulation on the block"></a><br><sub>7. Kapton insulation on the block</sub></td><td></td></tr>
</table>

## What is here

| Guide | Status |
|---|---|
| [Fitting the block: two spots it does not reach, a map of every pad, plus extra bosses](docs/fitment.md) | written, more photos to come |
| Step-by-step install (disassembly, paste, screw order, loop, leak test) | in progress |
| [Calibration: pump and radiator-fan duty vs temperature, HBM floor, noise](docs/calibration.md) | written |
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

## Results at a glance (250 W, `gpu_burn`)

- Radiator fans: 100 % (2900 rpm) vs 50 % (1660 rpm) is only about 2 C better (core 53 vs 55 C).
- The pump can sit near its minimum: 20 % to 100 % changes core and HBM by 1 to 2 C.
- Two fan curves: `quiet` 59 / 62 C (core / HBM) with fans and pump at about 30 %, practically inaudible at night; `cold` 55 / 60 C with fans up to about 50 %.
- HBM did not go below 44 to 46 C at idle or 51 to 52 C under load, whatever the cooling.

Details and caveats in [docs/calibration.md](docs/calibration.md).

## Honest limits

One build, one tester, one room (23 C). Nothing here is a general rule, and some numbers are unknown or unreproduced; each page says so where it matters. Corrections, other builds' data and translation fixes are welcome as issues or pull requests.

The same cooling measurements are also proposed for the community wiki, [Consensus-Protocol/cmp170hx](https://github.com/Consensus-Protocol/cmp170hx).

## Licence

**CC0 1.0 Universal**: everything here (text, data, code) is dedicated to the public domain. Use it for anything, commercial or not, without asking or crediting. See [LICENSE](LICENSE).
