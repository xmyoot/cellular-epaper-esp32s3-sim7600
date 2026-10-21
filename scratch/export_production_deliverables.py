import os
import subprocess
import csv
import pcbnew

ROOT = r"C:\Users\hecto\Documents\KiCAD_Projects\Low-Power_Cellular_ePaper_Device_ESP32-S3_SIM7600"
KICAD_CLI = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
PCB_FILE = os.path.join(ROOT, "Low-Power_Cellular_ePaper_Device_ESP32-S3_SIM7600.kicad_pcb")
FAB_DIR = os.path.join(ROOT, "fabrication")
RENDERS_DIR = os.path.join(ROOT, "renders")

os.makedirs(FAB_DIR, exist_ok=True)
os.makedirs(RENDERS_DIR, exist_ok=True)

# 1. Export Gerbers
print("Exporting production Gerbers (11 layers)...")
gerber_cmd = [
    KICAD_CLI, "pcb", "export", "gerbers",
    "--output", FAB_DIR,
    "--layers", "F.Cu,B.Cu,In1.Cu,In2.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,F.Paste,B.Paste,Edge.Cuts",
    "--subtract-soldermask",
    "--check-zones",
    PCB_FILE
]
subprocess.run(gerber_cmd, check=True)

# 2. Export Drill files
print("Exporting drill files (PTH, NPTH, PDF maps)...")
drill_cmd = [
    KICAD_CLI, "pcb", "export", "drill",
    "--output", FAB_DIR,
    "--format", "excellon",
    "--excellon-units", "mm",
    "--excellon-zeros-format", "decimal",
    "--excellon-separate-th",
    "--generate-map",
    "--map-format", "pdf",
    PCB_FILE
]
subprocess.run(drill_cmd, check=True)

# 3. Export Component Centroid / POS
print("Exporting pick-and-place POS CSV...")
pos_file = os.path.join(FAB_DIR, "Low-Power_Cellular_ePaper_Device_ESP32-S3_SIM7600_pos.csv")
pos_cmd = [
    KICAD_CLI, "pcb", "export", "pos",
    "--output", pos_file,
    "--format", "csv",
    "--units", "mm",
    "--side", "both",
    PCB_FILE
]
subprocess.run(pos_cmd, check=True)

# 4. Generate Comprehensive BOM
print("Generating Bill of Materials (BOM)...")
board = pcbnew.LoadBoard(PCB_FILE)
bom_items = {}

# Sourcing and descriptions dictionary
PART_INFO = {
    "ESP32-S3-WROOM-1-N16R8": ("Espressif", "ESP32-S3-WROOM-1-N16R8", "Dual-Core Xtensa LX7 MCU, 16MB Flash, 8MB PSRAM, Wi-Fi 4 + BLE 5.0", "C2913200"),
    "SIMCom_SIM7600G": ("SIMCom", "SIM7600G-H", "Multi-Band LTE-TDD/LTE-FDD/HSPA+ and GNSS LGA Module", "C2934336"),
    "TXS0108EPWR": ("Texas Instruments", "TXS0108EPWR", "8-Bit Bidirectional Voltage-Level Translator (TSSOP-20)", "C14120"),
    "MCP73831-2ATI/OT": ("Microchip", "MCP73831T-2ATI/OT", "Linear Li-Ion/Li-Polymer Battery Charger 500mA (SOT-23-5)", "C14881"),
    "AP2112K-3.3TRG1": ("Diodes Inc.", "AP2112K-3.3TRG1", "600mA Low-Dropout Linear Regulator, 3.3V, Low Noise (SOT-23-5)", "C78144"),
    "SHTC3": ("Sensirion", "SHTC3", "Digital Humidity & Temperature Sensor +/-2% RH, 0.2C (DFN-4)", "C194656"),
    "DMP2035U-7": ("Diodes Inc.", "DMP2035U-7", "P-Channel MOSFET -20V, -4.2A, Rds(on)=35mOhm (SOT-23)", "C148475"),
    "2N7002": ("Diodes Inc.", "2N7002", "N-Channel MOSFET 60V, 115mA (SOT-23)", "C8545"),
    "SI2301CDS": ("Vishay", "SI2301CDS-T1-GE3", "P-Channel MOSFET -20V, -3.1A (SOT-23)", "C10457"),
    "B0520WS": ("Diodes Inc.", "B0520WS", "Schottky Barrier Diode 20V, 0.5A (SOD-323)", "C80228"),
    "MBR0520": ("ON Semi", "MBR0520LT1G", "Schottky Diode 20V, 0.5A, Low Vf (SOD-123)", "C9142"),
    "SMAJ4.5A": ("Littelfuse", "SMAJ4.5A", "TVS Diode 4.5V, 400W Unidirectional (SMA/DO-214AC)", "C80092"),
    "USBLC6-2SC6": ("STMicroelectronics", "USBLC6-2SC6", "Ultra-Low Capacitance ESD Protection for USB (SOT-23-6)", "C7519"),
    "PESD0402-140": ("TE Connectivity", "PESD0402-140", "0402 Bidirectional ESD Protection Diode", "C9882"),
    "10uH": ("Sunlord", "SDCL1608C100JTDF", "Power Inductor 10uH, 1.2A, Shielded", "C168341"),
    "47uH": ("Coilcraft", "LPS4018-473MRB", "e-Paper Boost Inductor 47uH, 0.5A", "C112344"),
    "100uF_Tant": ("KEMET", "T495D107M010ATE100", "Low-ESR Tantalum Capacitor 100uF 10V Case D (7343), ESR=100mOhm", "C3399"),
    "220uF_Tant": ("KEMET", "T495X227M010ATE100", "Low-ESR Tantalum Capacitor 220uF 10V Case D (7343), ESR=100mOhm", "C7118"),
}

for fp in board.GetFootprints():
    ref = fp.GetReference()
    val = fp.GetValue()
    fp_name = fp.GetFPID().GetUniStringLibId()
    layer = "Top (F.Cu)" if not fp.IsFlipped() else "Bottom (B.Cu)"

    key = (val, fp_name)
    if key not in bom_items:
        bom_items[key] = {
            "refs": [],
            "val": val,
            "footprint": fp_name,
            "layer": set()
        }
    bom_items[key]["refs"].append(ref)
    bom_items[key]["layer"].add(layer)

bom_rows = []
for (val, fp_name), data in sorted(bom_items.items(), key=lambda x: x[1]["refs"][0]):
    refs_sorted = sorted(data["refs"], key=lambda r: (r[0], int(''.join(filter(str.isdigit, r)) or '0')))
    qty = len(refs_sorted)
    ref_str = ", ".join(refs_sorted)
    layers_str = "/".join(sorted(data["layer"]))

    # Match part info
    mfg = "Generic"
    mpn = val
    desc = f"{val} {fp_name}"
    lcsc = ""

    if val in PART_INFO:
        mfg, mpn, desc, lcsc = PART_INFO[val]
    elif val.endswith("uF") or val.endswith("nF") or val.endswith("pF"):
        desc = f"Ceramic Capacitor {val}, 50V/16V X7R/X5R"
        mfg = "Samsung / Murata"
    elif val.endswith("k") or val.endswith("M") or val.endswith("R") or val.endswith("m"):
        desc = f"Thick Film Resistor {val}, 1% tolerance"
        mfg = "Yageo / Uni-Ohm"

    bom_rows.append({
        "Quantity": qty,
        "Designators": ref_str,
        "Value": val,
        "Footprint": fp_name,
        "Manufacturer": mfg,
        "MPN": mpn,
        "Description": desc,
        "LCSC_Part": lcsc,
        "Layer": layers_str
    })

fieldnames = ["Quantity", "Designators", "Value", "Footprint", "Manufacturer", "MPN", "Description", "LCSC_Part", "Layer"]
bom_csv_path = os.path.join(FAB_DIR, "BOM.csv")
with open(bom_csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(bom_rows)

# Copy to root BOM.csv
with open(os.path.join(ROOT, "BOM.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(bom_rows)

print(f"Exported BOM with {len(bom_rows)} line items ({sum(r['Quantity'] for r in bom_rows)} total components).")

# 5. Generate 3D Renders
print("Rendering 3D Isometric View...")
iso_png = os.path.join(RENDERS_DIR, "pcb_3d_iso.png")
render_iso_cmd = [
    KICAD_CLI, "pcb", "render",
    "--output", iso_png,
    "--rotate", "-45,0,45",
    "--perspective",
    "--zoom", "1.3",
    "--quality", "high",
    "--floor",
    "--width", "1920",
    "--height", "1080",
    PCB_FILE
]
subprocess.run(render_iso_cmd, check=True)

print("Rendering 3D Top View...")
top_png = os.path.join(RENDERS_DIR, "pcb_3d_top.png")
render_top_cmd = [
    KICAD_CLI, "pcb", "render",
    "--output", top_png,
    "--side", "top",
    "--quality", "high",
    "--width", "1920",
    "--height", "1080",
    PCB_FILE
]
subprocess.run(render_top_cmd, check=True)

print("Rendering 3D Bottom View...")
bot_png = os.path.join(RENDERS_DIR, "pcb_3d_bottom.png")
render_bot_cmd = [
    KICAD_CLI, "pcb", "render",
    "--output", bot_png,
    "--side", "bottom",
    "--quality", "high",
    "--width", "1920",
    "--height", "1080",
    PCB_FILE
]
subprocess.run(render_bot_cmd, check=True)

# Also copy renders to root directory
import shutil
shutil.copy(iso_png, os.path.join(ROOT, "pcb_3d_iso.png"))
shutil.copy(top_png, os.path.join(ROOT, "pcb_3d_top.png"))
shutil.copy(bot_png, os.path.join(ROOT, "pcb_3d_bottom.png"))

print("All production deliverables generated successfully!")
