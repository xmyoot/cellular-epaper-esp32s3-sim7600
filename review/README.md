# Revision B engineering review — 2026-10-21

**Disposition: CAD routing complete; manufacturing and physical validation remain blocked.** This is an engineering prototype, not a demonstrated working product. The portfolio entry stays unpublished.

## Current native checks

KiCad 10.0.7, with refilled zones and schematic parity enabled:

| Check | Result | Evidence |
| --- | --- | --- |
| ERC | 0 errors, 1 library-comparison warning | [erc-current.json](erc-current.json) |
| PCB DRC | 0 violations | [drc-current.json](drc-current.json) |
| Unconnected PCB items | 0 | same report |
| Schematic/PCB parity | 0 issues | same report |
| Source / BOM / PCB pin-net consistency | 108 components, passed | `scripts/check_sources.py` |
| Critical circuit and modem footprint regressions | Passed | `scripts/check_hardware.py` |

The ERC warning is `lib_symbol_mismatch` on U6 (SHT4x). Its cached symbol was compared structurally to the installed standard-library definition and matches after removing the library prefix from its name; its four pin assignments are checked against the design map. The warning is retained, not excluded. It remains a library reconciliation item for the final independent review.

The initial six open connections have been repaired. C37 is on the SHT40 supply-pin side, with explicit straight pin escapes that respect the sensor footprint keepouts. C34/C39 supply connections and local USB resistor placement were corrected. Decorative silkscreen was clipped or moved to fabrication layers, with the resulting J1/U1/D7 derivatives saved in the project-local footprint library.

## What changed

The old design's malformed cached symbols concealed major pin and net errors. Revision B rebuilds the modem's 135-pad symbol and land pattern, SIM protection, UART enable/STATUS voltage domains, display boost circuit, exact MCU variant and battery power architecture. See [design report](../DESIGN_REPORT.md) for the circuit changes, manufacturer references and calculations. The original findings are preserved in [the historical review](legacy/electrical-review-before-redesign.md).

The replacement board is 100 × 80 mm, four layers, with an inner ground reference. RF geometry and USB routing still require qualification against an actual fabricator stackup. Four small signal/supply vias overlap SMD pad/paste areas and require **IPC-4761 Type VII filled, capped and plated via-in-pad processing**; see [fabrication constraints](../design/FABRICATION_CONSTRAINTS.md). No fabrication order is authorized by these checks.

The [schematic PDF](rev-b/schematic.pdf) and [top CAD view](rev-b/pcb-top.png) represent revision B. The modem and SIM socket have no installed 3D body models; visible lands are not a depopulation instruction. Renders cannot establish component fit.

## Reproduce checks

With KiCad 10 and its standard libraries installed, run from the repository root (replace `kicad-cli` with its installed path if needed):

```sh
python3 scripts/check_sources.py
python3 scripts/check_hardware.py
kicad-cli sch erc --format json -o review/erc-current.json Low-Power_Cellular_ePaper_Device_ESP32-S3_SIM7600.kicad_sch
kicad-cli sch export netlist -o review/netlist-current.net Low-Power_Cellular_ePaper_Device_ESP32-S3_SIM7600.kicad_sch
kicad-cli pcb drc --format json --schematic-parity --refill-zones --save-board -o review/drc-current.json Low-Power_Cellular_ePaper_Device_ESP32-S3_SIM7600.kicad_pcb
python3 scripts/check_release.py
```

The last command intentionally exits 1 while release gates remain open. JSON reports retain native severities; no ERC/DRC exclusions are used. Source hashes identify the reviewed source, rather than implying physical qualification.

`scripts/generate_revision_b.py` reconstructs the schematic, custom modem library and BOM from the net map. `scripts/place_revision_b.py` creates placement only and **replaces the routed board**; it is not a release regeneration command. The checked-in routed board is the reviewed layout. Historic `scratch/` experiments are not part of this workflow.

## Remaining release gates

Complete the qualified BOM, purchased-part orientation/footprint checks, fabricator stackup and via-in-pad process, RF/USB impedance review, supply-transient and thermal qualification, and all recorded prototype tests in [design/VALIDATION.md](../design/VALIDATION.md). Reconcile the retained ERC library warning during independent review. No measured battery-life, RF, display or sleep-current results are claimed.
