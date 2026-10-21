# Low-Power Cellular ePaper Device (ESP32-S3 + SIM7600)

### Remote IoT ePaper Display Node with LTE Cat-1 Cellular Connectivity
[![KiCad Version](https://img.shields.io/badge/KiCad-10.0-blue.svg)](https://www.kicad.org/)
[![PCB Layers](https://img.shields.io/badge/PCB-4--Layer%20ENIG-brightgreen.svg)](https://jlcpcb.com/)
[![Form Factor](https://img.shields.io/badge/Dimensions-85.1%20x%2057.6%20mm-orange.svg)]()

---

## Hardware Overview
A connected IoT display terminal integrating an **ESP32-S3-WROOM-1** with a **SIMCom SIM7600 LTE Cat-1 cellular module** and SPI ePaper display driver interface. Engineered for remote signage, transit schedules, and environmental status monitors that update over cellular and remain visible indefinitely with zero static power.

### Key Features
- **Processing Core:** Espressif **ESP32-S3-WROOM-1** (240 MHz dual-core LX7, Wi-Fi 4, BLE 5.0).
- **Cellular Connectivity:** SIMCom **SIM7600** LTE Cat-1 module with global band coverage, GNSS positioning, and Micro-SIM card slot (`J3`).
- **Display Interface:** Dedicated FPC connector for ultra-low-power electronic paper (EPD) panels.
- **Power Architecture:** Li-Ion / LiPo battery management with solar harvesting input support and high-current 4.2V cellular pulse regulator.
- **100% Routed:** 4-layer stackup with 1089 track segments, 208 vias, and 0 unconnected nets.
