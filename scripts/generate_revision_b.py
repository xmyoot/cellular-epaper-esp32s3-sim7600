#!/usr/bin/env python3
"""Generate the reviewable revision-B schematic and custom modem library.
Uses the explicit, version-controlled pin/net map; requires KiCad 10 libraries.
Does not route a PCB or qualify the design for fabrication.
"""
import copy,json,math,os,uuid,csv
from pathlib import Path
from kicad_data import Q,parse,children,one,props
ROOT=Path(__file__).resolve().parents[1]
LIB=Path(os.environ.get('KICAD10_SYMBOL_DIR','/Users/hector/Applications/KiCad/KiCad.app/Contents/SharedSupport/symbols'))
STEM='Low-Power_Cellular_ePaper_Device_ESP32-S3_SIM7600'
def q(s):return Q(str(s))
def dump(n):
 if isinstance(n,list):return '('+' '.join(dump(x) for x in n)+')'
 return json.dumps(n) if isinstance(n,Q) else str(n)
def write(p,n):p.write_text(dump(n)+'\n')
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,'cellular-revB/'+s))
def eff(sz=1):return ['effects',['font',['size',str(sz),str(sz)]]]
def prop(name,val,x,y,hide=False):return ['property',q(name),q(val),['at',str(x),str(y),'0'],eff(),*([['hide','yes']] if hide else [])]
def resolve(name,ls):
 s=copy.deepcopy(ls[name]);ex=one(s,'extends')
 if ex:
  base=resolve(ex[1],ls)
  s=[x for x in s if not(isinstance(x,list) and x[0]=='extends')]+[x for x in base[2:] if isinstance(x,list) and x[0] not in ['property','extends']]
 return s
# Pin names from SIMCom Hardware Design V1.07 (file distributed as V1.08), table 5.
names='GND GND PWRKEY RESET GND SPI_CLK SPI_MISO SPI_MOSI SPI_CS GND USB_VBUS USB_DN USB_DP GND VDD_1V8 USB_ID USIM_DATA USIM_RST USIM_CLK USIM_VDD SD_CMD SD_DATA0 SD_DATA1 SD_DATA2 SD_DATA3 SD_CLK SDIO_DATA1 SDIO_DATA2 SDIO_CMD SDIO_DATA0 SDIO_DATA3 SDIO_CLK GPIO3 GPIO6 HSIC_STROBE HSIC_DATA GND VBAT VBAT GND GND DBG_TXD GND VDD_AUX ISINK ADC2 ADC1 SD_DET STATUS GPIO43 NETLIGHT GPIO41 USIM_DET FLIGHTMODE SCL SDA GND GND AUX_ANT GND GND VBAT VBAT GND GND RTS CTS RXD RI DCD TXD DTR PCM_OUT PCM_IN PCM_SYNC PCM_CLK GND GND GNSS_ANT GND GND MAIN_ANT COEX1 COEX2 USB_BOOT COEX3 GPIO77 RESERVED RESERVED RESERVED RESERVED RESERVED GND GPIO4 GPIO2 GPIO1 GPIO54 GND RESERVED RESERVED RESERVED RESERVED RESERVED RESERVED RESERVED DBG_RXD RESERVED SGMII_RST_N SGMII_INT_N GND RESERVED SGMII_RX_P SGMII_RX_M SGMII_TX_M SGMII_TX_P SGMII_MDIO SGMII_MDC GND GPIO19'.split()+['GND']*16
assert len(names)==135
mod=['symbol',q('SIM7600G_H_135'),['pin_names',['offset','1.016']],['in_bom','yes'],['on_board','yes'],prop('Reference','U',0,90),prop('Value','SIM7600G_H_135',0,87),prop('Footprint','Cellular:SIM7600G_H_135',0,0,True),prop('Datasheet','https://files.waveshare.com/upload/5/52/SIM7600G%28-H%29_SIM7600NA%28-H%29_Hardware_Design_V1.08.pdf',0,0,True),['symbol',q('SIM7600G_H_135_0_1'),['rectangle',['start','-22.86','86.36'],['end','22.86','-86.36'],['stroke',['width','0.254'],['type','default']],['fill',['type','background']]]]]
body=['symbol',q('SIM7600G_H_135_1_1')]
for i,name in enumerate(names,1):
 left=i<=68;row=i-1 if left else i-69;y=83.82-row*2.54
 typ='passive'
 if name in ['GND','VBAT','USB_VBUS']:typ='power_in'
 elif name in ['VDD_1V8','VDD_AUX','USIM_VDD']:typ='power_out'
 elif name in ['TXD','CTS','STATUS','NETLIGHT','USIM_RST','USIM_CLK']:typ='output'
 elif name in ['PWRKEY','RESET','RXD','RTS','DTR']:typ='input'
 elif name in ['USIM_DATA']:typ='bidirectional'
 body.append(['pin',typ,'line',['at',str(-27.94 if left else 27.94),str(round(y,4)),'0' if left else '180'],['length','5.08'],['name',q(name),eff(.95)],['number',q(i),eff(.95)]])
mod.append(body)
custom=['kicad_symbol_lib',['version','20241209'],['generator',q('kicad_symbol_editor')],mod]
write(ROOT/'Cellular.kicad_sym',custom)
# Manufacturer recommended land pattern, figure 4. Top view, pin 1 top-right.
fp=['footprint',q('SIM7600G_H_135'),['version','20260206'],['generator',q('pcbnew')],['layer',q('F.Cu')],['descr',q('SIM7600G-H 135-pin LCC+LGA; SIMCom hardware design fig.4; verify purchased revision before assembly')],['attr','smd'],prop('Reference','U',0,-18),prop('Value','SIM7600G-H',0,18)]
# Footprint properties have layer and use PCB effects format.
for a in children(fp,'property'):a.insert(4,['layer',q('F.SilkS' if a[1]=='Reference' else 'F.Fab')])
def line(x1,y1,x2,y2,layer,w=.12):return ['fp_line',['start',str(x1),str(y1)],['end',str(x2),str(y2)],['stroke',['width',str(w)],['type','solid']],['layer',q(layer)]]
for a,b in [((-15,-15),(15,-15)),((15,-15),(15,15)),((15,15),(-15,15)),((-15,15),(-15,-15))]:fp.append(line(*a,*b,'F.Fab',.1))
for a,b in [((-17,-17),(17,-17)),((17,-17),(17,17)),((17,17),(-17,17)),((-17,17),(-17,-17))]:fp.append(line(*a,*b,'F.CrtYd',.05))
fp.append(['fp_circle',['center','9.5','-16.4'],['end','9.8','-16.4'],['stroke',['width','.12'],['type','solid']],['fill','none'],['layer',q('F.SilkS')]])
def pad(n,x,y,w,h):
 fp.append(['pad',q(n),'smd','rect',['at',str(round(x,4)),str(round(y,4))],['size',str(w),str(h)],['layers',q('F.Cu'),q('F.Paste'),q('F.Mask')]])
for n in range(1,21):pad(n,10.5-n,-14.7,.6,1.6)
pad(81,-10.5,-14.7,.6,1.6)
for n in range(21,41):pad(n,-14.7,n-30.5,1.6,.6)
pad(84,-14.7,-10.5,1.6,.6);pad(83,-14.7,10.5,1.6,.6)
for n in range(41,61):pad(n,n-50.5,14.7,.6,1.6)
pad(82,-10.5,14.7,.6,1.6);pad(85,10.5,14.7,.6,1.6)
for n in range(61,81):pad(n,14.7,70.5-n,1.6,.6)
pad(86,14.7,-10.5,1.6,.6);pad(87,14.7,10.5,1.6,.6)
for j in range(8):
 pad(88+j,6.3-1.8*j,-12,1.1,1.6);pad(96+j,-12,-6.3+1.8*j,1.6,1.1)
 pad(104+j,-6.3+1.8*j,12,1.1,1.6);pad(112+j,12,6.3-1.8*j,1.6,1.1)
for c,x in enumerate([6,2,-2,-6]):
 for r,y in enumerate([-6,-2,2,6]):pad(120+c*4+r,x,y,3.1,3.1)
# Pad120 pin-one chamfer, manufacturer 2.1 mm edge => 1mm cut at top-right.
p120=next(p for p in children(fp,'pad') if p[1]=='120');p120[3]='roundrect';p120.append(['roundrect_rratio','0']);p120 += [['chamfer_ratio',str(1/3.1)],['chamfer','top_right']]
# Physical module keepout areas: no copper or tracks on any copper layer.
for i,(cx,cy) in enumerate([(9.5,-12.6),(-12.6,9.5)]):
 pts=[(cx-1.2,cy-1.2),(cx+1.2,cy-1.2),(cx+1.2,cy+1.2),(cx-1.2,cy+1.2)]
 fp.append(['zone',['net','0'],['net_name',q('')],['layers',q('*.Cu')],['hatch','edge','.5'],['connect_pads',['clearance','0']],['min_thickness','.25'],['keepout',['tracks','not_allowed'],['vias','not_allowed'],['pads','not_allowed'],['copperpour','not_allowed'],['footprints','allowed']],['fill',['thermal_gap','.3'],['thermal_bridge_width','.3']],['polygon',['pts',*([ 'xy',str(x),str(y)] for x,y in pts)]]])
(ROOT/'Cellular.pretty').mkdir(exist_ok=True);write(ROOT/'Cellular.pretty/SIM7600G_H_135.kicad_mod',fp)
parts=json.loads((ROOT/'design/rev-b-netmap.json').read_text())
# Correct TVS cathode terminal to signal, anode terminal to ground.
for ref in ['D6','D7','D9']:
 parts[ref]['value']='PESD3V3U1UL';old=parts[ref]['nets'];parts[ref]['nets']={'1':next(n for n in old.values() if n!='GND'),'2':'GND'}
(ROOT/'design/rev-b-netmap.json').write_text(json.dumps(parts,indent=2)+'\n')
libs={};resolved={}
for ident in sorted({p['lib'] for p in parts.values()}|{'power:PWR_FLAG'}):
 ln,name=ident.split(':');
 if ln not in libs:libs[ln]={s[1]:s for s in children(parse((ROOT/'Cellular.kicad_sym' if ln=='Cellular' else LIB/(ln+'.kicad_sym')).read_text()),'symbol')}
 sym=resolve(name,libs[ln]);sym[1]=q(ident)
 for sub in children(sym,'symbol'):sub[1]=q(name+'_'+'_'.join(sub[1].rsplit('_',2)[-2:]))
 resolved[ident]=sym
# Functional sheets, all connections explicit at pin coordinates on 1.27mm grid.
groups={
 'power': ['J2','F1','U5','C3','C4','C5','Q6','Q7','R19','R20','R5','R6','C6','H1','H2','H3','H4'],
 'controller':['U1','C7','C8','C9','C10','R3','C20','SW1','R4','SW2','R7','LED1','J1','R1','R2','D2','R29','R30'],
 'modem':['U2','Q1','Q2','R8','R9','C11','C12','C13','C14','C15','C16','C17','C18','C19','Q3','Q4','R27','R28','C23','C24'],
 'interfaces':['U3','C21','C22','R11','R24','U7','C38','C39','J3','C29','C30','R13','R14','R15','D6','D7','D9','J4','R16','C31','C32','J5','C33','J8','J9'],
 'display':['J6','Q8','Q10','R21','R26','L2','Q9','R10','R25','D3','D4','D5','C25','C26','C27','C28','C35','C36','C40','C41','C42','C43'],
 'sensors':['U6','C37','R22','R23','J7','C34']}
assert set(sum(groups.values(),[]))==set(parts)
rootid=uid('root'); paths={};positions={}
notes={
'power':['Protected 1S LiPo, external charging only. USB does not power or charge this board.','Battery connector: pin 1 positive, pin 2 GND. Verify pack polarity before connection.','AP2112K: 600mA maximum, 55uA typical quiescent current. No 10uA system claim.','Disable modem before loaded battery falls below 3.6V; verify rail stays above 3.4V.','Battery ADC: enable divider, wait >=250ms before sampling (RC = 50ms).'],
'controller':['ESP32-S3-WROOM-1-N8: 8MB flash, no PSRAM. GPIO47 enables battery divider.','USB-C data/programming only. Protected battery must be connected.','Do not drive display SPI/reset high while VCC_EPD is off; disable internal pull-ups.'],
'modem':['SIM7600G-H 135-pad package, hardware design V1.07 table 5 and figure 4.','VBAT 3.4-4.2V, design for 2A transmit pulses. Validate battery and transient response.','Assert PWRKEY with N-FET for >=500ms; reset pulse 100-500ms.','Use AT+CPOF and wait for STATUS low before switching modem power off.','Unused and reserved module terminals explicitly NC; DTR held low for UART awake.'],
'interfaces':['TXS0104E OE is referenced to the 1.8V VCCA supply.','U7 translates STATUS to 3.3V; DIR tied to VCCA selects A-to-B.','Main and diversity LTE antennas required. GNSS connector is passive (no DC bias).','RF matching is provisional; use fabricator stackup and verify 50-ohm routes.','J9: external modem USB service, pin1 VBUS, pin2 D-, pin3 D+, pin4 GND.'],
'display':['GDEY029T94 2.9 inch 296x128 monochrome, four-wire SPI (BS1 grounded).','Panel pin18 VDD is an internal rail: capacitor only, never connect to 3.3V.','Reference: GDEY029T94 specification, page30 (PDF page29), typical application.','Q9 Si1308EDL; L2 47uH >=500mA; flying capacitor 4.7uF/25V; sense 2.2 ohm.','Verify FPC contact side and pin1 with panel mechanical drawing before ordering.'],
'sensors':['SHT40 and external Qwiic share 3.3V I2C. Pull-ups 4.7k.','Place sensor at board edge, away from modem, LDO and display boost heat.']}
def text(s,x,y,size=1.27):return ['text',q(s),['at',str(x),str(y),'0'],['effects',['font',['size',str(size),str(size)]],['justify','left']],['uuid',q(uid('text/'+s))]]
def base(id,title,page):return ['kicad_sch',['version','20250114'],['generator',q('eeschema')],['uuid',q(id)],['paper',q('A3')],['title_block',['title',q(title)],['date',q('2026-10-21')],['rev',q('B / PROTOTYPE')],['company',q('Hector / xmyoot')],['comment','1',q('Not released for fabrication; bench and RF validation required')]]]
def pins(lib):return [p for sub in children(lib,'symbol') for p in children(sub,'pin')]
def bounds(lib):
 xy=[one(p,'at')[1:3] for p in pins(lib)]
 return min(float(p[0]) for p in xy),max(float(p[0]) for p in xy),min(float(p[1]) for p in xy),max(float(p[1]) for p in xy)
def snap(x):return round(round(x/1.27)*1.27,4)
for page,(gn,refs) in enumerate(groups.items(),2):
 sid=uid('sheet/'+gn);doc=base(uid('doc/'+gn),gn.title(),page);cache=['lib_symbols']
 for ident in sorted({parts[r]['lib'] for r in refs}|({'power:PWR_FLAG'} if gn in ['power','modem','display','controller','interfaces'] else set())):cache.append(copy.deepcopy(resolved[ident]))
 doc.append(cache)
 for j,t in enumerate(notes[gn]):doc.append(text(t,15,15+j*4.2,1.1))
 # Packing: large ICs start column; normal parts laid into columns with ample label space.
 x=65.;y=60.;colwidth=100.;bottom=355. if gn!='sensors' else 255.
 if gn!='sensors':one(doc,'paper')[1]=q('A2')
 for ref in refs:
  p=parts[ref];lib=resolved[p['lib']];mnx,mxx,mny,mxy=bounds(lib);height=mxy-mny+35
  if y+height>bottom:x+=colwidth;y=60.
  if x>(550 if gn!='sensors' else 375):raise RuntimeError(('sheet overflow',gn,ref))
  cx=snap(x);cy=snap(y+mxy+16)
  sidref=uid(ref);path='/'+rootid+'/'+sid;paths[ref]=path+'/'+sidref;positions[ref]={'sheet':gn,'x':cx,'y':cy}
  inst=['symbol',['lib_id',q(p['lib'])],['at',str(cx),str(cy),'0'],['unit','1'],['in_bom','yes'],['on_board','yes'],['dnp','yes' if p['value']=='DNP' else 'no'],['uuid',q(sidref)],prop('Reference',ref,cx,cy-mxy-14),prop('Value',p['value'],cx,cy-mxy-10),prop('Footprint',p['footprint'],cx,cy,True),prop('Datasheet',props(lib).get('Datasheet',''),cx,cy,True),['instances',['project',q(STEM),['path',q(path),['reference',q(ref)],['unit','1']]]]]
  doc.append(inst)
  for pin in pins(lib):
   no=one(pin,'number')[1];pa=one(pin,'at');px=snap(cx+float(pa[1]));py=snap(cy-float(pa[2]));ang=float(pa[3]);n=p['nets'].get(no,'')
   if not n:
    doc.append(['no_connect',['at',str(px),str(py)],['uuid',q(uid(ref+'/'+no+'/nc'))]]);continue
   # Extend outward from pin endpoint; symbol pin angle points inward.
   dx=-math.cos(math.radians(ang))*5.08;dy=math.sin(math.radians(ang))*5.08;ex=snap(px+dx);ey=snap(py+dy)
   doc.append(['wire',['pts',['xy',str(px),str(py)],['xy',str(ex),str(ey)]],['stroke',['width','0'],['type','default']],['uuid',q(uid(ref+'/'+no+'/wire'))]])
   la=int((ang+180)%360)
   if ang in [90,270] and len(pins(lib))==2:
    hx=snap(ex+5.08)
    doc.append(['wire',['pts',['xy',str(ex),str(ey)],['xy',str(hx),str(ey)]],['stroke',['width','0'],['type','default']],['uuid',q(uid(ref+'/'+no+'/label-elbow'))]])
    ex=hx;la=0
   lab=['global_label',q(n),['shape','bidirectional'],['at',str(ex),str(ey),str(la)],['fields_autoplaced'],eff(.95),['uuid',q(uid(ref+'/'+no+'/label'))],prop('Intersheetrefs','${INTERSHEET_REFS}',ex,ey,True)]
   # KiCad labels use left/right justification at anchor; default generated label style.
   one(lab,'effects').append(['justify','left' if la in [0,90] else 'right'])
   doc.append(lab)
  y+=height+5
 # Power flags denote passive-fed source nets, not ignored ERC exclusions.
 flagmap={'power':['VBAT_RAW','VBAT','GND'],'modem':['VBAT_MODEM'],'display':['VCC_EPD'],'controller':['VBUS'],'interfaces':['MODEM_USB_VBUS']}
 for j,n in enumerate(flagmap.get(gn,[])):
  fx=snap(290+j*30);fy=snap(245);fr='#FLG'+str(page*10+j);u=uid('flag/'+n);path='/'+rootid+'/'+sid
  doc.append(['symbol',['lib_id',q('power:PWR_FLAG')],['at',str(fx),str(fy),'0'],['unit','1'],['in_bom','yes'],['on_board','yes'],['dnp','no'],['uuid',q(u)],prop('Reference',fr,fx,fy+4,True),prop('Value','PWR_FLAG',fx,fy-5),['instances',['project',q(STEM),['path',q(path),['reference',q(fr)],['unit','1']]]]])
  doc.append(['global_label',q(n),['shape','bidirectional'],['at',str(fx),str(fy),'0'],eff(.95),['uuid',q(uid('flaglabel/'+n))]])
 doc.append(['embedded_fonts','no']);write(ROOT/(gn+'.kicad_sch'),doc)
root=base(rootid,'Cellular ePaper - revision B architecture',1);root.append(['lib_symbols'])
for i,(gn,refs) in enumerate(groups.items()):
 x=30+(i%3)*125;y=70+(i//3)*90;suid=uid('sheet/'+gn)
 root.append(['sheet',['at',str(x),str(y)],['size','95','55'],['stroke',['width','.254'],['type','default']],['fill',['color','0','0','0','0']],['uuid',q(suid)],prop('Sheetname',gn.title(),x,y-2),prop('Sheetfile',gn+'.kicad_sch',x,y+58),['instances',['project',q(STEM),['path',q('/'+rootid),['page',q(i+2)]]]]])
root+= [text('Protected LiPo -> fused battery -> modem switch and 3.3V LDO -> ESP32 + switched ePaper',20,23,1.7),text('USB-C is data/programming only. Charge battery externally. Design remains a prototype.',20,32,1.4),text('Global net labels connect functional sheets. See DESIGN_REPORT.md for sequencing and validation gates.',20,41,1.4),['embedded_fonts','no']]
write(ROOT/(STEM+'.kicad_sch'),root)
(ROOT/'design/component-paths.json').write_text(json.dumps(paths,indent=2)+'\n')
# Write portable project-local library tables.
for typ,ext,pathkey,libnames in [('sym','kicad_sym','KICAD10_SYMBOL_DIR',{p['lib'].split(':')[0] for p in parts.values()}|{'power'}),('fp','pretty','KICAD10_FOOTPRINT_DIR',{p['footprint'].split(':')[0] for p in parts.values()})]:
 rows=[typ+'_lib_table',['version','7']]
 for ln in sorted(libnames):
  uri='${KIPRJMOD}/Cellular.'+ext if ln=='Cellular' else '${'+pathkey+'}/'+ln+'.'+ext
  rows.append(['lib',['name',q(ln)],['type',q('KiCad')],['uri',q(uri)],['options',q('')],['descr',q('')]])
 write(ROOT/(typ+'-lib-table'),rows)
with (ROOT/'BOM.csv').open('w') as f:
 w=csv.writer(f,lineterminator="\n");w.writerow(['Reference','Value','Footprint','Assembly','Qualification'])
 for r,p in sorted(parts.items()):w.writerow([r,p['value'],p['footprint'],'DNP' if p['value']=='DNP' else 'FIT','Engineering selection; validate ratings and procurement before fabrication'])
print('Generated 7 schematic sheets and 135-pad module footprint;',len(parts),'components')
