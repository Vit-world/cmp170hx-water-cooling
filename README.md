# Water-cooling the NVIDIA CMP 170HX

**English** · [Русский](README.ru.md)

A working water-cooling build for the **CMP 170HX** (GA100) using a **Bykski N-TESLA-A100-40G-SR** block: what fits, the spots where the block needs help, how the fans and pump are controlled, and the temperatures and noise you get. One build, one tester, documented with photos and raw data.

| | |
|---|---|
| ![Block test fit](images/03-block-test-fit-overview.jpg) | ![Pocket close-up](images/04-block-pocket-closeup.jpg) |
| Test fit of the block on the card | A pocket in the block where one component is not reached |

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
