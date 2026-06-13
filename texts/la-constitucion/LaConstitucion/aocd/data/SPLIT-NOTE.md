# spain_municipios_full.geojson is split

The original `spain_municipios_full.geojson` (~72 MB) is split into two
FeatureCollection halves so each fits under GitHub's 50 MB warning:

- `spain_municipios_full.part1.geojson` — features 0..4110
- `spain_municipios_full.part2.geojson` — features 4111..end

To recombine:

```python
import json
parts = ['spain_municipios_full.part1.geojson', 'spain_municipios_full.part2.geojson']
features = []
for p in parts:
    with open(p) as f:
        features += json.load(f)['features']
with open('spain_municipios_full.geojson', 'w') as f:
    json.dump({'type': 'FeatureCollection', 'features': features}, f)
```
