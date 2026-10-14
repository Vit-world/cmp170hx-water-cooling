# Fitting the Bykski N-TESLA-A100-40G-SR to a CMP 170HX

**English** · [Русский](fitment.ru.md) · [← back](../README.md)

The block fits the card almost perfectly, but **two components are not reached by the block's surface as delivered**, and the block has more raised pads (bosses) than its manual covers.

> [!CAUTION]
> Anything conductive near a powered PCB can short it. Read [Warnings](#warnings) before copying the spacer idea.

## Background: the air-cooled phase

Before the water block the card ran on air. A 120 mm fan with a 3D-printed adapter blew air into the card, and a second 120 mm fan was fixed on the rear of the case as an exhaust, with all the gaps around it sealed with double-sided nano tape so it draws air through the card instead of from inside the PC case.

![120 mm fan with a 3D-printed adapter on the card](../images/01-air-cooling-intake-shroud.jpg)
*Air cooling: 120 mm fan with a 3D-printed adapter feeding the card.*

![Rear exhaust fan taped to the case](../images/02-air-cooling-rear-exhaust.jpg)
*Air cooling: second 120 mm fan fixed on the case rear as an exhaust, gaps sealed with double-sided nano tape.*

## The rule: choose pads by trial, not by numbers

The thickness of the pads supplied with the block is not known in advance (the manufacturer's choice), so everything below is found by trial fitting.

- Fit the block on the card with pads on the chips, then take it off and look at every pad. Each one should show contact with the block.
- The contact must be even over the whole card. A chip with no contact overheats.
- The mounting screws must not put stress on the card. If tightening them bends the card or strains the PCB, a pad is too thick somewhere; the card has to sit flat.

## Soft thermal pads supplied with the block

The pads supplied with the block were 1.7 mm thick and very soft. They closely resemble the pads that were on the card from the factory: both cards the author took apart still had intact factory seals, so, judging by the seals, nobody had opened them before, and the pads on both were identical.

The author also had a set of pads bought separately (brand not recalled), and those turned out to be noticeably stiffer. The soft ones were chosen on purpose: if a gap is wrong by a fraction of a millimetre, a soft pad can be pressed down with light force, which lets every chip make contact without bending the card or straining the PCB. Stiffer pads would need a much more exact thickness.

## Test fit: where the water block does not touch the card's chips

I put old thermal pads on the chips, lowered the block, and took it off again. Pads that came off the chips and stuck to the block show where contact is made; a pad that stayed on its chip and left no mark on the block shows a gap.

### Spot 1: a pocket in the block above a component

![Block and card side by side after a test fit](../images/03-block-test-fit-overview.jpg)
*Block (top) and card (bottom) after a test fit. Red: the component whose pad did not reach the block. Green: a small IC where the block has a flat spot and the gap had to be closed with thicker padding.*

The component sits between two inductors on the PCIe-connector side of the GPU. In the block there is a large recess exactly above it, so the pad stayed on the chip and never touched the block.

![Close-up of the pocket and the component](../images/04-block-pocket-closeup.jpg)
*Close-up: the pocket in the block (top) and the component on the card (bottom).*

**Fix used:** a small rectangular aluminium spacer (a bar) cut from an old heatsink and fitted to the size of the recess. A thermal pad is glued to both sides, so the stack is chip, pad, aluminium bar, pad, block.

![Aluminium spacer in the block's pocket](../images/06-aluminium-spacer-in-pocket.jpg)
*The aluminium spacer (red ellipse) sitting in the pocket of the block, with pad material around it.*

**How the thickness was found:** it depends on the pads you have, so measure it on the spot. I 3D-printed blanks of the same size in thicknesses stepping by 0.5 mm, put each one between pads, fitted the block to the card, and kept the thickness that sat best. Then I cut an identical piece from aluminium. The footprint in this build is 15 x 7 mm. **The blanks are ready to print: [stl/](../stl/).**

In my case the bar came out 5.5 mm thick, with a 1.7 mm thermal pad above and another below it. But measure for your own build, because a lot depends on it: if the stack is too thin, the chip will not be cooled properly; if it is too thick, the PCB can crack when it heats up, or its inner layers can be damaged. Either way, take the time to print bars of different heights and do the test fit. The bar would be better made of copper, but I only had aluminium :)

When choosing the thickness, remember that there will be thermal paste on the GPU die, which adds a little thickness too. For the test fit I stuck on several strips of masking tape.

### Spot 2: a small IC near the power-connector end of the board

Here the block has no boss at all, just a flat surface, so the gap is simply the missing height.

[<img src="../images/08-spot2-flat-area-over-small-ic.jpg" width="560" alt="Spot 2: the small IC on the card and the flat area of the block above it">](../images/08-spot2-flat-area-over-small-ic.jpg)

*Spot 2: the small IC on the card (bottom) and the flat area of the block above it (top), both circled in green. No pocket, no boss. Click to enlarge.*

**Fix used:** two thermal pads from the block's kit glued together (2 x 1.7 mm). No spacer needed.

## Map: matching the pads on the card with the bosses on the block

Every pad on the card (top) is linked to the boss or ridge of the block it touches. Click the picture for full size.

[![Map of pads on the card and the matching bosses on the block](../images/05-pad-to-boss-map.jpg)](../images/05-pad-to-boss-map.jpg)

| Marking | What it is | In the block's manual? |
|---|---|---|
| yellow lines | long pad strips along the rows of inductors, meeting the long ridges of the block | yes |
| red ellipse | the component between two inductors at the PCIe-connector side of the GPU: Spot 1 above (aluminium spacer with pads) | the pocket is there, but the pad alone does not reach: spacer needed |
| blue squares | two small components on either side of it, each meeting a small boss of the block | yes |
| magenta squares | components beside the capacitors on the left and on the right, each meeting a boss of the block | **no** (to the best of the author's memory); pads added anyway |
| green ellipse | the small IC near the power-connector end of the board: Spot 2 above | **no** boss there at all; a double pad was used |

## Insulating the capacitors with Kapton tape

While reading about other builds the author came across the warning that some components of the card can touch the block and short out. By eye, the capacitors seemed able to touch the block in places, so those two areas of the block (red boxes in the picture) were covered with yellow Kapton (polyimide) tape. This is a precaution based on the author's judgement; it was not measured.

[![Areas of the block covered with Kapton tape](../images/07-kapton-insulation-areas.jpg)](../images/07-kapton-insulation-areas.jpg)
*Card (top) and block (bottom). The two red boxes mark the areas of the block covered with yellow Kapton tape.*

## Warnings

- **Aluminium conducts.** The spacer must be completely insulated by the pads on both sides: pads larger than the spacer, no overhang or metal burr touching anything else, and thermal pads that do not conduct electricity (make sure with a multimeter). Check for shorts before powering up.
- **Stacked pads conduct heat worse than a single pad,** and the chips in question have no temperature readout I could find (unknown), so there is no number for them. In this build the card ran `gpu_burn` at 250 W without errors or throttling, see [calibration](calibration.md); if you can, check the spots with a contact or IR thermometer.
- **Measure your own gaps** before choosing pad thickness (see [the rule above](#the-rule-choose-pads-by-trial-not-by-numbers)); pad squeeze, pad thickness and card revision may differ.

## Still to be written

The full step-by-step install (disassembly, paste, screw order, loop layout, leak test).

**At the time of writing: room temperature 23 °C, card idle, GPU core 27 °C, memory 45 °C, card power draw 33 W. Fans at 15 % (750 rpm), pump at 30 % (2842 rpm).**
