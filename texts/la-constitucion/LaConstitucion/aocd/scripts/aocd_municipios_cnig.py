#!/usr/bin/env python3
"""
AOCD — Geometría municipal oficial (IGN/CNIG, "Líneas límite", unidades
administrativas de 4º orden = municipios) convertida a GeoJSON con el mismo
campo de cruce que usa v1/scripts/aocd_preparar_datos.py (`mun_code`, código INE de 5 dígitos).

Entrada:  data/raw/cnig_lineas_limite/gml/au_AdministrativeUnit_4thOrder0.gml
          (INSPIRE AU, EPSG:4258 ETRS89 lat/lon; versión 10-08-2026)
Salida:   data/municipios_cnig_2026.geojson  (EPSG:4326 lon/lat, 7 decimales)
          Si supera 50 MB se escribe en partes municipios_cnig_2026.partN.geojson
          (mismo mecanismo que data/SPLIT-NOTE.md) y no se escribe el fichero único.

Se excluyen las 81 unidades 53xxx (territorios no municipalizados del IGN:
facerías, mancomunidades, Bardenas, etc.) y las 7 unidades 54xxx (plazas de
soberanía, Gibraltar, Isla de los Faisanes). Quedan 8.132 = municipios INE 2025.

Para regenerar la adyacencia municipal con esta geometría basta con cambiar
en v1/scripts/aocd_preparar_datos.py la ruta 'data/spain_municipios_full.geojson' (hoy v1/data/) por
'data/municipios_cnig_2026.geojson' (recombinando las partes si procede):
el script ya normaliza `mun_code` a 5 dígitos y usa `gdf.sindex`.

Ejecutar desde la raíz de aocd/:
    python3 -I scripts/aocd_municipios_cnig.py [--raiz RUTA_AOCD] [--max-mb 50]
"""

import argparse
import glob
import json
import os
import site
import sys
import time

sys.path.append(site.getusersitepackages())   # geopandas está en el site del usuario

import geopandas as gpd  # noqa: E402

LIMITE_MB_DEFECTO = 50


def log(msg):
    print(f'[AOCD-CNIG] {msg}', flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--raiz', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument('--max-mb', type=float, default=LIMITE_MB_DEFECTO)
    args = ap.parse_args()
    raiz = args.raiz
    entrada = os.path.join(raiz, 'data', 'raw', 'cnig_lineas_limite', 'gml', 'au_AdministrativeUnit_4thOrder0.gml')
    salida = os.path.join(raiz, 'data', 'municipios_cnig_2026.geojson')
    t0 = time.time()

    log(f'Leyendo {entrada}')
    g = gpd.read_file(entrada, engine='pyogrio', columns=['nationalCode', 'text'])
    log(f'  unidades: {len(g)}  CRS: {g.crs}  inválidas: {int((~g.is_valid).sum())}')
    g['mun_code'] = g['nationalCode'].astype(str).str[-5:]
    g = g[~g['mun_code'].str.startswith(('53', '54'))].copy()   # 53xxx territorios sin municipio; 54xxx plazas de soberanía/Gibraltar
    g['geometry'] = g.geometry.make_valid()
    g = g.rename(columns={'text': 'mun_name'})[['mun_code', 'mun_name', 'nationalCode', 'geometry']]
    g = g.to_crs(epsg=4326)
    log(f'  municipios exportados: {len(g)} (códigos únicos: {g["mun_code"].nunique()})')

    # GeoJSON compacto con 7 decimales (~1 cm): se serializa a mano para controlar tamaño.
    g['geometry'] = g.geometry.set_precision(1e-7)   # (GeoSeries.set_precision; en GeoDataFrame devolvería solo geometría)
    features = json.loads(g.to_json(drop_id=True))['features']
    texto = json.dumps({'type': 'FeatureCollection', 'features': features}, ensure_ascii=False, separators=(',', ':'))
    mb = len(texto.encode('utf-8')) / 1e6
    log(f'  tamaño GeoJSON único: {mb:.1f} MB')

    for ruta_vieja in glob.glob(os.path.join(raiz, 'data', 'municipios_cnig_2026*.geojson')):
        os.remove(ruta_vieja)   # salidas de ejecuciones anteriores
    if mb <= args.max_mb:
        with open(salida, 'w', encoding='utf-8') as f:
            f.write(texto)
        log(f'Escrito {salida}')
    else:
        # Reparto por BYTES acumulados (no por nº de features): cada parte < max_mb.
        limite = int(args.max_mb * 1e6 * 0.95)
        partes, actual, tam = [], [], 0
        for feat in features:
            s = json.dumps(feat, ensure_ascii=False, separators=(',', ':'))
            if actual and tam + len(s.encode('utf-8')) + 1 > limite:
                partes.append(actual)
                actual, tam = [], 0
            actual.append(s)
            tam += len(s.encode('utf-8')) + 1
        if actual:
            partes.append(actual)
        for k, parte in enumerate(partes):
            ruta = os.path.join(raiz, 'data', f'municipios_cnig_2026.part{k+1}.geojson')
            with open(ruta, 'w', encoding='utf-8') as f:
                f.write('{"type":"FeatureCollection","features":[' + ','.join(parte) + ']}')
            log(f'  escrita parte {k+1}/{len(partes)}: {ruta} ({len(parte)} features, {os.path.getsize(ruta)/1e6:.1f} MB)')
        log('Para recombinar: ver data/SPLIT-NOTE.md (mismo procedimiento, concatenar `features`).')
    log(f'Terminado en {time.time()-t0:.0f}s')


if __name__ == '__main__':
    main()
