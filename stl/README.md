# Spacer test blanks (15 x 7 mm)

**English** · [Русский](README.ru.md) · [← back](../README.md)

Eight plain blocks, **15 x 7 mm**, heights **3.0 to 6.5 mm in 0.5 mm steps**. Print them all at once on any 3D printer and use them to find how thick the aluminium spacer for [Spot 1](../docs/fitment.md#spot-1-red-a-pocket-in-the-block-above-a-component) must be with **your** thermal pads.

| Height | File |
|---|---|
| 3.0 mm | [blank_15x7x3.stl](blank_15x7x3.stl) |
| 3.5 mm | [blank_15x7x3p5.stl](blank_15x7x3p5.stl) |
| 4.0 mm | [blank_15x7x4.stl](blank_15x7x4.stl) |
| 4.5 mm | [blank_15x7x4p5.stl](blank_15x7x4p5.stl) |
| 5.0 mm | [blank_15x7x5.stl](blank_15x7x5.stl) |
| 5.5 mm | [blank_15x7x5p5.stl](blank_15x7x5p5.stl) |
| 6.0 mm | [blank_15x7x6.stl](blank_15x7x6.stl) |
| 6.5 mm | [blank_15x7x6p5.stl](blank_15x7x6p5.stl) |
| **all eight on one plate** (75 x 19 mm) | [blanks_plate_15x7.stl](blanks_plate_15x7.stl) |

## How to use

1. Print the plate (or single blanks). Any FDM printer and any filament will do: the blanks are only trial pieces, used with the card powered off.
2. **Measure each printed blank with calipers** and go by the measured height: a printed part can differ from the model by a few tenths of a millimetre.
3. At the pocket, stack pad, blank, pad on the component, lower the block as in the [test fit](../docs/fitment.md#test-fit-where-the-block-does-not-touch), take it off and look at the imprints. Repeat with other blanks and keep the thickness that makes even contact without straining the card.
4. Make the real spacer from aluminium with the same footprint and the chosen height, and insulate it completely with pads (see the [warnings](../docs/fitment.md#warnings)).

## Notes

- The 15 x 7 mm footprint is what fitted the pocket in the author's build. Check it against your own block before cutting anything.
- The right height depends on your pads. The pads supplied with the block in this build were 1.7 mm thick and very soft.
- The author's original set had 3.0 to 5.5 mm and 6.5 mm; the 6.0 mm blank is added here so that the steps are even.
- Regenerate or make other sizes with `python3 make_spacer_blanks.py --plate` (standard library only; see `--help` for `--length`, `--width`, `--heights`).
