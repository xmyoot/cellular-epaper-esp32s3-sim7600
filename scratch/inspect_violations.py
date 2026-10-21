import json

with open('scratch/drc_test_refilled.json') as f:
    d = json.load(f)

for v in d.get('violations', []):
    t = v.get('type')
    if t in ['copper_edge_clearance', 'track_dangling', 'starved_thermal']:
        print(f"=== {t}: {v.get('description')} ===")
        for it in v.get('items', []):
            print('  ', it.get('description'), it.get('pos'))
