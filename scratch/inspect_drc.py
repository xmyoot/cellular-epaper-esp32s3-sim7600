import json

with open('drc_current.json') as f:
    d = json.load(f)

for v in d.get('violations', []):
    t = v.get('type')
    if t in ['shorting_items', 'tracks_crossing', 'clearance', 'items_not_allowed', 'copper_edge_clearance']:
        print(f"=== {t}: {v.get('description')} ===")
        for it in v.get('items', []):
            print('  ', it.get('description'), it.get('pos'))

print("\n--- UNCONNECTED ITEMS BY NET ---")
unc_by_net = {}
for u in d.get('unconnected_items', []):
    desc = u.get('description', '')
    # try to parse net name from items
    net = "UNKNOWN"
    for it in u.get('items', []):
        d_str = it.get('description', '')
        if '[' in d_str and ']' in d_str:
            net = d_str.split('[')[1].split(']')[0]
            break
    unc_by_net[net] = unc_by_net.get(net, 0) + 1

for net, count in sorted(unc_by_net.items(), key=lambda x: -x[1]):
    print(f"  Net {net}: {count} unconnected endpoints")
