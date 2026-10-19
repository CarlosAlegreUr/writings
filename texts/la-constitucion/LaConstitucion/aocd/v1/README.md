# AOCD v1 (junio de 2026) — obsoleta

Primera simulación, con el municipio como unidad mínima: 928 distritos, ciudades enteras como distrito único y distritos serpiente de hasta 303 km. Se conserva como historia. La versión vigente es la v2 de la carpeta superior (`scripts/aocd_v2.py` sobre `data/secciones_unificadas.json`).

Contenido:
- `scripts/`: `aocd_preparar_datos.py` (cruce de los tres datasets municipales), `aocd_simulacion.py` (partición voraz + recocido) y `aocd_mapa.py`. Sus rutas relativas (`data/...`) se refieren a esta carpeta: ejecutar desde `v1/`.
- `data/`: Padrón 2024 por municipio, Atlas de Renta 2022 por municipio, geometría OpenDataSoft 2022 en dos trozos y `municipios_unificados.json` (8.131 municipios con adyacencia). La v2 también puede ejecutarse sobre este JSON: `python3 scripts/aocd_v2.py --entrada v1/data/municipios_unificados.json --salida v1/output/v2-municipios` desde la carpeta superior.
- `output/`: resultados de junio y, en `v2-municipios/`, la ejecución de la v2 sobre municipios del 19/10/2026 (351 distritos).
