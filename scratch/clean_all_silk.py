import pcbnew
import math

def mm(val):
    return pcbnew.FromMM(val)

PCB_PATH = r"scratch\test_routed.kicad_pcb"
b = pcbnew.LoadBoard(PCB_PATH)

# 1. Clean U2 (SIM7600G) silkscreen
u2 = b.FindFootprintByReference("U2")
if u2:
    # Remove the giant rectangle from F.Silkscreen
    items_to_del = []
    for g in u2.GraphicalItems():
        if g.GetLayerName() == "F.Silkscreen" and g.GetShapeStr() == "Rect":
            items_to_del.append(g)
    for g in items_to_del:
        u2.Remove(g)

    # Add neat corner ticks for U2 (module is 30mm x 30mm, center is at 0,0 local)
    # Pads are inset, so corner marks at +/-15.2 mm with 2mm arms
    corner_len = mm(2.0)
    corners = [
        (-15.2, -15.2, 1, 1),
        (15.2, -15.2, -1, 1),
        (15.2, 15.2, -1, -1),
        (-15.2, 15.2, 1, -1)
    ]
    for cx, cy, dx, dy in corners:
        # arm 1 (horizontal)
        s1 = pcbnew.PCB_SHAPE(u2)
        s1.SetShape(pcbnew.SHAPE_T_SEGMENT)
        s1.SetLayer(pcbnew.F_SilkS)
        s1.SetStart(pcbnew.VECTOR2I(mm(cx), mm(cy)))
        s1.SetEnd(pcbnew.VECTOR2I(mm(cx + dx * 2.0), mm(cy)))
        s1.SetWidth(mm(0.15))
        u2.Add(s1)
        # arm 2 (vertical)
        s2 = pcbnew.PCB_SHAPE(u2)
        s2.SetShape(pcbnew.SHAPE_T_SEGMENT)
        s2.SetLayer(pcbnew.F_SilkS)
        s2.SetStart(pcbnew.VECTOR2I(mm(cx), mm(cy)))
        s2.SetEnd(pcbnew.VECTOR2I(mm(cx), mm(cy + dy * 2.0)))
        s2.SetWidth(mm(0.15))
        u2.Add(s2)

    # Position U2 reference text neatly in the center of the module
    u2.Reference().SetPosition(u2.GetPosition())
    u2.Reference().SetVisible(True)

# 2. Hide mounting hole reference texts
for ref in ["H1", "H2", "H3", "H4"]:
    fp = b.FindFootprintByReference(ref)
    if fp:
        fp.Reference().SetVisible(False)

# 3. Position connector and IC reference texts safely
def adjust_ref(ref, dx_mm, dy_mm, visible=True):
    fp = b.FindFootprintByReference(ref)
    if fp:
        fp.Reference().SetVisible(visible)
        pos = fp.GetPosition()
        fp.Reference().SetPosition(pcbnew.VECTOR2I(pos.x + mm(dx_mm), pos.y + mm(dy_mm)))

adjust_ref("J1", 0.0, -3.5) # move up away from edge
adjust_ref("J7", 0.0, 2.5)  # move down away from top edge
adjust_ref("LED2", 0.0, 2.5) # move down away from top edge
adjust_ref("J4", 2.5, 0.0)  # move right away from U2 pads
adjust_ref("J5", 2.5, 0.0)  # move right away from U2 pads
adjust_ref("SW1", 0.0, -2.5)
adjust_ref("SW2", 0.0, 2.5)
adjust_ref("LED1", 0.0, 2.0)
adjust_ref("LED3", 0.0, 2.0)

# Hide small transistor reference texts on silk (kept on Fab)
for q_ref in ["Q1", "Q2", "Q3", "Q4", "Q6", "Q7", "Q8", "Q9", "Q10"]:
    fp = b.FindFootprintByReference(q_ref)
    if fp:
        fp.Reference().SetVisible(False)

# Clean J1 silkscreen lines that extend near edge
j1 = b.FindFootprintByReference("J1")
if j1:
    del_j1 = []
    for g in j1.GraphicalItems():
        if g.GetLayerName() == "F.Silkscreen":
            del_j1.append(g)
    for g in del_j1:
        j1.Remove(g)

b.Save(PCB_PATH)
print("Silkscreen cleaned and updated.")
