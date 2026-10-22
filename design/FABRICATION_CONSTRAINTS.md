# Revision B fabrication constraints — not a release package

- Board outline: 100 × 80 mm; four copper layers. In1.Cu is the ground reference. Final laminate, dielectric spacing, copper weight and impedance geometry remain to be agreed with a fabricator.
- Nominal routing clearance: 0.15 mm; nominal through vias: 0.60 mm outer diameter / 0.30 mm finished drill. Review all geometry against the chosen process; these nominal values do not constitute a capability signoff.
- Four vias overlap SMD pad/paste regions. They are marked `filling yes` / `capping yes` in the board. **IPC-4761 Type VII filled, capped and plated via-in-pad processing is mandatory for the current layout.** Ordinary open or tented barrels are not an acceptable substitution. Ask the fabricator/assembler to review the small pad/via geometry before procurement.

| Via coordinate (mm, KiCad board origin) | Net | Nearby pad |
| --- | --- | --- |
| 61.0, 55.8 | +3.3V | U1.2 |
| 96.9, 70.6 | +3.3V | U3.14 |
| 90.9, 87.1 | +3.3V | U7.6 |
| 142.0, 117.6 | I2C_SDA | R22.2 |

- Independently check the SIM7600G-H land pattern against the exact purchased 135-pad package, manufacturer keepouts, paste aperture treatment and module orientation. Confirm the panel FPC contact side and connector orientation.
- No controlled-impedance certification, complete assembly-qualified BOM or physical fit check is available yet. Gerbers, drills and assembly files for revision B must be generated only after the release gates close. Files under `fabrication/legacy/` are invalid for this revision.
