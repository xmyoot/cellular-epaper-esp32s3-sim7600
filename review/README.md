# Engineering review — 2026-10-21

**Disposition: redesign required, manufacturing release blocked.** This review repairs source integrity and incorrect claims; it does not certify circuit operation or close the electrical defects below.

## Confirmed source repairs

- Restored project instance paths and numeric power-symbol annotations.
- Rebuilt qualified cached standard symbols and resolved inherited definitions. The original netlist exported only U2; the repaired netlist exports all 100 board components. Restoring real symbol pins exposes errors that the malformed cache concealed.
- Added project symbol/footprint library tables and a local custom symbol library. The unqualified modem symbol remains identifiable as custom.
- Replaced 98 incorrect PCB value properties with their schematic values; all 100 PCB values now match the schematic.
- Regenerated the BOM as one row per reference, including explicit C31/C32 DNP entries. Removed invented manufacturer/MPN associations and marked procurement unqualified.
- Corrected the supply-droop unit error, contradictory sleep-current arithmetic, divider values/settling assumption, component descriptions, and unsupported manufacturing/performance claims.

These fixes preserve the original copper geometry. **No electrical rerouting or corrected manufacturing package is claimed.**

## Current native checks

KiCad 10.0.7, after source repairs:

| Check | Result | Artifact |
| --- | --- | --- |
| ERC | 494 errors; warnings are retained in JSON | [erc-current.json](erc-current.json) |
| Copper DRC, zones refilled in memory | 0 violations | [drc-current.json](drc-current.json) |
| PCB unconnected items | 0 | same report |
| Schematic parity | 304 issues | same report |
| Complete netlist | 100 components | [netlist-current.net](netlist-current.net) |

The original imported ERC report had 156 errors and 2 warnings. The fresh baseline before cache repair additionally reported missing local library links. Higher post-repair counts reflect restoration of previously missing symbol pins, not a new validated circuit. Original reports and renders are historical evidence only.

## Open hardware defects

| Priority | Evidence in current PCB/source | Required correction |
| --- | --- | --- |
| Critical | U2 routes PWRKEY to pad 87, reset to 86, TXD to 11, MAIN antenna to 73, GNSS antenna to 75. The reviewed SIM7600G/G-H document specifies PWRKEY 3, RESET 4, TXD 71, MAIN_ANT 82 and GNSS_ANT 79. | Replace the entire custom symbol and land pattern against the selected module revision; audit every pad and reroute. Do not merely rename nets. |
| Critical | D8 USBLC6-2SC6: pad 1 = USIM_CLK, pad 6 = GND, pad 3 = USIM_DATA, pad 4 = USIM_RST. Its internally common pairs are 1/6 and 3/4. | Use a correctly mapped SIM protection network; the present part grounds clock and joins data/reset internally. |
| High | LED1/LED2 place their cathodes toward the driven signal and anodes at GND. LED3 has cathode at VBUS and anode at CHG_STAT; both R18 pads are VBUS. | Correct LED polarity and insert a real series resistor for the charge indicator; review modem LED drive capability. |
| High | J6 pin 18 (VDD, internal logic supply output on the intended panel) is tied to VCC_EPD. D3's SOD-123 cathode is at EPD_SW, rather than a rectified positive output. | Rebuild the complete boost/panel network from the selected panel reference circuit, including VDD bypass, diode orientation, MOSFET/inductor ratings and connector orientation. |
| High | U3 OE pin 8 is directly tied to +3.3V while VCCA is the modem 1.8V domain; both R11 pads are +3.3V. | Implement OE control and default-off behavior referenced to VCCA per the translator datasheet; verify powered-off behavior. |
| High | MODEM_STATUS is directly connected to a 3.3V MCU input without qualified 1.8V-to-3.3V translation. | Check guaranteed input thresholds and add translation if needed; audit UART flow-control directions too. |
| High | Hundreds of schematic pins are unconnected; 46 labels are dangling; schematic and PCB disagree. D2/D8 use a two-pin TVS symbol for a six-pin device. | Rebuild functional sheets with correct symbols, explicit nets and justified no-connect markers; achieve schematic/PCB parity. |
| High | U5 has two alternative parts in one value; U1 memory variant is unspecified; EPD uses GPIOs whose availability depends on module variant. | Lock exact MPNs and review power pinouts, regulator limits and GPIO availability. |
| High | Direct battery modem rail, unqualified PTC/capacitor/MOSFET parts, charger/system-load interaction, and unmeasured sleep current. | Complete power/current/thermal analysis and bench tests; remove unsupported battery-life claims. |
| Medium | No fabricator-controlled stackup or impedance qualification; old fabrication outputs are not tied to a valid electrical design. | Validate RF return paths and antenna keepouts, select stackup, regenerate all release files only after fixes. |

Sources: [SIMCom hardware design, pin table pp. 12–13](https://simcom.ee/documents/SIM7600E/sim7600g_sim7600g-h_hardware_design_v1.00.pdf), [ST USBLC6-2 functional diagram](https://www.st.com/resource/en/datasheet/usblc6-2.pdf), [TI TXS0104E pin functions and OE guidance](https://www.ti.com/lit/ds/symlink/txs0104e.pdf), [Good Display panel specification](https://files.seeedstudio.com/wiki/Other_Display/29-epaper/GDEY029T94.pdf).

The modem document is a manufacturer-authored reference for identifying contradictions; confirm the final purchased module revision against current manufacturer documentation before implementing its footprint. No unspecified 24-pin panel should be treated as interchangeable.

## Reproduce the checks

Install KiCad 10 and standard symbol/footprint libraries. Run from the repository root:

```sh
kicad-cli sch export netlist -o review/netlist-current.net Low-Power_Cellular_ePaper_Device_ESP32-S3_SIM7600.kicad_sch
kicad-cli sch erc --format json -o review/erc-current.json Low-Power_Cellular_ePaper_Device_ESP32-S3_SIM7600.kicad_sch
kicad-cli pcb drc --schematic-parity --refill-zones --format json -o review/drc-current.json Low-Power_Cellular_ePaper_Device_ESP32-S3_SIM7600.kicad_pcb
python3 scripts/check_sources.py
python3 scripts/check_release.py
```

`--refill-zones` checks a refilled board in memory; no `--save-board` was used. This review does not silently change copper. A clean metadata test only checks reference/value/cache/export integrity. The release gate reads both CAD findings and explicitly open hardware blockers. It must fail for this revision.

## Release gates

1. Correct symbols, pinouts and device-specific circuits; achieve a complete, readable schematic with zero unexplained ERC errors.
2. Replace the modem land pattern and update PCB from the schematic; reroute, refill zones, then obtain zero unconnected items, no unexplained DRC errors and zero parity issues.
3. Qualify exact BOM MPNs, voltage/current ratings, tolerances, DNP status and assembler rotations; confirm connector mating and mechanical clearances.
4. Validate charging and startup safely on a current-limited supply; scope modem VBAT at worst-case input/load, verify power gating and deep sleep, test SIM attach/GNSS/USB/display, and measure regulator temperature.
5. Document actual results, regenerate fabrication files from the reviewed commit, and replace historical renders before presenting the project as a completed design.
