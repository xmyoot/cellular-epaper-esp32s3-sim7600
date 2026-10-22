#!/usr/bin/env python3
"""Create revision B placement from exported KiCad netlist; does not autoroute.
Run with KiCad's Python/pcbnew bindings. Existing board is replaced.
"""
import sys,json,os
from pathlib import Path
import pcbnew as pcb
from kicad_data import parse,children,one,props
R=Path(__file__).resolve().parents[1];STEM='Low-Power_Cellular_ePaper_Device_ESP32-S3_SIM7600'
L=Path(os.environ.get('KICAD10_FOOTPRINT_DIR','/Users/hector/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints'))
d=json.loads((R/'design/rev-b-netmap.json').read_text());paths=json.loads((R/'design/component-paths.json').read_text());netlist=parse((R/'review/netlist-current.net').read_text())
b=pcb.BOARD();b.SetCopperLayerCount(4)
def v(x,y):return pcb.VECTOR2I(pcb.FromMM(x),pcb.FromMM(y))
netinfo={};pins={};functions={}
for n in children(one(netlist,'nets'),'net'):
 name=str(one(n,'name')[1]);ni=pcb.NETINFO_ITEM(b,name);b.Add(ni);netinfo[name]=ni
 for node in children(n,'node'):
  key=(str(one(node,'ref')[1]),str(one(node,'pin')[1]));pins[key]=name;functions[key]=(one(node,'pinfunction',['pinfunction',''])[1],one(node,'pintype',['pintype','passive'])[1])
# Coordinates in mm on 100 x 80 board. Origin offset leaves normal drawing margins.
xy={
'U1':(20,10,0),'U2':(74,24,0),'U3':(44,24,0),'U5':(21,47,0),'U6':(96,68,0),'U7':(44,35,0),
'J1':(4,30,270),'J2':(15,65,0),'J3':(71,51,0),'J4':(55,44,0),'J5':(95,15,0),'J8':(89,46,0),'J9':(96,53,0),'J6':(65,75,0),'J7':(94,75,0),
'H1':(4,4,0),'H2':(96,4,0),'H3':(4,76,0),'H4':(96,61,0),
'SW1':(5,17,0),'SW2':(5,23,0),'LED1':(6,48,0),
'Q1':(51,34,0),'Q2':(47,34,0),'R8':(51,38,90),'R9':(47,38,90),
'Q3':(86,5,0),'Q4':(81,5,0),'R27':(89,5,90),'R28':(78,5,90),'C23':(86,8,0),'C24':(81,8,0),
'C11':(53,26,90),'C12':(94,29,90),'C13':(54,31,90),'C14':(94,34,90),'C15':(54,34,90),'C16':(91,35,90),'C17':(56,33,90),'C18':(90,32,90),'C19':(90,29,90),
'C7':(8,9,90),'C8':(8,12,90),'C9':(10,9,90),'C10':(10,12,90),'R3':(8,17,90),'C20':(10,17,90),'R4':(8,23,90),'R7':(6,45,90),
'C21':(41,30,0),'C22':(47,30,0),'R11':(42,32,0),'R24':(46,32,0),'C38':(41,35,90),'C39':(47,35,90),
'R13':(65,44,0),'R14':(69,44,0),'R15':(73,44,0),'D6':(65,46,90),'D7':(69,46,90),'D9':(73,46,90),'C29':(78,47,90),'C30':(80,47,90),
'R16':(58,42,0),'C31':(60,41,90),'C32':(56,41,90),'C33':(92,15,0),'C34':(27,23,90),
'R1':(9,31,90),'R2':(9,34,90),'D2':(11,27,0),'R29':(29,14,0),'R30':(29,16,0),
'F1':(21,65,0),'C3':(18,47,90),'C4':(24,47,90),'C5':(26,47,90),
'Q6':(28,53,0),'Q7':(28,58,0),'R19':(32,53,90),'R20':(32,58,90),'R5':(36,53,90),'R6':(36,58,90),'C6':(39,56,90),
'Q8':(48,58,0),'Q10':(44,58,0),'R21':(48,54,90),'R26':(44,54,90),'L2':(52,62,0),'Q9':(53,66,0),'R10':(50,66,90),'R25':(53,69,0),
'D3':(57,62,0),'D4':(60,66,90),'D5':(64,66,90),'C40':(57,66,90),'C25':(61,62,90),'C26':(67,66,90),'C27':(71,66,90),'C28':(75,66,90),'C35':(79,66,90),'C36':(48,61,90),'C41':(75,70,90),'C42':(71,70,90),'C43':(48,64,90),
'C37':(94,68,90),'R22':(92,69,90),'R23':(92,72,90)}

# Clearance corrections from first placement DRC; functional clusters retained.
xy.update({'J1':(6,30,270),'H1':(4,55,0),'H4':(87,76,0),
 'C7':(7,8,0),'C8':(7,12,0),'C9':(7,5,0),'C10':(7,15,0),
 'R3':(7,19,0),'C20':(7,21,0),'R4':(8,25,0),'SW1':(4,17,0),'SW2':(4,23,0),
 'R29':(32,14,0),'R30':(32,16,0),'C34':(25,25,0),
 'C3':(17,47,90),'C4':(25,47,90),'C5':(28,47,90),'F1':(24,65,0),
 'U7':(40,38,0),'C38':(37,38,90),'C39':(43,38,90),'R24':(46,30,0),
 'C11':(52,24,90),'C13':(53,31,0),'C15':(53,34,0),'C17':(54,36,0),
 'C12':(95,28,90),'C14':(95,35,0),'C16':(95,38,0),'C18':(93,32,90),'C19':(93,30,90),
 'C23':(86,3,0),'C24':(81,3,0),
 'J3':(72,54,0),'R13':(65,44,0),'R14':(69,44,0),'R15':(73,44,0),
 'D6':(65,46,90),'D7':(69,46,90),'D9':(73,46,90),'C29':(82,50,90),'C30':(82,47,90),
 'C31':(59,42,90),'C32':(56,40,90),'J4':(53,44,0),'R16':(57,42,0),'C33':(91,15,0),
 'C36':(48,62,90),'C43':(48,66,90),'C25':(61,61,90),'D4':(61,66,90),
 'R23':(90,74,90)})

xy.update({'SW1':(23,29,0),'SW2':(23,35,0),'R3':(19,29,0),'C20':(19,31.5,0),'R4':(19,35,0),'C23':(86,1,0),'C24':(81,1,0),'C33':(92,19,0),'C12':(95,24,90),'C19':(94,30,90),'C18':(94,32,90),'C15':(54,38,0),'C17':(54,40,0),'D6':(65,45.3,90),'D7':(69,45.3,90),'D9':(73,45.3,90),'R24':(39,32,0),'H4':(85,75,0),'R23':(87,69,90)})
xy.update({'R3':(18,29,0),'R4':(18,35,0)})
xy.update({'C37':(98.5,68,90),'C34':(26,44,0),'C39':(43,38,90),'R29':(8,20,0),'R30':(8,22.5,0)})
assert set(xy)==set(d),(set(d)-set(xy),set(xy)-set(d))
for ref,p in d.items():
 ln,fn=p['footprint'].split(':');folder=R/'Cellular.pretty' if ln=='Cellular' else L/(ln+'.pretty')
 fp=pcb.FootprintLoad(str(folder),fn)
 if not fp:raise RuntimeError((ref,p['footprint']))
 fp.SetReference(ref);fp.SetValue(p['value']);fp.SetAttributes(fp.GetAttributes() & ~pcb.FP_EXCLUDE_FROM_BOM);fp.SetFPID(pcb.LIB_ID(ln,fn));fp.SetPath(pcb.KIID_PATH(paths[ref]));fp.SetSheetname(paths[ref].split('/')[2]);fp.SetSheetfile('')
 if p['value']=='DNP':fp.SetAttributes(fp.GetAttributes()|pcb.FP_DNP)
 x,y,a=xy[ref];fp.SetOrientationDegrees(a);fp.SetPosition(v(50+x,50+y));b.Add(fp)
 sheet=next(fn for fn in R.glob('*.kicad_sch') if any(props(a).get('Reference')==ref for a in children(parse(fn.read_text()),'symbol')))
 ss=next(a for a in children(parse(sheet.read_text()),'symbol') if props(a).get('Reference')==ref)
 fp.GetField(pcb.FIELD_T_DATASHEET).SetText(str(props(ss).get('Datasheet','')))
 for pad in fp.Pads():
  key=(ref,pad.GetNumber());n=pins.get(key)
  if n:pad.SetNet(netinfo[n]);func,typ=functions[key];pad.SetPinFunction(func);pad.SetPinType(typ)
 # Standard library references are moved clear of the body and reduced consistently.
 fp.Reference().SetTextSize(v(.8,.8));fp.Reference().SetTextThickness(pcb.FromMM(.12));fp.Reference().SetTextAngle(pcb.EDA_ANGLE(0,pcb.DEGREES_T))
 # Preserve library recommended ref locations where practical; fix individual conflicts after DRC.
 fp.Value().SetVisible(False)
for a,c in [((50,50),(150,50)),((150,50),(150,130)),((150,130),(50,130)),((50,130),(50,50))]:
 sh=pcb.PCB_SHAPE();sh.SetShape(pcb.SHAPE_T_SEGMENT);sh.SetStart(v(*a));sh.SetEnd(v(*c));sh.SetWidth(pcb.FromMM(.05));sh.SetLayer(pcb.Edge_Cuts);b.Add(sh)
for s,x,y,sz in [('CELLULAR ePAPER / REV B',80,126,1.2),('ENGINEERING PROTOTYPE',80,128,1),('BAT +  /  -',64,118,.8),('USB DATA ONLY',57,89,.8)]:
 t=pcb.PCB_TEXT(b);t.SetText(s);t.SetPosition(v(x,y));t.SetTextSize(v(sz,sz));t.SetTextThickness(pcb.FromMM(.15));t.SetLayer(pcb.F_SilkS);b.Add(t)
# Solid inner ground reference. Outer ground pours added after routing.
z=pcb.ZONE(b);z.SetLayer(pcb.In1_Cu);z.SetNet(netinfo['GND']);z.SetLocalClearance(pcb.FromMM(.2));z.SetPadConnection(pcb.ZONE_CONNECTION_FULL);z.SetThermalReliefGap(pcb.FromMM(.25));z.SetThermalReliefSpokeWidth(pcb.FromMM(.25));o=z.Outline();o.NewOutline()
for x,y in [(50.5,50.5),(149.5,50.5),(149.5,129.5),(50.5,129.5)]:o.Append(int(pcb.FromMM(x)),int(pcb.FromMM(y)))
b.Add(z)
pcb.SaveBoard(str(R/(STEM+'.kicad_pcb')),b)
print('Placed',len(d),'components; no routes claimed')
