#!/usr/bin/env python3
"""
AOCD — Distribución de la renta por unidad de consumo por sección censal (ADRH).

Fuente: INE, Atlas de Distribución de Renta de los Hogares, tabla nacional 30826
"Porcentaje de población con ingresos por unidad de consumo por debajo de
determinados umbrales fijos por sexo" (variable literal del INE: "Distribución
de la renta por unidad de consumo"). Edición 2024 exportada de jaxiT3 en PC-Axis:
    data/raw/ine_adrh_tramos/30826_umbrales_fijos_sexo_nacional.px

OJO: el INE NO publica tramos disjuntos; publica porcentajes ACUMULADOS de
población con ingresos por unidad de consumo "por debajo de" 5.000, 7.500 y
10.000 euros (no existe umbral de 15.000). Los tramos disjuntos derivables son:
    <5.000 = p5000 ; 5.000–7.500 = p7500-p5000 ; 7.500–10.000 = p10000-p7500 ;
    >=10.000 = 100-p10000.
Se exportan los textos literales del INE, no los tramos derivados.

Salidas (solo Sexo = Total, un año):
  data/secciones_tramos_renta.csv   cusec,anyo,tramo,porcentaje   (todas las
                                    secciones con dato en la tabla)
  data/secciones_tramos_renta.json  {cusec: {tramo: porcentaje}} compacto,
                                    filtrado al seccionado 2025 (SECC_CE_20250101)

Ejecutar desde la raíz de aocd/:
    python3 -I scripts/aocd_tramos_renta.py [--anyo 2024] [--px RUTA] [--sexo Total]
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

sys.path.append(site.getusersitepackages())           # pyogrio está en el site del usuario
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # aocd_px
sys.dont_write_bytecode = True

from aocd_px import iterar_datos, leer_px  # noqa: E402

PX_DEFECTO = os.path.join('data', 'raw', 'ine_adrh_tramos', '30826_umbrales_fijos_sexo_nacional.px')


def log(msg):
    print(f'[AOCD-TRAMOS] {msg}', flush=True)


def cusec_seccionado_2025(raiz):
    rutas = glob.glob(os.path.join(raiz, 'data', 'raw', 'ine_seccionado', '2025', '*', 'SECC_CE_20250101.shp'))
    if rutas:
        import pyogrio
        df = pyogrio.read_dataframe(rutas[0], read_geometry=False, columns=['CUSEC'])
        log(f'Seccionado 2025 leído del shapefile: {len(df)} secciones')
        return set(df['CUSEC'])
    alt = os.path.join(raiz, 'data', 'poblacion_secciones_2025.csv')
    if os.path.exists(alt):
        with open(alt, 'r', encoding='utf-8', newline='') as f:
            s = {row['cusec'] for row in csv.DictReader(f)}
        log(f'Seccionado 2025 leído de {alt}: {len(s)} secciones')
        return s
    raise SystemExit('No se encuentra el seccionado 2025 (shapefile ni poblacion_secciones_2025.csv)')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--raiz', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument('--px', default=None)
    ap.add_argument('--anyo', default='2024')
    ap.add_argument('--sexo', default='Total')
    args = ap.parse_args()
    raiz = args.raiz
    ruta_px = args.px or os.path.join(raiz, PX_DEFECTO)
    t0 = time.time()

    log(f'Leyendo {ruta_px}')
    px = leer_px(ruta_px)
    stub = px['stub'][0]
    var_sexo, var_tramo, var_periodo = px['heading']
    tramos = px['values'][var_tramo]
    log(f'  TITLE={px["meta"].get(("TITLE", None))}')
    log(f'  variables: {px["stub"] + px["heading"]} | periodos: {px["values"][var_periodo]} | unidades: {px["meta"].get(("UNITS", None))}')
    log(f'  variable "{var_tramo}" = {tramos}')
    if args.anyo not in px['values'][var_periodo]:
        raise SystemExit(f'El periodo {args.anyo} no está en la tabla')
    if args.sexo not in px['values'][var_sexo]:
        raise SystemExit(f'El valor de sexo {args.sexo!r} no está en la tabla')

    datos = defaultdict(dict)        # cusec -> {tramo: valor}
    n_cod = Counter(len(c) for c in px['codes'][stub])
    nulos = Counter()
    for (unidad, sexo, tramo, anyo), valor in iterar_datos(px):
        if sexo != args.sexo or anyo != args.anyo:
            continue
        codigo = unidad.split(' ')[0]
        if len(codigo) != 10:
            continue
        if valor is None:
            nulos[tramo] += 1
        else:
            datos[codigo][tramo] = valor
    log(f'  códigos en la tabla: secciones={n_cod[10]} distritos={n_cod[7]} municipios={n_cod[5]}')
    log(f'  {args.anyo}, sexo={args.sexo}: secciones con algún dato {len(datos)}; '
        f'nulos por tramo {dict((t[-22:], n) for t, n in nulos.items())}')

    # coherencia: acumulados no decrecientes
    incoh = 0
    for c, d in datos.items():
        v = [d.get(t) for t in tramos]
        if all(x is not None for x in v) and not (v[0] <= v[1] <= v[2]):
            incoh += 1
    log(f'  secciones con acumulados no monótonos (p5000<=p7500<=p10000): {incoh}')

    # CSV largo
    ruta_csv = os.path.join(raiz, 'data', 'secciones_tramos_renta.csv')
    n = 0
    with open(ruta_csv, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['cusec', 'anyo', 'tramo', 'porcentaje'])
        for c in sorted(datos):
            for t in tramos:
                if t in datos[c]:
                    w.writerow([c, args.anyo, t, datos[c][t]])
                    n += 1
    log(f'Escrito {ruta_csv}: {n} filas ({len(datos)} secciones x hasta {len(tramos)} tramos)')

    # JSON filtrado al seccionado 2025
    s25 = cusec_seccionado_2025(raiz)
    salida = {c: datos[c] for c in sorted(datos) if c in s25}
    sin = s25 - set(datos)
    fuera = set(datos) - s25
    ruta_json = os.path.join(raiz, 'data', 'secciones_tramos_renta.json')
    with open(ruta_json, 'w', encoding='utf-8') as f:
        json.dump(salida, f, ensure_ascii=False, separators=(',', ':'))
    log(f'Escrito {ruta_json}: {len(salida)} secciones de {len(s25)} del seccionado 2025 '
        f'({len(sin)} sin dato = suprimidas/no publicadas; {len(fuera)} códigos con dato fuera del seccionado 2025); '
        f'{os.path.getsize(ruta_json):,} bytes')
    log(f'Terminado en {time.time()-t0:.0f}s')


if __name__ == '__main__':
    main()
