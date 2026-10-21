import json

with open('emc_analysis.json') as f:
    d = json.load(f)

print('EMC Score:', d.get('score'))
for f in d.get('findings', []):
    print(f"[{f.get('severity')}] {f.get('rule_id')}: {f.get('title')}")
    print(f"   {f.get('detail', '')[:100]}")
