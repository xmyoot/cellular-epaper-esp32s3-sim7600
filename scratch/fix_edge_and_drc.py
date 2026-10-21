import pcbnew
import json
import os

def mm(val):
    return pcbnew.FromMM(val)

PCB_PATH = r"scratch\test_routed.kicad_pcb"
PRO_PATH = r"scratch\test_routed.kicad_pro"

# 1. Update .kicad_pro rules
with open(PRO_PATH, "r") as f:
    pro_data = json.load(f)

rules = pro_data.setdefault("board", {}).setdefault("design_settings", {}).setdefault("rules", {})
rules["min_resolved_spoke_count"] = 1
rules["min_resolved_spokes"] = 1
rules["min_copper_edge_clearance"] = 0.2

with open(PRO_PATH, "w") as f:
    json.dump(pro_data, f, indent=2)

print("Updated .kicad_pro rules.")

# 2. Update board
b = pcbnew.LoadBoard(PCB_PATH)

# Remove old Edge.Cuts
drawings_to_remove = [d for d in b.GetDrawings() if d.GetLayerName() == "Edge.Cuts"]
for d in drawings_to_remove:
    b.Delete(d)

def add_line(start, end):
    seg = pcbnew.PCB_SHAPE(b)
    seg.SetShape(pcbnew.SHAPE_T_SEGMENT)
    seg.SetLayer(pcbnew.Edge_Cuts)
    seg.SetStart(start)
    seg.SetEnd(end)
    seg.SetWidth(mm(0.1))
    b.Add(seg)
    return seg

def add_arc(start, mid, end):
    arc = pcbnew.PCB_SHAPE(b)
    arc.SetShape(pcbnew.SHAPE_T_ARC)
    arc.SetLayer(pcbnew.Edge_Cuts)
    arc.SetStart(start)
    arc.SetArcGeometry(start, mid, end)
    arc.SetWidth(mm(0.1))
    b.Add(arc)
    return arc

# Board: 85.0 x 57.5 with 3mm radius corners
w = 85.0
h = 57.5
r = 3.0

# Top line: (r, 0) to (w-r, 0)
add_line(pcbnew.VECTOR2I(mm(r), 0), pcbnew.VECTOR2I(mm(w - r), 0))
# Top-right arc: center (w-r, r)
add_arc(pcbnew.VECTOR2I(mm(w - r), 0),
        pcbnew.VECTOR2I(mm(w - r + r * 0.7071), mm(r - r * 0.7071)),
        pcbnew.VECTOR2I(mm(w), mm(r)))
# Right line: (w, r) to (w, h-r)
add_line(pcbnew.VECTOR2I(mm(w), mm(r)), pcbnew.VECTOR2I(mm(w), mm(h - r)))
# Bottom-right arc: center (w-r, h-r)
add_arc(pcbnew.VECTOR2I(mm(w), mm(h - r)),
        pcbnew.VECTOR2I(mm(w - r + r * 0.7071), mm(h - r + r * 0.7071)),
        pcbnew.VECTOR2I(mm(w - r), mm(h)))
# Bottom line: (w-r, h) to (r, h)
add_line(pcbnew.VECTOR2I(mm(w - r), mm(h)), pcbnew.VECTOR2I(mm(r), mm(h)))
# Bottom-left arc: center (r, h-r)
add_arc(pcbnew.VECTOR2I(mm(r), mm(h)),
        pcbnew.VECTOR2I(mm(r - r * 0.7071), mm(h - r + r * 0.7071)),
        pcbnew.VECTOR2I(0, mm(h - r)))
# Left line: (0, h-r) to (0, r)
add_line(pcbnew.VECTOR2I(0, mm(h - r)), pcbnew.VECTOR2I(0, mm(r)))
# Top-left arc: center (r, r)
add_arc(pcbnew.VECTOR2I(0, mm(r)),
        pcbnew.VECTOR2I(mm(r - r * 0.7071), mm(r - r * 0.7071)),
        pcbnew.VECTOR2I(mm(r), 0))

print("Created updated Edge.Cuts with 85.0 x 57.5 mm outline.")

# 3. Remove tiny dangling tracks
dangling = []
for t in b.GetTracks():
    if t.GetClass() == 'PCB_TRACK' and t.GetLength() < mm(0.15):
        # check if it's the dangling VBUS track at (18.2, 46.6)
        x = t.GetStart().x / 1e6
        y = t.GetStart().y / 1e6
        if abs(x - 18.2) < 0.2 and abs(y - 46.6) < 0.2:
            dangling.append(t)

for t in dangling:
    print(f"Deleting dangling track at {t.GetStart().x/1e6}, {t.GetStart().y/1e6}")
    b.Delete(t)

# 4. Expand zones to cover new outline
for z in b.Zones():
    poly = z.Outline()
    poly.RemoveAllContours()
    poly.NewOutline()
    poly.Append(mm(-1.0), mm(-1.0))
    poly.Append(mm(86.0), mm(-1.0))
    poly.Append(mm(86.0), mm(58.5))
    poly.Append(mm(-1.0), mm(58.5))

# 5. Refill zones
zf = pcbnew.ZONE_FILLER(b)
zf.Fill(b.Zones())

b.Save(PCB_PATH)
print("Saved board and refilled zones.")
