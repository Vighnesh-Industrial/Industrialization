# Assembly & Cost Workbench

A local design-for-assembly and should-cost tool. It does the two jobs that
Boothroyd Dewhurst sells as separate products — assembly simplification and
part cost estimation — on your own data, in your own browser.

**Open `index.html` in any browser.** No install, no server, no build step, no
network. Double-click the file and it runs.

---

## What it does

**Assembly analysis (DFA)**

- Tests every part against the three minimum-part-count criteria and classifies
  it A (essential) or B (consolidation candidate)
- Scores handling and fitting difficulty as Lucas-style penalty indices
- Converts the same answers into assembly seconds and assembly labour cost
- Reports design efficiency, theoretical minimum part count, feeding and
  fitting ratios, and an assembly efficiency percentage
- Flags every part that breaches a target, with the specific driver named

**Should-cost**

- **CNC machining / drilling** — stock cost less scrap credit, roughing time
  from material removal rate, hole-by-hole drilling time from cutting speed and
  feed per revolution, a finishing pass, tool changes, load/unload, inspection,
  and setup amortised over batch size, with tolerance and surface-finish
  multipliers on cutting time
- **FDM** — shell volume from surface area × wall count × extrusion width,
  infill, support, volumetric flow rate, layer count and per-layer overhead,
  filament mass and waste, plate setup shared across parts, failure allowance
- **SLS / MJF** — parts per build from packing density, build time from layer
  count plus warm-up and cool-down, powder split into part mass and partly
  recycled cake, depowdering and finishing labour
- **Purchased** — quoted price, so the BOM rolls up completely

Every part carries a cost basis: **vendor should-cost** adds scrap, factory
overhead, supplier margin and freight on top of the direct cost, giving you a
target price to negotiate against. **In-house shop cost** stops at direct cost
for make-vs-buy. Set a project default, override per part.

Each estimate shows its full working — every rate, time and assumption — under
"Show the working". That transparency is the whole point: an estimate you can
put in front of a supplier beats a number you cannot explain.

---

## Where the numbers come from

The assembly method follows the **published Lucas/Hull DFA structure**:
functional A/B analysis, a handling index and a fitting index, with a per-part
index above 1.5 flagging a redesign candidate. On top of it sits a time model
that turns the same answers into seconds.

**The coefficients shipped in the Library tab are plausible starting points,
not measured data**, and are not taken from any vendor's proprietary tables.
Until you calibrate them, trust the tool for *ranking design alternatives
against each other* — which is what design decisions actually need — and treat
absolute values as indicative. See `CALIBRATION.md` for what to measure.

---

## Layout

| Tab | What lives there |
|---|---|
| **Setup** | Project identity, annual volume, default cost basis, live summary |
| **Parts** | Part list and the editor: identity, minimum-part-count test, handling, fitting, cost |
| **Analysis** | KPIs, part-by-part table, cost split, ranked list of what to change, print-to-PDF |
| **Library** | Rates, materials, machines, DFA method tables, cost model coefficients — all editable |
| **Data** | Export/import project JSON, CSV BOM import, results CSV export, reset |

## Saving your work

Work is held in the browser's local storage, which is **per-browser and
per-file-path** — open the file from a different folder, browser or profile and
you start empty. **Export the project JSON** and commit it to this repo for
anything you want to keep or share. Import restores it anywhere.

## Importing a BOM

Data tab → *Download blank template* gives you the exact header row. Columns:

```
name, partNo, qty, process, price, volume, bx, by, bz, material,
moves, material_diff, service, size, sym, fix, fixCount
```

Unknown columns are ignored and missing ones take defaults, so a two-column
`name,qty` file imports fine and you fill in the analysis afterwards.

## Reporting

Analysis tab → *Print / save as PDF* produces a clean report with the navigation
and buttons stripped out. *Export results as CSV* gives you the per-part table
plus the product-level summary for a spreadsheet or a supplier pack.

---

## Roadmap

Deliberately out of scope for v1, in rough order of value:

1. **Design alternatives side by side** — clone a project, change it, and see
   both costed in one view. This is the highest-value addition: DFA earns its
   keep by comparing a redesign against the original.
2. **STEP file import** for bounding box, volume and surface area, removing the
   manual geometry entry. Feature recognition (holes, pockets, bends) is a much
   larger job and should stay manual until the rest is calibrated.
3. **Sheet metal and injection moulding** process models, if the part mix moves
   that way.
4. **Assembly sequence** — the current model treats parts as an unordered set.
   A sequence would let re-orientation costs be attributed properly.
