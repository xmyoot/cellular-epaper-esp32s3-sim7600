# Revision B validation record

All items below are **pending** unless a dated measurement is recorded. Native CAD checks are tracked separately in `review/`. Do not infer test success from an empty table or rendered PCB.

## Before assembly

1. Match the purchased SIM7600G-H's 135-pad package and manufacturer revision to the symbol and a 1:1 printed footprint; independently check orientation, inner grounds and keepouts.
2. Match GDEY029T94 FPC contact side, pin 1 and FH12 bottom-contact connector. Other 24-pin panels are not interchangeable.
3. Complete BOM manufacturer/MPN selection. Check ceramic DC bias, polymer ESR/ripple/derating, 25 V display capacitors, diode polarity, fuse pulse/time curve and ≤35 mΩ fuse resistance target, battery protection impedance, MOSFET ratings and assembler rotations.
4. Confirm the filled/capped/plated via-in-pad process in `FABRICATION_CONSTRAINTS.md`. Agree a four-layer fabricator stackup, then calculate RF/USB impedance and adjust trace geometry if needed. Review ground reference, antenna keepouts, module overhang and enclosure clearances.
5. Regenerate ERC, netlist, PCB DRC and parity at the exact reviewed commit. Regenerate manufacturing outputs only after the remaining gates are signed off.

## Current-limited bring-up

- Disconnect USB and panel initially. With the modem/display off, inject 3.8 V at the battery input with a low current limit. Check polarity, shorts, 3.3 V regulation and heating before raising the limit.
- Confirm USB VBUS cannot power or charge the battery rail. Connect a protected, ≥3 A 1S pack with pin 1 positive / pin 2 ground. Charge it offboard.
- Test BOOT/RESET and native USB enumeration. Check the battery ADC against a calibrated meter after ≥250 ms divider settling.
- Scope VBAT_MODEM at the module through startup, network registration and transmit at low battery / weak signal. Its minimum must remain ≥3.4 V and maximum ≤4.2 V; verify fuse, switch, connector and LDO temperatures.
- Confirm VDD_EXT, UART OE and STATUS translation. Verify modem-off leakage and absence of back-power through UART/USB service lines. Use the manufacturer PWRKEY timing, and AT+CPOF before hard power-off.
- Check SIM communication, network attach, data transfer, main/diversity antennas and passive GNSS reception. Document region/operator/module firmware and RF setup.
- With the correct panel connected, start with a current-limited supply. Scope boost rails and GDR/RESE operation, then verify a full refresh and busy timeout at temperature limits. Check for abnormal negative/positive rail excursions.
- Check all SPI/control outputs and pull-ups are disabled before removing display power. Confirm startup, reset, full refresh and shutdown across repeated cycles.
- Compare SHT40 readings with a reference and check thermal bias during LTE transmit/display refresh.
- Measure deep-sleep current, each switched rail's leakage, registration energy, refresh energy and duty-cycle average. Record pack capacity/temperature and avoid unsupported multi-year life estimates.

## Results

| Test | Conditions / instrument | Measured result | Date / reviewer |
| --- | --- | --- | --- |
| Physical prototype tests | Not yet performed | Pending | — |

Publish the portfolio case study only after the required tests and remaining release gates are documented as passed. Do not use the publication flag as a substitute for test evidence.
