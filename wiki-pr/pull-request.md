**Title:** cooling: water-loop calibration (pump and radiator-fan duty vs temperature at 250 W, HBM floor)

**What this adds**

A subsection under *Water cooling* in `docs/operations/cooling.md` with measured pump duty vs temperature and radiator-fan duty vs temperature at 250 W
on one water loop, a subjective noise ranking, and an HBM temperature floor observation. The page currently lists these as unmeasured
("no pump duty versus temperature data, no radiator fan duty versus temperature at 250 W", and HBM temperature on water as an open question).

**Evidence and wording**

- One tester, one machine, one loop, so every row is marked "one report" and the HBM statement is hedged as an open problem, following `docs/appendix/methodology.md`.
- The first run started with a cold loop and its first points read about 2 °C low; the affected rows are labelled, and the warm re-run values are used where available.
- No individual is named in the proposed text.
- I did not touch the `docs/zh/` mirror. Happy to add it, or to leave it to your translation workflow.

**Raw data and tools**

5-second samples, plateau tables and the scripts (a small cooling daemon and the calibration runner) are in
https://github.com/Vit-world/cmp170hx-water-cooling, kept outside the wiki so the wiki stays free of handles. Feel free to copy any of it into `docs/`
if you want the data in-tree.

Files in this PR: `docs/operations/cooling.md` only.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
