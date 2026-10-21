#!/usr/bin/env python3
"""Check source metadata; this is NOT electrical or manufacturing sign-off."""
import csv
from pathlib import Path
from kicad_data import parse, children, one, props
root = Path(__file__).resolve().parents[1]
schematic = parse(next(root.glob('*.kicad_sch')).read_text())
board = parse(next(root.glob('*.kicad_pcb')).read_text())
symbols = {props(s)['Reference']: s for s in children(schematic, 'symbol') if not props(s)['Reference'].startswith('#')}
footprints = {props(f)['Reference']: f for f in children(board, 'footprint')}
assert len(symbols) == len(footprints) == 100
assert symbols.keys() == footprints.keys()
cached = {s[1]: s for s in children(one(schematic, 'lib_symbols'), 'symbol')}
for ref, symbol in symbols.items():
    assert one(symbol, 'instances'), f'{ref}: missing instance path'
    lib = cached[one(symbol, 'lib_id')[1]]
    assert not one(lib, 'extends'), f'{ref}: unresolved inherited symbol'
    assert any(children(s, 'pin') for s in children(lib, 'symbol')), f'{ref}: no cached pins'
    assert props(footprints[ref])['Value'] == props(symbol)['Value'], f'{ref}: value mismatch'
with (root / 'BOM.csv').open() as f:
    rows = list(csv.DictReader(f))
assert len(rows) == 100 and {r['Reference'] for r in rows} == symbols.keys()
for row in rows:
    source = props(symbols[row['Reference']])
    assert row['Value'] == source['Value']
    assert row['Footprint'] == source['Footprint']
    assert (row['Assembly'] == 'DNP') == (source['Value'] == 'DNP')
netlist = parse((root / 'review/netlist-current.net').read_text())
exported = {one(c, 'ref')[1] for c in children(one(netlist, 'components'), 'comp')}
assert exported == symbols.keys(), 'Netlist export omits source components'
print('PASS: 100 component references, cached pins, instance paths, PCB values, BOM rows, and exported references agree.')
print('This metadata check does not validate wiring, footprints, routing, or circuit operation.')
