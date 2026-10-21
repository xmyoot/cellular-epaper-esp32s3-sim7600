import json

with open('scratch/drc_fixed.json') as f:
    d = json.load(f)

for i, v in enumerate(d.get('violations', []), 1):
    items = ' vs '.join([it.get('description', '') for it in v.get('items', [])])
    print(f"{i:2d}. [{v.get('type')}] {items}")
