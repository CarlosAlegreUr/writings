# AOCD — Algoritmo de Optimización de la Corruptibilidad de Distritos

**Estado (19/10/2026):** versión 2 ejecutada a escala nacional sobre las 36.554 secciones censales del INE: 469 distritos, 457 en rango, 12 excepciones por territorio aislado, P25 de renta mínimo 8.941 €. La v1 de junio (municipios, 928 distritos) y la ejecución de la v2 sobre municipios están archivadas en `v1/`.

## Qué es

El AOCD es el algoritmo con el que la Constitución Democrática delimita los distritos electorales. Esta carpeta contiene su implementación sobre datos públicos de España, los datos de entrada y los resultados. Artículos que implementa (texto en `../../human-rewriting/partes/es/parte-1-constitucion-completa.md`):

- **Artículo 16, Tamaño y Restricciones de los Distritos.** Cada distrito tiene entre 95.000 y 120.000 habitantes (restricción 1); es un territorio continuo, sin enclaves ni exclaves y de la menor extensión posible (restricción 2); respeta las fronteras municipales, comarcales, provinciales y autonómicas, y solo las cruza cuando es estrictamente necesario para cumplir el rango, primero la municipal, luego la comarcal, luego la provincial y en último término la autonómica (restricción 3); y puede exceder ó no alcanzar el rango, con la desviación mínima necesaria, cuando las restricciones 2 y 3 impidan formarlo (restricción 4).
- **Artículo 17, Algoritmo de Delimitación de los Distritos.** El AOCD maximiza el valor mínimo del percentil 25 de renta entre todos los distritos del país, respetando el artículo 16. Datos de entrada: población por unidad geográfica mínima disponible (municipio, sección censal ó equivalente), distribución de renta por unidad geográfica y mapa del territorio. Puede sustituirse ó modificarse por consenso de Nivel N5.
- **Artículo 18, Actualización de Distritos y Censo Distrital.** Los distritos se actualizan cada 21 años con el algoritmo vigente, por una comisión técnica independiente y con ratificación del Legislativo (consenso N1). Esta carpeta no implementa nada del artículo 18: fija la cadencia y el procedimiento, no el cálculo.

## Resultado

![Mapa de distritos — ejecución nacional sobre secciones censales](output/aocd_v2_mapa.png)

| | |
|---|---|
| Unidades | 36.554 secciones censales (INE, 1-1-2025), 49.128.297 hab. |
| Distritos | **469** (objetivo teórico 49.128.297 / 107.500 ≈ 457) |
| En rango 95.000–120.000 | **457** (97,4 %), con 48.360.087 hab. (98,4 % de la población) |
| Fuera de rango | 12, todos por territorio aislado: islas, Ceuta y Melilla (art. 16, restricción 4) |
| Distritos con más de una provincia | 14 |
| P25 de renta mínimo | **8.941 €** (distrito #026, Torrevieja); mediana 13.373 €, máximo 27.150 € |
| Diámetro de distrito | mediana 18,6 km; máximo 204,1 km |
| Tiempo | 303,3 s (`scripts/aocd_v2.py`, semilla 42, parámetros por defecto) |

Detalle en `output/INFORME.md`; cifras y argumentos en `output/resumen.json`; distritos con sus secciones en `output/distritos_legible.txt`.

## Estructura de la carpeta

```
aocd/
├── README.md
├── scripts/
│   ├── aocd_v2.py                   # AOCD v2 (arts. 16 y 17) sobre unidades genéricas
│   ├── aocd_nombrar.py              # nombres propios automáticos para los distritos del resultado
│   ├── aocd_mapa_v2.py              # mapa de distritos (coloreado de grafo; Canarias en recuadro)
│   ├── aocd_preparar_secciones.py   # seccionado + Censo + ADRH + comarcas → data/secciones_unificadas.json
│   ├── aocd_comarcas.py             # municipio → comarca (agrarias MAPA; autonómicas aparte)
│   ├── aocd_municipios_cnig.py      # GML IGN/CNIG → data/municipios_cnig_2026.part1..3.geojson (opcional)
│   ├── aocd_tramos_renta.py         # ADRH tabla 30826 → data/secciones_tramos_renta.{csv,json} (opcional)
│   └── aocd_px.py                   # lector mínimo de PC-Axis (.px) del INE
├── data/
│   ├── secciones_unificadas.json    # ENTRADA del AOCD: 36.554 secciones con población, renta, vecinos y jerarquía
│   ├── poblacion_secciones_2025.csv # intermedio: población por sección (Censo 1-1-2025)
│   ├── renta_adrh_2024_secciones_distritos_municipios.csv   # intermedio: renta ADRH 2024 por sección, distrito y municipio
│   ├── secciones_renta_imputada_2024.csv    # las 97 secciones sin renta propia y de dónde se rellenó
│   ├── secciones_tramos_renta.{csv,json}    # % de población bajo 5.000/7.500/10.000 € por unidad de consumo (no usado por aocd_v2.py)
│   ├── municipio_comarca.csv        # 8.132 municipios → comarca agraria MAPA (la que usa el pipeline)
│   ├── municipio_comarca_autonomicas.csv    # comarcas oficiales/autonómicas y Wikidata (no usado por el pipeline)
│   ├── provincia_comunidad.csv      # 52 provincias → comunidad autónoma (escalón autonómico de R5)
│   ├── municipios_cnig_2026.part1..3.geojson   # polígonos municipales IGN/CNIG en tres trozos (ver SPLIT-NOTE.md)
│   ├── SPLIT-NOTE.md                # cómo se parten y recombinan los GeoJSON de más de 50 MB
│   └── raw/                         # fuentes brutas (≈850 MB; FUENTES.md, SHA256SUMS.txt, .gitignore)
├── output/                          # ejecución nacional sobre secciones, 19/10/2026
│   ├── aocd_v2_resultado.json       # lista de distritos: unidades, población, P25, provincias, métricas
│   ├── distritos_legible.txt        # los 469 distritos con sus secciones
│   ├── INFORME.md                   # informe de la ejecución: distritos, diámetros, cruces, excepciones, bloques
│   ├── resumen.json                 # cifras, notas, bloques, enlaces artificiales y argumentos usados
│   ├── aocd_v2_mapa.png             # mapa
│   ├── nombres_distritos.{json,csv,md}  # nombre propio de cada distrito (automático, provisional; scripts/aocd_nombrar.py)
│   ├── interactivo/                 # distritos.geojson (polígonos simplificados con nombre) y municipios_por_distrito.json, para un mapa interactivo
│   └── log.txt, mapa_log.txt        # salida de la shell, no se suben al repositorio; (los scripts no los escriben)
└── v1/                              # junio de 2026 y la v2 sobre municipios; README propio
```

## Dependencias

Probado con Python 3.12.3, numpy 1.26.4, pandas 3.0.2, geopandas 1.1.3, shapely 2.1.2, pyogrio 0.12.1, pyproj 3.7.2 y matplotlib 3.10.8.

```bash
pip install numpy pandas geopandas shapely pyogrio pyproj matplotlib
```

- `aocd_v2.py` y `aocd_px.py` solo usan la librería estándar más `numpy` (métricas de salida).
- Los scripts de preparación se ejecutan con `python3 -I` (modo aislado: no entra en `sys.path` ni el directorio actual ni el del script ni el `site-packages` del usuario), porque leen descargas de `data/raw/`; cada uno vuelve a añadir explícitamente el `site-packages` del usuario para encontrar geopandas y, los que importan `aocd_px`, su propio directorio.
- `aocd_mapa_v2.py` importa geopandas directamente: se ejecuta con `python3` sin `-I` (con `-I` falla con `ModuleNotFoundError: No module named 'geopandas'` cuando geopandas está en el site del usuario).

## Pipeline

Todos los comandos se ejecutan desde esta carpeta (`aocd/`); las rutas por defecto de los scripts son relativas a ella.

```bash
# 0. Datos brutos: descarga manual con las URL de data/raw/FUENTES.md y comprobación de checksums
cd data/raw && sha256sum -c SHA256SUMS.txt && cd ../..

# 1. Comarcas: municipio → comarca agraria (MAPA) y, en fichero aparte, comarcas autonómicas
python3 -I scripts/aocd_comarcas.py
#    → data/municipio_comarca.csv, data/municipio_comarca_autonomicas.csv

# 2. Secciones censales: seccionado 2025 + Censo 2025 + ADRH 2024 + comarcas, con adyacencia real de polígonos
python3 -I scripts/aocd_preparar_secciones.py
#    → data/secciones_unificadas.json (+ poblacion_secciones_2025.csv,
#      renta_adrh_2024_secciones_distritos_municipios.csv, secciones_renta_imputada_2024.csv)
#    Con la renta 2023 de respaldo: --anyo-renta 2023 --px-renta data/raw/ine_adrh/px_renta/30824.px

# 3. (opcional) Distribución de renta por umbrales fijos, por sección (ADRH tabla 30826)
python3 -I scripts/aocd_tramos_renta.py
#    → data/secciones_tramos_renta.csv, data/secciones_tramos_renta.json

# 4. (opcional) Geometría municipal oficial IGN/CNIG en GeoJSON troceado
python3 -I scripts/aocd_municipios_cnig.py
#    → data/municipios_cnig_2026.part1..3.geojson

# 5. AOCD v2 (por defecto: --entrada data/secciones_unificadas.json --salida output)
python3 scripts/aocd_v2.py
#    → output/aocd_v2_resultado.json, distritos_legible.txt, INFORME.md, resumen.json

# 6. Mapa (por defecto lee output/aocd_v2_resultado.json, data/secciones_unificadas.json
#    y el shapefile data/raw/ine_seccionado/2025/*/SECC_CE_20250101.shp, código en CUSEC)
python3 scripts/aocd_mapa_v2.py
#    → output/aocd_v2_mapa.png
```

Orden: 1 antes de 2 (si falta `municipio_comarca.csv`, las secciones salen sin comarca y la jerarquía pierde ese nivel), 2 antes de 5 y 5 antes de 6. El paso 2 descomprime `data/raw/ine_seccionado/seccionado_2025.zip` si no encuentra el shapefile. Los pasos 3 y 4 no alimentan a `aocd_v2.py`: el 3 deja preparados datos de distribución de renta que aún no se usan (ver "Limitaciones") y el 4 produce la geometría municipal oficial para quien quiera repetir la variante municipal con ella; `aocd_comarcas.py` lee el GML bruto directamente.

Parámetros útiles de `aocd_v2.py` (`--help` para la lista completa): `--min`/`--max` (rango), `--semilla` (42), `--holgura N` (holgura por distrito exigida al bloque vecino en una transferencia; 0 = literal del art. 16: cruzar solo si no existe ningún reparto en rango), `--comunidades` (tabla provincia → comunidad), `--sin-bloques-municipales`, `--sin-transferencias` (no cruzar provincias: los bloques estructurales quedan como excepción), `--radio-aislados KM` (30), `--peso-compacidad` (100 € de P25 por km), `--tau` (250 €), `--solo-provincias 28,45` (depuración).

Variante sobre municipios (la unidad de la v1): ver `v1/README.md`. Desde esta carpeta, `python3 scripts/aocd_v2.py --entrada v1/data/municipios_unificados.json --salida v1/output/v2-municipios` y, para el mapa, `python3 scripts/aocd_mapa_v2.py --resultado v1/output/v2-municipios/aocd_v2_resultado.json --unidades v1/data/municipios_unificados.json --geojson v1/data/spain_municipios_full.part1.geojson v1/data/spain_municipios_full.part2.geojson --campo-codigo mun_code --salida v1/output/v2-municipios/aocd_v2_mapa.png`. La ejecución archivada en `v1/output/v2-municipios/` usó `--holgura 2000` (entonces el valor por defecto) y una versión del script anterior a los cambios del 19/10, así que no se reproduce exactamente.

## Fuentes de datos

Todo descargado el 19-10-2026. Procedencia, URL exactas, licencias, recuentos, cruces de códigos y lo que se intentó sin éxito, en **`data/raw/FUENTES.md`**; checksums en `data/raw/SHA256SUMS.txt`.

| Dato | Fuente | Referencia | Registros | Uso |
|---|---|---|---|---|
| Población por sección censal | INE, Censo anual de población, tabla 65032 | 1-1-2025 | 36.554 secciones, 49.128.297 hab. | población de cada unidad |
| Renta neta media por persona | INE, Atlas de Distribución de Renta de los Hogares (ADRH) 2024, tabla 30824, edición del 15-10-2026 | 2024 | 36.457 secciones con dato; 97 imputadas | renta media de cada unidad, de la que se estima el P25 |
| Distribución de renta por unidad de consumo | INE, ADRH 2024, tabla 30826: % de población por debajo de 5.000, 7.500 y 10.000 € | 2024 | 34.852 secciones con dato | preparado (`secciones_tramos_renta.*`), no usado |
| Cartografía de secciones | INE, seccionado 1-1-2025 (`SECC_CE_20250101.shp`, EPSG:25830) | 2025 | 36.554 polígonos | adyacencia real, centroides, mapa |
| Comarcas (cobertura nacional) | MAPA, Comarcas Agrarias (ArcGIS REST; geometría de enero de 2022) | 2022 | 339 polígonos, 338 usadas | nivel "comarca" de la jerarquía |
| Comarcas oficiales ó autonómicas | IDESCAT, Aragón Open Data, Xunta/IDEG, GeoEuskadi, Wikidata | vigentes | 947 / 731 / 313 / 257 / 3.334 municipios | `municipio_comarca_autonomicas.csv`, no usado |
| Geometría municipal | IGN/CNIG, Líneas límite (GML INSPIRE, versión 10-08-2026) | 2026 | 8.132 municipios | asignación espacial de comarcas; GeoJSON opcional |
| Provincia → comunidad autónoma | tabla estática `data/provincia_comunidad.csv` (no la genera ningún script) | — | 52 provincias | escalón autonómico de R5 |

**Aviso:** `data/raw/` pesa unos 850 MB (`du -sb` = 850.111.760 bytes el 19/10/2026) y no va al repositorio: el `.gitignore` de `aocd/` excluye todo su contenido salvo `FUENTES.md`, `SHA256SUMS.txt` y su propio `.gitignore`, de modo que las fuentes se re-descargan con las instrucciones de `FUENTES.md` y se verifican con las sumas. Los datos preparados de `data/` (unos 129 MB, ningún fichero por encima de 50 MB) sí se suben, igual que los municipales de junio en `v1/data/`.

## Versión 2: el algoritmo (arts. 16 y 17)

`scripts/aocd_v2.py` trabaja sobre unidades geográficas genéricas. Entrada: JSON `{código: {nombre, poblacion, renta_media, provincia, lat, lon, vecinos[], municipio, distrito_municipal, comarca, cusec}}`. Con secciones censales, `comarca`, `municipio` y `distrito_municipal` dan la jerarquía de la restricción 3; con el JSON municipal de la v1 no hay comarca y cada municipio es un nodo.

### Reglas

- **R1 — Unidad mayor que el máximo sin subunidades.** Distrito propio, marcado "requiere subdivisión por secciones censales"; no se junta con nada. Con secciones no ocurre (0 casos); con municipios afectó a 56 ciudades.
- **R2 — Territorios y bloques.** Territorio = componente conexa de una provincia sobre el grafo de vecindad (Burgos tiene T1 y T2, el Condado de Treviño; Illes Balears T1–T4 son sus islas). Dentro de cada territorio, todo municipio conexo cuya población admite por sí sola una partición en rango es un bloque propio: no se cruza su frontera si no es estrictamente necesario. El resto del territorio forma bloques por componentes conexas. Cada bloque se resuelve por separado. Si un bloque restante no puede arreglarse con transferencias dentro de su provincia, la provincia se reconstruye sin bloques municipales antes de cruzar provincias (vuelta atrás; ocurrió en Murcia).
- **R3 — Factibilidad.** Un bloque de población P es factible si existe K con K·95.000 ≤ P ≤ K·120.000; K objetivo = round(P / 107.500) acotado a ese intervalo.
- **R4 — Artefactos.** Bloque infactible cuyo territorio completo sí es factible (la infactibilidad la causan las ciudades R1 apartadas): se resuelve como excepción con desviación mínima, sin cruzar provincia. Con secciones no ocurre.
- **R5 — Transferencias.** Bloque infactible por estructura (su territorio tampoco es factible: Soria, Ávila, Segovia, Palencia, Zamora, Teruel, exclaves): se cruza la frontera con la mínima población movida (más 1.000 habitantes equivalentes por unidad movida, para favorecer transferencias compactas), probando por este orden un bloque de la misma provincia (nivel 0), de otra provincia de la misma comunidad (nivel 1) y de otra comunidad (nivel 2, tabla `data/provincia_comunidad.csv`), con tres opciones: recibir unidades de un bloque vecino, cederle unidades ó unirse a él entero (solo bloques menores que un distrito). Condiciones: contigüidad de ambos bloques tras el movimiento y que el vecino no empeore (sigue siendo factible con la holgura `--holgura` por distrito, por defecto 0). Sin opción viable (islas, Ceuta, Melilla): excepción.
- **R6 — Nodos jerárquicos.** Dentro de un bloque las unidades se agrupan en nodos indivisibles por el nivel más grueso (comarca > municipio > distrito municipal > sección) cuya población no supere el máximo y sea conexo. Si con esos nodos no se encuentra partición en rango, se refinan los nodos de los distritos fuera de rango (se rompe la comarca, después el municipio) y se reintenta.
- **R7 — Partición y equilibrado.** Semillas k-means++ ponderadas por población (los nodos que alcanzan el mínimo son semillas forzadas), crecimiento multi-fuente por distancia al centroide con capacidad y 3 iteraciones de Lloyd; después, recocido de equilibrado con movimientos de nodos de frontera (contigüidad comprobada por BFS) y reparación por fusión/división. En el equilibrado cada rotura de coherencia cuesta habitantes equivalentes: provincia 60.000, comarca 25.000, municipio 12.000, distrito municipal 5.000.
- **R8 — Objetivo lexicográfico.** (a) Factibilidad: rango, contigüidad, no aumentar cruces de provincia ni roturas de comarca. (b) Maximizar el P25 mínimo, con un softmin de temperatura `--tau` (250 €) sobre los distritos del bloque que aproxima el leximin. (c) Compacidad: radio cuadrático medio ponderado por población al centroide, en km, con peso `--peso-compacidad` (100 € de P25 por km).

Las unidades sin vecinos en la geometría (enclaves, islotes, huecos del shapefile) reciben una adyacencia artificial con la unidad más cercana de su provincia si está a menos de `--radio-aislados` km (30); el informe las lista.

Cambios del 19/10/2026 respecto a la ejecución sobre municipios: bloques municipales con vuelta atrás por provincia (R2), escalón autonómico con `data/provincia_comunidad.csv` (R5) y holgura por defecto 0 en lugar de 2.000.

### Compacidad: la medida de la restricción 2

La Constitución pide distritos "de la menor extensión posible". La v2 lo mide con tres cantidades por distrito (`metricas_distrito`): el **radio RMS** (raíz de la suma de los autovalores de la covarianza de las posiciones de las unidades ponderada por población, en km), que es el término (c) del objetivo y también pesa en el equilibrado (`--peso-comp-eq`, 150 habitantes equivalentes por km); el **diámetro** (máxima distancia haversine entre centroides de unidades), que solo se informa; y la **elongación** (raíz del cociente entre el autovalor mayor y el menor), que solo se informa.

### P25 estimado

El artículo 17 pide el percentil 25 de renta de cada distrito. El INE no publica la distribución completa de la renta por sección —solo medias, medianas y porcentajes acumulados por debajo de umbrales fijos (`FUENTES.md`, punto 2c)—, así que el P25 se estima como **percentil poblacional de las rentas medias de las unidades**: se ordenan las unidades del distrito por renta neta media por persona y se toma la renta de la unidad en la que la población acumulada alcanza el 25 % del total (`p25_estimado`, sustituible asignando otra función a `P25_FUNC`). Es la misma estimación de la v1, con 36.554 unidades en vez de 8.131.

## Resultados en detalle (ejecución nacional, `output/`)

Comando: `python3 scripts/aocd_v2.py` con los valores por defecto (rango 95.000–120.000, semilla 42, holgura 0, peso de compacidad 100 €/km, tau 250 €, `data/provincia_comunidad.csv`); 303,3 s.

**Bloques.** 104 bloques: 94 normales y 10 aislados. 42 municipios se resolvieron como bloque propio por caber solos en el rango, y suman 140 distritos: Madrid (3.477.497 hab., 32 distritos), Barcelona (1.713.247, 16), València (841.558, 8), Zaragoza (699.007, 7), Sevilla (688.714, 6), Málaga (597.173, 6), Palma (4), Las Palmas de Gran Canaria (4), Bilbao, Córdoba, Valladolid, Vigo y L'Hospitalet de Llobregat (3 cada uno), 13 municipios con 2 distritos y 16 con 1 (de Jaén, 112.119 hab., a San Sebastián de los Reyes, 97.330). El informe cuenta 44 porque incluye Cartagena y Lorca, descartados al reconstruir Murcia sin bloques municipales (único caso de vuelta atrás). En 32 bloques hubo que refinar nodos (527 en total).

**Fuera de rango: 12 distritos, todos por territorio aislado (art. 16, restricción 4).** Eivissa en dos distritos (84.194 y 80.071 hab.), Formentera (11.690), Lanzarote en dos (83.496 y 83.382), Fuerteventura en uno por encima del máximo (129.080), A Illa de Arousa (4.813), La Palma (86.297), La Gomera (22.560), El Hierro (11.993), Ceuta (83.567) y Melilla (87.067).

**Diámetros.** Mínimo 2,3 km; P25 7,7; mediana 18,6; P75 52,1; P90 90,5; máximo 204,1. 40 distritos superan los 100 km y 12 los 150: Zaragoza 1 (204,1 km, elongación 3,12), Badajoz 5 (190,4), Zamora 1 (189,7), Burgos T1 2 (183,8), Teruel (179,9), León 4 (174,0), Ciudad Real T1 5 (167,5, elongación 4,05), Guadalajara 2 (163,3), Cáceres B1 3 (161,8), Cuenca 1 (158,1), Ciudad Real T1 2 (157,6) y Soria (153,9).

**Cruces provinciales.** 14 distritos con unidades de más de una provincia, producto de 17 transferencias R5, todas justificadas en el informe con "el bloque … no admite partición en [95.000, 120.000] (art. 16, restr. 3 …; opción de mínima población movida)":

- Nivel 0 (dentro de la provincia): 1. Aliseda (1.727 hab., 2 secciones) se une al bloque municipal de Cáceres.
- Nivel 1 (otra provincia de la misma comunidad): 12. Las voluminosas: Ávila recibe 29.281 hab. (60 secciones) de Salamanca; Segovia recibe 31.752 de Burgos (23 secciones, entre ellas las de Aranda de Duero); Palencia T1 recibe 30.665 de Burgos (18 secciones, incluidas secciones de la ciudad de Burgos) y además recibe Castrojeriz (792); Zamora recibe 24.251 de Valladolid (16 secciones: Arroyo de la Encomienda, Medina del Campo, Tordesillas…); Teruel cede 16.663 (Alcañiz, Albalate del Arzobispo…) a Zaragoza; Soria recibe 4.975 de Burgos (dos secciones de Aranda de Duero, Fresnillo de las Dueñas y Santa Cruz de la Salceda). Las demás son exclaves ó bolsas: Orduña (4.243) a Álava; Berzosilla (45) y Villodrigo (100) a Burgos; Anchuras (265) a Toledo; Quintanilla del Molar y Roales de Campos (199) a Zamora.
- Nivel 2 (otra comunidad autónoma): 4, todos exclaves ó bolsas sin alternativa: Petilla de Aragón (Navarra, 29 hab.) a Zaragoza; Valle de Villaverde (Cantabria, 249) a Bizkaia; Condado de Treviño y La Puebla de Arganzón (Burgos, 2.034) a Álava; el exclave valenciano de Ademuz (Ademuz, Casas Altas, Casas Bajas, Castielfabib, Puebla de San Miguel, Torrebaja…, 2.158 hab., 7 secciones) a Cuenca.

**P25 de renta.** Mínimo 8.941 € (#026 Torrevieja, bloque municipal), mediana 13.373 €, máximo 27.150 €. Comparación: v2 sobre municipios 8.147 €; v1 7.779 €.

**Enlaces artificiales (4).** Hacinas → Villanueva de Carazo (3,5 km), Monasterio de la Sierra → Valle de Valdelaguna (6,4 km), Llívia → Puigcerdà (5,5 km) y Teguise sección 01010 (La Graciosa) → Haría (7,7 km). Son huecos reales del shapefile del INE (`FUENTES.md`).

**Verificación automática del informe.** Cada unidad asignada exactamente una vez; ningún distrito no contiguo (BFS sobre `vecinos`); la suma de poblaciones de los distritos es la población total.


Las salidas de estas dos pruebas no se conservan en el repositorio (se regeneran con los comandos indicados):
- `v2-test`: `--solo-provincias 07,09,34,42,50,17,01,48` (Illes Balears, Burgos, Palencia, Soria, Zaragoza, Girona, Álava, Bizkaia): 4.333 secciones, 50 distritos, 47 en rango, 7,8 s. Prueba de transferencias y exclaves.
- `v2-secciones-28`: `--solo-provincias 28 --holgura 2000` (Madrid): 4.518 secciones, 64 distritos, todos en rango, P25 mínimo 10.935 €, 621 s; ejecutada con una versión del script anterior a los cambios del 19/10 (su `resumen.json` no tiene los argumentos `comunidades` ni `sin_bloques_municipales`).

## Historia

- **v1 (junio de 2026, `v1/`).** Municipio como unidad: 8.131 municipios (Padrón 2024, 48.583.241 hab.; Atlas de Renta 2022; geometría OpenDataSoft 2022). Partición voraz desde los municipios más poblados y recocido simulado que solo movía municipios de frontera. Resultado: 928 distritos (objetivo ≈ 452), 680 fuera de rango, P25 mínimo 7.779 €, ciudades enteras como distrito único (Madrid, 3.416.771 hab.) y distritos serpiente de hasta 303 km. Falló porque no tenía fase de fusión (cada semilla rural que no podía crecer quedaba como distrito diminuto), el recocido no lograba ninguna mejora del P25 mínimo con esa fragmentación, no conocía las comarcas y no limitaba los cruces provinciales. Ficheros: `v1/README.md`, `v1/scripts/`, `v1/data/`, `v1/output/`.
- **v2 sobre municipios (19/10/2026, `v1/output/v2-municipios/`).** Primera versión de `aocd_v2.py` (reglas R1–R8, holgura 2.000) sobre el mismo JSON municipal: 351 distritos, 251 en rango y 100 fuera (56 ciudades de más de 120.000 hab. sin subunidades, 20 bloques factibles sin partición contigua en rango, 14 bloques artefacto, 10 territorios aislados); solo el 54,9 % de la población en distritos en rango; P25 mínimo 8.147 €; 250,1 s. Demostró que con municipios no hay solución: Cornellà de Llobregat, El Prat, San Fernando, Pozuelo de Alarcón, Fuengirola, Benalmádena ó Águilas no caben en ningún distrito contiguo en rango porque todos sus vecinos son demasiado grandes.
- **v2 sobre secciones censales (19/10/2026, `output/`).** Datos nuevos (Censo y seccionado 2025, ADRH 2024, comarcas agrarias, geometría CNIG) y tres cambios en el algoritmo (bloques municipales con vuelta atrás, escalón autonómico, holgura 0). Es la ejecución documentada arriba.

## Limitaciones conocidas

1. **P25 estimado, no medido.** Se calcula sobre rentas medias por sección, no sobre la distribución individual de la renta (ver "P25 estimado"). Los únicos datos de distribución que publica el INE por sección —porcentajes acumulados de población por debajo de 5.000, 7.500 y 10.000 € por unidad de consumo, con 1.702 secciones sin dato— están preparados en `data/secciones_tramos_renta.json` pero `aocd_v2.py` no los usa.
2. **Municipios de 120.000 hab. ó menos repartidos entre distritos: 21** (recuento sobre `output/aocd_v2_resultado.json`). Cinco por las transferencias R5 documentadas en el informe: Aranda de Duero (33.904 hab.) entre Segovia 2 y Soria, sin que quede ninguna sección en un distrito de Burgos; Alcañiz entre Teruel y Zaragoza 1; Arroyo de la Encomienda, Medina del Campo y Tordesillas entre Valladolid y Zamora 1. Dieciséis dentro de su propio bloque, lo que R6 solo permite tras refinar el nodo municipal: Lorca (98.613), Cornellà de Llobregat (92.255, en tres distritos), Chiclana de la Frontera (90.997), Pontevedra (83.339), Gandia (82.909), Santa Lucía de Tirajana (79.506), Benalmádena (78.787), Santa Eulària des Riu, Torre-Pacheco, Arucas, Mazarrón, Sant Josep de sa Talaia, Alhama de Murcia, Mogán, San Bartolomé y Pasaia. Además, secciones de la ciudad de Burgos (que debe partirse de todos modos) van a un distrito de Palencia.
3. **Comarcas agrarias como sustituto de las comarcas oficiales.** No existe una tabla oficial nacional municipio → comarca (`FUENTES.md`, puntos 4a y 4c); el pipeline usa las 339 comarcas agrarias del MAPA (338 con municipios) asignadas por geometría, y las comarcas oficiales de Cataluña, Aragón, Galicia y Euskadi quedan en `municipio_comarca_autonomicas.csv` sin usar. De las 253 comarcas agrarias de 120.000 hab. ó menos, 36 quedan repartidas entre dos ó más distritos; las otras 85 superan el máximo y deben partirse (recuento sobre el resultado).
4. **Murcia reconstruida sin bloques municipales.** Es la única provincia en la que los bloques municipales (Cartagena, 220.400 hab.; Lorca, 98.613) no dejaban un resto resoluble dentro de la provincia; la vuelta atrás los disolvió y Lorca quedó partida en dos distritos.
5. **Enlaces artificiales y grupos aislados.** La reparación de adyacencia solo actúa sobre unidades sin ningún vecino: enlaza 4 secciones (Hacinas, Monasterio de la Sierra, Llívia y La Graciosa) a la más cercana de su provincia a menos de 30 km. Un grupo de secciones aislado pero conexo entre sí no se enlaza: A Illa de Arousa (3 secciones, 4.813 hab.) queda como excepción, mientras que en la ejecución municipal, al ser una sola unidad, se enlazó a Cambados (7,9 km).
6. **Excepciones insulares con desviación grande.** Fuerteventura forma un solo distrito de 129.080 hab.; Eivissa y Lanzarote, dos distritos de entre 80.071 y 84.194 hab. cada uno; Formentera, La Gomera, El Hierro y A Illa de Arousa son distritos de 4.813 a 22.560 hab.
7. **Distritos muy extensos en la España despoblada.** 40 distritos superan los 100 km de diámetro y 12 los 150; Zaragoza 1 llega a 204,1 km con elongación 3,12, y Ciudad Real T1 5 a 167,5 km con elongación 4,05.
8. **Transferencias de nivel 1 voluminosas.** Cuatro mueven entre 24.251 y 31.752 hab. (Salamanca → Ávila, Burgos → Segovia, Burgos → Palencia, Valladolid → Zamora); el informe las justifica como estrictamente necesarias para que la provincia receptora quepa en el rango.
9. **Renta imputada en 97 secciones.** 17 toman la renta de su distrito municipal y 80 la media provincial ponderada (`data/secciones_renta_imputada_2024.csv`).
10. **Discrepancias internas del informe.** `INFORME.md` cuenta 44 municipios como bloque propio, pero los resueltos son 42 (Cartagena y Lorca se descartaron con Murcia). En la tabla "Bloques resueltos", K es el objetivo, no el número final de distritos: difieren en Alicante (18 frente a 19), Barcelona (29 frente a 31), Murcia (15 frente a 14) y Bizkaia T1 (7 frente a 6), por lo que la suma de K es 468 y los distritos son 469.
11. **Heurística sin garantía de óptimo.** Partición inicial y recocido con semilla fija (42) y tope de tiempo por bloque; otra semilla ó otros pesos (`--tau`, `--peso-compacidad`) dan otra partición. Los informes registran cuántas mejoras del P25 mínimo encontró cada bloque, no su distancia al óptimo.
12. **Fechas distintas en los datos.** Población a 1-1-2025, renta de 2024, seccionado a 1-1-2025, geometría de comarcas agrarias de enero de 2022 y municipios IGN de agosto de 2026.
13. **Mapa.** `aocd_mapa_v2.py` calcula centroides en coordenadas geográficas para separar Canarias (avisos `UserWarning` en `output/mapa_log.txt`); solo afecta a ese reparto entre paneles, no a los distritos.
14. **Artículo 18 sin implementar.** La actualización cada 21 años, la comisión técnica y la ratificación son procedimiento, no cálculo; aquí no hay nada de ello.
