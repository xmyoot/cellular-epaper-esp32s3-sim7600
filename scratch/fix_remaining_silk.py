import pcbnew

def mm(val):
    return pcbnew.FromMM(val)

PCB_PATH = r"scratch\test_routed.kicad_pcb"
b = pcbnew.LoadBoard(PCB_PATH)

# 1. Clean U2 corner ticks and reference text
u2 = b.FindFootprintByReference("U2")
if u2:
    # Delete previous shapes we added
    items = [g for g in u2.GraphicalItems() if g.GetLayerName() == "F.Silkscreen" and g.GetShapeStr() == "Segment"]
    for g in items:
        u2.Remove(g)

    # Add 1mm corner ticks (well clear of U1 and pads)
    corners = [
        (-14.8, -14.8, 1, 1),
        (14.8, -14.8, -1, 1),
        (14.8, 14.8, -1, -1),
        (-14.8, 14.8, 1, -1)
    ]
    for cx, cy, dx, dy in corners:
        s1 = pcbnew.PCB_SHAPE(u2)
        s1.SetShape(pcbnew.SHAPE_T_SEGMENT)
        s1.SetLayer(pcbnew.F_SilkS)
        s1.SetStart(pcbnew.VECTOR2I(mm(cx), mm(cy)))
        s1.SetEnd(pcbnew.VECTOR2I(mm(cx + dx * 1.0), mm(cy)))
        s1.SetWidth(mm(0.15))
        u2.Add(s1)

        s2 = pcbnew.PCB_SHAPE(u2)
        s2.SetShape(pcbnew.SHAPE_T_SEGMENT)
        s2.SetLayer(pcbnew.F_SilkS)
        s2.SetStart(pcbnew.VECTOR2I(mm(cx), mm(cy)))
        s2.SetEnd(pcbnew.VECTOR2I(mm(cx), mm(cy + dy * 1.0)))
        s2.SetWidth(mm(0.15))
        u2.Add(s2)

    # U2 is a large metal-canned module, hide text on silk to avoid the thermal pads, kept on F.Fab
    u2.Reference().SetVisible(False)

# 2. Adjust reference text positions
def set_ref_pos(ref, x_mm, y_mm, visible=True):
    fp = b.FindFootprintByReference(ref)
    if fp:
        fp.Reference().SetVisible(visible)
        fp.Reference().SetPosition(pcbnew.VECTOR2I(mm(x_mm), mm(y_mm)))

# Clear positions on F.Cu:
# J7 is at (66.5, 3.5), place text at (66.5, 6.0)
set_ref_pos("J7", 66.5, 6.0)

# J4 is at (76.0, 15.0), place text at (79.0, 15.0)
set_ref_pos("J4", 79.0, 15.0)

# J5 is at (76.0, 23.0), place text at (79.0, 23.0)
set_ref_pos("J5", 79.0, 23.0)

# LED1 is at (47.0, 5.0), place text at (47.0, 7.5)
set_ref_pos("LED1", 47.0, 7.5)

# LED2 is at (47.0, 1.5), place text at (47.0, -1.0) -> wait, board edge is at 0, place at (51.0, 1.5)
set_ref_pos("LED2", 51.0, 1.5)

# LED3 is at (23.0, 48.0), place text at (23.0, 46.0)
set_ref_pos("LED3", 23.0, 45.8)

# SW1 is at (5.0, 22.0), place text at (5.0, 18.5)
set_ref_pos("SW1", 5.0, 18.5)

# SW2 is at (5.0, 31.0), place text at (5.0, 34.5)
set_ref_pos("SW2", 5.0, 34.5)

b.Save(PCB_PATH)
print("Updated all silk placements.")
