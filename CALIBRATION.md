# Calibration checklist

The tool ships with placeholder coefficients so it runs out of the box. This is
the list of real data that turns it from a ranking tool into one whose absolute
numbers you can defend to a supplier.

Work top to bottom — the items are ordered by how much they move the result.
Everything here is edited in the **Library** tab and travels with your exported
project JSON.

---

## 1. Rates — biggest effect, smallest effort

| Field | What to find out |
|---|---|
| Direct labour ₹/hr | Fully loaded operator cost: wages + benefits + statutory, ÷ productive hours |
| Assembly labour ₹/hr | Same, for the assembly line — usually lower than machining |
| Factory overhead % | Indirect cost recovered on conversion cost. Ask finance for the current absorption rate |
| Scrap allowance % | Actual scrap + rework rate for comparable parts, from quality records |
| Supplier margin % | What your suppliers actually earn. From past cost breakdowns or benchmark quotes |
| Packaging + freight % | Inbound logistics as a share of part cost |

Vendor-basis estimates are only as good as the overhead and margin rates. If
you can get one number right, make it overhead.

## 2. Machine hourly rates

For each machine, per productive hour:

- Depreciation (purchase price ÷ expected life hours)
- Floor space, power, compressed air
- Tooling consumables — inserts, drills, nozzles, build plates
- Maintenance contract and expected repairs
- **Not** operator labour — the tool adds that separately, so including it here
  double-counts

Divide by **realistic** annual running hours, not nameplate hours. A machine
quoted at 4,000 hr/yr that actually runs 1,600 has a rate 2.5× higher than the
optimistic figure.

## 3. Materials

| Field | Source |
|---|---|
| ₹/kg | Your last three purchase orders, not list price |
| Scrap recovery ₹/kg | What your scrap merchant actually pays for that alloy |
| Density | Material datasheet |
| MRR (mm³/min) | Measure it: time a known roughing cut and divide the volume removed by the minutes. One measurement per material class is enough to start |
| Cutting speed Vc, feed/rev | Tooling supplier's recommendation for your insert grade and that material |
| Powder bulk density | Powder datasheet — it is roughly half the solid density and the model needs both |

## 4. DFA time tables — the calibration that matters most

This is the one that needs a stopwatch, and it is worth an afternoon.

1. Pick 10–15 assembly operations across your product range that span the
   classes in the table: an easy symmetric part, a small fiddly one, one that
   tangles, one inserted from below, one screwed down, one that needs a
   re-orientation.
2. Time each one five times with an experienced operator at normal pace. Take
   the median, not the best.
3. Split each observed time into handling (reach, grasp, orient, move) and
   fitting (position, insert, secure).
4. Overwrite the **seconds** column in Library → DFA tables so the model
   reproduces your observations.
5. Leave the **index** column alone unless a specific penalty consistently
   misranks parts — the indices drive the redesign flags, not the cost.

Sanity check afterwards: pick a product you have never analysed, predict its
assembly time, then time the real build. Within ±20% on the total is a working
model. Iterate once if you are outside that.

## 4b. Airframe process coefficients

Three models were added for composite, foam and harness work. Each has one
coefficient that dominates it — measure that one first and the rest can wait.

| Process | The number that decides it | How to get it |
|---|---|---|
| **Harness** | Crimp seconds per contact, and connector assembly seconds | Time one real harness build end to end, then divide by the contact and connector counts. Harness cost is almost entirely labour, so nothing else matters as much |
| **Composite** | Layup minutes per ply per m² | Time one real part: cutting, positioning and consolidating each ply. Include the debulks. This single number moves composite cost more than material price does |
| **Foam** | Block margin, for CNC parts | Measure the blank you actually buy against the finished part. The yield figure the tool reports should match what you see on the floor |

Two more worth an early look:

- **Composite scrap rate.** Use your own reject rate, not the 8% placeholder.
  Composites scrap far higher than machining and the number is very shop-specific.
- **Powder-bed and cure-cycle loading.** `partsPerCure` and `partsPerBuild`
  divide the most expensive line in each of those models. Getting the loading
  wrong by a factor of two moves the part cost by the same factor.

## 4c. Mass

The mass roll-up is only as complete as your purchased-part entries. Machined,
printed, composite, foam and harness parts compute their own mass; **bought-in
items cannot**, and the analysis tells you how many are still missing.

Weigh them rather than trusting datasheets — connectors, fasteners and cable
account for more grams than anyone expects, and a datasheet mass rarely includes
the pigtail, the backshell or the mounting hardware.

## 5. Process model coefficients

- **Machining** — operator attendance % (what fraction of cycle time the
  operator is actually tied to the machine), load/unload seconds, inspection
  seconds, finishing rate mm²/min
- **FDM** — waste %, failed-print allowance % (from your own print logs, not
  the vendor's claim), post-processing minutes
- **Powder** — packing density % is the single most sensitive number in the SLS
  and MJF model. Get it from your bureau or from your own build logs; a build
  packed at 12% costs a third less per part than one at 8%. Recycle rate too:
  refresh ratio is a real cost driver and bureaus vary widely

## 6. Tolerance and finish multipliers

Derive these from your own quote history rather than accepting the defaults:
take a family of similar parts quoted at different tolerances and read the
ratio straight off the prices.

---

## Validating the whole thing

Once calibrated, run the benchmark before you rely on it:

1. Take 8–12 parts across your real process mix with **known** PO prices.
2. Estimate each one in the tool without looking at the actual.
3. Compare. Absolute error under ±20% is good for early-stage costing.
4. More important: cost three variants of one part — cheaper material,
   looser tolerance, larger batch — and check the tool ranks them in the
   order your experience says it should. **Rank-order correctness is what
   design decisions need.** Absolute accuracy matters for negotiation.

Record what you find here so the next person knows how far to trust it.

| Date | Parts tested | Median error | Rank order correct? | Notes |
|---|---|---|---|---|
| | | | | |
