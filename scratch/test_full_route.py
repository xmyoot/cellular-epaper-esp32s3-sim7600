import subprocess
import os

KICAD_PYTHON = r"C:\Program Files\KiCad\10.0\bin\python.exe"
ROUTER = r"tools\KiCadRoutingTools\py_router\route.py"
IN_PCB = r"scratch\clean_unrouted.kicad_pcb"
OUT_PCB = r"scratch\test_routed.kicad_pcb"

cmd = [
    KICAD_PYTHON, ROUTER,
    IN_PCB, OUT_PCB,
    "--layers", "F.Cu", "B.Cu",
    "--ordering", "mps",
    "--power-nets", "VBAT_MODEM", "VBAT", "VBUS", "VCC_EPD", "VBAT_RAW",
    "--power-nets-widths", "1.5", "1.0", "0.8", "0.8", "1.0",
    "--neckdown-length", "1.0",
    "--overwrite"
]

print("Running route.py on all nets...")
res = subprocess.run(cmd, capture_output=True, text=True)
print("Return code:", res.returncode)
print("STDOUT (last 40 lines):")
for line in res.stdout.splitlines()[-40:]:
    print(line)
if res.stderr:
    print("STDERR (first 20 lines):")
    for line in res.stderr.splitlines()[:20]:
        print(line)
