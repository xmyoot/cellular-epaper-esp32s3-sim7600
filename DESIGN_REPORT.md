# Cellular ePaper device: corrected engineering assessment

Reviewed 2026-10-21 with KiCad 10.0.7. **This is a design study requiring electrical and PCB redesign, not a production-ready device.** The original production/certification claims are withdrawn. The original report remains recoverable in Git history.

## Architecture present in the source

The board combines an ESP32-S3-WROOM-1, a custom SIM7600 footprint, TXS0104ED four-channel translator, MCP73831 charger, a SOT-23-5 3.3 V regulator position, SHT40 sensor, nano-SIM connector, two U.FL connectors, and a 24-pin display connector. P-channel MOSFET stages gate the modem, display, and battery divider.

The source uses AO3401A P-FETs and BSS138 N-FETs. Earlier claims of TXS0108E, SHTC3, Micro-SIM, DMP2035U switches, and 500 mA battery fuse did not match the schematic. The schematic specifies a 2.5 A PTC. These are source descriptions, not confirmation that the circuits operate correctly.

## Corrected power calculations

The original report evaluated `I × t / C` with 2.5 A, 577 µs, and 540 µF as 2.67 mV. The correct result is **2.67 V**. Adding the report's assumed 33.3 mΩ ESR gives approximately **2.75 V**, not 86 mV. This is a capacitor-only illustrative calculation; an actual battery/trace/capacitor transient requires a source-impedance model and measurement. It does not predict the assembled board's droop or guarantee modem operation.

The source actually specifies C11/C12 = 220 µF each, C13/C14 = 47 µF each, and C15/C16 = 10 µF each: **554 µF nominal**, excluding small decouplers. Effective capacitance depends on selected parts, DC bias and tolerance. The report's capacitor references and ESR assumptions were not a qualified BOM.

For an AP2112 implementation, the manufacturer's typical regulator quiescent current alone is 55 µA. Combining that with the old report's assumed 7 µA MCU sleep current gives 62 µA before other loads. Therefore the claimed 8.5 µA board sleep current is unsupported. The schematic's `RT9080-33 / AP2112K` value is ambiguous; the next revision must select one exact regulator and validate its pinout, output-current, dropout, stability and leakage requirements. [Diodes AP2112](https://www.diodes.com/datasheet/download/AP2112.pdf)

The 1 MΩ / 1 MΩ divider in the schematic draws 2.1 µA at 4.2 V while enabled. With C6 = 100 nF, its nominal Thevenin time constant is `500 kΩ × 100 nF = 50 ms`; a 100 µs sampling interval cannot be assumed settled. Allow settling, validate ADC input requirements, and characterize measurement error.

The modem rail is switched battery voltage, not a regulated 4.2 V rail. Battery discharge, PTC resistance, switch resistance, inrush, thermal behavior and low-voltage cutoff need analysis. The MCP73831 topology is not a solar MPPT/power-path controller; charging under system load and USB current limits require review. No multi-year battery-life estimate is justified without measured duty-cycle energy, modem registration time, display refresh energy and cell self-discharge.

## Selected redesign targets

- **SIM7600G-H:** use a single manufacturer hardware revision and its exact symbol/land pattern. The existing custom pin mapping is wrong. The manufacturer offers distinct SIM7600 families; the previous generic Cat-1 claim must not be applied to the selected H variant. [SIMCom SIM7600X-H](https://www.simcom.com/product/SIM7600X-H.html)
- **GDEY029T94:** a documented 2.9-inch 296 × 128 monochrome SPI panel with a manufacturer reference circuit. Match its power network and connector contact orientation; the existing generic 24-pin circuit is not approved for it. [Good Display product and documentation](https://www.good-display.com/product/389.html)
- **ESP32-S3 module:** select an exact memory variant and recheck every GPIO against that variant's reserved flash/PSRAM pins before committing the pin assignment.

These selections define the next revision; they are not claims that the current CAD has been converted.

## Layout and validation limits

Four copper layers exist, but the reported 50.2 Ω RF impedance has not been substantiated against a fabricator stackup. Fabricator dielectric thickness, material properties, copper thickness, trace geometry, and continuous return paths must be confirmed. No IPC class certification, EMC compliance, or assembly qualification has been demonstrated.

Current checks distinguish geometric routing from electrical correctness: zero copper DRC violations coexist with 494 ERC errors and 304 schematic/PCB parity issues. See the [detailed review](review/README.md), including the uncorrected hardware defects and release gates.
