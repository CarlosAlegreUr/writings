#!/usr/bin/env python3
"""
AOCD v2 — Mapa de distritos (coloreado de grafo: distritos vecinos nunca
comparten color). Península + Baleares, Canarias en recuadro; Ceuta y Melilla
aparecen en el panel principal.

Uso:
  python3 scripts/aocd_mapa_v2.py --resultado output/aocd_v2_resultado.json \
      --unidades data/secciones_unificadas.json --salida output/aocd_v2_mapa.png

Por defecto lee el shapefile del seccionado INE 2025 (`data/raw/ine_seccionado/2025/*/SECC_CE_20250101.shp`,
código en la propiedad CUSEC) y lo reproyecta a WGS84. Para unidades municipales (v1):
`--geojson v1/data/spain_municipios_full.part1.geojson v1/data/spain_municipios_full.part2.geojson --campo-codigo mun_code`;
las partes se unen en memoria.
"""

import argparse
import json
import math
import sys
from collections import defaultdict

import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

# Paleta categórica (instancia de referencia de la skill dataviz, modo claro).
# La identidad no se codifica por color: el color solo separa vecinos; la
# codificación secundaria es el contorno negro de cada distrito.
# Orden: los cuatro primeros (los más usados por DSatur) pasan la separación CVD
# todos-contra-todos del validador de la skill; el suelo de visión normal
# (ΔE >= 15) no lo alcanza ninguna paleta de más de 3 colores, por eso el
# contorno negro de cada distrito es la codificación secundaria obligatoria.
PALETA = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#6250d6", "#8c6d31"]
COLOR_CIUDAD = "#4d4d4d"       # unidad que requiere subdivisión por secciones
COLOR_SIN_DATO = "#f0f0f0"


def log(msg):
    print(f"[AOCD-MAPA-v2] {msg}", flush=True)


def cargar_geometria(rutas, campo_codigo):
    partes = []
    for r in rutas:
        log(f"Leyendo {r} ...")
        g = gpd.read_file(r)
        partes.append(g)
    gdf = gpd.GeoDataFrame(pd.concat(partes, ignore_index=True), crs=partes[0].crs)
    if gdf.crs is not None and gdf.crs.to_epsg() != 4326:
        log(f"  Reproyectando de {gdf.crs.to_epsg()} a 4326 ...")
        gdf = gdf.to_crs(4326)
    gdf["codigo"] = gdf[campo_codigo].astype(str).str.zfill(5)
    dup = gdf["codigo"].duplicated().sum()
    if dup:
        log(f"  Duplicados eliminados: {dup}")
        gdf = gdf.drop_duplicates(subset="codigo", keep="first")
    log(f"  Features: {len(gdf)}")
    return gdf


def colorear_grafo(distritos, unidades):
    """DSatur sobre el grafo de adyacencia entre distritos (vía `vecinos` de las unidades)."""
    dist_de = {}
    for d in distritos:
        for u in d["municipios"]:
            dist_de[u] = d["distrito"]
    ady = defaultdict(set)
    for u, info in unidades.items():
        du = dist_de.get(u)
        if du is None:
            continue
        for v in info.get("vecinos", []):
            dv = dist_de.get(v)
            if dv is not None and dv != du:
                ady[du].add(dv)
                ady[dv].add(du)
    ids = [d["distrito"] for d in distritos]
    color = {}
    sat = {i: set() for i in ids}
    pendientes = set(ids)
    while pendientes:
        i = max(pendientes, key=lambda k: (len(sat[k]), len(ady[k]), -k))
        usados = sat[i]
        c = 0
        while c in usados:
            c += 1
        color[i] = c
        pendientes.discard(i)
        for j in ady[i]:
            sat[j].add(c)
    n_col = max(color.values()) + 1 if color else 0
    log(f"  Colores usados por DSatur: {n_col} (paleta de {len(PALETA)})")
    if n_col > len(PALETA):
        log("  AVISO: más colores que paleta; se reutilizan cíclicamente")
    return {i: PALETA[c % len(PALETA)] for i, c in color.items()}, dist_de


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--resultado", default="output/aocd_v2_resultado.json")
    ap.add_argument("--unidades", default="data/secciones_unificadas.json")
    ap.add_argument("--geojson", nargs="+", default=None,
                    help="geometrías (GeoJSON ó shapefile); por defecto el seccionado INE 2025")
    ap.add_argument("--campo-codigo", default="CUSEC")
    ap.add_argument("--salida", default="output/aocd_v2_mapa.png")
    ap.add_argument("--dpi", type=int, default=170)
    args = ap.parse_args(argv)
    if not args.geojson:
        import glob
        args.geojson = sorted(glob.glob("data/raw/ine_seccionado/2025/*/SECC_CE_20250101.shp"))
        if not args.geojson:
            log("No se encuentra el seccionado INE 2025 en data/raw/ine_seccionado/2025/; pasa --geojson")
            return 1

    with open(args.resultado, encoding="utf-8") as f:
        distritos = json.load(f)
    with open(args.unidades, encoding="utf-8") as f:
        unidades = json.load(f)
    log(f"Distritos: {len(distritos)}")
    colores, dist_de = colorear_grafo(distritos, unidades)
    por_id = {d["distrito"]: d for d in distritos}

    gdf = cargar_geometria(args.geojson, args.campo_codigo)
    gdf["distrito"] = gdf["codigo"].map(dist_de)
    sin = gdf["distrito"].isna().sum()
    if sin:
        log(f"  Features sin distrito (no están en la entrada): {sin}")
    gdf = gdf.dropna(subset=["distrito"]).copy()
    gdf["distrito"] = gdf["distrito"].astype(int)
    gdf["tipo"] = gdf["distrito"].map(lambda d: por_id[d]["tipo_bloque"])
    gdf["en_rango"] = gdf["distrito"].map(lambda d: por_id[d]["en_rango"])
    gdf["color"] = gdf["distrito"].map(colores)
    gdf.loc[gdf["tipo"] == "ciudad", "color"] = COLOR_CIUDAD
    gdf["prov"] = gdf["codigo"].str[:2]

    log("Disolviendo contornos de distrito y provincia ...")
    bordes_d = gdf.dissolve(by="distrito").boundary
    bordes_p = gdf.dissolve(by="prov").boundary

    cx = gdf.geometry.centroid.x
    cy = gdf.geometry.centroid.y
    canarias = gdf[cx < -11]
    principal = gdf[cx >= -11]
    bd_can = bordes_d[bordes_d.centroid.x < -11]
    bd_pri = bordes_d[bordes_d.centroid.x >= -11]
    bp_can = bordes_p[bordes_p.centroid.x < -11]
    bp_pri = bordes_p[bordes_p.centroid.x >= -11]

    fig = plt.figure(figsize=(22, 15))
    ax = fig.add_axes([0.01, 0.02, 0.98, 0.9])
    ax_c = fig.add_axes([0.03, 0.06, 0.26, 0.17])

    def pintar(axx, capa, bd, bp, lw_scale):
        normal = capa[capa["en_rango"] | (capa["tipo"] == "ciudad")]
        exc = capa[~capa["en_rango"] & (capa["tipo"] != "ciudad")]
        if len(normal):
            normal.plot(ax=axx, color=normal["color"], edgecolor="none", linewidth=0)
        if len(exc):
            exc.plot(ax=axx, color=exc["color"], edgecolor="#333333", linewidth=0.1,
                     hatch="....", alpha=0.95)
        bd.plot(ax=axx, color="#1a1a1a", linewidth=0.45 * lw_scale)
        bp.plot(ax=axx, color="#000000", linewidth=1.0 * lw_scale)
        axx.set_aspect(1 / math.cos(math.radians(40)))
        axx.axis("off")

    pintar(ax, principal, bd_pri, bp_pri, 1.0)
    ax.set_xlim(-9.6, 4.6)
    ax.set_ylim(35.1, 44.0)
    pintar(ax_c, canarias, bd_can, bp_can, 1.2)
    ax_c.set_title("Canarias", fontsize=12)
    for s in ax_c.spines.values():
        s.set_visible(True)

    n = len(distritos)
    en_rango = sum(1 for d in distritos if d["en_rango"])
    ciudades = sum(1 for d in distritos if d["tipo_bloque"] == "ciudad")
    pob = sum(d["poblacion"] for d in distritos)
    fig.suptitle(
        f"AOCD v2 — Distritos electorales (arts. 16 y 17): {n} distritos, {en_rango} en rango "
        f"95.000–120.000, {ciudades} ciudades pendientes de subdivisión | {pob:,} hab.".replace(",", "."),
        fontsize=16, y=0.965)
    leyenda = [
        Patch(facecolor=COLOR_CIUDAD, edgecolor="#1a1a1a", label="Unidad > 120.000 hab.: requiere subdivisión por secciones"),
        Patch(facecolor="#ffffff", edgecolor="#333333", hatch="....", label="Distrito fuera de rango (excepción art. 16, restr. 4)"),
        Line2D([0], [0], color="#1a1a1a", lw=1.0, label="Límite de distrito"),
        Line2D([0], [0], color="#000000", lw=2.0, label="Límite provincial"),
    ]
    ax.legend(handles=leyenda, loc="lower right", fontsize=11, frameon=True)
    fig.text(0.5, 0.925, "Los colores solo separan distritos vecinos (coloreado de grafo); no codifican ningún valor.",
             ha="center", fontsize=11, color="#444444")
    fig.savefig(args.salida, dpi=args.dpi, facecolor="white")
    log(f"Mapa guardado en {args.salida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
