# Assembly & Cost Workbench

A local design-for-assembly and should-cost tool. It does the two jobs that
Boothroyd Dewhurst sells as separate products — assembly simplification and
part cost estimation — on your own data, in your own browser.

**Open `index.html` in any browser.** No install, no server, no build step, no
network. Double-click the file and it runs.

---

## What it does

**Mass**

Grams are the second currency. Machined, printed, foam and harness parts
calculate their own mass from geometry; purchased parts take an entered
value. Set a mass budget and the analysis reports mass beside cost, cost per
gram, how many grams sit in parts that fail the minimum-part-count tests, and
which parts have no mass recorded yet.

**Modules**

Every part carries a module — Wing LH, Boom LH, Fuselage, Payload, Fasteners —
and every result is also reported per module. It is the only way a
several-hundred-part BOM stays legible, and it shows which module to send to a
consolidation review first.

**Field deployment**

Parts marked `fieldAssembly` produce a second, separate assembly time: what the
operator does on site, out of the transport case. Anything field-assembled that
is not `toolFree`, or that is joined with a screw, rivet, weld or lockwire, is
flagged — if tool-free deployment is a product promise, this is where it gets
measured against a target.

**Serviceability**

Build cost and mass both reward a soldered wire-to-board joint: no connector to
buy, no grams, quick to fit. The entire cost arrives later, at every repair —
which is why the practice survives design reviews that only look at build.

Each part carries a service class, expected removals over life, how many parts
must be removed to reach it, and how many soldered joints must be broken. From
that the tool prices one service event (fault-finding, access in and out,
desolder and remake, refit, retest), the labour, the risk of writing off the
assembly during rework, and the lifetime cost across expected removals. For any
soldered joint it also runs the trade: what connectorising costs in rupees and
grams, and how many removals it takes to pay back.

On an expensive board the write-off risk dominates the labour — at Indian labour
rates a connector rarely pays back on labour alone, but a 4% chance of killing a
₹38,000 board changes the answer completely. The payback figure prices those two
things only; turnaround time, flight-line versus bench repair, and aircraft
availability are usually the deciding arguments and are not in the number.

**Domains**

Parts are tagged mechanical, electrical, wiring or electromechanical, and rolled
up that way — so the interface between the mechanical and electrical sides, where
most integration problems live, can be looked at on its own.

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
- **Foam** — CNC or hot-wire from block (block cost, cut time, yield) or bead
  moulded (cycle time, cavities, tooling amortised)
- **Wire harness** — wire by the metre per conductor, connectors and contacts,
  cut/strip/crimp/connector-assembly times, sleeving, heatshrink, labels, ties,
  and continuity test
- **Purchased** — quoted price, so the BOM rolls up completely

Every part carries a cost basis: **vendor should-cost** adds scrap, factory
overhead, supplier margin and freight on top of the direct cost, giving you a
target price to negotiate against. **In-house shop cost** stops at direct cost
for make-vs-buy. Set a project default, override per part.

Each estimate shows its full working — every rate, time and assumption — under
"Show the working". That transparency is the whole point: an estimate you can
put in front of a supplier beats a number you cannot explain.

---

A composite layup model exists in the code (`costComposite`) but is left out of
the process dropdown, since it is not part of the current BOM. Re-enabling it is
a one-line change, marked in `processFields`.

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
| **Analysis** | KPIs, part-by-part table, per-module and per-domain rollups, serviceability, field deployment, cost split, ranked list of what to change, print-to-PDF |
| **Library** | Rates, materials, machines, DFA method tables, cost model coefficients — all editable |
| **Data** | Export/import project JSON, CSV BOM import, results CSV export, reset |

## Saving your work

Work is held in the browser's local storage, which is **per-browser and
per-file-path** — open the file from a different folder, browser or profile and
you start empty. **Export the project JSON** and commit it to this repo for
anything you want to keep or share. Import restores it anywhere.

## Importing a BOM

**`input-template.xlsx`** is the input specification: a Parts sheet with all 106
columns and dropdowns on every one that takes a fixed value, a field guide
saying what each column means and where the answer comes from, the accepted
values, and a sheet listing the inputs that live in the tool's Library rather
than in the file.

Fill it in, save the Parts sheet as CSV (File → Save As → CSV UTF-8), then
Data tab → *Import CSV*.

Column order does not matter, unknown columns are ignored, and missing ones
keep their defaults — so a two-column `name,qty` file imports fine and you
finish the analysis in the tool. Values that are not recognised are listed back
to you on import rather than silently dropped. The Data tab documents every
column too, and *Download blank template* gives you the header row alone.

106 columns cover every process. Most analyses need 25–35 — delete the column
groups for processes you do not use.

The bare minimum is `name`. For a DFA result you want `qty`, `module`, the three
minimum-part-count answers, `size`, `sym`, `dir`, `fix` and `fixCount`; for a
cost result, `process`, `material`, `volume` and the bounding box; for a mass
result, `massG` on every purchased part, since bought-in items have no geometry
to calculate from.

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
3. **Assembly sequence** — the model currently treats parts as an unordered set.
   A sequence would let re-orientation costs be attributed properly, and would
   let the field-deployment estimate follow the actual deployment procedure
   rather than summing the parts.
4. **Sheet metal and injection moulding** process models, if the part mix moves
   that way.
5. **Harness formboard length** from routed CAD rather than a typed length.
