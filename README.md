# Cellular ePaper node — ESP32-S3 + SIM7600

**Status: hardware redesign required; not released for fabrication.**

A four-layer, battery-powered cellular display design exploring ESP32-S3 control, modem power gating, an SPI ePaper interface, USB charging, and environmental sensing. This repository contains CAD source and a documented engineering review, not a tested product.

![Original board layout visualization](pcb_3d_iso.png)

*The render depicts the original routed layout. It is not evidence of functional validation.*

## Review status — 2026-10-21

An independent source review found incorrect modem pin assignments, schematic connectivity failures, and inconsistent manufacturing documentation. Source metadata and documentation have been corrected; circuit and layout repair remain open.

| Check | Current result |
| --- | --- |
| Schematic components exported to netlist | 100 / 100 (previous export contained only U2) |
| PCB/BOM value consistency | Pass, 100 components |
| KiCad 10.0.7 electrical check | 494 errors |
| PCB copper DRC after zone refill | 0 violations, 0 unconnected items |
| Schematic-to-PCB parity | 304 issues |
| Prototype, RF, power and display measurements | Not provided / not validated |

**A routed PCB is not necessarily a correct circuit.** See the [review and blocking defects](review/README.md) before using these files.

## Files

- `Low-Power_Cellular_ePaper_Device_ESP32-S3_SIM7600.kicad_pro`: open this project in KiCad 10 with its standard libraries installed.
- Matching `.kicad_sch` and `.kicad_pcb`: working source; electrical redesign is outstanding.
- `Cellular.kicad_sym`, project `.pretty/`, and library tables: portable custom library definitions. The modem definition is retained for traceability and is **not qualified**.
- [BOM.csv](BOM.csv): schematic-derived component values and footprints. Exact procurement MPNs remain unqualified; do not order from it as a released assembly BOM.
- [DESIGN_REPORT.md](DESIGN_REPORT.md): corrected analysis and revision direction.
- [review/](review/): current checks, source netlist, and reproduction instructions.
- [fabrication/](fabrication/README.md): **unvalidated historical exports**, not a manufacturing release.

## Revision direction

Use one explicitly identified modem variant, **SIM7600G-H**, and the documented monochrome **Good Display GDEY029T94** 296 × 128 SPI panel as redesign targets. These choices have not yet been integrated or validated in the existing board. A fixed module revision, verified land pattern, and panel reference circuit must precede rerouting.

There is no firmware, fabricated prototype evidence, battery-life measurement, controlled-impedance certification, or production qualification in this repository. No solar charging circuit or regulated 4.2 V modem supply is implemented.

## Checks

```sh
python3 scripts/check_sources.py
python3 scripts/check_release.py
```

The first command checks metadata consistency. The release check intentionally fails while the documented electrical and hardware blockers remain open. Regenerate KiCad reports using [these commands](review/README.md#reproduce-the-checks); saved reports are snapshots, not automatic validation of future edits.
