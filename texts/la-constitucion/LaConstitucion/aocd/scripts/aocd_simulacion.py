#!/usr/bin/env python3
"""
AOCD — Algoritmo de Optimización de la Corruptabilidad de Distritos
Simulación con datos reales de España.

Uso:
  1. Descargar datos (el script descarga automáticamente del INE si no existen)
  2. python3 aocd_simulacion.py

Dependencias:
  pip install numpy matplotlib
  pip install geopandas shapely  # para adyacencia geográfica real (opcional)
"""

import json
import os
import random
import math
import csv
from collections import defaultdict
from copy import deepcopy
from pathlib import Path

# ============================================================
# PARÁMETROS CONSTITUCIONALES (Art. 13)
# ============================================================
MIN_HAB = 95_000
MAX_HAB = 120_000

# ============================================================
# ESTRUCTURAS DE DATOS
# ============================================================

class Municipio:
    def __init__(self, id: str, nombre: str, poblacion: int,
                 renta_media: float, provincia: str,
                 lat: float = 0, lon: float = 0):
        self.id = id
        self.nombre = nombre
        self.poblacion = poblacion
        self.renta_media = renta_media
        self.provincia = provincia
        self.lat = lat
        self.lon = lon
        self.vecinos: list[str] = []

    def __repr__(self):
        return f"{self.nombre} ({self.poblacion:,} hab, {self.renta_media:.0f}€)"


# ============================================================
# CARGA DE DATOS
# ============================================================

def cargar_datos_csv(ruta_poblacion: str, ruta_renta: str) -> dict[str, Municipio]:
    """
    Carga municipios desde CSVs.
    Formato esperado población: codigo,nombre,provincia,poblacion,lat,lon
    Formato esperado renta: codigo,renta_media
    """
    municipios = {}

    with open(ruta_poblacion, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            m = Municipio(
                id=row['codigo'],
                nombre=row['nombre'],
                poblacion=int(row['poblacion']),
                renta_media=0,
                provincia=row['provincia'],
                lat=float(row.get('lat', 0)),
                lon=float(row.get('lon', 0))
            )
            municipios[m.id] = m

    with open(ruta_renta, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            codigo = row['codigo']
            if codigo in municipios:
                municipios[codigo].renta_media = float(row['renta_media'])

    return municipios


def generar_datos_sinteticos_espana(n_municipios: int = 8131) -> dict[str, Municipio]:
    """
    Genera datos sintéticos basados en estadísticas reales de España.
    Población total ~47M, distribución realista por provincias.
    Usar esto para probar el algoritmo antes de tener datos reales.
    """
    random.seed(42)

    # Provincias con población aproximada (INE 2024)
    provincias = {
        'Madrid': 6_800_000, 'Barcelona': 5_700_000,
        'Valencia': 2_600_000, 'Sevilla': 1_950_000,
        'Alicante': 1_900_000, 'Málaga': 1_700_000,
        'Murcia': 1_500_000, 'Cádiz': 1_250_000,
        'Vizcaya': 1_150_000, 'A Coruña': 1_130_000,
        'Las Palmas': 1_130_000, 'Asturias': 1_010_000,
        'Santa Cruz': 1_050_000, 'Pontevedra': 950_000,
        'Granada': 920_000, 'Zaragoza': 980_000,
        'Tarragona': 810_000, 'Córdoba': 780_000,
        'Girona': 780_000, 'Guipúzcoa': 730_000,
        'Toledo': 710_000, 'Almería': 730_000,
        'Badajoz': 680_000, 'Jaén': 630_000,
        'Navarra': 660_000, 'Cantabria': 580_000,
        'Castellón': 590_000, 'Valladolid': 520_000,
        'Ciudad Real': 500_000, 'León': 460_000,
        'Huelva': 520_000, 'Lleida': 440_000,
        'Burgos': 360_000, 'Álava': 340_000,
        'Salamanca': 330_000, 'Lugo': 330_000,
        'Cáceres': 400_000, 'Ourense': 310_000,
        'La Rioja': 320_000, 'Huesca': 230_000,
        'Guadalajara': 270_000, 'Albacete': 390_000,
        'Cuenca': 200_000, 'Segovia': 155_000,
        'Teruel': 135_000, 'Ávila': 160_000,
        'Zamora': 170_000, 'Soria': 90_000,
        'Palencia': 165_000, 'Baleares': 1_200_000,
    }

    # Renta media por provincia (aprox, INE)
    renta_base = {
        'Madrid': 15_000, 'Barcelona': 14_000, 'Vizcaya': 14_500,
        'Guipúzcoa': 14_800, 'Navarra': 14_200, 'Álava': 14_000,
        'Girona': 12_500, 'Lleida': 12_000, 'Tarragona': 12_000,
        'Baleares': 12_500, 'Zaragoza': 12_000, 'La Rioja': 11_800,
        'Cantabria': 11_500, 'Asturias': 11_000, 'Valladolid': 11_000,
    }
    renta_default = 10_500  # media nacional aprox

    municipios = {}
    municipio_id = 0

    for provincia, pob_total in provincias.items():
        # Distribuir municipios proporcional a población
        n_mun = max(3, int(n_municipios * pob_total / 47_000_000))
        renta_prov = renta_base.get(provincia, renta_default)

        # Distribución de población tipo Zipf (realista)
        pesos = [1.0 / (i + 1) ** 0.8 for i in range(n_mun)]
        suma_pesos = sum(pesos)
        poblaciones = [max(50, int(pob_total * p / suma_pesos)) for p in pesos]

        # Ajustar para que sume exactamente
        diff = pob_total - sum(poblaciones)
        poblaciones[0] += diff

        for i in range(n_mun):
            mid = f"M{municipio_id:05d}"
            # Renta con variación realista (log-normal dentro de provincia)
            renta = renta_prov * random.lognormvariate(0, 0.3)
            # Coordenadas ficticias dentro de una cuadrícula por provincia
            lat = random.uniform(36, 43.5)
            lon = random.uniform(-9, 3)

            municipios[mid] = Municipio(
                id=mid,
                nombre=f"{provincia}_{i:04d}",
                poblacion=poblaciones[i],
                renta_media=renta,
                provincia=provincia,
                lat=lat, lon=lon
            )
            municipio_id += 1

    return municipios


# ============================================================
# ADYACENCIA
# ============================================================

def construir_adyacencia_por_distancia(municipios: dict[str, Municipio],
                                        k_vecinos: int = 6) -> None:
    """
    Aproximación: los k municipios más cercanos son vecinos.
    Con datos reales, usar fronteras geográficas (shapefiles).
    """
    ids = list(municipios.keys())
    coords = {mid: (municipios[mid].lat, municipios[mid].lon) for mid in ids}

    for mid in ids:
        lat1, lon1 = coords[mid]
        distancias = []
        for other in ids:
            if other == mid:
                continue
            lat2, lon2 = coords[other]
            d = math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)
            distancias.append((d, other))
        distancias.sort()
        municipios[mid].vecinos = [oid for _, oid in distancias[:k_vecinos]]

    # Asegurar simetría
    for mid in ids:
        for vecino in municipios[mid].vecinos:
            if mid not in municipios[vecino].vecinos:
                municipios[vecino].vecinos.append(mid)


def construir_adyacencia_desde_shapefile(municipios, shapefile_path):
    """
    Construye adyacencia real desde shapefile de municipios.
    Requiere: pip install geopandas shapely
    """
    try:
        import geopandas as gpd
    except ImportError:
        print("geopandas no instalado. Usando adyacencia por distancia.")
        construir_adyacencia_por_distancia(municipios)
        return

    gdf = gpd.read_file(shapefile_path)
    # Ajustar según la columna de código municipal del shapefile
    for idx, row in gdf.iterrows():
        codigo = str(row.get('NATCODE', row.get('codigo', '')))
        if codigo not in municipios:
            continue
        geom = row.geometry
        vecinos = gdf[gdf.geometry.touches(geom)]
        for _, v in vecinos.iterrows():
            vc = str(v.get('NATCODE', v.get('codigo', '')))
            if vc in municipios and vc != codigo:
                if vc not in municipios[codigo].vecinos:
                    municipios[codigo].vecinos.append(vc)


# ============================================================
# FUNCIONES DEL ALGORITMO (Art. 13)
# ============================================================

def percentil_25_distrito(distrito: list[str],
                          municipios: dict[str, Municipio]) -> float:
    """
    P25 de renta del distrito.
    Aproximación: ponderamos la renta media de cada municipio por su
    población para estimar la distribución agregada.
    Con datos individuales reales, se usaría la distribución completa.
    """
    rentas_ponderadas = []
    for mid in distrito:
        m = municipios[mid]
        # Simulamos distribución interna como log-normal centrada en la media
        rentas_ponderadas.append((m.renta_media, m.poblacion))

    # Ordenar por renta y encontrar P25 ponderado
    rentas_ponderadas.sort(key=lambda x: x[0])
    total_pob = sum(p for _, p in rentas_ponderadas)
    objetivo = total_pob * 0.25
    acumulado = 0
    for renta, pob in rentas_ponderadas:
        acumulado += pob
        if acumulado >= objetivo:
            return renta
    return rentas_ponderadas[-1][0]


def poblacion_distrito(distrito: list[str],
                       municipios: dict[str, Municipio]) -> int:
    return sum(municipios[mid].poblacion for mid in distrito)


def es_contiguo(distrito: list[str],
                municipios: dict[str, Municipio]) -> bool:
    """Verifica continuidad geográfica mediante búsqueda en anchura."""
    if len(distrito) <= 1:
        return True
    ids = set(distrito)
    visitados = set()
    cola = [distrito[0]]
    while cola:
        actual = cola.pop(0)
        if actual in visitados:
            continue
        visitados.add(actual)
        for vecino in municipios[actual].vecinos:
            if vecino in ids and vecino not in visitados:
                cola.append(vecino)
    return visitados == ids


def funcion_objetivo(particion: list[list[str]],
                     municipios: dict[str, Municipio]) -> float:
    """Maximizar el mínimo P25 entre todos los distritos."""
    if not particion:
        return 0
    return min(percentil_25_distrito(d, municipios) for d in particion)


def cumple_restricciones(distrito: list[str],
                         municipios: dict[str, Municipio],
                         min_hab: int = MIN_HAB,
                         max_hab: int = MAX_HAB) -> bool:
    pob = poblacion_distrito(distrito, municipios)
    if not (min_hab <= pob <= max_hab):
        return False
    if not es_contiguo(distrito, municipios):
        return False
    return True


def desviacion_minima_necesaria(distrito: list[str],
                                 municipios: dict[str, Municipio],
                                 min_hab: int = MIN_HAB,
                                 max_hab: int = MAX_HAB) -> bool:
    """
    Restricción 4: Excepción por imposibilidad geográfica.
    Permite distritos fuera de rango solo si no hay alternativa viable.
    Retorna True si el distrito es aceptable (dentro de rango O excepción).
    """
    pob = poblacion_distrito(distrito, municipios)
    if min_hab <= pob <= max_hab:
        return True

    # Verificar si algún municipio del distrito tiene vecinos fuera del distrito
    # que podrían añadirse/quitarse para acercar al rango
    for mid in distrito:
        for vecino in municipios[mid].vecinos:
            if vecino not in distrito:
                # Hay expansión posible, no aplica excepción
                return False

    # Distrito aislado geográficamente, excepción válida
    return es_contiguo(distrito, municipios)


# ============================================================
# PARTICIÓN INICIAL (greedy)
# ============================================================

def particion_inicial(municipios: dict[str, Municipio],
                      min_hab: int = MIN_HAB,
                      max_hab: int = MAX_HAB) -> list[list[str]]:
    """
    Construye partición inicial agrupando municipios contiguos
    hasta alcanzar el rango de población.
    Usa cola de frontera para eficiencia con muchos municipios pequeños.
    """
    import time
    t0 = time.time()
    asignado = set()
    distritos = []

    # Ordenar TODOS los municipios por población descendente (semillas grandes primero)
    semillas = sorted(municipios.keys(),
                      key=lambda x: municipios[x].poblacion, reverse=True)

    for semilla in semillas:
        if semilla in asignado:
            continue

        distrito = [semilla]
        asignado.add(semilla)
        pob = municipios[semilla].poblacion

        # Cola de frontera: vecinos no asignados del distrito actual
        frontera = set()
        for vecino in municipios[semilla].vecinos:
            if vecino not in asignado and vecino in municipios:
                frontera.add(vecino)

        # Expandir por vecindad hasta alcanzar mínimo
        while pob < min_hab and frontera:
            # Elegir el vecino con más población que quepa
            mejor = None
            mejor_pob = -1
            for candidato in frontera:
                vp = municipios[candidato].poblacion
                if pob + vp <= max_hab and vp > mejor_pob:
                    mejor = candidato
                    mejor_pob = vp

            if mejor is None:
                # Todos excederían max_hab: tomar el más pequeño
                mejor = min(frontera, key=lambda x: municipios[x].poblacion)

            frontera.discard(mejor)
            distrito.append(mejor)
            asignado.add(mejor)
            pob += municipios[mejor].poblacion

            # Actualizar frontera con vecinos del nuevo municipio
            for vecino in municipios[mejor].vecinos:
                if vecino not in asignado and vecino in municipios:
                    frontera.add(vecino)

        distritos.append(distrito)

        if len(distritos) % 50 == 0:
            elapsed = time.time() - t0
            print(f"  Distritos formados: {len(distritos)}, "
                  f"municipios asignados: {len(asignado)}/{len(municipios)}, "
                  f"tiempo: {elapsed:.1f}s")

    # Asignar municipios huérfanos al distrito vecino más cercano
    huerfanos = [mid for mid in municipios if mid not in asignado]
    for mid in huerfanos:
        mejor_dist = None
        for i, dist in enumerate(distritos):
            for dmid in dist:
                if mid in municipios[dmid].vecinos:
                    mejor_dist = i
                    break
            if mejor_dist is not None:
                break
        if mejor_dist is not None:
            distritos[mejor_dist].append(mid)
            asignado.add(mid)
        else:
            distritos.append([mid])
            asignado.add(mid)

    elapsed = time.time() - t0
    print(f"  Partición inicial: {len(distritos)} distritos en {elapsed:.1f}s")
    return distritos


# ============================================================
# OPTIMIZACIÓN: RECOCIDO SIMULADO
# ============================================================

def encontrar_frontera(particion: list[list[str]],
                       municipios: dict[str, Municipio]) -> list[tuple[int, int, str]]:
    """
    Encuentra municipios fronterizos: aquellos que tienen vecinos
    en otro distrito. Retorna (distrito_origen, distrito_destino, municipio).
    """
    # Mapa inverso: municipio -> índice de distrito
    mapa = {}
    for i, dist in enumerate(particion):
        for mid in dist:
            mapa[mid] = i

    frontera = []
    for i, dist in enumerate(particion):
        for mid in dist:
            for vecino in municipios[mid].vecinos:
                j = mapa.get(vecino)
                if j is not None and j != i:
                    frontera.append((i, j, mid))
    return frontera


def aocd(municipios: dict[str, Municipio],
         min_hab: int = MIN_HAB,
         max_hab: int = MAX_HAB,
         iteraciones: int = 50_000,
         temp_inicial: float = 500.0,
         enfriamiento: float = 0.9999,
         verbose: bool = True) -> list[list[str]]:
    """
    Recocido simulado optimizado: evaluación incremental del objetivo.
    Solo recalcula P25 de los 2 distritos afectados por cada movimiento.
    """
    import time
    t0 = time.time()

    particion = particion_inicial(municipios, min_hab, max_hab)

    # Pre-calcular P25 de cada distrito y cachear
    p25_cache = [percentil_25_distrito(d, municipios) for d in particion]
    pob_cache = [poblacion_distrito(d, municipios) for d in particion]
    mejor_valor = min(p25_cache)

    # Mapa inverso: municipio -> índice de distrito
    mapa = {}
    for i, dist in enumerate(particion):
        for mid in dist:
            mapa[mid] = i

    mejor_particion = deepcopy(particion)
    mejor_p25_cache = list(p25_cache)
    temp = temp_inicial

    aceptados = 0
    mejoras = 0

    if verbose:
        n_distritos = len(particion)
        pob_total = sum(municipios[m].poblacion for m in municipios)
        print(f"Población total: {pob_total:,}")
        print(f"Distritos iniciales: {n_distritos}")
        print(f"Objetivo inicial (min P25): {mejor_valor:,.0f}€")
        print(f"Iteraciones: {iteraciones:,}")
        print()

    for iteracion in range(iteraciones):
        # Encontrar municipios fronterizos directamente desde mapa
        # (más rápido que recalcular toda la frontera cada vez)
        mid = random.choice(list(municipios.keys()))
        origen_idx = mapa[mid]

        # Buscar si tiene vecinos en otro distrito
        destinos = set()
        for vecino in municipios[mid].vecinos:
            if vecino in mapa:
                j = mapa[vecino]
                if j != origen_idx:
                    destinos.add(j)

        if not destinos:
            continue

        destino_idx = random.choice(list(destinos))

        # No dejar distrito vacío
        if len(particion[origen_idx]) <= 1:
            continue

        # Población después del movimiento
        pob_mid = municipios[mid].poblacion
        nueva_pob_o = pob_cache[origen_idx] - pob_mid
        nueva_pob_d = pob_cache[destino_idx] + pob_mid

        # Verificar restricciones de población (rápido)
        origen_ok = (min_hab <= nueva_pob_o <= max_hab)
        destino_ok = (min_hab <= nueva_pob_d <= max_hab)

        if not origen_ok or not destino_ok:
            # Permitir excepciones geográficas solo para distritos pequeños
            if not origen_ok and nueva_pob_o < min_hab:
                # ¿El distrito origen quedaría demasiado pequeño?
                # Solo aceptar si ya era pequeño (excepción geográfica)
                if pob_cache[origen_idx] >= min_hab:
                    continue
            if not destino_ok and nueva_pob_d > max_hab:
                continue

        # Verificar contigüidad del distrito origen sin el municipio
        nuevo_origen = [m for m in particion[origen_idx] if m != mid]
        if not es_contiguo(nuevo_origen, municipios):
            continue

        # Evaluar incrementalmente: solo recalcular P25 de los 2 distritos
        nuevo_destino = particion[destino_idx] + [mid]
        nuevo_p25_o = percentil_25_distrito(nuevo_origen, municipios)
        nuevo_p25_d = percentil_25_distrito(nuevo_destino, municipios)

        # Calcular nuevo mínimo global
        nuevo_min = min(nuevo_p25_o, nuevo_p25_d)
        for k in range(len(p25_cache)):
            if k != origen_idx and k != destino_idx:
                if p25_cache[k] < nuevo_min:
                    nuevo_min = p25_cache[k]

        delta = nuevo_min - mejor_valor

        # Criterio de aceptación
        if delta > 0 or (temp > 0 and random.random() < math.exp(max(delta, -100) / max(temp, 0.01))):
            # Aplicar movimiento
            particion[origen_idx] = nuevo_origen
            particion[destino_idx] = nuevo_destino
            p25_cache[origen_idx] = nuevo_p25_o
            p25_cache[destino_idx] = nuevo_p25_d
            pob_cache[origen_idx] = nueva_pob_o
            pob_cache[destino_idx] = nueva_pob_d
            mapa[mid] = destino_idx
            aceptados += 1

            if nuevo_min > mejor_valor:
                mejor_valor = nuevo_min
                mejor_particion = deepcopy(particion)
                mejor_p25_cache = list(p25_cache)
                mejoras += 1

        temp *= enfriamiento

        if verbose and (iteracion + 1) % 5000 == 0:
            elapsed = time.time() - t0
            print(f"  iter {iteracion+1:>6,}: min P25 = {mejor_valor:,.0f}€  "
                  f"temp = {temp:.1f}  aceptados = {aceptados}  "
                  f"mejoras = {mejoras}  ({elapsed:.0f}s)")

    return mejor_particion


# ============================================================
# ANÁLISIS DE RESULTADOS
# ============================================================

def analizar_resultados(particion: list[list[str]],
                        municipios: dict[str, Municipio]) -> None:
    print("\n" + "=" * 60)
    print("RESULTADOS AOCD")
    print("=" * 60)

    n = len(particion)
    poblaciones = [poblacion_distrito(d, municipios) for d in particion]
    p25s = [percentil_25_distrito(d, municipios) for d in particion]

    print(f"\nDistritos totales: {n}")
    print(f"Población total: {sum(poblaciones):,}")
    print(f"\nPoblación por distrito:")
    print(f"  Mínima:  {min(poblaciones):>10,}")
    print(f"  Máxima:  {max(poblaciones):>10,}")
    print(f"  Media:   {sum(poblaciones)//n:>10,}")

    fuera_rango = sum(1 for p in poblaciones if p < MIN_HAB or p > MAX_HAB)
    print(f"  Fuera de rango ({MIN_HAB:,}-{MAX_HAB:,}): {fuera_rango}")

    print(f"\nPercentil 25 de renta por distrito:")
    print(f"  Mínimo (objetivo):  {min(p25s):>10,.0f}€")
    print(f"  Máximo:             {max(p25s):>10,.0f}€")
    print(f"  Media:              {sum(p25s)/n:>10,.0f}€")

    # Peor caso: coste de captura
    peor_p25 = min(p25s)
    peor_idx = p25s.index(peor_p25)
    peor_pob = poblaciones[peor_idx]
    coste_captura = peor_pob * 0.19 * peor_p25  # 19% de la población * P25
    print(f"\nAnálisis de seguridad:")
    print(f"  Distrito más vulnerable: #{peor_idx}")
    print(f"  Población: {peor_pob:,}")
    print(f"  P25 renta: {peor_p25:,.0f}€")
    print(f"  Coste teórico de captura (19% * P25): {coste_captura:,.0f}€")

    # Los 5 peores distritos
    peores = sorted(range(n), key=lambda i: p25s[i])[:5]
    print(f"\n5 distritos más vulnerables:")
    for i in peores:
        provincias = set(municipios[m].provincia for m in particion[i])
        print(f"  #{i}: P25={p25s[i]:,.0f}€  "
              f"pob={poblaciones[i]:,}  "
              f"provincias={', '.join(sorted(provincias))}")


def exportar_json(particion, municipios, ruta="aocd_resultado.json"):
    resultado = []
    for i, distrito in enumerate(particion):
        resultado.append({
            "distrito": i,
            "municipios": distrito,
            "poblacion": poblacion_distrito(distrito, municipios),
            "p25_renta": round(percentil_25_distrito(distrito, municipios), 2),
            "provincias": list(set(municipios[m].provincia for m in distrito))
        })
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    print(f"\nResultado exportado a: {ruta}")


# ============================================================
# MAIN
# ============================================================

def cargar_datos_reales(ruta_json: str) -> dict[str, Municipio]:
    """
    Carga datos reales desde JSON unificado (generado por aocd_preparar_datos.py).
    """
    with open(ruta_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    municipios = {}
    for codigo, info in data.items():
        m = Municipio(
            id=codigo,
            nombre=info['nombre'],
            poblacion=info['poblacion'],
            renta_media=info['renta_media'],
            provincia=info['provincia'],
            lat=info['lat'],
            lon=info['lon'],
        )
        m.vecinos = info['vecinos']
        municipios[codigo] = m

    return municipios


if __name__ == "__main__":
    print("AOCD — Algoritmo de Optimización de la Corruptibilidad de Distritos")
    print("=" * 60)

    # --- Detectar datos reales ---
    datos_reales = Path('data/municipios_unificados.json')
    usar_reales = datos_reales.exists()

    if usar_reales:
        print("\nCargando datos reales de España...")
        municipios = cargar_datos_reales(str(datos_reales))
        print(f"Municipios cargados: {len(municipios)}")
        iteraciones = 100_000
        archivo_salida = "aocd_resultado_espana.json"
    else:
        print("\nDatos reales no encontrados. Usando datos sintéticos...")
        municipios = generar_datos_sinteticos_espana()
        print(f"Municipios generados: {len(municipios)}")
        print("Construyendo grafo de adyacencia...")
        construir_adyacencia_por_distancia(municipios, k_vecinos=8)
        iteraciones = 30_000
        archivo_salida = "aocd_resultado.json"

    # --- Ejecutar AOCD ---
    print(f"\nEjecutando optimización ({iteraciones:,} iteraciones)...\n")
    resultado = aocd(
        municipios,
        iteraciones=iteraciones,
        temp_inicial=500.0,
        enfriamiento=0.99995 if usar_reales else 0.9998,
        verbose=True
    )

    # --- Resultados ---
    analizar_resultados(resultado, municipios)
    exportar_json(resultado, municipios, ruta=archivo_salida)
