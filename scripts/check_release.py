#!/usr/bin/env python3
"""Fail closed when saved KiCad checks contain electrical or parity defects.
Regenerate reports with commands in review/README.md before using this gate.
"""
import json
from pathlib import Path
root = Path(__file__).resolve().parents[1] / 'review'
erc = json.loads((root / 'erc-current.json').read_text())
drc = json.loads((root / 'drc-current.json').read_text())
errors = [v for s in erc['sheets'] for v in s['violations'] if v['severity'] == 'error']
counts = {'ERC errors': len(errors), 'DRC violations': len(drc['violations']),
          'Unconnected PCB items': len(drc['unconnected_items']),
          'Schematic/PCB parity issues': len(drc['schematic_parity'])}
for label, count in counts.items():
    print(f'{label}: {count}')
status = json.loads((root / 'release-status.json').read_text())
blocked = any(counts.values()) or status['status'] != 'released' or bool(status['open_blockers'])
print('BLOCKED: see review/README.md.' if blocked else 'PASS: recorded release gates are closed.')
raise SystemExit(1 if blocked else 0)
