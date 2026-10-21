import re
import pcbnew

b = pcbnew.LoadBoard("Low-Power_Cellular_ePaper_Device_ESP32-S3_SIM7600.kicad_pcb")
pcb_nets = {net.GetNetname() for net in b.GetNetsByName().values() if net.GetNetname()}
print(f"PCB has {len(pcb_nets)} named nets.")

with open("sch_netlist.net", "r") as f:
    sch_text = f.read()

# Match multiline (net (code "...") (name "...")
sch_nets = set(re.findall(r'\(net\s+\(code\s+"[^"]+"\)\s+\(name\s+"([^"]+)"\)', sch_text, re.DOTALL))
print(f"SCH has {len(sch_nets)} nets total.")

# Filter out unconnected-(...)
named_sch_nets = {n for n in sch_nets if not n.startswith("unconnected-")}
print(f"SCH has {len(named_sch_nets)} functional named nets.")

diff_pcb = pcb_nets - named_sch_nets
diff_sch = named_sch_nets - pcb_nets
print("In PCB but not named SCH:", diff_pcb)
print("In named SCH but not PCB:", diff_sch)
