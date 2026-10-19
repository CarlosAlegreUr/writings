# GeoJSON troceados

Los GeoJSON de más de 50 MB se guardan partidos en varias `FeatureCollection`
para que cada trozo quede por debajo del aviso de 50 MB de GitHub. De los
scripts actuales, solo `scripts/aocd_mapa_v2.py` lee estos GeoJSON, y une las
partes en memoria cuando se le pasan con `--geojson parte1 parte2 …`; los
scripts de la v1 leen el fichero único y necesitan la recombinación de abajo.

## `municipios_cnig_2026.part1..3.geojson` (en `data/`)

Polígonos municipales oficiales IGN/CNIG ("Líneas límite", unidades
administrativas de 4.º orden, versión 10-08-2026): 8.132 municipios
(5.121 + 2.847 + 164 features), EPSG:4326, 7 decimales, propiedades
`mun_code` (código INE de 5 dígitos), `mun_name` y `nationalCode`. Los
genera `scripts/aocd_municipios_cnig.py` a partir de
`data/raw/cnig_lineas_limite/gml/au_AdministrativeUnit_4thOrder0.gml`,
cortando por tamaño en bytes (`--max-mb 50`, por defecto); borra las partes
anteriores antes de escribir. Ningún otro script los lee.

## `spain_municipios_full.part1..2.geojson` (en `v1/data/`)

Geometría municipal OpenDataSoft 2022 de la v1: 8.223 features; la parte 1
lleva las 4.111 primeras (índices 0..4110) y la parte 2 las 4.112 restantes.
`v1/scripts/aocd_preparar_datos.py` lee el fichero único
`data/spain_municipios_full.geojson` (ruta relativa a `v1/`), así que hay que
recombinarlas antes de ejecutarlo. Para regenerar la adyacencia municipal con
la geometría oficial basta con apuntar `cargar_geometria()` de ese script al
fichero CNIG recombinado: la columna `mun_code` es la que espera.

## Recombinar

Concatenar `features` en orden de parte:

```python
import json
partes = ['municipios_cnig_2026.part1.geojson',
          'municipios_cnig_2026.part2.geojson',
          'municipios_cnig_2026.part3.geojson']
features = []
for p in partes:
    with open(p, encoding='utf-8') as f:
        features += json.load(f)['features']
with open('municipios_cnig_2026.geojson', 'w', encoding='utf-8') as f:
    json.dump({'type': 'FeatureCollection', 'features': features}, f)
```

Para los de la v1, sustituir la lista de partes y el nombre de salida
(`spain_municipios_full.geojson`).
