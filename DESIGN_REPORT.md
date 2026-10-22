# Revision B engineering design report

2026-10-21. Status: engineering prototype, manufacturing release blocked pending the recorded validation gates. No physical hardware tests, compliance certification, or measured battery-life results are claimed.

## Review and redesign

The original schematic cached incomplete symbols and exported only one component. Restoring real pins exposed 494 ERC errors and 304 schematic/PCB parity issues. The old zero-unconnected PCB result did not establish electrical correctness. The initial electrical review is preserved in [review/legacy/electrical-review-before-redesign.md](review/legacy/electrical-review-before-redesign.md); original source remains in Git history.

Revision B replaces that connectivity with an explicit [pin/net map](design/rev-b-netmap.json), a hierarchical schematic, and a replacement PCB. These corrections address the identified circuit defects:

| Subsystem | Revision B implementation |
| --- | --- |
| MCU | ESP32-S3-WROOM-1-N8: 8 MB flash, no PSRAM. Battery-divider enable moved from strapping GPIO3 to GPIO47. USB uses GPIO19/20 and 22 Ω series resistors. |
| Modem | SIM7600G-H, 135 pads. PWRKEY 3, RESET 4, VDD_1V8 15, SIM 17–20, STATUS 49, RTS/CTS 66/67, RXD/TXD 68/71, diversity/GNSS/main RF 59/79/82. Unused/reserved terminals are NC. |
| UART | TXS0104ED, VCCA = modem 1.8 V, VCCB = 3.3 V. OE pulled to VCCA through 10 kΩ and down by 100 kΩ. Separate SN74LVC1T45 translates STATUS with DIR tied to VCCA. |
| SIM | Correct SIM socket symbol, VPP NC, three independent PESD3V3U1UL protectors with cathodes on signals. No internally paired ESD array can join reset/data or ground clock. |
| Display | GDEY029T94 four-wire SPI, BS1 grounded. Pin 18 is bypassed internally generated VDD, isolated from external VCC. Positive/negative rectifiers, flying capacitor and bypass rails follow the panel reference circuit. |
| Display boost | Si1308EDL SC-70 MOSFET; SRN4018-470M 47 µH, 600 mA rated / 620 mA saturation; 2.2 Ω sense resistor; 4.7 µF/25 V flying capacitor and 1 µF/25 V rail capacitors. |
| Battery | Protected, externally charged 1S LiPo rated ≥3 A; 2.5 A fast fuse; switched modem supply; AP2112K-3.3TRG1 600 mA LDO. USB has no charging/system-power path. |
| RF | Main + diversity LTE U.FL connectors and passive GNSS U.FL. Main π-network shunt capacitors remain DNP. No active GNSS antenna DC bias. |
| Indicators | User LED cathode grounded, anode fed through 1 kΩ. Original charger/network indicators removed. |

USBLC6-2SC6 uses its actual six-pin symbol: D+ on 1/6, D− on 3/4, GND on 2 and VBUS on 5. PWRKEY/reset and power-gate controls have default-off pull-downs. Firmware must gracefully stop the modem before removing its supply.

## Power limits and calculations

The modem runs from switched battery voltage, with an operating requirement of 3.4–4.2 V at its supply pins and transmit pulses approaching 2 A. A charged 4.2 V cell leaves no allowance for an overvoltage charging source: never attach a bench supply above 4.2 V to the battery input. Disable the modem before the loaded battery falls below 3.6 V and verify the actual rail remains above 3.4 V. The pack protection circuit is a last-resort protection, not the normal modem shutdown mechanism.

C11/C12 select KEMET T520D227M006ATE015 polymer capacitors (220 µF, 6.3 V, 15 mΩ nominal ESR specification). C13/C14 contribute 47 µF each and C15/C16 10 µF each: 554 µF nominal total, excluding small bypass capacitors. Effective MLCC capacitance and pulse impedance require qualification.

The original calculation `2.5 A × 577 µs / 540 µF` equals **2.67 V**, not 2.67 mV. Capacitors alone cannot support a modem burst. Supply impedance, fuse resistance, MOSFET resistance, copper geometry and cell condition must be measured together. Do not reuse the original droop or multi-year runtime claims.

AP2112 typical quiescent current is 55 µA. Thus a sub-10 µA board sleep claim is unsupported. ESP32 sleep, translator leakage, sensor current and switches add to that figure. At 600 mA and 4.2 V input, the LDO dissipates approximately `(4.2−3.3)×0.6 = 0.54 W`; it is a peak limit, not a guaranteed continuous thermal operating point.

The enabled 1 MΩ/1 MΩ divider draws 2.1 µA at 4.2 V. With C6 = 100 nF its nominal time constant is 50 ms. Wait at least 250 ms before an ADC reading, then characterize ADC gain, attenuation, source impedance and offset. Duty-cycle energy and measured registration/refresh times are required for runtime estimates.

## Layout and footprint basis

The board has four copper layers, with In1.Cu reserved for the continuous ground reference and signal routing on the outer layers / In2.Cu. The modem footprint is reconstructed from SIMCom hardware design figure 4: 30 mm body, 31 mm outer pad extent, 0.60 mm perimeter pad width / 1 mm pitch, 1.60 mm radial pad length (centres ±14.70 mm), 1.8 mm inner-ring pitch, and 3.10 mm centre ground lands on 4 mm pitch. Pad 120 has the indicated corner chamfer. Two manufacturer keepout regions prohibit copper, tracks and vias on all copper layers. The selected module revision and a 1:1 footprint print must be checked before procurement.

RF traces stay on F.Cu above the ground reference. Their provisional geometry is not an impedance certification. Final stackup, dielectric spacing/material, copper thickness and coplanar ground clearance must be agreed with the fabricator and checked before ordering. Confirm the ESP32 antenna clearance against its module guidelines and enclosure.

The routed board contains four SMD pad/paste-overlapping vias that require IPC-4761 Type VII filled, capped and plated processing. Locations and process constraints are recorded in [fabrication constraints](design/FABRICATION_CONSTRAINTS.md). This process must be confirmed before ordering.

## Validation still required

See [validation procedure](design/VALIDATION.md). Full BOM MPN selection/ratings, exact purchased modem package, panel FPC contact orientation, thermal limits, controlled impedance, prototype bring-up, cellular attach/GNSS, display waveforms, power sequencing and measured sleep remain release gates. Historic fabrication exports are not valid for this revision. The portfolio entry remains unpublished.

## Primary references

- [SIMCom hardware design V1.07 (distributed filename V1.08)](https://files.waveshare.com/upload/5/52/SIM7600G%28-H%29_SIM7600NA%28-H%29_Hardware_Design_V1.08.pdf), pin table, power, UART and footprint figures.
- [Good Display GDEY029T94 specification](https://files.seeedstudio.com/wiki/Other_Display/29-epaper/GDEY029T94.pdf), pin table and typical application circuit.
- [TI TXS0104E](https://www.ti.com/lit/ds/symlink/txs0104e.pdf) and [SN74LVC1T45](https://www.ti.com/lit/ds/symlink/sn74lvc1t45.pdf), supply/enable references and powered-off isolation.
- [ST USBLC6-2](https://www.st.com/resource/en/datasheet/usblc6-2.pdf), internal diode topology and pin mapping.
- [Nexperia PESD3V3U1UL](https://assets.nexperia.com/documents/data-sheet/PESD3V3U1UL.pdf), cathode 1, anode 2.
- [Espressif schematic checklist](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/schematic-checklist.html) and [layout guidance](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/pcb-layout-design.html).
- [Diodes AP2112](https://www.diodes.com/assets/Datasheets/AP2112.pdf), [Vishay Si1308EDL](https://www.vishay.com/docs/63399/si1308edl.pdf), [Bourns SRN4018](https://www.bourns.com/docs/product-datasheets/srn4018.pdf), [KEMET T520D227M006ATE015](https://search.kemet.com/component-documentation/download/specsheet/T520D227M006ATE015).
