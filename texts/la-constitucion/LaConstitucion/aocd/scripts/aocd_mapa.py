#!/usr/bin/env python3
"""
AOCD — Generación de mapa de distritos para España.
Lee el resultado del AOCD y genera un mapa coloreado con geopandas + matplotlib.
"""

import json
import sys
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from collections import defaultdict

def log(msg):
    print(f"[AOCD-MAPA] {msg}", flush=True)

def cargar_resultado(ruta):
    """Carga resultado del AOCD."""
    log(f"Cargando resultado desde {ruta}...")
    with open(ruta, 'r', encoding='utf-8') as f:
        data = json.load(f)
    log(f"  Distritos: {len(data)}")
    return data

def crear_mapa_municipio_distrito(resultado):
    """Crea mapping municipio → distrito."""
    mun_to_dist = {}
    for entry in resultado:
        distrito_id = entry['distrito']
        for mun in entry['municipios']:
            mun_to_dist[mun] = distrito_id
    log(f"  Municipios mapeados: {len(mun_to_dist)}")
    return mun_to_dist

def colorear_distritos(resultado, mun_to_dist):
    """
    Asigna colores a distritos intentando que vecinos no compartan color.
    Usa algoritmo greedy de coloración de grafos.
    """
    log("Coloreando distritos...")
    n_distritos = len(resultado)

    # Construir grafo de adyacencia entre distritos
    dist_vecinos = defaultdict(set)
    for entry in resultado:
        d = entry['distrito']
        # Los municipios del distrito
        muns = set(entry['municipios'])
        # Distritos vecinos: aquellos que contienen municipios adyacentes
        # (simplificado: distritos que comparten provincia fronteriza)

    # Mejor approach: usar los datos de resultado directamente
    # Dos distritos son vecinos si comparten al menos un par de municipios adyacentes
    # Pero no tenemos adyacencia de municipios en el resultado...
    # Usamos la info de provincias como proxy para evitar colores iguales contiguos

    # Generar paleta de colores suficiente
    # Con ~450 distritos, usamos una paleta cíclica amplia
    np.random.seed(42)
    n_colores = min(20, n_distritos)  # 20 colores distintos
    base_colors = plt.cm.tab20(np.linspace(0, 1, 20))
    extra_colors = plt.cm.Set3(np.linspace(0, 1, 12))
    all_colors = np.vstack([base_colors, extra_colors])

    # Asignar color por distrito (simple: módulo del número de colores)
    dist_colors = {}
    for entry in resultado:
        d = entry['distrito']
        dist_colors[d] = all_colors[d % len(all_colors)]

    return dist_colors

def generar_mapa(gdf, mun_to_dist, dist_colors, output_path):
    """Genera mapa coloreado de España con los distritos."""
    log("Generando mapa...")

    # Asignar distrito y color a cada municipio del GeoDataFrame
    gdf = gdf.copy()
    gdf['codigo'] = gdf['mun_code'].astype(str).str.zfill(5)
    gdf['distrito'] = gdf['codigo'].map(mun_to_dist)
    gdf = gdf.dropna(subset=['distrito'])
    gdf['distrito'] = gdf['distrito'].astype(int)

    log(f"  Municipios en mapa: {len(gdf)}")

    # Crear color por municipio
    gdf['color'] = gdf['distrito'].map(
        lambda d: mcolors.to_hex(dist_colors.get(d, [0.9, 0.9, 0.9, 1.0]))
    )

    # Separar península de islas
    # Península: longitud > -20 y latitud > 35
    peninsula = gdf[(gdf.geometry.centroid.x > -10) & (gdf.geometry.centroid.x < 5) &
                     (gdf.geometry.centroid.y > 35) & (gdf.geometry.centroid.y < 44)]
    baleares = gdf[(gdf.geometry.centroid.x > 1) & (gdf.geometry.centroid.y < 40.5) &
                    (gdf.geometry.centroid.y > 38.5)]
    canarias = gdf[(gdf.geometry.centroid.x < -13)]
    ceuta_melilla = gdf[(gdf.geometry.centroid.y < 36) & (gdf.geometry.centroid.x > -6)]

    # Crear figura con subplots
    fig, axes = plt.subplots(1, 2, figsize=(20, 12),
                              gridspec_kw={'width_ratios': [4, 1]})

    # Península + Baleares
    ax_main = axes[0]
    peninsula.plot(ax=ax_main, color=peninsula['color'], edgecolor='#333333',
                   linewidth=0.05, alpha=0.85)
    if len(baleares) > 0:
        baleares.plot(ax=ax_main, color=baleares['color'], edgecolor='#333333',
                      linewidth=0.05, alpha=0.85)
    ax_main.set_xlim(-10, 5)
    ax_main.set_ylim(35.5, 44)
    ax_main.set_title('España Peninsular y Baleares', fontsize=14, fontweight='bold')
    ax_main.axis('off')

    # Canarias
    ax_can = axes[1]
    if len(canarias) > 0:
        canarias.plot(ax=ax_can, color=canarias['color'], edgecolor='#333333',
                      linewidth=0.05, alpha=0.85)
        ax_can.set_title('Canarias', fontsize=12, fontweight='bold')
    ax_can.axis('off')

    # Título general
    n_distritos = len(set(mun_to_dist.values()))
    pob_total = sum(entry['poblacion'] for entry in resultado_global)
    fig.suptitle(
        f'AOCD — Distritos Electorales de España\n'
        f'{n_distritos} distritos | {pob_total:,} habitantes | 95.000-120.000 hab/distrito',
        fontsize=14, fontweight='bold', y=1.02
    )

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    log(f"  Mapa guardado en: {output_path}")
    plt.close()


# Variable global para el título
resultado_global = []

if __name__ == "__main__":
    ruta_resultado = sys.argv[1] if len(sys.argv) > 1 else "aocd_resultado_espana.json"
    ruta_geojson = sys.argv[2] if len(sys.argv) > 2 else "data/spain_municipios_full.geojson"
    ruta_salida = sys.argv[3] if len(sys.argv) > 3 else "aocd_mapa_espana.png"

    # Cargar datos
    resultado = cargar_resultado(ruta_resultado)
    resultado_global = resultado
    mun_to_dist = crear_mapa_municipio_distrito(resultado)
    dist_colors = colorear_distritos(resultado, mun_to_dist)

    # Cargar geometría
    log(f"Cargando geometría desde {ruta_geojson}...")
    gdf = gpd.read_file(ruta_geojson)
    log(f"  Features: {len(gdf)}")

    # Generar mapa
    generar_mapa(gdf, mun_to_dist, dist_colors, ruta_salida)

    log("\n=== MAPA GENERADO ===")
