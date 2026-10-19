# Fuentes brutas del AOCD por sección censal

Fecha de descarga de todo lo que sigue: **19-10-2026** (UTC 11:40–13:40), desde
esta máquina con `curl`. Checksums SHA-256 de cada fichero en `SHA256SUMS.txt`
(`cd data/raw && sha256sum -c SHA256SUMS.txt`). Nada de este directorio se
ejecuta: los scripts están en `../../scripts/` y leen por ruta con `python3 -I`.

Convención de esta nota: lo que no lleva marca está verificado (cabecera HTTP,
fichero leído, recuento calculado). `[inferido]`, `[supuesto]` y
`[no verificado]` marcan lo demás.

Ficheros > 50 MB: están listados en `.gitignore` de este directorio y **no deben
subirse**; se regeneran con las URL de abajo. El CSV del Censo se guarda
comprimido (`.gz`, 10,7 MB) y el script lo lee así.

---

## 1. Población por sección censal — INE, Censo anual de población (1-1-2025)

**Directorio:** `ine_censo_anual_secciones/`
**Fichero:** `censo_anual_65032_poblacion_sexo_nacionalidad_secciones.csv.gz`
(10.743.602 bytes; descomprimido 210.275.146 bytes, SHA-256
`d72c3712732b83e29abd52847ef5e0838b3c634db922acd1187dd8f0bbe5b92a`).

- URL exacta: `https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/65032.csv?nocab=1`
  (HTTP 200, `text/plain;charset=ISO-8859-15`). Tabla 65032 "Población por sexo y
  nacionalidad (española/extranjera)", operación INE 463 *Censo anual de
  población*, código de tabla `NAC-SECC-MUN-PROV`. Página INEbase: Censo anual de
  población → Resultados por secciones censales → Total nacional
  (`https://www.ine.es/dynt3/inebase/index.htm?padre=11555&capsel=11101`,
  "Última modificación: 02/12/2025"; la página avisa de que "debido al volumen de
  las tablas de este apartado, sólo se ofrecen las descargas").
- Contenido: 2.028.465 filas de datos; separador `;`; miles con `.`; columnas
  `Total Nacional;Provincias;Municipios;Secciones;Sexo;Nacionalidad;Periodo;Total`.
  Periodos 2021, 2022, 2023, 2024 y 2025 (población a 1 de enero). Unidades:
  52 provincias, 8.132 municipios, 36.892 códigos de sección (10 dígitos:
  provincia+municipio+distrito+sección). Para 2025 solo tienen valor 36.554
  códigos, exactamente los del seccionado 2025; los 338 restantes son códigos de
  años anteriores con celda vacía en 2025.
- Total nacional 2025: 49.128.297; suma de las 36.554 secciones 2025: 49.128.297.
- Licencia: aviso legal del INE
  (`https://www.ine.es/ss/Satellite?L=es_ES&c=Page&cid=1254735849170&p=1254735849170&pagename=Ayuda%2FINELayout`):
  "el INE solo autoriza la reutilización de aquélla cuya fuente original sea el
  propio INE. Esta reutilización podrá tener objeto comercial o no comercial …
  Debe citarse la fuente de la información objeto de reutilización … Elaboración
  propia con datos extraídos del sitio web del INE: www.ine.es".
- Alternativa descartada: la *Estadística del Padrón continuo* "Datos por
  secciones censales" (ficheros PC-Axis `https://www.ine.es/pcaxisdl/t20/e245/p07/a2022/l0/PP01.px`,
  uno por provincia PP) llega solo hasta el 1-1-2022 en INEbase
  (`index.htm?type=pcaxis&path=/t20/e245/p07/a2022&file=pcaxis&L=0`); el INE
  no publica ese producto para 2023 en adelante (comprobado en el selector de
  años de la página de resultados). Por eso se usa el Censo anual.
- La API JSON (`servicios.ine.es/wstempus/js/ES/DATOS_TABLA/65032?nult=1`)
  responde `{"status":"No puede mostrarse por restricciones de volumen"}`.

## 2. Renta por sección, distrito y municipio — INE, Atlas de Distribución de Renta de los Hogares (ADRH)

**Directorio:** `ine_adrh/`. Dos ediciones:

### 2a. ADRH 2024 (edición publicada el 15-10-2026) — la que usa el pipeline

- Ficheros: `px_jaxiT3_2026-10-19/30824.px` (28.479.022 bytes, tabla NACIONAL
  "Indicadores de renta media y mediana", todas las provincias) y
  `px_jaxiT3_2026-10-19/30833.px` (847.778 bytes, tabla provincial de
  Alicante/Alacant, descargada como prueba).
- URL exacta: `https://www.ine.es/jaxiT3/files/t/es/px/30824.px?nocab=1`
  (HTTP 200, `application/pc-axis`; `CREATION-DATE="20261019"`). Operación INE
  353 ADRH; en INEbase: Atlas de distribución de renta de los hogares →
  "Resultados por municipios, distritos y secciones censales"
  (`https://www.ine.es/dynt3/inebase/index.htm?padre=12385&capsel=12384`).
- Contenido: STUB `Unidades territoriales` (8.139 municipios, 10.517 distritos,
  37.229 secciones, con bloque `CODES`), HEADING `Indicadores de renta media`
  × `Periodo` (2015–2024). Indicadores: *Renta neta media por persona*, *Renta
  neta media por hogar*, media y mediana de la renta por unidad de consumo,
  renta bruta media por persona y por hogar. Unidad: euros, 0 decimales.
  **El pipeline usa "Renta neta media por persona"** (y exporta también "por
  hogar" al CSV derivado).
- Cobertura 2024: 36.457 secciones, 10.377 distritos y 8.052 municipios con
  renta neta media por persona. Las 36.457 secciones están todas en el seccionado
  2025 (`SECC_CE_20250101`): el ADRH 2024 usa el seccionado a 1-1-2025. Quedan
  97 secciones del seccionado 2025 sin dato (secreto estadístico / tamaño).
- Que la edición 2024 existe se comprobó en la API con la tabla nacional
  pequeña 53689 (`DATOS_TABLA/53689?nult=2`: 2024 = 15.948 €, 2023 = 15.036 €
  de renta neta media por persona, Total Nacional) y en el propio PC-Axis.
- Importante: la exportación jaxiT3 de estas tablas **falló durante ~1 hora**
  (HTTP 500, página "599": "Debido a cuestiones técnicas, la web del INE no
  funciona con normalidad") y funcionó a las 13:30 UTC. Si vuelve a fallar,
  usar la publicación completa (2b) o esperar. La API `DATOS_TABLA/30824`
  rechaza la tabla por volumen incluso con `nult=1`.
- La publicación completa de la edición 2024 (`/daco/inebase_mensual/octubre_2026/adrh.zip`)
  daba 404 el 19-10-2026.

### 2b. ADRH 2023 — publicación completa (octubre 2025), de respaldo

- Fichero: `adrh_2023_octubre_2025.zip` (77.728.566 bytes; `Last-Modified:
  Tue, 11 Nov 2025 16:30:38 GMT`). URL exacta:
  `https://www.ine.es/daco/inebase_mensual/octubre_2025/adrh.zip`, enlazada desde
  "Descarga de publicaciones completas"
  (`https://www.ine.es/CDINEbase/consultar.do?id_oper=217`, "Período 2023 —
  Octubre 2025"). El zip (564 ficheros, 854 MB) contiene `adrh/DATOS/px/*.px`
  (las 540 tablas del ADRH), `metodologia_adrh.pdf` e índices HTML.
- Extraído aquí: `px_renta/` (52 tablas "Indicadores de renta media y mediana"
  `DIST-SECC-MUN`: 51 provinciales + la nacional 30824; Illes Balears solo está
  en la nacional), `px_demograficos/` (53: 52 provinciales + nacional 30832;
  indicadores: edad media, % <18, % ≥65, tamaño medio del hogar, % hogares
  unipersonales, **Población**, % población española), `metodologia_adrh.pdf`,
  `cap2_adrh.htm`, `inicio.htm`.
- Cobertura 2023 (versión del zip): 36.394 secciones con renta neta media por
  persona; 36.314 de ellas en el seccionado 2025. En el PC-Axis de 2a, los
  valores 2023 aparecen ligeramente revisados (36.383 secciones).
- Para usar 2023 en el pipeline:
  `python3 -I scripts/aocd_preparar_secciones.py --anyo-renta 2023 --px-renta data/raw/ine_adrh/px_renta/30824.px`.

### 2c. ADRH — "Distribución de la renta por unidad de consumo" por sección (umbrales fijos), edición 2024

**Directorio:** `ine_adrh_tramos/` (encargo posterior, 19-10-2026 13:24 UTC).

- El ADRH **no publica tramos de renta disjuntos** (no existe ninguna tabla
  "Distribución por tramos de renta…": comprobado en el catálogo de la API
  `TABLAS_OPERACION/353` —540 tablas, 10 familias—, en las páginas INEbase de
  resultados por secciones (`padre=12385&capsel=12384`, 0 menciones de "tramo")
  y nacionales (`capsel=8752`, solo "tramos de edad"), y en
  `ine_adrh/metodologia_adrh.pdf`). Lo que publica, por sección, distrito y
  municipio, es la tabla **"Porcentaje de población con ingresos por unidad de
  consumo por debajo de determinados umbrales fijos por sexo"**, cuya variable
  de columna se llama literalmente `Distribución de la renta por unidad de
  consumo` con tres valores ACUMULADOS: `Población con ingresos por unidad de
  consumo por debajo de 5.000 Euros`, `… por debajo de 7.500 Euros`, `… por
  debajo de 10.000 Euros` (UNITS "%", 1 decimal). No hay umbral de 15.000 €.
  Tramos disjuntos derivables: <5.000; 5.000–7.500; 7.500–10.000; ≥10.000.
  (Existe además la tabla hermana de umbrales relativos: por debajo del 40/50/60 %
  y por encima del 140/160/200 % de la mediana nacional; id nacional 30829, no
  descargada en 2024; su versión 2023 está en el zip de 2b.)
- Unidad: **renta por unidad de consumo** (renta neta del hogar dividida por sus
  unidades de consumo según la escala OCDE modificada: 1 el primer adulto, 0,5
  los demás de 14 o más años, 0,3 los menores de 14; valor asignado a cada
  miembro). Porcentaje de población, por sexo (Total/Hombres/Mujeres). Fuente de
  la definición: `metodologia_adrh.pdf`, pág. 4–5.
- Fichero 2024: `30826_umbrales_fijos_sexo_nacional.px` (25.367.824 bytes;
  `CREATION-DATE="20261019"`), URL exacta
  `https://www.ine.es/jaxiT3/files/t/es/px/30826.px?nocab=1` (HTTP 200,
  `application/pc-axis`). Tabla nacional (52 provincias): 37.229 códigos de
  sección, 10.517 distritos, 8.139 municipios; periodos 2015–2024.
  Cobertura 2024, sexo Total: **34.852 secciones con dato, todas del seccionado
  2025; 1.702 secciones del seccionado 2025 sin dato**; los tres umbrales están
  presentes o ausentes a la vez.
- Fichero 2023 de respaldo: `30826_umbrales_fijos_sexo_nacional_edicion2023_del_zip.px`
  (23.244.601 bytes), copia extraída de `ine_adrh/adrh_2023_octubre_2025.zip`
  (`adrh/DATOS/px/30826.px`). Cobertura 2023: 31.629 secciones (31.556 del
  seccionado 2025).
- Supresión (metodología, pág. 7–8): estos indicadores "solo se publican en
  unidades con al menos 500 residentes"; "cuando un municipio o distrito cuenta
  con varias subunidades territoriales … y alguna de ellas no alcanza el umbral
  poblacional establecido, los indicadores no se publican en ninguna de las
  subunidades"; se excluyen las secciones con renta agregada negativa y los
  "tramos de renta negativos". Las 1.702 secciones sin dato se atribuyen a
  estas reglas `[inferido: el fichero no distingue el motivo]`.
- Derivados: `../secciones_tramos_renta.csv` (cusec, anyo, tramo literal,
  porcentaje; sexo Total, año 2024) y `../secciones_tramos_renta.json`
  ({cusec: {tramo: porcentaje}}, filtrado al seccionado 2025), generados por
  `scripts/aocd_tramos_renta.py`.

## 3. Cartografía de secciones censales — INE, "Cartografía digitalizada del seccionado"

**Directorio:** `ine_seccionado/`

- `seccionado_2025.zip` (60.298.555 bytes; `Last-Modified: Mon, 12 May 2025
  09:27:30 GMT`), URL exacta `https://www.ine.es/prodyser/cartografia/seccionado_2025.zip`.
  Extraído en `2025/Espaдa_Seccionado2025_ETRS89H30/` (el nombre de carpeta
  con "д" viene así en el zip): `SECC_CE_20250101.shp` + dbf/shx/prj/cpg/sbn/sbx.
  **36.554 secciones** (todas con CUSEC único), 8.132 CUMUN, 10.457 CUDIS,
  EPSG:25830 (ETRS89 / UTM 30N, también Canarias), 35.902 Polygon + 652
  MultiPolygon, 0 geometrías inválidas. Campos: `CUSEC, CUMUN, CSEC, CDIS, CMUN,
  CPRO, CCA, CUDIS, CLAU2, NPRO, NCA, CNUT0..CNUT3, NMUN`. Seccionado a 1-1-2025
  (en el nombre del fichero). **Es el usado por el pipeline** (misma fecha que
  la población y que el ADRH 2024).
- `seccionado_2026.zip` (65.414.784 bytes; `Last-Modified: Mon, 23 Mar 2026
  08:13:26 GMT`), misma URL con 2026: 36.669 secciones, 14 inválidas, 8.132
  CUMUN. Descargado para comparar; no se usa (su carpeta extraída se borró; se
  regenera con `unzip`). 36.521 CUSEC comunes con 2025; 148 nuevos; 33 de 2025
  desaparecen.
- También existen `seccionado_2024.zip` (65.690.243 bytes, 21-03-2024) y
  `seccionado_2023.zip` (64.929.708 bytes, 26-02-2024) con el mismo patrón de URL
  (comprobado con HEAD, no descargados).
- Página del producto: `https://www.ine.es/ss/Satellite?L=es_ES&c=Page&cid=1259952026632&p=1259952026632&pagename=ProductosYServicios%2FPYSLayout`.
  Licencia: el HTML de esa página enlaza `creativecommons.org/licenses/by/4.0/`
  con el título "Este sitio web y su contenido están bajo licencia CC BY-SA
  4.0" (texto contradictorio entre enlace y título; se cita tal cual) y rige el
  aviso legal del INE del punto 1. El `.shp.xml` de 2026 no contiene cláusula de
  licencia.

## 4. Comarcas

### 4a. Nacional — Comarcas Agrarias del MAPA (339 polígonos, actualización enero 2022)

**Directorio:** `mapa_comarcas_agrarias/`

- Servicio: ArcGIS REST `https://sig.mapa.gob.es/arcgis/rest/services/25830/comunComarcasAgrarias/MapServer`,
  capa 2 "Comarcas Agrarias" (campos `co_provinc, ds_provinc, co_comarca,
  ds_comarca`; `maxRecordCount` 1000; referencia 25830, origen 4258). Una sola
  consulta de las 339 geometrías devolvía `{"error":{"code":500,...}}` y
  `f=geojson` una página HTML de error, así que se descargó en páginas de 20:
  `esrijson_paginas/pagina_NNN.json` (18 ficheros), URL exacta de cada página
  `.../MapServer/2/query?where=1%3D1&outFields=co_provinc,ds_provinc,co_comarca,ds_comarca&returnGeometry=true&outSR=4258&f=json&resultOffset=NNN&resultRecordCount=20`.
  Total 339 features = 339 comarcas distintas (`co_comarca` de 4 dígitos =
  provincia + número), 53 "provincias": 50 + Ceuta (51) + Melilla (52) +
  "Territorios no asociados a ninguna provincia" (54).
- `comarcas_agrarias_mapa_epsg4258.geojson` (34.562.860 bytes): fusión de las
  páginas, anillos Esri convertidos a polígonos, coordenadas redondeadas a 6
  decimales. 0 geometrías inválidas.
- Página de descarga del MAPA: `https://www.mapa.gob.es/es/cartografia-y-sig/ide/descargas/agricultura/comarcas_agrarias`.
  Lo único descargable allí es `lyr-comarcas-agrarias.zip` (2.311 bytes, un
  `.lyr` de ArcGIS de 2014, sin datos: guardado como evidencia) y el PDF
  `https://sig.mapama.gob.es/Docs/PDFServicios/ComarcasAgrarias.pdf`
  (`ComarcasAgrarias.pdf`, 349.119 bytes): "Comarcalización Agraria del
  Ministerio de Agricultura, Pesca y Alimentación … Escala: Cartografía digital
  1:25.000. Fecha de Actualización: Enero 2022".
- Año de referencia: comarcalización agraria vigente (la de 1996 según la
  bibliografía `[inferido de resultados de búsqueda, no verificado en fuente
  primaria]`), geometría actualizada en enero de 2022.
- Licencia: el servicio no declara `copyrightText`; no se ha verificado el
  aviso legal del MAPA `[no verificado]`.
- No existe (o no se ha encontrado) una tabla oficial municipio → comarca
  agraria descargable; por eso `aocd_comarcas.py` asigna cada municipio por
  geometría (punto representativo dentro del polígono; 2 municipios por mayor
  área de solape). Resultado: 8.132 municipios asignados, 338 comarcas usadas.
- Nota TLS: `www.mapa.gob.es` presenta una cadena con la raíz "AC RAIZ FNMT-RCM
  SERVIDORES SEGUROS G2R", que el almacén local no contiene, por lo que `curl`
  falla con "self-signed certificate in certificate chain". La cadena se verificó
  a mano por la vía cruzada (hoja → "AC SERVIDORES SEGUROS TIPO2 G2R" → G2R
  firmada por "AC RAIZ FNMT-RCM", que sí está en el almacén): `openssl verify`
  devolvió `OK`; las descargas de `www.mapa.gob.es` se hicieron con
  `--pinnedpubkey sha256//kRvCLzT3Wy/zWulD3TTVi0lw0IPPU6B/6TjyhUWbxuc=`. El
  servicio `sig.mapa.gob.es` se descargó con `-k` `[cadena no verificada]`.

### 4b. Oficiales / autonómicas

- **Cataluña — IDESCAT** (`idescat_comarques/idescat_codis_municipis.csv`,
  33.916 bytes). URL exacta
  `https://www.idescat.cat/codis/?id=50&n=9&lang=es&f=csv` (HTTP 200,
  `text/csv`). 947 municipios con `Codi` (6 dígitos: los 5 primeros son el
  código INE, el sexto es de control), `Nom`, `Codi comarca` (2 dígitos), `Nom
  comarca`. Códigos territoriales vigentes de Idescat (comarcas oficiales).
  Licencia: no figura en el fichero `[no verificado]`.
- **Aragón — Aragón Open Data** (`aragon_opendata/informacion_general_municipios_aragon.csv`,
  167.076 bytes). URL exacta
  `https://opendata.aragon.es/GA_OD_Core/download?resource_id=11&formato=csv&name=municipios_aragon`,
  dataset CKAN `informacion-general-de-los-municipios-de-aragon` ("Información
  general de los municipios de Aragón"; licencia **Creative Commons Attribution
  4.0** según `package_show`; recurso `last_modified` 2014-06-18; metadatos
  modificados 2026-03-17). 731 filas = 731 municipios; columnas `codigo_mun`
  (código INE), `codigo_comarc`, `comarca`, etc. Las comarcas de Aragón no han
  cambiado desde su creación (2001–2003) `[supuesto]`.
- **Galicia — Xunta / IDEG** (`xunta_galicia_limites/`). Servicio ArcGIS REST
  `https://ideg.xunta.gal/servizos/rest/services/LimitesAdministrativos/LimitesAdministrativos/MapServer`
  ("Límites administrativos de Galicia actualizados … cos límites
  administrativos do IGN"). Capa 9 "Comarcas (Febreiro 2026)": 53 comarcas
  (`CODCOM, CODPROV, COMARCA`), fichero
  `comarcas_galicia_capa9_esrijson_epsg4258.json` (7.838.164 bytes); capa 12
  "Concellos (Febreiro 2026)": 313 concellos (`NATCODE, CODPROV, CODCONC` =
  código INE, `CONCELLO`), fichero `concellos_galicia_capa12_esrijson_epsg4258.json`
  (10.888.568 bytes). URL de consulta
  `.../MapServer/<capa>/query?where=1%3D1&outFields=...&returnGeometry=true&outSR=4258&f=json`.
  La capa de concellos no trae el código de comarca: se asigna por geometría
  (313/313 por punto representativo). Catálogo:
  `https://abertos.xunta.gal/catalogo/territorio-vivienda-transporte/-/dataset/0343/limites-administrativos-galicia`.
  Las 53 comarcas son las oficiales (Decreto 65/1997 `[de memoria, no
  verificado]`). Licencia: no aparece en la ficha de datos.gob.es
  (`a12002994-limites-administrativos-de-galicia1`) `[no verificado]`.
- **País Vasco — GeoEuskadi** (`geoeuskadi_limites/`). URLs exactas
  `https://www.geo.euskadi.eus/cartografia/DatosDescarga/Limites/MUNICIPIOS_5000_ETRS89.zip`
  (3.601.805 bytes; shapefile 259 features, campos `EUSTAT` = código INE,
  `COMARCA`, `COMARC_EUS`, `MUN_PROV`, `MUN_COMR`, …) y
  `.../COMARCAS_5000_ETRS89.zip` (1.459.734 bytes; 20 comarcas, `COM_PROV,
  COM_COM, COMARCA`). EPSG:25830. Página:
  `https://www.euskadi.eus/gobierno-vasco/-/limites-administrativos-del-pais-vasco/`
  ("Fecha de actualización 07/05/2025"; licencia: "Se permite cualquier uso si
  se menciona la autoría del siguiente modo: Eusko Jaurlaritza / Gobierno
  Vasco"). Son las comarcas estadísticas de Eustat (no entidades locales;
  en Álava las cuadrillas sí son entidades locales). 257 códigos INE distintos
  (251 municipios vascos + 6 enclaves de Burgos/Cantabria incluidos en el
  shapefile; en el CSV se les pone la CCAA de su código).
- **Resto (Wikidata, CC0)** (`wikidata/`). Dos consultas SPARQL a
  `https://query.wikidata.org/sparql` (texto exacto en `*.sparql`, fecha en
  `fecha_descarga_utc.txt` = 2026-10-19T12:15:48Z):
  `wikidata_municipio_P131_comarca.csv` (2.645 filas, 2.034 municipios cuya
  P131 "situado en" es un ítem de clase ⊂ comarca Q12829) y
  `wikidata_comarca_P150_municipio.csv` (2.914 filas, 2.836 municipios listados
  en P150 "contiene" de comarcas españolas). Unión: 3.334 municipios.
  Cobertura desigual: Comunidad Valenciana 542/542, Andalucía ~772/785, Navarra
  152, Baleares 60/67, Soria, Salamanca…; casi nula en Asturias, Cantabria,
  Castilla-La Mancha, Extremadura, Madrid, Murcia, Canarias, La Rioja. 46
  municipios con más de una comarca candidata (se elige la de tipo autonómico y
  se anota `n_candidatos_wikidata`). No oficial.

### 4c. Intentado y no conseguido

- **Navarra (IDENA / datosabiertos.navarra.es):** `idena.navarra.es` no
  respondió (timeout de conexión a los 60 s en `/descargas/` y en varias URL de
  shapefile). Manual: `https://idena.navarra.es/` → Descargas → límites
  administrativos / comarcas; o `https://datosabiertos.navarra.es/`. Mientras
  tanto Navarra solo tiene Wikidata ("comarca de Navarra", 152 municipios).
- **Eustat (lista oficial municipio→comarca):** no se encontró fichero; el PDF
  `https://www.eustat.eus/document/datos/cmtcomar_i.pdf` solo describe las 11
  cuencas de empleo. Se usó GeoEuskadi (4b).
- **Registro de Entidades Locales (REL, `ssweb.seap.minhap.es/REL/`):** HTTP
  403 con y sin User-Agent de navegador.
- **MAPA tabla municipio→comarca agraria:** no localizada (ver 4a).

## 5. Geometría municipal oficial — IGN/CNIG "Líneas límite" (opcional)

**Directorio:** `cnig_lineas_limite/`

- `lineas_limite_gml.zip` (66.245.318 bytes; `Last-Modified: Mon, 10 Aug 2026
  14:06:10 GMT`). URL exacta
  `https://centrodedescargas.cnig.es/CentroDescargas/documentos/atom/au/lineas_limite_gml.zip`,
  tomada del feed ATOM INSPIRE del IGN
  `https://www.ign.es/atom/dataset_feeds/lin_lim_mun.es.xml` ("Base de Datos de
  Límites Jurisdiccionales de España", `updated 2026-08-10T15:00:00Z`, GML
  ETRS89 lat/lon). Contiene 12 ficheros (AdministrativeBoundary 1º–4º orden y
  AdministrativeUnit 1º–4º orden; `readme.txt`). Extraídos solo `readme.txt` y
  `gml/au_AdministrativeUnit_4thOrder0.gml` (144.543.817 bytes): **8.220
  unidades** (EPSG:4258, MultiPolygon, 5 inválidas), campos INSPIRE
  (`nationalCode`, `text`, …). `nationalCode` = "34" + CCAA(2) + provincia(2) +
  **código INE de 5 dígitos** (p. ej. `34100303076` → 03076 Guardamar del
  Segura). 8.132 códigos coinciden con los municipios del seccionado 2025
  (todos); además 81 unidades `53xxx` (territorios sin municipio: facerías,
  mancomunidades, Bardenas…) y 7 `54xxx` (Isla de Perejil, Peñón de Vélez,
  Chafarinas, Alhucemas, Islas Alhucemas, Gibraltar, Isla de los Faisanes), que
  los scripts excluyen.
- El shapefile `LINEAS_LIMITE.ZIP` (156,96 MB, 28/07/2026, ETRS89/REGCAN95
  geográficas, `detalleArchivo?sec=9000029`) **no se pudo descargar**: el
  formulario `POST /CentroDescargas/descargaDir` devuelve `HTTP 403` con
  cabecera `X-Action: Block-Bot`. Descarga manual:
  `https://centrodedescargas.cnig.es/CentroDescargas/limites-municipales-provinciales-autonomicos`
  → "Límites y Unidades Administrativas Actuales" → LINEAS_LIMITE.ZIP (también
  GeoPackage 2023 y 2024 históricos). El `index.jsp` del centro de descargas
  solo responde con User-Agent de navegador (sin él: "Empty reply from server").
- Licencia (texto de la ficha): "El uso de la información de los productos y
  servicios de datos geográficos definidos en la Orden FOM/2807/2015 … conlleva
  la aceptación por el usuario de las condiciones generales de dicha orden,
  concretada en una licencia de uso …" (equivalente a CC BY 4.0 según el IGN
  `[inferido, no leído en la ficha]`).
- Derivado: `../municipios_cnig_2026.part1..3.geojson` (8.132 municipios,
  EPSG:4326, 7 decimales, 47,5 + 47,5 + 1,7 MB; generado por
  `scripts/aocd_municipios_cnig.py`). Cómo regenerar la adyacencia municipal con
  él: ver `../SPLIT-NOTE.md`.

---

## Resumen de recuentos y cruces de códigos

| Dato | Unidad | Año | Registros | Fichero bruto |
|---|---|---|---|---|
| Población | sección | 1-1-2025 | 36.554 (de 36.892 códigos en la tabla) | `ine_censo_anual_secciones/*.csv.gz` |
| Renta neta media por persona/hogar | sección / distrito / municipio | 2024 | 36.457 / 10.377 / 8.052 | `ine_adrh/px_jaxiT3_2026-10-19/30824.px` |
| Ídem (respaldo) | ídem | 2023 | 36.394 / 10.387 / 8.059 | `ine_adrh/px_renta/30824.px` |
| Distribución renta/unidad de consumo (% bajo 5.000/7.500/10.000 €) | sección | 2024 | 34.852 (de 36.554) | `ine_adrh_tramos/30826_umbrales_fijos_sexo_nacional.px` |
| Polígonos de sección | sección | 1-1-2025 | 36.554 | `ine_seccionado/2025/...shp` |
| Comarcas agrarias | comarca | geometría ene-2022 | 339 | `mapa_comarcas_agrarias/` |
| Comarcas Cataluña / Aragón / Galicia / Euskadi | municipio | vigentes | 947 / 731 / 313 / 257 | ver 4b |
| Wikidata | municipio | 19-10-2026 | 3.334 | `wikidata/` |
| Municipios IGN | municipio | 10-08-2026 | 8.132 (+88 no municipales) | `cnig_lineas_limite/` |

Cruce (calculado por `scripts/aocd_preparar_secciones.py`): seccionado 2025 ∩
Censo 2025 = 36.554/36.554; seccionado 2025 ∩ ADRH 2024 = 36.457/36.554 (97 sin
renta directa: 17 rellenadas con el distrito municipal, 80 con la media
provincial ponderada por población de las secciones con dato; ninguna necesitó
el nivel municipio porque el ADRH suprime municipios enteros). Lista en
`../secciones_renta_imputada_2024.csv`. Con ADRH 2023: 36.314 directas, 167
distrito, 73 provincia.

Cambios de códigos de sección entre años: las tablas del INE (Censo y ADRH)
mantienen un universo acumulado de códigos (36.892 y 37.229) con celdas vacías
en los años en que la sección no existe; hay que filtrar por el seccionado del
año. Entre 2025 y 2026 cambian 148 + 33 secciones. Los municipios son los
mismos 8.132 en el seccionado 2025, 2026, el Censo 2025 y el CNIG 2026; el
ADRH lista 8.139 (7 municipios históricos sin dato reciente).

Secciones sin vecinos por geometría (huecos reales en el shapefile del INE):
Hacinas 0915401001 (hueco de 621 m hasta Salas de los Infantes), Monasterio de
la Sierra 0922301001 (758 m), Llívia 1709401001 (enclave, 1.641 m hasta
Puigcerdà), Teguise 3502401010 (La Graciosa, 1.066 m hasta Haría). Una sección
con población 0: Yaiza 3503401004.
