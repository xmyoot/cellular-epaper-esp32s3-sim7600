#!/usr/bin/env python3
"""Verify hierarchical source, BOM, netlist and PCB agree at pin level.
This is a source-consistency check, not manufacturing or operational sign-off.
"""
import csv,json
from pathlib import Path
from kicad_data import parse, children, one, props
root=Path(__file__).resolve().parents[1]
expected=json.loads((root/'design/rev-b-netmap.json').read_text())
symbols={};caches={}
for path in root.glob('*.kicad_sch'):
 doc=parse(path.read_text());cache={s[1]:s for s in children(one(doc,'lib_symbols'),'symbol')}
 for s in children(doc,'symbol'):
  ref=props(s)['Reference']
  if ref.startswith('#'):continue
  assert ref not in symbols,f'duplicate {ref}'
  symbols[ref]=s;caches[ref]=cache[one(s,'lib_id')[1]]
board=parse(next(root.glob('*.kicad_pcb')).read_text())
footprints={props(f)['Reference']:f for f in children(board,'footprint')}
assert symbols.keys()==footprints.keys()==expected.keys()
for ref,s in symbols.items():
 p=props(s);f=footprints[ref];lib=caches[ref]
 assert one(s,'instances'),f'{ref}: missing instance path'
 assert not one(lib,'extends'),f'{ref}: unresolved symbol inheritance'
 assert any(children(a,'pin') for a in children(lib,'symbol')),f'{ref}: missing cached pins'
 assert p['Value']==props(f)['Value']==expected[ref]['value'],f'{ref}: value mismatch'
 assert p['Footprint']==f[1]==expected[ref]['footprint'],f'{ref}: footprint mismatch'
with (root/'BOM.csv').open() as file:rows=list(csv.DictReader(file))
assert len(rows)==len(symbols) and {r['Reference'] for r in rows}==symbols.keys()
for row in rows:
 source=props(symbols[row['Reference']]);assert row['Value']==source['Value'];assert row['Footprint']==source['Footprint']
 assert (row['Assembly']=='DNP')==(source['Value']=='DNP')
netlist=parse((root/'review/netlist-current.net').read_text())
assert {one(c,'ref')[1] for c in children(one(netlist,'components'),'comp')}==symbols.keys()
exported={}
for n in children(one(netlist,'nets'),'net'):
 for node in children(n,'node'):exported[(one(node,'ref')[1],one(node,'pin')[1])]=one(n,'name')[1]
for ref,comp in expected.items():
 for pin,net in comp['nets'].items():
  if not pin:continue
  if net:assert exported.get((ref,pin))==net,f'{ref}.{pin}: source pin/net differs from design map'
 for pad in children(footprints[ref],'pad'):
  pin=pad[1]
  if not pin:continue
  target=exported.get((ref,pin),'');actual=one(pad,'net',['net',''])[-1]
  assert target==actual,f'{ref}.{pin}: PCB {actual} differs from schematic {target}'
print(f'PASS: {len(symbols)} components; hierarchical source, BOM, values, footprints, and every exported PCB pad net agree.')
print('Native ERC/DRC, manufacturing review and prototype tests are separate requirements.')
