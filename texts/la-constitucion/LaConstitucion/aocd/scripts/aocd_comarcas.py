#!/usr/bin/env python3
"""
AOCD — Asignación municipio (código INE de 5 dígitos) -> comarca.

Produce dos ficheros en data/:

  municipio_comarca.csv              (cobertura NACIONAL)
      codigo_ine,comarca_id,comarca_nombre,fuente
      Fuente: Comarcas Agrarias del MAPA (339 polígonos, servicio ArcGIS REST
      25830/comunComarcasAgrarias, descargado en data/raw/mapa_comarcas_agrarias/).
      La asignación es ESPACIAL: punto representativo del municipio (geometría
      CNIG "Líneas límite", data/raw/cnig_lineas_limite/) dentro del polígono
      de la comarca; si no cae en ninguno, comarca con mayor área de solape.
      comarca_id = "MAPA-" + co_comarca (4 dígitos: provincia + nº comarca).

  municipio_comarca_autonomicas.csv  (comarcas OFICIALES o de uso autonómico)
      codigo_ine,ccaa,comarca_id,comarca_nombre,fuente,oficial
      Cataluña  -> IDESCAT (oficial)             data/raw/idescat_comarques/
      Aragón    -> Aragón Open Data (oficial)    data/raw/aragon_opendata/
      Galicia   -> Xunta/IDEG REST, espacial (oficial) data/raw/xunta_galicia_limites/
      Euskadi   -> GeoEuskadi (atributo COMARCA; comarcas Eustat, no entidad local)
      Resto     -> Wikidata (P131 ∪ P150), no oficial, con posibles ambigüedades.

Ejecutar desde la raíz de aocd/:
    python3 -I scripts/aocd_comarcas.py [--raiz RUTA_AOCD]
"""

import argparse
import csv
import glob
import json
import os
import site
import sys
import time
from collections import Counter, defaultdict

# `python3 -I` desactiva el site-packages del usuario, donde está geopandas.
# Se vuelve a añadir SOLO esa ruta (no el cwd ni el directorio del script).
sys.path.append(site.getusersitepackages())

import geopandas as gpd  # noqa: E402
import shapely  # noqa: E402
from shapely.geometry import MultiPolygon, Polygon  # noqa: E402

CCAA_POR_PROV = {
    '01': '16', '20': '16', '48': '16',            # País Vasco
    '02': '08', '13': '08', '16': '08', '19': '08', '45': '08',  # C-LM
    '03': '10', '12': '10', '46': '10',            # C. Valenciana
    '04': '01', '11': '01', '14': '01', '18': '01', '21': '01', '23': '01', '29': '01', '41': '01',  # Andalucía
    '05': '07', '09': '07', '24': '07', '34': '07', '37': '07', '40': '07', '42': '07', '47': '07', '49': '07',  # CyL
    '06': '11', '10': '11',                        # Extremadura
    '07': '04',                                    # Baleares
    '08': '09', '17': '09', '25': '09', '43': '09',  # Cataluña
    '15': '12', '27': '12', '32': '12', '36': '12',  # Galicia
    '22': '02', '44': '02', '50': '02',            # Aragón
    '26': '17',                                    # La Rioja
    '28': '13',                                    # Madrid
    '30': '14',                                    # Murcia
    '31': '15',                                    # Navarra
    '33': '03',                                    # Asturias
    '35': '05', '38': '05',                        # Canarias
    '39': '06',                                    # Cantabria
    '51': '18', '52': '19',                        # Ceuta, Melilla
}


def log(msg):
    print(f'[AOCD-COMARCAS] {msg}', flush=True)


# ---------------------------------------------------------------- Esri JSON
def esri_a_geometria(g):
    """Convierte {'rings': [...]} de ArcGIS REST a Polygon/MultiPolygon.
    Convención Esri: anillos exteriores en sentido horario, huecos antihorario."""
    anillos = [Polygon(r) for r in g.get('rings', []) if len(r) >= 4]
    exteriores, huecos = [], []
    for a in anillos:
        (huecos if a.exterior.is_ccw else exteriores).append(a)
    polys = []
    for e in exteriores:
        hs = [h for h in huecos if e.contains(h.representative_point())]
        polys.append(Polygon(e.exterior.coords, [h.exterior.coords for h in hs]))
    if not polys:
        return None
    geom = MultiPolygon(polys) if len(polys) > 1 else polys[0]
    if not geom.is_valid:
        geom = shapely.make_valid(geom)
    return geom


def cargar_esrijson(rutas, campos):
    filas = []
    for ruta in rutas:
        with open(ruta, 'r', encoding='utf-8') as f:
            d = json.load(f)
        if 'error' in d:
            raise RuntimeError(f'{ruta}: {d["error"]}')
        for x in d.get('features', []):
            a = x['attributes']
            filas.append({**{c: a.get(c) for c in campos}, 'geometry': esri_a_geometria(x['geometry'])})
    return gpd.GeoDataFrame(filas, geometry='geometry', crs='EPSG:4258')


# ---------------------------------------------------------------- asignación espacial
def asignar_espacial(municipios, zonas, campo_id, etiqueta):
    """Para cada municipio devuelve el id de zona: punto representativo dentro
    de la zona; si no, zona con mayor área de intersección; si no, None."""
    t0 = time.time()
    zonas = zonas.to_crs(municipios.crs)
    sindex = zonas.sindex
    puntos = municipios.geometry.representative_point()
    resultado, metodo = {}, Counter()
    for i, (codigo, geom) in enumerate(zip(municipios['codigo'], municipios.geometry)):
        p = puntos.iloc[i]
        cand = list(sindex.query(p, predicate='within'))
        if len(cand) == 1:
            resultado[codigo] = zonas.iloc[cand[0]][campo_id]
            metodo['punto'] += 1
            continue
        cand = list(sindex.query(geom, predicate='intersects'))
        mejor, mejor_area = None, 0.0
        for j in cand:
            try:
                a = geom.intersection(zonas.geometry.iloc[j]).area
            except Exception:
                a = shapely.make_valid(geom).intersection(shapely.make_valid(zonas.geometry.iloc[j])).area
            if a > mejor_area:
                mejor, mejor_area = zonas.iloc[j][campo_id], a
        if mejor is not None and mejor_area > 0:
            resultado[codigo] = mejor
            metodo['area'] += 1
        else:
            resultado[codigo] = None
            metodo['sin_zona'] += 1
    log(f'  {etiqueta}: {len(resultado)} municipios en {time.time()-t0:.0f}s; método {dict(metodo)}')
    return resultado


# ---------------------------------------------------------------- fuentes
def cargar_municipios_cnig(raiz):
    ruta = os.path.join(raiz, 'data', 'raw', 'cnig_lineas_limite', 'gml', 'au_AdministrativeUnit_4thOrder0.gml')
    log(f'Cargando geometría municipal CNIG: {ruta}')
    g = gpd.read_file(ruta, engine='pyogrio', columns=['nationalCode', 'text'])
    g['codigo'] = g['nationalCode'].astype(str).str[-5:]
    # 53xxx = territorios sin municipio (facerías, mancomunidades...); 54xxx = plazas de soberanía, Gibraltar, Isla de los Faisanes
    g = g[~g['codigo'].str.startswith(('53', '54'))].copy()
    g['geometry'] = g.geometry.make_valid()
    log(f'  municipios CNIG (sin 53xxx/54xxx): {len(g)}')
    return g[['codigo', 'text', 'geometry']].reset_index(drop=True)


def comarcas_mapa(raiz, municipios):
    rutas = sorted(glob.glob(os.path.join(raiz, 'data', 'raw', 'mapa_comarcas_agrarias', 'esrijson_paginas', '*.json')))
    log(f'Comarcas agrarias MAPA: {len(rutas)} páginas Esri JSON')
    z = cargar_esrijson(rutas, ['co_provinc', 'ds_provinc', 'co_comarca', 'ds_comarca'])
    z = z[~z.geometry.isna()].copy()
    z['id'] = z['co_comarca'].astype(int).map(lambda v: f'{v:04d}')
    nombres = dict(zip(z['id'], z['ds_comarca']))
    log(f'  polígonos: {len(z)}; comarcas distintas: {z["id"].nunique()}')
    asig = asignar_espacial(municipios, z, 'id', 'MAPA comarcas agrarias')
    return asig, nombres


def comarcas_idescat(raiz):
    ruta = os.path.join(raiz, 'data', 'raw', 'idescat_comarques', 'idescat_codis_municipis.csv')
    filas = {}
    with open(ruta, 'r', encoding='utf-8-sig') as f:
        lineas = [l for l in f.read().splitlines()]
    # Las 3 primeras líneas son título/fuente/URL; la 4ª es la cabecera.
    inicio = next(i for i, l in enumerate(lineas) if l.startswith('Codi,'))
    for row in csv.DictReader(lineas[inicio:]):
        codi = (row.get('Codi') or '').strip()
        if len(codi) != 6 or not codi.isdigit():
            continue
        filas[codi[:5]] = (f'CAT-{row["Codi comarca"].strip()}', row['Nom comarca'].strip())
    log(f'  IDESCAT: {len(filas)} municipios')
    return filas


def comarcas_aragon(raiz):
    ruta = os.path.join(raiz, 'data', 'raw', 'aragon_opendata', 'informacion_general_municipios_aragon.csv')
    filas = {}
    with open(ruta, 'r', encoding='utf-8', newline='') as f:
        for row in csv.DictReader(f):
            cod = row['codigo_mun'].strip().zfill(5)
            filas[cod] = (f'ARA-{row["codigo_comarc"].strip().zfill(2)}', row['comarca'].strip())
    log(f'  Aragón Open Data: {len(filas)} municipios')
    return filas


def comarcas_galicia(raiz):
    base = os.path.join(raiz, 'data', 'raw', 'xunta_galicia_limites')
    com = cargar_esrijson([os.path.join(base, 'comarcas_galicia_capa9_esrijson_epsg4258.json')],
                          ['CODCOM', 'CODPROV', 'COMARCA'])
    con = cargar_esrijson([os.path.join(base, 'concellos_galicia_capa12_esrijson_epsg4258.json')],
                          ['CODCONC', 'CONCELLO'])
    com['id'] = [f'GAL-{int(p):02d}{int(c):02d}' for p, c in zip(com['CODPROV'], com['CODCOM'])]
    nombres = dict(zip(com['id'], com['COMARCA']))
    con['codigo'] = con['CODCONC'].astype(int).map(lambda v: f'{v:05d}')
    asig = asignar_espacial(con, com, 'id', 'Galicia (Xunta)')
    return {k: (v, nombres.get(v)) for k, v in asig.items() if v}


def comarcas_euskadi(raiz):
    ruta = glob.glob(os.path.join(raiz, 'data', 'raw', 'geoeuskadi_limites', 'MUNICIPIOS_5000_ETRS89', '*.shp'))[0]
    g = gpd.read_file(ruta, engine='pyogrio')
    filas = {}
    for _, r in g.iterrows():
        cod = str(r['EUSTAT']).zfill(5)
        if cod in filas:
            continue
        filas[cod] = (f'EUS-{str(r["MUN_PROV"]).zfill(2)}{str(r["MUN_COMR"]).zfill(2)}', str(r['COMARCA']).strip())
    log(f'  GeoEuskadi: {len(filas)} municipios')
    return filas


def comarcas_wikidata(raiz):
    base = os.path.join(raiz, 'data', 'raw', 'wikidata')
    cand = defaultdict(dict)   # ine -> {qid: (nombre, tipo)}
    for nombre in ['wikidata_municipio_P131_comarca.csv', 'wikidata_comarca_P150_municipio.csv']:
        with open(os.path.join(base, nombre), 'r', encoding='utf-8', newline='') as f:
            for row in csv.DictReader(f):
                ine = row['ine'].strip().zfill(5)
                if len(ine) != 5 or not ine.isdigit():
                    continue
                qid = row['com'].rsplit('/', 1)[-1]
                cand[ine][qid] = (row['comLabel'], row['typeLabel'])
    log(f'  Wikidata: {len(cand)} municipios con alguna comarca')
    return cand


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--raiz', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    args = ap.parse_args()
    raiz = args.raiz
    t0 = time.time()

    municipios = cargar_municipios_cnig(raiz)
    codigos = sorted(municipios['codigo'])

    # ---- nacional: MAPA comarcas agrarias
    asig_mapa, nombres_mapa = comarcas_mapa(raiz, municipios)
    salida = os.path.join(raiz, 'data', 'municipio_comarca.csv')
    sin = 0
    with open(salida, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['codigo_ine', 'comarca_id', 'comarca_nombre', 'fuente'])
        for c in codigos:
            cid = asig_mapa.get(c)
            if cid is None:
                sin += 1
                w.writerow([c, '', '', 'MAPA comarcas agrarias (sin asignación espacial)'])
            else:
                w.writerow([c, f'MAPA-{cid}', nombres_mapa.get(cid, ''), 'MAPA comarcas agrarias (ArcGIS REST, ene-2022), asignación espacial sobre CNIG'])
    log(f'Escrito {salida}: {len(codigos)} municipios, {sin} sin comarca, '
        f'{len(set(v for v in asig_mapa.values() if v))} comarcas usadas')

    # ---- autonómicas
    oficiales = {}   # ine -> (ccaa, id, nombre, fuente, oficial)
    for c, (cid, nom) in comarcas_idescat(raiz).items():
        oficiales[c] = ('09', cid, nom, 'IDESCAT codis territorials (municipis->comarca)', 'si')
    for c, (cid, nom) in comarcas_aragon(raiz).items():
        oficiales[c] = ('02', cid, nom, 'Aragón Open Data: Información general de los municipios de Aragón', 'si')
    for c, (cid, nom) in comarcas_galicia(raiz).items():
        oficiales[c] = ('12', cid, nom, 'Xunta/IDEG LimitesAdministrativos (capas Comarcas/Concellos feb-2026), espacial', 'si')
    for c, (cid, nom) in comarcas_euskadi(raiz).items():
        oficiales[c] = ('16', cid, nom, 'GeoEuskadi MUNICIPIOS_5000_ETRS89 (atributo COMARCA, comarcas Eustat)', 'no (estadística Eustat)')

    wd = comarcas_wikidata(raiz)
    salida2 = os.path.join(raiz, 'data', 'municipio_comarca_autonomicas.csv')
    n_of, n_wd, n_amb, n_sin = 0, 0, 0, 0
    por_ccaa = Counter()
    with open(salida2, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['codigo_ine', 'ccaa', 'comarca_id', 'comarca_nombre', 'fuente', 'oficial', 'n_candidatos_wikidata'])
        for c in codigos:
            ccaa = CCAA_POR_PROV.get(c[:2], '')
            if c in oficiales:
                cc, cid, nom, fu, of = oficiales[c]
                # ccaa del municipio por su código INE (GeoEuskadi incluye enclaves de Burgos/Cantabria)
                w.writerow([c, ccaa, cid, nom, fu, of, ''])
                n_of += 1
                por_ccaa[ccaa] += 1
            elif c in wd:
                cands = wd[c]
                # preferir tipos específicos de la comunidad frente a genéricos
                def rango(item):
                    tipo = item[1][1].lower()
                    return (0 if tipo not in ('comarca', 'comarca de españa') else 1, item[1][0])
                qid, (nom, tipo) = sorted(cands.items(), key=rango)[0]
                w.writerow([c, ccaa, f'WD-{qid}', nom, f'Wikidata ({tipo})', 'no', len(cands)])
                n_wd += 1
                if len(cands) > 1:
                    n_amb += 1
                por_ccaa[ccaa] += 1
            else:
                w.writerow([c, ccaa, '', '', '', '', ''])
                n_sin += 1
    log(f'Escrito {salida2}: oficiales/autonómicas {n_of}, Wikidata {n_wd} (ambiguos {n_amb}), sin comarca {n_sin}')
    log(f'  cobertura por CCAA (municipios con comarca): {dict(sorted(por_ccaa.items()))}')
    log(f'Terminado en {time.time()-t0:.0f}s')


if __name__ == '__main__':
    main()
