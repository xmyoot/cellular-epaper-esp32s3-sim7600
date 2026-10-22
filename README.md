# Cellular ePaper — ESP32-S3 + SIM7600G-H

Revision B is an **engineering prototype under validation**. It is not released for fabrication or presented as a working, tested device. The portfolio case study remains unpublished pending validation.

This battery-powered design combines an ESP32-S3-WROOM-1-N8, SIM7600G-H LTE modem, GDEY029T94 2.9-inch monochrome ePaper panel interface, and SHT40 temperature/humidity sensor. It uses a protected 1S LiPo, switched modem/display supplies, native USB programming, and 1.8 V UART translation.

## Revision B changes

The initial review found an incorrect modem pinout and footprint, disconnected schematic pins, schematic/PCB disagreement, a SIM protection short, reversed LEDs, unsafe translator enable voltage, and an incompatible display power circuit. Revision B rebuilds the functional schematics and PCB from an explicit pin/net map. See [design report](DESIGN_REPORT.md) and [review results](review/README.md).

To simplify the power architecture, **the battery is charged externally**. USB-C is data/programming only; it does not power or charge the board. The original MCP73831 charger and its unresolved operation under system load have been removed. Use only a protected 1S pack capable of at least 3 A, verify connector polarity, and disconnect the pack for charging.

## Open in KiCad

Use KiCad 10 with the standard libraries installed. Open `Low-Power_Cellular_ePaper_Device_ESP32-S3_SIM7600.kicad_pro`. The project includes its custom 135-pad modem symbol/footprint and six functional schematic sheets. The board is 100 × 80 mm with four copper layers.

- [Component pin/net map](design/rev-b-netmap.json)
- [BOM](BOM.csv): engineering selections; procurement and assembly qualification remain open
- [Bring-up and validation procedure](design/VALIDATION.md)
- [Release status](review/release-status.json)

## CAD review artifacts

[Revision B schematic PDF](review/rev-b/schematic.pdf) · [PCB top CAD view](review/rev-b/pcb-top.png). Native checks report 0 ERC errors (1 retained library warning), 0 PCB DRC violations, 0 open connections and 0 schematic/PCB parity issues. Fabrication requires the [recorded via-in-pad process and stackup qualification](design/FABRICATION_CONSTRAINTS.md).

## Checks and release status

Run `python3 scripts/check_sources.py` for source consistency and `python3 scripts/check_hardware.py` for the audited critical connections. Regenerate native ERC/DRC reports using the commands in [review/README.md](review/README.md).

`python3 scripts/check_release.py` deliberately fails until all manufacturing and physical-validation gates are closed. A clean ERC/DRC result alone does not establish RF performance, battery life, display compatibility, or successful hardware operation.

Original manufacturing files, reports, and renders are retained only as explicitly marked historical material. Do not fabricate from those exports.
