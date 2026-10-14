**Title:** cooling: water-loop data for a second block (fit notes, pump / fan duty vs temperature, HBM floor)

**What this adds**

To the *Water cooling* section of `docs/operations/cooling.md`:

1. a row in the table of blocks for the Bykski N-TESLA-A100-40G-SR, with measured temperatures at 250 W;
2. a subsection with fit notes for that block (two spots its contact surface does not reach on this card, the fixes used, extra bosses the manual does not cover, Kapton insulation of the capacitors, soft pads) and a caution about the conductive spacer;
3. a subsection with pump-duty and radiator-fan-duty versus temperature tables, a subjective noise ranking, and the HBM temperature floor observed;
4. one paragraph appended to the existing *Open problem: HBM temperature on water* note: this loop's HBM readings agree with the 58 C reported there for the budget block (two loops, not reproduced).

The page currently has no pump-duty or radiator-fan-duty data, and it lists HBM temperature on water as an open problem; this is meant to give one more data point, not to close it.

**Evidence and wording**

- One tester, one machine, one loop, so rows are marked "one report" and the HBM statement is hedged, following `docs/appendix/methodology.md`.
- The first run started with a cold loop and its first points read about 2 C low; the affected rows are labelled and the warm re-run values are used where available.
- No individual is named in the proposed text.
- I did not touch the `docs/zh/` mirror. Happy to add it, or to leave it to your translation workflow.

**Raw data, photos and tools**

5-second samples, plateau tables, scripts, the fitment photos with a pad-to-boss map, and printable spacer blanks are in
https://github.com/Vit-world/cmp170hx-water-cooling, kept outside the wiki so the wiki stays free of handles. Feel free to copy any of it into `docs/` if you want it in-tree.

Files in this PR: `docs/operations/cooling.md` only.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
