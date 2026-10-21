import pcbnew

def mm(val):
    return pcbnew.FromMM(val)

PCB_PATH = r"scratch\test_routed.kicad_pcb"
b = pcbnew.LoadBoard(PCB_PATH)

# Remove all custom shapes from U2 silkscreen
u2 = b.FindFootprintByReference("U2")
if u2:
    items = [g for g in u2.GraphicalItems() if g.GetLayerName() == "F.Silkscreen"]
    for g in items:
        u2.Remove(g)
    u2.Reference().SetVisible(False)

def set_ref(ref, x, y, visible=True):
    fp = b.FindFootprintByReference(ref)
    if fp:
        fp.Reference().SetVisible(visible)
        fp.Reference().SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))

# Clear positions in open zones:
set_ref("J7", 66.5, 8.0)
set_ref("J4", 81.5, 15.0)
set_ref("J5", 81.5, 23.0)
set_ref("J2", 31.5, 47.0)
set_ref("SW1", 7.0, 18.0)
set_ref("SW2", 7.5, 30.5)

# For LEDs, place text neatly:
# LED1 at (47.0, 5.0) -> text at (47.0, 9.0)
set_ref("LED1", 47.0, 9.0)
# LED2 at (47.0, 1.5) -> text at (44.0, 1.5)
set_ref("LED2", 43.5, 1.5)
# LED3 at (23.0, 48.0) -> text at (23.0, 43.5)
set_ref("LED3", 23.0, 43.5)

b.Save(PCB_PATH)
print("Applied perfected text positions.")
