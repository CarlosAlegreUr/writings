#!/usr/bin/env python3
"""
AOCD — Preparación de datos por SECCIÓN CENSAL.

Cruza:
  - Cartografía de secciones censales INE a 1-1-2025
        data/raw/ine_seccionado/2025/*/SECC_CE_20250101.shp   (36.554 secciones)
  - Población a 1-1-2025 por sección (Censo anual de población, tabla INE 65032)
        data/raw/ine_censo_anual_secciones/censo_anual_65032_...csv.gz
  - Renta neta media por persona 2024 (Atlas de Distribución de Renta de los
    Hogares, edición publicada el 15-10-2026; tabla nacional 30824 exportada
    de jaxiT3 en PC-Axis el 19-10-2026)
        data/raw/ine_adrh/px_jaxiT3_2026-10-19/30824.px
    (alternativa: --anyo-renta 2023 --px-renta data/raw/ine_adrh/px_renta/30824.px,
     que es la misma tabla de la publicación completa ADRH 2023 de octubre-2025)
  - Comarca por municipio: data/municipio_comarca.csv (generado por aocd_comarcas.py)

Produce data/secciones_unificadas.json con el mismo esquema que
v1/data/municipios_unificados.json (el de la v1 municipal):
    {cusec: {nombre, poblacion, renta_media, provincia, lat, lon, vecinos,
             municipio, distrito_municipal, comarca, cusec}}
y además los CSV intermedios data/poblacion_secciones_2025.csv,
data/renta_adrh_<año>_secciones_distritos_municipios.csv y
data/secciones_renta_imputada_<año>.csv (secciones cuya renta no viene de la
propia sección y de dónde se ha rellenado).

`vecinos` se calcula por adyacencia real de polígonos con índice espacial
(igual que v1/scripts/aocd_preparar_datos.py). Las secciones sin renta en el ADRH reciben
la renta del distrito municipal; si tampoco hay, la del municipio; si tampoco,
la media provincial ponderada; el script informa de cuántas hay en cada caso.

Ejecutar desde la raíz de aocd/:
    python3 -I scripts/aocd_preparar_secciones.py [--raiz RUTA_AOCD]
"""

import argparse
import csv
import glob
import gzip
import json
import os
import site
import sys
import time
import zipfile
from collections import Counter, defaultdict

# `python3 -I` desactiva el site-packages del usuario (donde está geopandas):
# se vuelve a añadir solo esa ruta, nunca el cwd ni el directorio del script.
sys.path.append(site.getusersitepackages())
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # para aocd_px
sys.dont_write_bytecode = True  # no crear scripts/__pycache__

import geopandas as gpd  # noqa: E402

from aocd_px import iterar_datos, leer_px  # noqa: E402

ANYO_POBLACION = '2025'
ANYO_RENTA = '2024'   # se puede cambiar con --anyo-renta
PX_RENTA_DEFECTO = os.path.join('data', 'raw', 'ine_adrh', 'px_jaxiT3_2026-10-19', '30824.px')
INDICADOR_RENTA = 'Renta neta media por persona'
INDICADOR_RENTA_HOGAR = 'Renta neta media por hogar'


def log(msg):
    print(f'[AOCD-SECC] {msg}', flush=True)


# ---------------------------------------------------------------- cartografía
def cargar_seccionado(raiz):
    patron = os.path.join(raiz, 'data', 'raw', 'ine_seccionado', '2025', '*', 'SECC_CE_20250101.shp')
    rutas = glob.glob(patron)
    if not rutas:
        # La carpeta extraída está en .gitignore (>50 MB): se regenera desde el zip descargado.
        zip_ruta = os.path.join(raiz, 'data', 'raw', 'ine_seccionado', 'seccionado_2025.zip')
        if not os.path.exists(zip_ruta):
            raise SystemExit(f'No se encuentra el seccionado: ni {patron} ni {zip_ruta} '
                             '(descarga: https://www.ine.es/prodyser/cartografia/seccionado_2025.zip)')
        log(f'Extrayendo {zip_ruta} ...')
        with zipfile.ZipFile(zip_ruta) as z:
            z.extractall(os.path.join(raiz, 'data', 'raw', 'ine_seccionado', '2025'))
        rutas = glob.glob(patron)
        if not rutas:
            raise SystemExit(f'El zip no contiene {patron}')
    log(f'Cargando seccionado {rutas[0]}')
    g = gpd.read_file(rutas[0], engine='pyogrio')
    log(f'  secciones: {len(g)}  CRS: {g.crs.to_epsg()}  inválidas: {int((~g.is_valid).sum())}')
    if (~g.is_valid).any():
        g['geometry'] = g.geometry.make_valid()
    g = g.drop_duplicates(subset='CUSEC').reset_index(drop=True)
    return g


def calcular_adyacencia(gdf):
    """Vecinos por contacto real de polígonos, con índice espacial (STRtree)."""
    log('Calculando adyacencia de secciones...')
    t0 = time.time()
    codigos = gdf['CUSEC'].tolist()
    sindex = gdf.sindex
    # Un solo query vectorizado: pares (i, j) cuyas geometrías se tocan o intersecan.
    izq, der = sindex.query(gdf.geometry, predicate='intersects')
    ady = defaultdict(set)
    for i, j in zip(izq, der):
        if i != j:
            ady[codigos[i]].add(codigos[j])
            ady[codigos[j]].add(codigos[i])
    n_con = sum(1 for c in codigos if ady.get(c))
    grados = [len(ady.get(c, ())) for c in codigos]
    log(f'  adyacencia en {time.time()-t0:.0f}s; con vecinos: {n_con}/{len(codigos)}; '
        f'grado min={min(grados)} media={sum(grados)/len(grados):.1f} max={max(grados)}')
    return {c: sorted(v) for c, v in ady.items()}


# ---------------------------------------------------------------- población
def cargar_poblacion_censo(raiz):
    ruta = os.path.join(raiz, 'data', 'raw', 'ine_censo_anual_secciones',
                        'censo_anual_65032_poblacion_sexo_nacionalidad_secciones.csv')
    if not os.path.exists(ruta) and os.path.exists(ruta + '.gz'):
        ruta = ruta + '.gz'   # en data/raw se guarda comprimido (el CSV plano pesa 210 MB)
    log(f'Cargando población (Censo anual, tabla 65032) desde {ruta}')
    pob_secc, pob_mun, nombres_mun = {}, {}, {}
    abrir = gzip.open if ruta.endswith('.gz') else open
    with abrir(ruta, 'rt', encoding='latin-1', newline='') as f:
        r = csv.reader(f, delimiter=';')
        next(r)
        for row in r:
            if row[4] != 'Total' or row[5] != 'Total' or row[6] != ANYO_POBLACION:
                continue
            valor = row[7].strip()
            if valor in ('', '..', '.'):
                continue
            n = int(valor.replace('.', ''))
            if row[3]:
                pob_secc[row[3].split(' ')[0]] = n
            elif row[2]:
                cod, _, nombre = row[2].partition(' ')
                pob_mun[cod] = n
                nombres_mun[cod] = nombre
    log(f'  secciones con población {ANYO_POBLACION}: {len(pob_secc)}; municipios: {len(pob_mun)}; '
        f'total secciones: {sum(pob_secc.values()):,}')
    return pob_secc, pob_mun, nombres_mun


# ---------------------------------------------------------------- renta
def cargar_renta_adrh(raiz, ruta_px=None):
    ruta = ruta_px or os.path.join(raiz, PX_RENTA_DEFECTO)
    log(f'Cargando renta ADRH {ANYO_RENTA} desde {ruta}')
    px = leer_px(ruta)
    stub = px['stub'][0]
    ind_var = px['heading'][0]
    nombres = dict(zip(px['codes'][stub], px['values'][stub]))
    renta = {}          # codigo (5, 7 o 10 dígitos) -> {indicador: valor}
    for (unidad, indicador, periodo), valor in iterar_datos(px):
        if periodo != ANYO_RENTA or indicador not in (INDICADOR_RENTA, INDICADOR_RENTA_HOGAR):
            continue
        codigo = unidad.split(' ')[0]
        renta.setdefault(codigo, {})[indicador] = valor
    n = Counter(len(c) for c in renta)
    con = Counter(len(c) for c, v in renta.items() if v.get(INDICADOR_RENTA) is not None)
    log(f'  unidades en la tabla: secciones={n[10]} distritos={n[7]} municipios={n[5]}; '
        f'con "{INDICADOR_RENTA}" {ANYO_RENTA}: secciones={con[10]} distritos={con[7]} municipios={con[5]}')
    return renta, nombres, ind_var


# ---------------------------------------------------------------- comarcas
def cargar_comarcas(raiz):
    ruta = os.path.join(raiz, 'data', 'municipio_comarca.csv')
    if not os.path.exists(ruta):
        log(f'  AVISO: no existe {ruta}; comarca=null en todas las secciones (ejecuta aocd_comarcas.py)')
        return {}
    com = {}
    with open(ruta, 'r', encoding='utf-8', newline='') as f:
        for row in csv.DictReader(f):
            if row['comarca_id']:
                com[row['codigo_ine']] = row['comarca_id']
    log(f'  municipios con comarca: {len(com)}')
    return com


# ---------------------------------------------------------------- cruce
def cruzar(gdf, adyacencia, pob_secc, pob_mun, nombres_mun, renta, comarcas):
    log('Cruzando población + renta + geometría por sección...')
    # centroides en lat/lon
    cent = gdf.geometry.representative_point().to_crs(epsg=4326)
    lat = dict(zip(gdf['CUSEC'], cent.y))
    lon = dict(zip(gdf['CUSEC'], cent.x))

    # media provincial ponderada (secciones con renta directa) como último recurso
    prov_num, prov_den = defaultdict(float), defaultdict(float)
    for cusec, p in pob_secc.items():
        v = renta.get(cusec, {}).get(INDICADOR_RENTA)
        if v is not None:
            prov_num[cusec[:2]] += v * p
            prov_den[cusec[:2]] += p
    prov_media = {k: prov_num[k] / prov_den[k] for k in prov_num if prov_den[k] > 0}

    resultado = {}
    origen = Counter()
    sin_pob = []
    imputadas = []   # (cusec, origen del relleno, valor)
    for _, row in gdf.iterrows():
        cusec = row['CUSEC']
        cumun, cudis = row['CUMUN'], row['CUDIS']
        pob = pob_secc.get(cusec)
        if pob is None:
            sin_pob.append(cusec)
            pob = 0
        r = renta.get(cusec, {}).get(INDICADOR_RENTA)
        if r is not None:
            fuente = 'seccion'
        else:
            r = renta.get(cudis, {}).get(INDICADOR_RENTA)
            if r is not None:
                fuente = 'distrito'
            else:
                r = renta.get(cumun, {}).get(INDICADOR_RENTA)
                if r is not None:
                    fuente = 'municipio'
                elif cusec[:2] in prov_media:
                    r = prov_media[cusec[:2]]
                    fuente = 'provincia'
                else:
                    r = None
                    fuente = 'sin_renta'
        origen[fuente] += 1
        vecinos = adyacencia.get(cusec, [])
        resultado[cusec] = {
            'nombre': f'{row["NMUN"]} sección {row["CDIS"]}{row["CSEC"]}',
            'poblacion': pob,
            'renta_media': round(r, 2) if r is not None else None,
            'provincia': row['CPRO'],
            'lat': round(float(lat[cusec]), 6),
            'lon': round(float(lon[cusec]), 6),
            'vecinos': vecinos,
            'municipio': cumun,
            'distrito_municipal': cudis,
            'comarca': comarcas.get(cumun),
            'cusec': cusec,
        }
        if fuente != 'seccion':
            imputadas.append((cusec, fuente, r))
    log('\n  === RESUMEN CRUCE ===')
    log(f'  secciones finales: {len(resultado)}')
    log(f'  población total: {sum(s["poblacion"] for s in resultado.values()):,}')
    log(f'  secciones sin población en el censo: {len(sin_pob)} {sin_pob[:10]}')
    log(f'  renta por origen: {dict(origen)}')
    sin_vec = [c for c, s in resultado.items() if not s['vecinos']]
    log(f'  secciones sin vecinos: {len(sin_vec)}')
    for c in sin_vec[:15]:
        log(f'    - {c}: {resultado[c]["nombre"]} ({resultado[c]["poblacion"]:,} hab)')
    sin_com = sum(1 for s in resultado.values() if s['comarca'] is None)
    log(f'  secciones sin comarca: {sin_com}')
    # municipios: cuadre de población sección vs municipio
    agg = defaultdict(int)
    for s in resultado.values():
        agg[s['municipio']] += s['poblacion']
    desc = [m for m, p in pob_mun.items() if agg.get(m, 0) != p]
    log(f'  municipios cuya suma de secciones != población municipal del censo: {len(desc)} {desc[:10]}')
    return resultado, imputadas


def exportar_csv_intermedios(raiz, pob_secc, renta, nombres):
    ruta = os.path.join(raiz, 'data', f'poblacion_secciones_{ANYO_POBLACION}.csv')
    with open(ruta, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['cusec', 'poblacion'])
        for c in sorted(pob_secc):
            w.writerow([c, pob_secc[c]])
    log(f'  escrito {ruta} ({len(pob_secc)} filas)')
    ruta = os.path.join(raiz, 'data', f'renta_adrh_{ANYO_RENTA}_secciones_distritos_municipios.csv')
    n = 0
    with open(ruta, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['codigo', 'nivel', 'nombre', 'renta_neta_media_persona', 'renta_neta_media_hogar'])
        for c in sorted(renta):
            v = renta[c]
            if v.get(INDICADOR_RENTA) is None and v.get(INDICADOR_RENTA_HOGAR) is None:
                continue
            nivel = {5: 'municipio', 7: 'distrito', 10: 'seccion'}.get(len(c), '?')
            w.writerow([c, nivel, nombres.get(c, ''), v.get(INDICADOR_RENTA), v.get(INDICADOR_RENTA_HOGAR)])
            n += 1
    log(f'  escrito {ruta} ({n} filas con dato)')


def main():
    global ANYO_RENTA
    ap = argparse.ArgumentParser()
    ap.add_argument('--raiz', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument('--salida', default=None, help='JSON de salida (por defecto data/secciones_unificadas.json)')
    ap.add_argument('--anyo-renta', default=None, help=f'periodo ADRH a usar (por defecto {ANYO_RENTA})')
    ap.add_argument('--px-renta', default=None, help=f'fichero PC-Axis de la tabla 30824 (por defecto {PX_RENTA_DEFECTO})')
    args = ap.parse_args()
    raiz = args.raiz
    if args.anyo_renta:
        ANYO_RENTA = args.anyo_renta
    salida = args.salida or os.path.join(raiz, 'data', 'secciones_unificadas.json')
    t0 = time.time()
    log('=== PREPARACIÓN DE DATOS AOCD POR SECCIÓN CENSAL ===')

    gdf = cargar_seccionado(raiz)
    pob_secc, pob_mun, nombres_mun = cargar_poblacion_censo(raiz)
    renta, nombres_renta, _ = cargar_renta_adrh(raiz, args.px_renta)
    comarcas = cargar_comarcas(raiz)
    adyacencia = calcular_adyacencia(gdf)

    # diagnóstico de códigos
    cusec = set(gdf['CUSEC'])
    log(f'  códigos: seccionado={len(cusec)} | censo {ANYO_POBLACION}={len(pob_secc)} '
        f'(∩={len(cusec & set(pob_secc))}) | ADRH {ANYO_RENTA} secciones con renta='
        f'{sum(1 for c, v in renta.items() if len(c) == 10 and v.get(INDICADOR_RENTA) is not None)} '
        f'(∩ seccionado={sum(1 for c in cusec if renta.get(c, {}).get(INDICADOR_RENTA) is not None)})')

    resultado, imputadas = cruzar(gdf, adyacencia, pob_secc, pob_mun, nombres_mun, renta, comarcas)
    exportar_csv_intermedios(raiz, pob_secc, renta, nombres_renta)
    ruta_imp = os.path.join(raiz, 'data', f'secciones_renta_imputada_{ANYO_RENTA}.csv')
    with open(ruta_imp, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['cusec', 'relleno', 'renta_media_asignada'])
        for cusec, fuente, r in imputadas:
            w.writerow([cusec, fuente, round(r, 2) if r is not None else ''])
    log(f'  escrito {ruta_imp} ({len(imputadas)} secciones con renta imputada)')

    log(f'Exportando {salida}...')
    with open(salida, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=1)
    log(f'  tamaño: {os.path.getsize(salida):,} bytes')
    log(f'=== COMPLETADO en {time.time()-t0:.0f}s ===')


if __name__ == '__main__':
    main()
