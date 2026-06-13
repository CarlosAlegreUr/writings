#!/usr/bin/env python3
"""
AOCD — Preparación de datos reales de España.
Cruza población (INE), renta (INE) y geometría (GeoJSON) por código municipal.
Calcula adyacencia geográfica real y exporta JSON unificado.
"""

import csv
import json
import sys
import time
from collections import defaultdict

def log(msg):
    print(f"[AOCD-PREP] {msg}", flush=True)

def cargar_poblacion(ruta):
    """Carga población por municipio desde CSV del INE."""
    log(f"Cargando población desde {ruta}...")
    municipios = {}
    with open(ruta, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            codigo = row['codigo'].strip().zfill(5)
            municipios[codigo] = {
                'nombre': row['nombre'].strip(),
                'poblacion': int(row['poblacion']),
            }
    log(f"  Municipios con población: {len(municipios)}")
    log(f"  Población total: {sum(m['poblacion'] for m in municipios.values()):,}")
    return municipios

def cargar_renta(ruta):
    """Carga renta media por municipio desde CSV consolidado."""
    log(f"Cargando renta desde {ruta}...")
    rentas = {}
    with open(ruta, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            codigo = row['codigo'].strip().zfill(5)
            rentas[codigo] = float(row['renta_media'])
    log(f"  Municipios con renta: {len(rentas)}")
    log(f"  Renta media: {sum(rentas.values())/len(rentas):,.0f}€")
    return rentas

def cargar_geometria(ruta):
    """Carga geometría de municipios desde GeoJSON."""
    log(f"Cargando geometría desde {ruta}...")
    import geopandas as gpd
    gdf = gpd.read_file(ruta)
    log(f"  Features cargadas: {len(gdf)}")

    # Normalizar código municipal a 5 dígitos
    gdf['codigo'] = gdf['mun_code'].astype(str).str.zfill(5)

    # Eliminar duplicados (quedarse con el primero)
    duplicados = gdf['codigo'].duplicated().sum()
    if duplicados > 0:
        log(f"  Duplicados eliminados: {duplicados}")
        gdf = gdf.drop_duplicates(subset='codigo', keep='first')

    log(f"  Municipios únicos con geometría: {len(gdf)}")
    return gdf

def calcular_adyacencia(gdf):
    """Calcula adyacencia real entre municipios usando geometría."""
    log("Calculando adyacencia geográfica (esto puede tardar)...")
    t0 = time.time()

    adyacencia = defaultdict(list)
    codigos = gdf['codigo'].tolist()
    geometrias = gdf.geometry.tolist()

    # Crear índice espacial para acelerar
    sindex = gdf.sindex

    total = len(gdf)
    for i in range(total):
        if (i + 1) % 500 == 0:
            elapsed = time.time() - t0
            log(f"  Procesando municipio {i+1}/{total} ({elapsed:.0f}s)")

        geom_i = geometrias[i]
        codigo_i = codigos[i]

        # Usar índice espacial para candidatos
        candidatos = list(sindex.intersection(geom_i.bounds))

        for j in candidatos:
            if i == j:
                continue
            codigo_j = codigos[j]
            if codigo_j in adyacencia[codigo_i]:
                continue

            # Verificar si realmente se tocan
            if geom_i.touches(geometrias[j]) or geom_i.intersects(geometrias[j]):
                adyacencia[codigo_i].append(codigo_j)
                adyacencia[codigo_j].append(codigo_i)

    # Eliminar duplicados en listas de vecinos
    for codigo in adyacencia:
        adyacencia[codigo] = list(set(adyacencia[codigo]))

    elapsed = time.time() - t0
    n_con_vecinos = sum(1 for v in adyacencia.values() if v)
    avg_vecinos = sum(len(v) for v in adyacencia.values()) / max(n_con_vecinos, 1)
    max_vecinos = max(len(v) for v in adyacencia.values()) if adyacencia else 0
    min_vecinos = min(len(v) for v in adyacencia.values()) if adyacencia else 0

    log(f"  Adyacencia calculada en {elapsed:.0f}s")
    log(f"  Municipios con vecinos: {n_con_vecinos}")
    log(f"  Vecinos por municipio: min={min_vecinos}, media={avg_vecinos:.1f}, max={max_vecinos}")

    return dict(adyacencia)

def cruzar_datos(poblacion, rentas, gdf, adyacencia):
    """Cruza los tres datasets por código municipal."""
    log("Cruzando datos...")

    # Códigos disponibles en cada dataset
    codigos_pob = set(poblacion.keys())
    codigos_renta = set(rentas.keys())
    codigos_geo = set(gdf['codigo'].tolist())

    # Intersección: municipios con los 3 datos
    codigos_comunes = codigos_pob & codigos_geo
    log(f"  Municipios con población + geometría: {len(codigos_comunes)}")

    sin_renta = codigos_comunes - codigos_renta
    con_renta = codigos_comunes & codigos_renta
    log(f"  Con renta directa: {len(con_renta)}")
    log(f"  Sin renta (usarán media provincial): {len(sin_renta)}")

    # Calcular media provincial para rellenar
    prov_rentas = defaultdict(list)
    for codigo, renta in rentas.items():
        prov = codigo[:2]
        prov_rentas[prov].append(renta)

    prov_media = {}
    for prov, lista in prov_rentas.items():
        prov_media[prov] = sum(lista) / len(lista)

    # Media nacional como fallback final
    media_nacional = sum(rentas.values()) / len(rentas)
    log(f"  Media nacional de renta: {media_nacional:,.0f}€")

    # Calcular centroides
    centroides = {}
    for _, row in gdf.iterrows():
        codigo = row['codigo']
        centroid = row.geometry.centroid
        centroides[codigo] = (centroid.y, centroid.x)  # lat, lon

    # Construir resultado
    resultado = {}
    sin_renta_count = 0
    fallback_nacional_count = 0

    for codigo in sorted(codigos_comunes):
        pob_data = poblacion[codigo]

        # Renta
        if codigo in rentas:
            renta = rentas[codigo]
        else:
            prov = codigo[:2]
            if prov in prov_media:
                renta = prov_media[prov]
                sin_renta_count += 1
            else:
                renta = media_nacional
                fallback_nacional_count += 1

        # Provincia (2 primeros dígitos)
        prov_code = codigo[:2]

        # Centroide
        lat, lon = centroides.get(codigo, (0, 0))

        # Vecinos
        vecinos = adyacencia.get(codigo, [])
        # Filtrar vecinos que no están en codigos_comunes
        vecinos = [v for v in vecinos if v in codigos_comunes]

        resultado[codigo] = {
            'nombre': pob_data['nombre'],
            'poblacion': pob_data['poblacion'],
            'renta_media': round(renta, 2),
            'provincia': prov_code,
            'lat': round(lat, 6),
            'lon': round(lon, 6),
            'vecinos': vecinos,
        }

    log(f"\n  === RESUMEN CRUCE ===")
    log(f"  Municipios finales: {len(resultado)}")
    log(f"  Población total: {sum(m['poblacion'] for m in resultado.values()):,}")
    log(f"  Con renta directa: {len(con_renta)}")
    log(f"  Con renta provincial: {sin_renta_count}")
    log(f"  Con renta nacional (fallback): {fallback_nacional_count}")

    # Municipios sin vecinos
    sin_vecinos = [c for c, m in resultado.items() if not m['vecinos']]
    log(f"  Municipios sin vecinos (islas/enclaves): {len(sin_vecinos)}")
    if sin_vecinos[:10]:
        for c in sin_vecinos[:10]:
            log(f"    - {c}: {resultado[c]['nombre']} ({resultado[c]['poblacion']:,} hab)")

    return resultado

def exportar(resultado, ruta):
    """Exporta resultado a JSON."""
    log(f"Exportando a {ruta}...")
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    log(f"  Tamaño: {len(json.dumps(resultado)):,} bytes")

if __name__ == "__main__":
    log("=== PREPARACIÓN DE DATOS AOCD ===\n")

    # Cargar datasets
    poblacion = cargar_poblacion('data/poblacion_municipios_2024.csv')
    rentas = cargar_renta('data/renta_municipios_2022.csv')
    gdf = cargar_geometria('data/spain_municipios_full.geojson')

    # Adyacencia
    adyacencia = calcular_adyacencia(gdf)

    # Cruzar
    resultado = cruzar_datos(poblacion, rentas, gdf, adyacencia)

    # Exportar
    exportar(resultado, 'data/municipios_unificados.json')

    log("\n=== PREPARACIÓN COMPLETADA ===")
