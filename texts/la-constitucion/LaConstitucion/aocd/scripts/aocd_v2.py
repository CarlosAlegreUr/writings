#!/usr/bin/env python3
"""
AOCD v2 — Algoritmo de Optimización de la Corruptibilidad de Distritos.
Implementación de los artículos 16 (tamaño y restricciones de los distritos)
y 17 (algoritmo de delimitación, AOCD) de la Constitución sobre unidades
geográficas genéricas (municipios ó secciones censales).

Uso:
  python3 scripts/aocd_v2.py --entrada data/secciones_unificadas.json \
      --min 95000 --max 120000 --semilla 42 --salida output

Esquema de entrada (JSON, dict código -> unidad):
  {nombre, poblacion, renta_media, provincia (2 dígitos), lat, lon,
   vecinos: [códigos],
   opcionales: municipio, distrito_municipal, comarca, cusec}

Reglas implementadas (resumen; detalle en README.md, sección "Versión 2"):

  R1  Unidad con población > máx. y sin subunidades: distrito propio marcado
      "requiere subdivisión por secciones censales". No se junta con nada.
  R2  Territorio = componente conexa de una provincia sobre el grafo completo.
      Dentro de cada territorio, todo municipio conexo cuya población admita
      por sí sola una partición en rango es un bloque propio (no se cruza su
      frontera si no es estrictamente necesario, art. 16 restr. 3). El resto
      del territorio, tras apartar también las unidades R1, forma bloques por
      componentes conexas. Cada bloque se resuelve por separado. Si un bloque
      restante no puede arreglarse con transferencias dentro de la provincia,
      la provincia se reconstruye sin bloques municipales (comportamiento
      anterior) antes de cruzar provincias.
  R3  Un bloque es factible si existe K con K*min <= P <= K*max. K objetivo =
      round(P/((min+max)/2)) acotado a ese intervalo.
  R4  Bloque infactible cuyo territorio completo SÍ es factible: la
      infactibilidad es un artefacto de las ciudades sin subdividir (R1).
      Se resuelve como excepción con la desviación mínima (K que minimiza la
      desviación por distrito) y NO se cruza la frontera provincial.
  R5  Bloque infactible por estructura (su territorio tampoco es factible,
      p. ej. Soria, Ávila, Segovia, Palencia, Zamora, Teruel, Guadalajara,
      exclaves provinciales): se cruza la frontera con la MÍNIMA
      población movida, prefiriendo por este orden un bloque de la misma
      provincia, de otra provincia de la misma comunidad autónoma y, en último
      término, de otra comunidad (tabla --comunidades), (más 1.000 hab. equivalentes por unidad movida, para
      favorecer transferencias compactas) entre tres opciones: recibir unidades de un bloque
      vecino, ceder unidades a un bloque vecino, ó (solo si el bloque es
      menor que un distrito: exclaves, bolsas) unirse entero a un bloque
      vecino. Condiciones: contigüidad de ambos bloques tras el movimiento y
      que el bloque vecino no empeore (si era factible sigue siéndolo con
      holgura --holgura por distrito; si era artefacto su desviación no crece).
      Sin opción viable (Ceuta, Melilla, islas): excepción.
  R6  Dentro de un bloque las unidades se agrupan en nodos indivisibles por
      el nivel jerárquico más grueso disponible (comarca > municipio >
      distrito_municipal) cuya población no supere el máximo y sea conexo.
      Si con esos nodos no se encuentra partición en rango, se refinan los
      nodos de los distritos fuera de rango (se rompe la comarca) y se
      reintenta.
  R7  Partición inicial compacta: semillas k-means++ ponderadas por población
      (nodos >= min son semillas forzadas), crecimiento multi-fuente por
      distancia al centroide con capacidad, 3 iteraciones de Lloyd. Después,
      recocido de equilibrado con movimientos de nodos de frontera (siempre
      contiguos, comprobación BFS) y reparación por fusión/división.
  R8  Objetivo lexicográfico: (a) factibilidad: rango, contigüidad, no
      aumentar cruces de provincia ni roturas de comarca; (b) maximizar el
      P25 mínimo (softmin con temperatura --tau sobre los distritos del
      bloque, que aproxima el leximin); (c) compacidad: radio cuadrático
      medio ponderado por población al centroide, en km, con peso
      --peso-compacidad (€ de P25 por km).

El P25 se estima como percentil poblacional de las rentas medias de las
unidades (función `p25_estimado`, sustituible por `P25_FUNC`).
"""

from __future__ import annotations

import argparse
import heapq
import json
import math
import os
import random
import sys
import time
from collections import Counter, defaultdict, deque
from pathlib import Path

# ---------------------------------------------------------------------------
# Parámetros por defecto (art. 16)
# ---------------------------------------------------------------------------
MIN_HAB_DEFECTO = 95_000
MAX_HAB_DEFECTO = 120_000

# Niveles jerárquicos bajo la provincia, de más grueso a más fino. Los nodos
# indivisibles se forman por el nivel más grueso que quepa en el máximo (R6).
NIVELES = ("comarca", "municipio", "distrito_municipal")

# Penalización (habitantes equivalentes) por cada unidad movida en una
# transferencia entre provincias (R5): favorece transferencias compactas.
PENAL_UNIDAD = 1_000

# Peso (en "habitantes equivalentes") de cada rotura de coherencia en la fase
# de equilibrado: un distrito con una provincia extra, una comarca repartida
# entre dos distritos, etc.
PESOS_COHERENCIA = {
    "provincia": 60_000,
    "comarca": 25_000,
    "municipio": 12_000,
    "distrito_municipal": 5_000,
}


def log(msg: str) -> None:
    print(f"[AOCD-v2] {msg}", flush=True)


def cargar_comunidades(ruta: str) -> dict[str, str]:
    """Tabla provincia (2 dígitos) -> comunidad autónoma. Si falta, todas en una."""
    import csv
    tabla: dict[str, str] = {}
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                tabla[str(row["provincia"]).zfill(2)] = str(row["comunidad"])
    except FileNotFoundError:
        log(f"AVISO: no existe {ruta}; sin escalón autonómico (todas las provincias en una comunidad)")
    return tabla


# ---------------------------------------------------------------------------
# Geometría
# ---------------------------------------------------------------------------
R_TIERRA_KM = 6371.0088


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = p2 - p1
    dlmb = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2) ** 2
    return 2 * R_TIERRA_KM * math.asin(math.sqrt(a))


def proyectar_km(lat: float, lon: float, lat0: float) -> tuple[float, float]:
    """Proyección equirrectangular local (km). Suficiente para compacidad."""
    x = math.radians(lon) * R_TIERRA_KM * math.cos(math.radians(lat0))
    y = math.radians(lat) * R_TIERRA_KM
    return x, y


# ---------------------------------------------------------------------------
# Unidades
# ---------------------------------------------------------------------------
class Unidad:
    __slots__ = ("id", "nombre", "pob", "renta", "prov", "lat", "lon",
                 "vecinos", "grupos", "x", "y")

    def __init__(self, uid: str, info: dict):
        self.id = uid
        self.nombre = str(info.get("nombre", uid))
        self.pob = int(info["poblacion"])
        self.renta = float(info["renta_media"])
        self.prov = str(info["provincia"]).zfill(2)
        self.lat = float(info["lat"])
        self.lon = float(info["lon"])
        self.vecinos: list[str] = []
        # Claves de grupo por nivel (None si el campo no existe).
        self.grupos = {"provincia": self.prov}
        for nivel in NIVELES:
            v = info.get(nivel)
            self.grupos[nivel] = (str(v) if v not in (None, "") else None)
        self.x = 0.0
        self.y = 0.0


def cargar_unidades(ruta: str) -> dict[str, Unidad]:
    with open(ruta, "r", encoding="utf-8") as f:
        data = json.load(f)
    unidades: dict[str, Unidad] = {}
    for uid, info in data.items():
        unidades[uid] = Unidad(uid, info)
    # Vecinos: solo los presentes, simetrizados, sin auto-bucles.
    for uid, info in data.items():
        for v in info.get("vecinos", []):
            if v != uid and v in unidades:
                unidades[uid].vecinos.append(v)
    for u in unidades.values():
        for v in u.vecinos:
            if u.id not in unidades[v].vecinos:
                unidades[v].vecinos.append(u.id)
    for u in unidades.values():
        u.vecinos = sorted(set(u.vecinos))
    # Proyección local común (España cabe con error de pocos % en x).
    lat0 = sum(u.lat for u in unidades.values()) / max(1, len(unidades))
    for u in unidades.values():
        u.x, u.y = proyectar_km(u.lat, u.lon, lat0)
    return unidades


def reparar_aislados(unidades: dict[str, Unidad], radio_km: float) -> list[dict]:
    """
    Unidades sin vecinos (islas pequeñas, enclaves, defectos de geometría):
    se les añade una adyacencia artificial con la unidad más cercana de su
    misma provincia si está a menos de `radio_km`. Devuelve el registro.
    """
    registro = []
    por_prov: dict[str, list[Unidad]] = defaultdict(list)
    for u in unidades.values():
        por_prov[u.prov].append(u)
    for u in unidades.values():
        if u.vecinos:
            continue
        mejor, dmin = None, float("inf")
        for w in por_prov[u.prov]:
            if w.id == u.id:
                continue
            d = haversine_km(u.lat, u.lon, w.lat, w.lon)
            if d < dmin:
                mejor, dmin = w, d
        if mejor is not None and dmin <= radio_km:
            u.vecinos.append(mejor.id)
            mejor.vecinos.append(u.id)
            registro.append({"unidad": u.id, "nombre": u.nombre, "con": mejor.id,
                             "nombre_con": mejor.nombre, "km": round(dmin, 1)})
        else:
            registro.append({"unidad": u.id, "nombre": u.nombre, "con": None,
                             "nombre_con": None,
                             "km": (round(dmin, 1) if mejor else None)})
    return registro


# ---------------------------------------------------------------------------
# P25 (sustituible)
# ---------------------------------------------------------------------------
def p25_estimado(pares) -> float:
    """
    Percentil 25 poblacional de las rentas medias de las unidades:
    se ordenan las unidades por renta media y se toma la renta de la unidad en
    la que la población acumulada alcanza el 25 % del total. Es la misma
    estimación de la v1. Con datos de distribución por sección censal puede
    sustituirse asignando otra función a `P25_FUNC` con la misma firma
    (lista de pares (renta, poblacion) -> float).
    """
    pares = sorted(pares)
    total = 0
    for _, p in pares:
        total += p
    objetivo = total * 0.25
    acum = 0
    for renta, p in pares:
        acum += p
        if acum >= objetivo:
            return renta
    return pares[-1][0] if pares else 0.0


P25_FUNC = p25_estimado


# ---------------------------------------------------------------------------
# Grafo de unidades
# ---------------------------------------------------------------------------
def componentes(ids, vecinos_de) -> list[list[str]]:
    """Componentes conexas del subgrafo inducido por `ids` (iterable)."""
    pendientes = set(ids)
    salida = []
    while pendientes:
        inicio = min(pendientes)   # determinista (independiente del hash de cadenas)
        comp = [inicio]
        pendientes.discard(inicio)
        cola = deque([inicio])
        while cola:
            a = cola.popleft()
            for v in vecinos_de(a):
                if v in pendientes:
                    pendientes.discard(v)
                    comp.append(v)
                    cola.append(v)
        salida.append(sorted(comp))
    return salida


def es_conexo(ids_set: set, vecinos_de) -> bool:
    if len(ids_set) <= 1:
        return True
    inicio = next(iter(ids_set))
    visto = {inicio}
    cola = deque([inicio])
    while cola:
        a = cola.popleft()
        for v in vecinos_de(a):
            if v in ids_set and v not in visto:
                visto.add(v)
                cola.append(v)
    return len(visto) == len(ids_set)


# ---------------------------------------------------------------------------
# Factibilidad de rango
# ---------------------------------------------------------------------------
def ks_factibles(P: int, lo: int, hi: int) -> list[int]:
    """K tales que K*lo <= P <= K*hi."""
    if P <= 0:
        return []
    k_min = max(1, math.ceil(P / hi))
    k_max = P // lo
    return list(range(k_min, k_max + 1)) if k_max >= k_min else []


def k_objetivo(P: int, lo: int, hi: int) -> int:
    ks = ks_factibles(P, lo, hi)
    k0 = max(1, round(P / ((lo + hi) / 2)))
    if not ks:
        return k0
    return min(ks, key=lambda k: (abs(k - k0), k))


def desviacion_minima(P: int, lo: int, hi: int) -> tuple[int, int]:
    """
    (K, desviación por distrito) que minimiza la desviación respecto al rango
    cuando no hay K factible. Si lo hay, desviación 0.
    """
    ks = ks_factibles(P, lo, hi)
    if ks:
        return k_objetivo(P, lo, hi), 0
    mejor = None
    for k in range(1, max(2, math.ceil(P / lo) + 1)):
        media = P / k
        dev = max(0.0, lo - media, media - hi)
        cand = (dev, k)
        if mejor is None or cand < mejor:
            mejor = cand
    return mejor[1], int(round(mejor[0]))


def desviacion_con_holgura(P: int, lo: int, hi: int, holgura: int) -> int:
    """Desviación mínima por distrito exigiendo holgura por distrito."""
    return desviacion_minima(P, lo + holgura, hi - holgura)[1]


# ---------------------------------------------------------------------------
# Nombres de provincia (solo para etiquetas; códigos INE)
# ---------------------------------------------------------------------------
NOMBRES_PROV = {
    "01": "Araba/Álava", "02": "Albacete", "03": "Alicante/Alacant", "04": "Almería",
    "05": "Ávila", "06": "Badajoz", "07": "Illes Balears", "08": "Barcelona",
    "09": "Burgos", "10": "Cáceres", "11": "Cádiz", "12": "Castellón/Castelló",
    "13": "Ciudad Real", "14": "Córdoba", "15": "A Coruña", "16": "Cuenca",
    "17": "Girona", "18": "Granada", "19": "Guadalajara", "20": "Gipuzkoa",
    "21": "Huelva", "22": "Huesca", "23": "Jaén", "24": "León", "25": "Lleida",
    "26": "La Rioja", "27": "Lugo", "28": "Madrid", "29": "Málaga", "30": "Murcia",
    "31": "Navarra", "32": "Ourense", "33": "Asturias", "34": "Palencia",
    "35": "Las Palmas", "36": "Pontevedra", "37": "Salamanca",
    "38": "Santa Cruz de Tenerife", "39": "Cantabria", "40": "Segovia",
    "41": "Sevilla", "42": "Soria", "43": "Tarragona", "44": "Teruel",
    "45": "Toledo", "46": "Valencia/València", "47": "Valladolid", "48": "Bizkaia",
    "49": "Zamora", "50": "Zaragoza", "51": "Ceuta", "52": "Melilla",
}


def nombre_prov(cod: str) -> str:
    return f"{cod} {NOMBRES_PROV.get(cod, '')}".strip()


# ---------------------------------------------------------------------------
# Bloques (R1–R5)
# ---------------------------------------------------------------------------
class Bloque:
    _seq = 0

    def __init__(self, nombre: str, unidades: set[str], prov: str, tipo: str):
        Bloque._seq += 1
        self.id = Bloque._seq
        self.nombre = nombre
        self.unidades = set(unidades)
        self.prov = prov
        self.tipo = tipo          # normal | ciudad | artefacto | estructural | aislado | sin_donante | unido
        self.motivo: str | None = None
        self.cruces: list[dict] = []   # justificaciones de cruce provincial
        self.K = 1
        self.lo = 0
        self.hi = 0
        self.notas: list[str] = []
        self.municipal = False     # bloque = un municipio que cabe solo (R2)

    def pob(self, U: dict[str, Unidad]) -> int:
        return sum(U[u].pob for u in self.unidades)

    def __repr__(self):
        return f"Bloque({self.nombre}, {self.tipo}, {len(self.unidades)} u.)"


def fmt(n) -> str:
    return f"{int(round(n)):,}".replace(",", ".")


def crecer_transferencia(fuente: set[str], destino: set[str], necesidad: int,
                         U: dict[str, Unidad], valido, max_unidades: int = 100):
    """
    Conjunto T ⊆ fuente, contiguo y adyacente a `destino`, con población
    >= necesidad y coste mínimo (población + PENAL_UNIDAD por unidad). Desde
    cada unidad de la frontera se crece de dos maneras: "ajuste" (la unidad
    adyacente cuya población más se acerca a lo que falta) y "mancha" (la
    más poblada de las adyacentes cercanas a la semilla que no exceden lo que
    falta). Se devuelve el mejor candidato que supere `valido(T)`.
    """
    semillas = sorted(u for u in fuente if any(v in destino for v in U[u].vecinos))
    mejor = None
    for s in semillas:
        for modo in ("ajuste", "mancha"):
            S = {s}
            pS = U[s].pob
            ok = True
            xs, ys = U[s].x, U[s].y
            while pS < necesidad:
                cand = set()
                for u in S:
                    for v in U[u].vecinos:
                        if v in fuente and v not in S:
                            cand.add(v)
                if not cand or len(S) >= max_unidades:
                    ok = False
                    break
                rem = necesidad - pS
                if modo == "ajuste":
                    # la unidad cuya población más se acerca a lo que falta
                    v = min(cand, key=lambda c: (abs(U[c].pob - rem), -U[c].pob, c))
                else:
                    # mancha compacta: la más poblada de las cercanas que no exceden
                    sin_exceso = [c for c in cand if U[c].pob <= rem]
                    if sin_exceso:
                        dist = {c: math.hypot(U[c].x - xs, U[c].y - ys) for c in sin_exceso}
                        dmin = min(dist.values())
                        cercanos = [c for c in sin_exceso if dist[c] <= 1.5 * dmin + 5.0]
                        v = max(cercanos, key=lambda c: (U[c].pob, -dist[c], c))
                    else:
                        v = min(cand, key=lambda c: (U[c].pob - rem, c))
                S.add(v)
                pS += U[v].pob
            if not ok:
                continue
            clave = (pS + PENAL_UNIDAD * len(S), pS, len(S))
            if mejor is not None and clave >= mejor[0]:
                continue
            if valido(S):
                mejor = (clave, S)
    return mejor[1] if mejor else None


def nombre_municipio(U: dict[str, Unidad], ids) -> str:
    """Nombre del municipio a partir de sus unidades ('X sección NNNNN' -> 'X')."""
    n = U[min(ids)].nombre
    return n.split(" sección")[0].strip()


def construir_bloques(U: dict[str, Unidad], lo: int, hi: int, holgura: int,
                      transferir: bool = True, carve: bool = True,
                      ca_de: dict[str, str] | None = None) -> tuple[list[Bloque], dict]:
    """Aplica R1–R5 y devuelve los bloques a resolver y notas para el informe."""
    ca_de = ca_de or {}
    notas = {"ciudades": [], "artefactos": [], "transferencias": [],
             "aislados": [], "territorios_infactibles": [], "municipales": [],
             "provincias_sin_bloques_municipales": []}

    # R1: unidades mayores que el máximo (solo puede ocurrir sin subunidades).
    ciudades = {u.id for u in U.values() if u.pob > hi}
    bloques_ciudad: list[Bloque] = []
    for uid in sorted(ciudades, key=lambda i: -U[i].pob):
        b = Bloque(f"{U[uid].nombre} ({nombre_prov(U[uid].prov)})", {uid}, U[uid].prov, "ciudad")
        b.motivo = (f"Unidad de {fmt(U[uid].pob)} hab. > máximo {fmt(hi)}: "
                    f"requiere subdivisión por secciones censales")
        bloques_ciudad.append(b)
        notas["ciudades"].append({"id": uid, "nombre": U[uid].nombre, "poblacion": U[uid].pob,
                                  "provincia": U[uid].prov})

    por_prov: dict[str, list[str]] = defaultdict(list)
    for u in U.values():
        por_prov[u.prov].append(u.id)

    def clave_mun(uid: str) -> str:
        return U[uid].grupos.get("municipio") or uid

    def bloques_de_provincia(prov: str, con_municipales: bool) -> list[Bloque]:
        """R2 para una provincia: bloques municipales (si procede) + resto por componentes."""
        salida: list[Bloque] = []
        ids_prov = set(por_prov[prov])
        vec_prov = lambda a, ids_prov=ids_prov: (v for v in U[a].vecinos if v in ids_prov)
        territorios = componentes(ids_prov, vec_prov)
        territorios.sort(key=lambda c: -sum(U[u].pob for u in c))
        for ti, terr in enumerate(territorios):
            P_terr = sum(U[u].pob for u in terr)
            factible_terr = bool(ks_factibles(P_terr, lo + holgura, hi - holgura))
            hay_ciudades_r1 = bool(ciudades & set(terr))
            resto = set(terr) - ciudades
            if not resto:
                continue
            sufijo_t = "" if len(territorios) == 1 else f" T{ti + 1}"
            # Bloques municipales: municipios conexos que caben solos en el rango.
            if con_municipales:
                por_mun: dict[str, set[str]] = defaultdict(set)
                for u in resto:
                    por_mun[clave_mun(u)].add(u)
                for mk in sorted(por_mun):
                    us = por_mun[mk]
                    if len(us) == 1 and U[next(iter(us))].grupos.get("municipio") is None:
                        continue  # datos municipales: la unidad ya es el municipio entero
                    P_m = sum(U[u].pob for u in us)
                    if not ks_factibles(P_m, lo, hi):
                        continue
                    comps = componentes(us, lambda a, us=us: (v for v in U[a].vecinos if v in us))
                    if len(comps) != 1:
                        continue
                    b = Bloque(f"{nombre_municipio(U, us)} ({nombre_prov(prov)}{sufijo_t})", us, prov, "normal")
                    b.municipal = True
                    salida.append(b)
                    resto -= us
                    notas["municipales"].append({"bloque": b.nombre, "poblacion": P_m, "unidades": len(us)})
            if not resto:
                continue
            vec_resto = lambda a, resto=resto: (v for v in U[a].vecinos if v in resto)
            subs = componentes(resto, vec_resto)
            subs.sort(key=lambda c: -sum(U[u].pob for u in c))
            for si, sub in enumerate(subs):
                P = sum(U[u].pob for u in sub)
                sufijo_s = "" if len(subs) == 1 else f" B{si + 1}"
                nombre = f"{nombre_prov(prov)}{sufijo_t}{sufijo_s}"
                if ks_factibles(P, lo, hi):
                    tipo = "normal"
                elif factible_terr and hay_ciudades_r1:
                    tipo = "artefacto"
                else:
                    tipo = "estructural"
                b = Bloque(nombre, sub, prov, tipo)
                if tipo == "artefacto":
                    cortantes = sorted({U[v].nombre for u in sub for v in U[u].vecinos
                                        if v in ciudades}, key=str)
                    b.motivo = (f"Bloque de {fmt(P)} hab. sin partición en rango; la provincia "
                                f"completa ({fmt(P_terr)} hab.) sí la admite: artefacto de las "
                                f"unidades sin subdividir (adyacentes: "
                                f"{', '.join(cortantes) or 'ninguna'}). "
                                f"Se resolverá con secciones censales; no se cruza provincia")
                    notas["artefactos"].append({"bloque": nombre, "poblacion": P, "unidades": len(sub),
                                                "ciudades": cortantes})
                if not factible_terr and tipo == "estructural":
                    notas["territorios_infactibles"].append({"bloque": nombre, "poblacion": P,
                                                             "territorio": P_terr})
                salida.append(b)
        return salida

    bloques: list[Bloque] = list(bloques_ciudad)
    con_municipales: dict[str, bool] = {}
    for prov in sorted(por_prov):
        con_municipales[prov] = carve
        bloques.extend(bloques_de_provincia(prov, carve))

    bloque_de: dict[str, Bloque] = {}
    por_id: dict[int, Bloque] = {}

    def reindexar():
        bloque_de.clear()
        por_id.clear()
        for b in bloques:
            por_id[b.id] = b
            for u in b.unidades:
                bloque_de[u] = b

    reindexar()

    def vecinos_bloque(b: Bloque) -> Counter:
        c = Counter()
        for u in b.unidades:
            for v in U[u].vecinos:
                ob = bloque_de[v]
                if ob is not b:
                    c[ob.id] += 1
        return c

    def nivel_cruce(B: Bloque, D: Bloque) -> int:
        """0 = misma provincia (cruce municipal/comarcal), 1 = misma comunidad, 2 = otra comunidad."""
        if B.prov == D.prov:
            return 0
        if ca_de.get(B.prov) is not None and ca_de.get(B.prov) == ca_de.get(D.prov):
            return 1
        return 2

    NOMBRE_NIVEL = {0: "cruce dentro de la provincia", 1: "cruce provincial dentro de la misma comunidad",
                    2: "cruce entre comunidades autónomas"}

    def dev_h(P):
        return desviacion_con_holgura(P, lo, hi, holgura)

    def aceptable(D: Bloque, P_despues: int) -> bool:
        if D.tipo == "normal":
            return bool(ks_factibles(P_despues, lo + holgura, hi - holgura))
        return dev_h(P_despues) <= dev_h(D.pob(U))

    def mejor_opcion(B: Bloque, max_nivel: int):
        P = B.pob(U)
        vec = vecinos_bloque(B)
        opciones = []
        K_high = max(1, math.ceil(P / lo))
        need_recv = K_high * (lo + holgura) - P
        K_low = P // hi
        need_give = P - K_low * (hi - holgura) if K_low >= 1 else None
        for did, compartidas in vec.items():
            D = por_id[did]
            if D.tipo in ("ciudad", "unido"):
                continue
            nivel = nivel_cruce(B, D)
            if nivel > max_nivel:
                continue
            PD = D.pob(U)
            # recibir
            if need_recv > 0:
                T = crecer_transferencia(
                    D.unidades, B.unidades, need_recv, U,
                    lambda S, D=D, PD=PD: (aceptable(D, PD - sum(U[u].pob for u in S))
                                           and es_conexo(D.unidades - S, lambda a: U[a].vecinos)))
                if T is not None:
                    pT = sum(U[u].pob for u in T)
                    if ks_factibles(P + pT, lo + holgura, hi - holgura):
                        opciones.append((nivel, pT, len(T), -compartidas, "recibir", D, T))
            # ceder
            if need_give is not None and need_give > 0:
                T = crecer_transferencia(
                    B.unidades, D.unidades, need_give, U,
                    lambda S, D=D, PD=PD, P=P: (
                        bool(ks_factibles(P - sum(U[u].pob for u in S), lo + holgura, hi - holgura))
                        and aceptable(D, PD + sum(U[u].pob for u in S))
                        and es_conexo(B.unidades - S, lambda a: U[a].vecinos)))
                if T is not None:
                    pT = sum(U[u].pob for u in T)
                    opciones.append((nivel, pT, len(T), -compartidas, "ceder", D, T))
            # unir: bloques menores que un distrito (exclaves, bolsas) siempre que el
            # vecino lo admita; bloques mayores solo como último recurso.
            if aceptable(D, PD + P) and (P < lo or ks_factibles(PD + P, lo + holgura, hi - holgura)):
                opciones.append((nivel, min(P, PD), len(B.unidades), -compartidas, "unir", D, set(B.unidades)))
        if not opciones:
            if os.environ.get("AOCD_DEBUG"):
                log(f"    [opciones] {B.nombre} ({fmt(P)}): ninguna viable hasta nivel {max_nivel}; vecinos "
                    f"{[por_id[d].nombre for d in vec]}")
            return None
        # Orden: nivel de cruce (provincia < comunidad < otra comunidad), después coste =
        # población movida + penalización por unidad movida (transferencias compactas).
        opciones.sort(key=lambda o: (o[0], o[1] + PENAL_UNIDAD * o[2], o[1], o[3], o[5].id))
        if os.environ.get("AOCD_DEBUG"):
            log(f"    [opciones] {B.nombre} ({fmt(P)} hab., necesita recibir {fmt(need_recv)}"
                f"{'' if need_give is None else ' ó ceder ' + fmt(need_give)}): "
                + "; ".join(f"n{o[0]} {o[4]} {o[5].nombre} {fmt(o[1])}/{o[2]}u"
                            for o in opciones[:6]))
        return opciones[0]

    def ejecutar_transferencias(max_nivel: int):
        """R5: resuelve bloques estructurales con transferencias hasta el nivel de cruce dado."""
        while True:
            estructurales = [b for b in bloques if b.tipo == "estructural"]
            if not estructurales:
                break
            candidatos = []
            for B in estructurales:
                op = mejor_opcion(B, max_nivel)
                if op is not None:
                    candidatos.append((op[0], op[1] + PENAL_UNIDAD * op[2], op[1], B.id, op, B))
            if not candidatos:
                break
            candidatos.sort(key=lambda c: (c[0], c[1], c[2], c[3]))
            _, _, _, _, op, B = candidatos[0]
            nivel, pT, nT, _, tipo, D, T = op
            P_antes = B.pob(U)
            nombres = sorted(U[u].nombre for u in T)
            lista = ", ".join(nombres[:6]) + (f" … (+{len(nombres) - 6})" if len(nombres) > 6 else "")
            base = (f"el bloque {B.nombre} ({fmt(P_antes)} hab.) no admite partición en "
                    f"[{fmt(lo)}, {fmt(hi)}] (art. 16, restr. 3: {NOMBRE_NIVEL[nivel]}, estrictamente "
                    f"necesario; opción de mínima población movida)")
            if tipo == "recibir":
                for u in T:
                    D.unidades.discard(u)
                    B.unidades.add(u)
                    bloque_de[u] = B
                texto = f"{B.nombre} recibe {fmt(pT)} hab. ({nT} unidades: {lista}) de {D.nombre}: {base}"
                B.cruces.append({"tipo": "recibir", "de": D.nombre, "a": B.nombre, "poblacion": pT,
                                 "nivel": nivel, "unidades": sorted(T), "texto": texto, "ids": sorted(T)})
                D.notas.append(f"Cede {fmt(pT)} hab. ({nT} unidades) a {B.nombre}")
                B.tipo = "normal"
            elif tipo == "ceder":
                for u in T:
                    B.unidades.discard(u)
                    D.unidades.add(u)
                    bloque_de[u] = D
                texto = f"{B.nombre} cede {fmt(pT)} hab. ({nT} unidades: {lista}) a {D.nombre}: {base}"
                D.cruces.append({"tipo": "ceder", "de": B.nombre, "a": D.nombre, "poblacion": pT,
                                 "nivel": nivel, "unidades": sorted(T), "texto": texto, "ids": sorted(T)})
                B.notas.append(f"Cede {fmt(pT)} hab. ({nT} unidades) a {D.nombre}")
                B.tipo = "normal"
            else:  # unir
                for u in B.unidades:
                    D.unidades.add(u)
                    bloque_de[u] = D
                texto = (f"{B.nombre} ({fmt(P_antes)} hab., {nT} unidades: {lista}) se une a {D.nombre} "
                         f"({fmt(D.pob(U) - P_antes)} hab.): {base}")
                D.cruces.append({"tipo": "unir", "de": B.nombre, "a": D.nombre, "poblacion": P_antes,
                                 "nivel": nivel, "unidades": sorted(B.unidades), "texto": texto})
                if P_antes >= lo:
                    D.nombre = f"{D.nombre}+{B.nombre}"
                if B.municipal or D.municipal:
                    D.municipal = False
                B.unidades = set()
                B.tipo = "unido"
            if tipo == "recibir":
                id_origen, id_destino = D.id, B.id
            else:
                id_origen, id_destino = B.id, D.id
            notas["transferencias"].append({"tipo": tipo, "nivel": nivel, "texto": texto, "poblacion": pT,
                                            "unidades": nT, "ids": sorted(T),
                                            "id_origen": id_origen, "id_destino": id_destino})
            log(f"  Transferencia (nivel {nivel}): {texto}")
            for b in bloques:
                if b.tipo in ("artefacto", "estructural") and ks_factibles(b.pob(U), lo, hi):
                    b.tipo = "normal"

    if transferir:
        # Primero solo dentro de cada provincia (cruce municipal/comarcal).
        ejecutar_transferencias(0)
        if carve:
            # Provincias con bloques municipales que no se han podido arreglar sin cruzar
            # provincia: se reconstruyen sin bloques municipales (comportamiento anterior).
            # Solo cuentan los bloques estructurales que tienen vecinos en su misma provincia
            # (los territorios aislados, islas y exclaves, no se arreglan deshaciendo nada).
            fallidas_set = set()
            for b in bloques:
                if b.tipo != "estructural":
                    continue
                if not any(ob.municipal for ob in bloques if ob.prov == b.prov):
                    continue
                if any(por_id[d].prov == b.prov for d in vecinos_bloque(b)):
                    fallidas_set.add(b.prov)
            fallidas = sorted(fallidas_set)
            for prov in fallidas:
                bloques[:] = [b for b in bloques if not (b.prov == prov and b.tipo != "ciudad")]
                notas["transferencias"] = [tr for tr in notas["transferencias"]
                                           if por_id.get(tr["id_origen"]) is None or por_id[tr["id_origen"]].prov != prov]
                bloques.extend(bloques_de_provincia(prov, False))
                con_municipales[prov] = False
                notas["provincias_sin_bloques_municipales"].append(nombre_prov(prov))
                log(f"  Provincia {nombre_prov(prov)}: sin solución con bloques municipales; "
                    f"se reconstruye como bloque provincial")
            reindexar()
            # Unidades que hubieran cambiado de bloque dentro de esa provincia vuelven a
            # su territorio: la reconstrucción parte de por_prov, así que ya están.
            ejecutar_transferencias(0)
        # Después, cruzando provincias: misma comunidad antes que otra comunidad.
        ejecutar_transferencias(2)

    # Deshacer transferencias que han quedado innecesarias (p. ej. un bloque que
    # recibió población y después se unió a otro): se revierten, de la última a la
    # primera, las que dejan factibles con holgura a ambos bloques.
    for tr in reversed(notas["transferencias"]):
        if tr["tipo"] not in ("recibir", "ceder"):
            continue
        origen = por_id.get(tr["id_origen"])
        destino = por_id.get(tr["id_destino"])
        if origen is None or destino is None or origen.tipo == "unido" or destino.tipo == "unido":
            continue
        T = set(tr["ids"])
        if not T <= destino.unidades:
            continue
        P_o, P_d = origen.pob(U), destino.pob(U)
        pT = sum(U[u].pob for u in T)
        if not (ks_factibles(P_o + pT, lo + holgura, hi - holgura)
                and ks_factibles(P_d - pT, lo + holgura, hi - holgura)):
            continue
        if not es_conexo(destino.unidades - T, lambda a: U[a].vecinos):
            continue
        for u in T:
            destino.unidades.discard(u)
            origen.unidades.add(u)
            bloque_de[u] = origen
        destino.cruces = [c for c in destino.cruces if c.get("ids") != tr["ids"]]
        tr["revertida"] = True
        log(f"  Transferencia revertida por innecesaria: {tr['texto'][:90]} …")
    notas["transferencias"] = [tr for tr in notas["transferencias"] if not tr.get("revertida")]

    for b in bloques:
        if b.tipo == "estructural":
            P = b.pob(U)
            if not vecinos_bloque(b):
                b.tipo = "aislado"
                b.motivo = (f"Territorio aislado ({fmt(P)} hab.) sin vecinos geográficos: "
                            f"imposibilidad geográfica (art. 16, restr. 4), desviación mínima")
            else:
                b.tipo = "sin_donante"
                b.motivo = (f"Bloque de {fmt(P)} hab. sin partición en rango y sin bloque vecino "
                            f"que admita transferencia viable: desviación mínima (art. 16, restr. 4)")
            notas["aislados"].append({"bloque": b.nombre, "poblacion": P, "tipo": b.tipo})

    bloques[:] = [b for b in bloques if b.tipo != "unido"]

    # K y rango efectivo de cada bloque.
    for b in bloques:
        P = b.pob(U)
        if b.tipo == "ciudad":
            b.K, b.lo, b.hi = 1, lo, hi
        elif b.tipo == "normal":
            b.K, b.lo, b.hi = k_objetivo(P, lo, hi), lo, hi
        else:
            K, _ = desviacion_minima(P, lo, hi)
            media = P / K
            tol = max(2_000, 0.03 * media)
            b.K = K
            b.lo = min(lo, int(math.floor(media - tol)))
            b.hi = max(hi, int(math.ceil(media + tol)))
    return bloques, notas


# ---------------------------------------------------------------------------
# Nodos indivisibles (R6)
# ---------------------------------------------------------------------------
class Nodo:
    __slots__ = ("idx", "unidades", "pob", "pares", "x", "y", "sx", "sy", "sxx", "syy",
                 "prov", "grupos", "nivel", "adj")

    def __init__(self, idx: int, unidades: list[str], U: dict[str, Unidad], nivel: str):
        self.idx = idx
        self.unidades = list(unidades)
        self.nivel = nivel
        self.pob = sum(U[u].pob for u in unidades)
        self.pares = sorted((U[u].renta, U[u].pob) for u in unidades)
        self.sx = sum(U[u].pob * U[u].x for u in unidades)
        self.sy = sum(U[u].pob * U[u].y for u in unidades)
        self.sxx = sum(U[u].pob * U[u].x * U[u].x for u in unidades)
        self.syy = sum(U[u].pob * U[u].y * U[u].y for u in unidades)
        if self.pob > 0:
            self.x, self.y = self.sx / self.pob, self.sy / self.pob
        else:
            self.x = sum(U[u].x for u in unidades) / len(unidades)
            self.y = sum(U[u].y for u in unidades) / len(unidades)
        provs = {U[u].prov for u in unidades}
        self.prov = Counter(U[u].prov for u in unidades).most_common(1)[0][0]
        self.grupos: dict[str, tuple | None] = {}
        self.grupos["provincia"] = (self.prov,) if len(provs) == 1 else None
        for n in NIVELES:
            claves = {clave_grupo(U[u], n) for u in unidades}
            k = next(iter(claves))
            self.grupos[n] = k if (len(claves) == 1 and k is not None) else None
        self.adj: list[int] = []


def clave_grupo(u: Unidad, nivel: str):
    if u.grupos.get(nivel) is None:
        return None
    claves = [u.prov]
    for n in NIVELES:
        claves.append(u.grupos.get(n) or "")
        if n == nivel:
            break
    return tuple(claves)


def construir_nodos(ids: set[str], U: dict[str, Unidad], hi: int,
                    refinados: set[tuple]) -> list[Nodo]:
    """
    Agrupa las unidades del bloque por el nivel más grueso cuyo grupo tenga
    población <= hi y sea conexo. Los grupos cuya clave esté en `refinados`
    se rompen al siguiente nivel.
    """
    grupos: list[tuple[list[str], str]] = []

    def procesar(sub: set[str], i_nivel: int):
        if i_nivel >= len(NIVELES):
            for u in sorted(sub):
                grupos.append(([u], "unidad"))
            return
        nivel = NIVELES[i_nivel]
        por_clave: dict[tuple, set[str]] = defaultdict(set)
        sueltas = set()
        for u in sub:
            k = clave_grupo(U[u], nivel)
            if k is None:
                sueltas.add(u)
            else:
                por_clave[k].add(u)
        if sueltas:
            procesar(sueltas, i_nivel + 1)
        for k in sorted(por_clave):
            miembros = por_clave[k]
            if (nivel, k) in refinados:
                procesar(miembros, i_nivel + 1)
                continue
            comps = componentes(miembros, lambda a, m=miembros: (v for v in U[a].vecinos if v in m))
            for comp in comps:
                if sum(U[u].pob for u in comp) <= hi:
                    grupos.append((sorted(comp), nivel))
                else:
                    procesar(set(comp), i_nivel + 1)

    procesar(set(ids), 0)
    nodos = [Nodo(i, us, U, nivel) for i, (us, nivel) in enumerate(grupos)]
    nodo_de: dict[str, int] = {}
    for nd in nodos:
        for u in nd.unidades:
            nodo_de[u] = nd.idx
    for nd in nodos:
        vec = set()
        for u in nd.unidades:
            for v in U[u].vecinos:
                j = nodo_de.get(v)
                if j is not None and j != nd.idx:
                    vec.add(j)
        nd.adj = sorted(vec)
    return nodos


# ---------------------------------------------------------------------------
# Estado de una partición de nodos en K distritos
# ---------------------------------------------------------------------------
class Estado:
    def __init__(self, nodos: list[Nodo], K: int, asig: list[int]):
        self.nodos = nodos
        self.K = K
        self.n = len(nodos)
        self.asig = list(asig)
        self.miembros: list[set[int]] = [set() for _ in range(K)]
        self.pob = [0] * K
        self.sx = [0.0] * K
        self.sy = [0.0] * K
        self.sxx = [0.0] * K
        self.syy = [0.0] * K
        self.prov_cnt: list[Counter] = [Counter() for _ in range(K)]
        self.grupo_cnt: dict[tuple, Counter] = defaultdict(Counter)
        for i, d in enumerate(self.asig):
            self._add(i, d)
        self.con_p25 = getattr(self, "con_p25", False)
        self.p25 = [self.calc_p25(d) for d in range(K)] if self.con_p25 else [0.0] * K

    # -- agregados ---------------------------------------------------------
    def _add(self, i: int, d: int):
        nd = self.nodos[i]
        self.miembros[d].add(i)
        self.pob[d] += nd.pob
        self.sx[d] += nd.sx
        self.sy[d] += nd.sy
        self.sxx[d] += nd.sxx
        self.syy[d] += nd.syy
        self.prov_cnt[d][nd.prov] += 1
        for nivel, k in nd.grupos.items():
            if k is not None and nivel != "provincia":
                self.grupo_cnt[(nivel, k)][d] += 1

    def _del(self, i: int, d: int):
        nd = self.nodos[i]
        self.miembros[d].discard(i)
        self.pob[d] -= nd.pob
        self.sx[d] -= nd.sx
        self.sy[d] -= nd.sy
        self.sxx[d] -= nd.sxx
        self.syy[d] -= nd.syy
        self.prov_cnt[d][nd.prov] -= 1
        if self.prov_cnt[d][nd.prov] == 0:
            del self.prov_cnt[d][nd.prov]
        for nivel, k in nd.grupos.items():
            if k is not None and nivel != "provincia":
                c = self.grupo_cnt[(nivel, k)]
                c[d] -= 1
                if c[d] == 0:
                    del c[d]

    def snapshot(self) -> list[int]:
        return list(self.asig)

    def restaurar(self, asig: list[int]):
        self.__init__(self.nodos, self.K, asig)

    def mover(self, i: int, d2: int):
        d1 = self.asig[i]
        self._del(i, d1)
        self._add(i, d2)
        self.asig[i] = d2
        if self.con_p25:
            self.p25[d1] = self.calc_p25(d1)
            self.p25[d2] = self.calc_p25(d2)

    def activar_p25(self):
        self.con_p25 = True
        self.p25 = [self.calc_p25(d) for d in range(self.K)]

    # -- métricas ------------------------------------------------------------
    def calc_p25(self, d: int) -> float:
        pares = []
        for i in self.miembros[d]:
            pares.extend(self.nodos[i].pares)
        return P25_FUNC(pares) if pares else 0.0

    def p25_si(self, d: int, quitar: int | None = None, poner: int | None = None) -> float:
        pares = []
        for i in self.miembros[d]:
            if i != quitar:
                pares.extend(self.nodos[i].pares)
        if poner is not None:
            pares.extend(self.nodos[poner].pares)
        return P25_FUNC(pares) if pares else 0.0

    @staticmethod
    def _rms(P, sx, sy, sxx, syy) -> float:
        if P <= 0:
            return 0.0
        var = (sxx / P - (sx / P) ** 2) + (syy / P - (sy / P) ** 2)
        return math.sqrt(max(var, 0.0))

    def rms(self, d: int) -> float:
        return self._rms(self.pob[d], self.sx[d], self.sy[d], self.sxx[d], self.syy[d])

    def rms_si(self, d: int, quitar: int | None = None, poner: int | None = None) -> float:
        P, sx, sy, sxx, syy = self.pob[d], self.sx[d], self.sy[d], self.sxx[d], self.syy[d]
        if quitar is not None:
            nd = self.nodos[quitar]
            P, sx, sy, sxx, syy = P - nd.pob, sx - nd.sx, sy - nd.sy, sxx - nd.sxx, syy - nd.syy
        if poner is not None:
            nd = self.nodos[poner]
            P, sx, sy, sxx, syy = P + nd.pob, sx + nd.sx, sy + nd.sy, sxx + nd.sxx, syy + nd.syy
        return self._rms(P, sx, sy, sxx, syy)

    def coherencia_delta(self, i: int, d1: int, d2: int) -> float:
        """Variación (ponderada) de cruces de provincia y roturas de grupo al mover i de d1 a d2."""
        nd = self.nodos[i]
        delta = 0.0
        # provincia: coste por distrito = nº provincias - 1
        if self.prov_cnt[d1][nd.prov] == 1 and len(self.prov_cnt[d1]) > 1:
            delta -= PESOS_COHERENCIA["provincia"]
        if self.prov_cnt[d2].get(nd.prov, 0) == 0 and len(self.prov_cnt[d2]) >= 1:
            delta += PESOS_COHERENCIA["provincia"]
        # grupos: coste por grupo = nº distritos - 1
        for nivel, k in nd.grupos.items():
            if k is None or nivel == "provincia":
                continue
            c = self.grupo_cnt[(nivel, k)]
            if c.get(d1, 0) == 1:
                delta -= PESOS_COHERENCIA[nivel]
            if c.get(d2, 0) == 0:
                delta += PESOS_COHERENCIA[nivel]
        return delta

    def coste_rango_total(self, lo: int, hi: int) -> int:
        return sum(max(0, lo - p) + max(0, p - hi) for p in self.pob)

    def fuera_de_rango(self, lo: int, hi: int) -> list[int]:
        return [d for d in range(self.K) if self.pob[d] < lo or self.pob[d] > hi]

    def puede_salir(self, i: int) -> bool:
        """¿Sigue conexo el distrito de i si i se marcha? (BFS local)."""
        d = self.asig[i]
        if len(self.miembros[d]) <= 1:
            return False
        vec_d = [j for j in self.nodos[i].adj if self.asig[j] == d]
        if len(vec_d) <= 1:
            return True
        objetivo = set(vec_d)
        inicio = vec_d[0]
        objetivo.discard(inicio)
        visto = {inicio}
        cola = deque([inicio])
        asig = self.asig
        nodos = self.nodos
        while cola and objetivo:
            a = cola.popleft()
            for b in nodos[a].adj:
                if b != i and asig[b] == d and b not in visto:
                    visto.add(b)
                    cola.append(b)
                    objetivo.discard(b)
        return not objetivo

    def distritos_vecinos(self, d: int) -> set[int]:
        out = set()
        for i in self.miembros[d]:
            for j in self.nodos[i].adj:
                e = self.asig[j]
                if e != d:
                    out.add(e)
        return out

    def contiguo(self, d: int) -> bool:
        m = self.miembros[d]
        return es_conexo(set(m), lambda a: self.nodos[a].adj)

    def frontera(self, d: int) -> list[int]:
        return [i for i in self.miembros[d] if any(self.asig[j] != d for j in self.nodos[i].adj)]


# ---------------------------------------------------------------------------
# Partición inicial compacta (R7)
# ---------------------------------------------------------------------------
def elegir_semillas(nodos: list[Nodo], sub: list[int], K: int, lo: int, rng: random.Random,
                    fijas: list[int] | None = None) -> list[int]:
    """Semillas forzadas (nodos >= lo), anclas (>= lo/2) y k-means++ ponderado por población."""
    semillas: list[int] = list(fijas or [])
    forzadas = sorted((i for i in sub if nodos[i].pob >= lo and i not in semillas),
                      key=lambda i: -nodos[i].pob)
    for i in forzadas:
        if len(semillas) >= K:
            break
        semillas.append(i)
    anclas = sorted((i for i in sub if 0.5 * lo <= nodos[i].pob < lo and i not in semillas),
                    key=lambda i: -nodos[i].pob)
    for i in anclas:
        if len(semillas) >= K:
            break
        semillas.append(i)
    restantes = [i for i in sub if i not in set(semillas)]
    while len(semillas) < K and restantes:
        if not semillas:
            pesos = [max(1, nodos[i].pob) for i in restantes]
        else:
            pesos = []
            for i in restantes:
                nd = nodos[i]
                d2 = min((nd.x - nodos[s].x) ** 2 + (nd.y - nodos[s].y) ** 2 for s in semillas)
                pesos.append(max(1, nd.pob) * (d2 + 1.0))
        i = rng.choices(restantes, weights=pesos, k=1)[0]
        semillas.append(i)
        restantes.remove(i)
    return semillas


def crecer_desde_semillas(nodos: list[Nodo], sub: set[int], semillas: list[int],
                          centros: list[tuple[float, float]], capacidades: list[float]) -> dict[int, int]:
    """
    Crecimiento multi-fuente por distancia al centro de cada distrito con
    capacidad de población. Devuelve nodo -> índice local de distrito.
    """
    asig: dict[int, int] = {}
    pob_d = [0] * len(semillas)
    heap: list[tuple[float, int, int]] = []
    for d, s in enumerate(semillas):
        asig[s] = d
        pob_d[d] += nodos[s].pob
        cx, cy = centros[d]
        for j in nodos[s].adj:
            if j in sub and j not in asig:
                heapq.heappush(heap, ((nodos[j].x - cx) ** 2 + (nodos[j].y - cy) ** 2, j, d))
    while heap:
        _, j, d = heapq.heappop(heap)
        if j in asig or pob_d[d] >= capacidades[d]:
            continue
        asig[j] = d
        pob_d[d] += nodos[j].pob
        cx, cy = centros[d]
        for k in nodos[j].adj:
            if k in sub and k not in asig:
                heapq.heappush(heap, ((nodos[k].x - cx) ** 2 + (nodos[k].y - cy) ** 2, k, d))
    # Huérfanos (todos los vecinos llenos): al distrito adyacente con menos población, por capas.
    pendientes = sorted(i for i in sub if i not in asig)
    while pendientes:
        progreso = False
        for i in list(pendientes):
            cands = {asig[j] for j in nodos[i].adj if j in asig}
            if cands:
                d = min(cands, key=lambda d: pob_d[d])
                asig[i] = d
                pob_d[d] += nodos[i].pob
                pendientes.remove(i)
                progreso = True
        if not progreso:
            # Solo ocurre si el subconjunto no es conexo: al centro más cercano.
            i = pendientes.pop()
            d = min(range(len(semillas)),
                    key=lambda d: (nodos[i].x - centros[d][0]) ** 2 + (nodos[i].y - centros[d][1]) ** 2)
            asig[i] = d
            pob_d[d] += nodos[i].pob
    return asig


def particion_inicial(nodos: list[Nodo], sub: set[int], K: int, lo: int, rng: random.Random,
                      lloyd: int = 3, fijas: list[int] | None = None) -> dict[int, int]:
    sub_l = sorted(sub)
    P = sum(nodos[i].pob for i in sub_l)
    semillas = elegir_semillas(nodos, sub_l, K, lo, rng, fijas)
    K_eff = len(semillas)
    forzadas = {s for s in semillas if nodos[s].pob >= lo}
    P_libre = P - sum(nodos[s].pob for s in forzadas)
    n_libres = max(1, K_eff - len(forzadas))
    objetivo = P_libre / n_libres
    capacidades = [nodos[s].pob if s in forzadas else objetivo for s in semillas]
    centros = [(nodos[s].x, nodos[s].y) for s in semillas]
    asig = crecer_desde_semillas(nodos, sub, semillas, centros, capacidades)
    for _ in range(lloyd):
        # Centroides ponderados por población; nueva semilla = nodo del distrito más cercano al centroide.
        sx = [0.0] * K_eff
        sy = [0.0] * K_eff
        sp = [0] * K_eff
        for i, d in asig.items():
            sx[d] += nodos[i].sx
            sy[d] += nodos[i].sy
            sp[d] += nodos[i].pob
        nuevas = []
        nuevos_centros = []
        for d in range(K_eff):
            if semillas[d] in forzadas or sp[d] <= 0:
                nuevas.append(semillas[d])
                nuevos_centros.append(centros[d])
                continue
            cx, cy = sx[d] / sp[d], sy[d] / sp[d]
            miembros = [i for i, dd in asig.items() if dd == d]
            s = min(miembros, key=lambda i: (nodos[i].x - cx) ** 2 + (nodos[i].y - cy) ** 2)
            nuevas.append(s)
            nuevos_centros.append((cx, cy))
        semillas, centros = nuevas, nuevos_centros
        asig = crecer_desde_semillas(nodos, sub, semillas, centros, capacidades)
    return asig


# ---------------------------------------------------------------------------
# Equilibrado (R7) y reparación por fusión/división
# ---------------------------------------------------------------------------
W_RANGO = 10.0   # peso de la violación del rango frente a la banda blanda


def equilibrar(E: Estado, lo: int, hi: int, rng: random.Random, iters: int, w_comp: float,
               T0: float = 3000.0, T1: float = 20.0) -> bool:
    """
    Recocido sobre coste = W_RANGO·(violación de rango) + (distancia a la banda
    blanda [lo+b, hi-b]) + coherencia + w_comp·Σ radio RMS. Solo movimientos de
    nodos de frontera que mantienen la contigüidad. Devuelve True si al final
    todos los distritos están en [lo, hi].
    """
    banda = (hi - lo) / 4.0
    blo, bhi = lo + banda, hi - banda

    def f(p):
        return (W_RANGO * (max(0, lo - p) + max(0, p - hi))
                + (max(0, blo - p) + max(0, p - bhi)))

    coste = sum(f(p) for p in E.pob) + w_comp * sum(E.rms(d) for d in range(E.K))
    C1 = E.coste_rango_total(lo, hi)
    mejor = (C1, coste, E.snapshot())
    focos: list[int] = []
    n = E.n
    for it in range(iters):
        if it % 100 == 0:
            if C1 == 0:
                break
            fuera = E.fuera_de_rango(lo, hi)
            conj = set()
            for d in fuera:
                conj.update(E.frontera(d))
                for e in E.distritos_vecinos(d):
                    for i in E.miembros[e]:
                        if any(E.asig[j] == d for j in E.nodos[i].adj):
                            conj.add(i)
            focos = sorted(conj)
        T = T0 * (T1 / T0) ** (it / max(1, iters))
        if focos and rng.random() < 0.7:
            i = focos[rng.randrange(len(focos))]
        else:
            i = rng.randrange(n)
        d1 = E.asig[i]
        dests = sorted({E.asig[j] for j in E.nodos[i].adj} - {d1})
        if not dests:
            continue
        p = E.nodos[i].pob
        if len(dests) > 1 and rng.random() < 0.7:
            d2 = min(dests, key=lambda e: f(E.pob[e] + p) - f(E.pob[e]))
        else:
            d2 = dests[rng.randrange(len(dests))]
        if rng.random() < 0.3:
            # Intercambio: i (d1 -> d2) y un nodo j de d2 fronterizo con d1 (d2 -> d1).
            # j debe seguir tocando d1 sin contar a i, e i debe seguir tocando d2 sin contar a j.
            cand_j = sorted(j for j in E.miembros[d2]
                            if any(E.asig[k] == d1 and k != i for k in E.nodos[j].adj))
            if not cand_j:
                continue
            j = cand_j[rng.randrange(len(cand_j))]
            if not any(E.asig[k] == d2 and k != j for k in E.nodos[i].adj):
                continue
            q = E.nodos[j].pob
            delta = (f(E.pob[d1] - p + q) + f(E.pob[d2] + p - q) - f(E.pob[d1]) - f(E.pob[d2]))
            delta += E.coherencia_delta(i, d1, d2) + E.coherencia_delta(j, d2, d1)
            delta += w_comp * (E.rms_si(d1, quitar=i, poner=j) + E.rms_si(d2, quitar=j, poner=i)
                               - E.rms(d1) - E.rms(d2))
            if delta <= 0 or rng.random() < math.exp(-delta / T):
                if not E.puede_salir(i):
                    continue
                E.mover(i, d2)
                if not E.puede_salir(j):
                    E.mover(i, d1)
                    continue
                E.mover(j, d1)
                coste += delta
                C1 = E.coste_rango_total(lo, hi)
                if (C1, coste) < (mejor[0], mejor[1]):
                    mejor = (C1, coste, E.snapshot())
            continue
        delta = f(E.pob[d1] - p) + f(E.pob[d2] + p) - f(E.pob[d1]) - f(E.pob[d2])
        delta += E.coherencia_delta(i, d1, d2)
        delta += w_comp * (E.rms_si(d1, quitar=i) + E.rms_si(d2, poner=i) - E.rms(d1) - E.rms(d2))
        if delta <= 0 or rng.random() < math.exp(-delta / T):
            if not E.puede_salir(i):
                continue
            E.mover(i, d2)
            coste += delta
            C1 = E.coste_rango_total(lo, hi)
            if (C1, coste) < (mejor[0], mejor[1]):
                mejor = (C1, coste, E.snapshot())
    if E.coste_rango_total(lo, hi) > mejor[0]:
        E.restaurar(mejor[2])
    return E.coste_rango_total(lo, hi) == 0


def arbol_aleatorio(E: Estado, conjunto: set[int], rng: random.Random,
                    sesgo_distancia: bool = True) -> dict[int, list[int]]:
    """
    Árbol de expansión aleatorio (Kruskal con pesos aleatorios). Con
    `sesgo_distancia` los pesos son distancia·ruido (árboles más compactos);
    sin él son uniformes (cortes más variados, estilo ReCom).
    """
    aristas = []
    for i in sorted(conjunto):
        ni = E.nodos[i]
        for j in ni.adj:
            if j in conjunto and i < j:
                if sesgo_distancia:
                    nj = E.nodos[j]
                    d = math.hypot(ni.x - nj.x, ni.y - nj.y)
                    aristas.append((d * (0.3 + rng.random()), i, j))
                else:
                    aristas.append((rng.random(), i, j))
    aristas.sort()
    padre = {i: i for i in conjunto}

    def raiz(a):
        while padre[a] != a:
            padre[a] = padre[padre[a]]
            a = padre[a]
        return a

    arbol = {i: [] for i in conjunto}
    for _, i, j in aristas:
        ri, rj = raiz(i), raiz(j)
        if ri != rj:
            padre[ri] = rj
            arbol[i].append(j)
            arbol[j].append(i)
    return arbol


def corte_equilibrado(E: Estado, union: set[int], lo: int, hi: int, rng: random.Random,
                      intentos: int = 20):
    """
    Estilo ReCom: árbol de expansión aleatorio de la unión de dos distritos y
    corte de la arista que deja ambas mitades lo más dentro del rango posible.
    Devuelve (lado_A, violación) ó None. Ambos lados son conexos por construcción.
    """
    P2 = sum(E.nodos[i].pob for i in union)
    mejor = None
    nodos_l = sorted(union)
    for t in range(intentos):
        arbol = arbol_aleatorio(E, union, rng, sesgo_distancia=(t % 2 == 0))
        raiz = nodos_l[rng.randrange(len(nodos_l))]
        orden = [raiz]
        padre = {raiz: None}
        pila = [raiz]
        while pila:
            v = pila.pop()
            for w in arbol[v]:
                if w not in padre:
                    padre[w] = v
                    orden.append(w)
                    pila.append(w)
        if len(orden) != len(union):
            continue  # unión no conexa (no debería ocurrir)
        sub = {v: E.nodos[v].pob for v in union}
        for v in reversed(orden):
            if padre[v] is not None:
                sub[padre[v]] += sub[v]
        for v in orden[1:]:
            a = sub[v]
            b = P2 - a
            viol = max(0, lo - a) + max(0, a - hi) + max(0, lo - b) + max(0, b - hi)
            clave = (viol, abs(a - b))
            if mejor is None or clave < mejor[0]:
                mejor = (clave, v, arbol, padre)
        if mejor is not None and mejor[0][0] == 0 and t >= 3:
            break
    if mejor is None:
        return None
    clave, v, arbol, padre = mejor
    A = set()
    pila = [v]
    while pila:
        a = pila.pop()
        A.add(a)
        for w in arbol[a]:
            if padre.get(w) == a:
                pila.append(w)
    return A, clave[0]


def reparar(E: Estado, lo: int, hi: int, rng: random.Random, rondas: int, iters_eq: int,
            w_comp: float) -> bool:
    """
    Fusión del peor distrito con un vecino y nueva división en dos: primero
    por corte equilibrado de árbol (ReCom), si no mejora por semillas; después
    reequilibrado corto.
    """
    def viol(d):
        return max(0, lo - E.pob[d]) + max(0, E.pob[d] - hi)

    for _ in range(rondas):
        fuera = E.fuera_de_rango(lo, hi)
        if not fuera:
            return True
        progreso = False
        for d in sorted(fuera, key=lambda d: -viol(d)):
            vec = E.distritos_vecinos(d)
            if not vec:
                continue
            bajo = E.pob[d] < lo
            vec_ord = sorted(vec, key=lambda v: (-E.pob[v] if bajo else E.pob[v], v))
            for e in vec_ord[:4]:
                antes = viol(d) + viol(e)
                r = corte_equilibrado(E, E.miembros[d] | E.miembros[e], lo, hi, rng)
                if r is None or r[1] >= antes:
                    continue
                A, _ = r
                asig = E.snapshot()
                for i in E.miembros[d] | E.miembros[e]:
                    asig[i] = d if i in A else e
                E.restaurar(asig)
                progreso = True
                break
            if progreso:
                break
        if not progreso:
            d = max(fuera, key=lambda d: viol(d))
            vec = E.distritos_vecinos(d)
            if not vec:
                return False
            if E.pob[d] < lo:
                e = max(vec, key=lambda v: (E.pob[v], -v))
            else:
                e = min(vec, key=lambda v: (E.pob[v], v))
            union = E.miembros[d] | E.miembros[e]
            sub_asig = particion_inicial(E.nodos, union, 2, lo, rng, lloyd=2)
            asig = E.snapshot()
            for i, parte in sub_asig.items():
                asig[i] = d if parte == 0 else e
            E.restaurar(asig)
        if equilibrar(E, lo, hi, rng, iters_eq, w_comp):
            return True
    return not E.fuera_de_rango(lo, hi)


# ---------------------------------------------------------------------------
# Optimización (R8): softmin de P25 y compacidad, manteniendo factibilidad
# ---------------------------------------------------------------------------
def softmin(vals, tau: float) -> float:
    m = min(vals)
    if tau <= 0:
        return m
    s = sum(math.exp(-(v - m) / tau) for v in vals)
    return m - tau * math.log(s)


def optimizar(E: Estado, lo: int, hi: int, rng: random.Random, iters: int, tau: float,
              w_comp: float, T0: float = 60.0, T1: float = 1.0) -> tuple[int, int]:
    """Recocido sobre J = softmin_tau(P25) − w_comp·(radio RMS medio, km); solo movimientos factibles."""
    K = E.K

    def J_de(p25s, rmss):
        return softmin(p25s, tau) - w_comp * (sum(rmss) / K)

    rmss = [E.rms(d) for d in range(K)]
    actual = J_de(E.p25, rmss)
    mejor = (actual, E.snapshot())
    mejoras = 0
    aceptados = 0
    for it in range(iters):
        T = T0 * (T1 / T0) ** (it / max(1, iters))
        i = rng.randrange(E.n)
        d1 = E.asig[i]
        dests = sorted({E.asig[j] for j in E.nodos[i].adj} - {d1})
        if not dests:
            continue
        d2 = dests[rng.randrange(len(dests))]
        p = E.nodos[i].pob
        if E.pob[d1] - p < lo or E.pob[d2] + p > hi:
            continue
        if E.coherencia_delta(i, d1, d2) > 0:
            continue
        n1 = E.p25_si(d1, quitar=i)
        n2 = E.p25_si(d2, poner=i)
        r1 = E.rms_si(d1, quitar=i)
        r2 = E.rms_si(d2, poner=i)
        p25s = list(E.p25)
        p25s[d1], p25s[d2] = n1, n2
        rms_n = list(rmss)
        rms_n[d1], rms_n[d2] = r1, r2
        nuevo = J_de(p25s, rms_n)
        delta = nuevo - actual
        if delta >= 0 or rng.random() < math.exp(delta / T):
            if not E.puede_salir(i):
                continue
            E.mover(i, d2)
            rmss[d1], rmss[d2] = r1, r2
            actual = nuevo
            aceptados += 1
            if actual > mejor[0] + 1e-9:
                mejor = (actual, E.snapshot())
                mejoras += 1
    E.restaurar(mejor[1])
    return mejoras, aceptados


# ---------------------------------------------------------------------------
# Resolución de un bloque
# ---------------------------------------------------------------------------
class Params:
    def __init__(self, **kw):
        self.__dict__.update(kw)


def resolver_bloque(b: Bloque, U: dict[str, Unidad], params: Params,
                    rng: random.Random) -> tuple[list[list[str]], dict]:
    t0 = time.time()
    ids = set(b.unidades)
    P = b.pob(U)
    info = {"bloque": b.nombre, "tipo": b.tipo, "K": b.K, "lo": b.lo, "hi": b.hi,
            "poblacion": P, "unidades": len(ids), "factible": None, "refinados": 0,
            "intentos": [], "mejoras_p25": 0, "segundos": 0.0, "nodos": len(ids)}
    if b.K == 1 or len(ids) == 1:
        info["factible"] = (b.lo <= P <= b.hi)
        info["segundos"] = time.time() - t0
        return [sorted(ids)], info

    if b.tipo == "normal":
        ks = sorted(ks_factibles(P, b.lo, b.hi), key=lambda k: (abs(k - b.K), k))
    else:
        ks = [b.K]
    refinados: set[tuple] = set()
    asig_unidad: dict[str, int] | None = None
    mejor_global = None   # (C1, Estado)
    E_ok = None
    for _ronda in range(len(NIVELES) + 1):
        nodos = construir_nodos(ids, U, b.hi, refinados)
        info["nodos"] = len(nodos)
        sub = set(range(len(nodos)))
        for K in ks:
            for r in range(params.reinicios):
                if asig_unidad is not None and r == 0:
                    asig = [asig_unidad[nd.unidades[0]] for nd in nodos]
                else:
                    asig_d = particion_inicial(nodos, sub, K, b.lo, rng, params.lloyd)
                    asig = [asig_d[i] for i in range(len(nodos))]
                E = Estado(nodos, K, asig)
                iters = min(params.max_iter, params.iter_eq * len(nodos))
                ok = equilibrar(E, b.lo, b.hi, rng, iters, params.peso_comp_eq)
                if not ok:
                    ok = reparar(E, b.lo, b.hi, rng, params.rondas_reparacion, iters // 2,
                                 params.peso_comp_eq)
                C1 = E.coste_rango_total(b.lo, b.hi)
                info["intentos"].append({"K": K, "reinicio": r, "C1": C1})
                if mejor_global is None or C1 < mejor_global[0]:
                    mejor_global = (C1, E)
                if ok:
                    E_ok = E
                    break
            if E_ok is not None:
                break
        if E_ok is not None:
            break
        # Refinar nodos (romper comarcas/municipios) en los distritos fuera de rango y vecinos.
        C1, E = mejor_global
        cand = set()
        for d in E.fuera_de_rango(b.lo, b.hi):
            for e in E.distritos_vecinos(d) | {d}:
                for i in E.miembros[e]:
                    nd = E.nodos[i]
                    if nd.nivel != "unidad" and nd.grupos.get(nd.nivel) is not None:
                        cand.add((nd.nivel, nd.grupos[nd.nivel]))
        if not cand:
            break
        refinados |= cand
        info["refinados"] += len(cand)
        asig_unidad = {u: E.asig[i] for i, nd in enumerate(E.nodos) for u in nd.unidades}
        ks = [E.K]
    if E_ok is None and mejor_global is not None:
        # Reintentos adicionales con otras semillas hasta agotar el presupuesto de tiempo.
        nodos = mejor_global[1].nodos
        sub = set(range(len(nodos)))
        extra = 0
        while (time.time() - t0) < params.tiempo_bloque and extra < params.reinicios_extra:
            extra += 1
            K = mejor_global[1].K
            asig_d = particion_inicial(nodos, sub, K, b.lo, rng, params.lloyd)
            E = Estado(nodos, K, [asig_d[i] for i in range(len(nodos))])
            iters = min(params.max_iter, params.iter_eq * len(nodos))
            ok = equilibrar(E, b.lo, b.hi, rng, iters, params.peso_comp_eq)
            if not ok:
                ok = reparar(E, b.lo, b.hi, rng, params.rondas_reparacion, iters // 2,
                             params.peso_comp_eq)
            C1 = E.coste_rango_total(b.lo, b.hi)
            info["intentos"].append({"K": K, "reinicio": f"extra{extra}", "C1": C1})
            if C1 < mejor_global[0]:
                mejor_global = (C1, E)
            if ok:
                E_ok = E
                break
    if E_ok is not None:
        E = E_ok
        info["factible"] = True
    else:
        _, E = mejor_global
        info["factible"] = False
    E.activar_p25()
    iters = min(params.max_iter, params.iter_opt * E.n)
    mejoras, aceptados = optimizar(E, b.lo, b.hi, rng, iters, params.tau, params.peso_compacidad)
    info["mejoras_p25"] = mejoras
    info["aceptados_opt"] = aceptados
    distritos = []
    for d in range(E.K):
        us = []
        for i in E.miembros[d]:
            us.extend(E.nodos[i].unidades)
        distritos.append(sorted(us))
    info["segundos"] = time.time() - t0
    return distritos, info


# ---------------------------------------------------------------------------
# Imposibilidad demostrable con la granularidad disponible
# ---------------------------------------------------------------------------
def unidades_sin_distrito_valido(ids: set[str], U: dict[str, Unidad], lo: int, hi: int) -> list[str]:
    """
    Unidades u del bloque con población < lo tales que todo vecino v (dentro
    del bloque) cumple pob(u)+pob(v) > hi: ningún distrito contiguo en rango
    puede contener a u, luego el bloque no admite partición en rango con
    estas unidades (p. ej. Pozuelo rodeado de Madrid, Majadahonda, Las Rozas).
    """
    salida = []
    for u in ids:
        pu = U[u].pob
        if pu >= lo:
            continue
        vecs = [v for v in U[u].vecinos if v in ids]
        if vecs and all(pu + U[v].pob > hi for v in vecs):
            salida.append(u)
    return sorted(salida, key=lambda u: -U[u].pob)


# ---------------------------------------------------------------------------
# Métricas y salida
# ---------------------------------------------------------------------------
def metricas_distrito(ids: list[str], U: dict[str, Unidad]) -> dict:
    import numpy as np
    P = sum(U[u].pob for u in ids)
    p25 = P25_FUNC([(U[u].renta, U[u].pob) for u in ids])
    provs = sorted({U[u].prov for u in ids})
    lat = np.array([U[u].lat for u in ids])
    lon = np.array([U[u].lon for u in ids])
    pob = np.array([U[u].pob for u in ids], dtype=float)
    w = pob / pob.sum() if pob.sum() > 0 else np.full(len(ids), 1.0 / len(ids))
    clat, clon = float((w * lat).sum()), float((w * lon).sum())
    # Diámetro: máxima distancia haversine entre centroides de unidades.
    if len(ids) == 1:
        diam = 0.0
    else:
        p1 = np.radians(lat)[:, None]
        p2 = np.radians(lat)[None, :]
        dl = np.radians(lon)[:, None] - np.radians(lon)[None, :]
        a = np.sin((p1 - p2) / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dl / 2) ** 2
        diam = float((2 * R_TIERRA_KM * np.arcsin(np.sqrt(np.clip(a, 0, 1)))).max())
    # Radio RMS y elongación (ejes principales de la covarianza ponderada, en km).
    x = np.array([U[u].x for u in ids])
    y = np.array([U[u].y for u in ids])
    cx, cy = (w * x).sum(), (w * y).sum()
    dx, dy = x - cx, y - cy
    cov = np.array([[(w * dx * dx).sum(), (w * dx * dy).sum()],
                    [(w * dx * dy).sum(), (w * dy * dy).sum()]])
    ev = np.linalg.eigvalsh(cov)
    rms = float(math.sqrt(max(ev.sum(), 0.0)))
    elong = float(math.sqrt(ev[1] / ev[0])) if ev[0] > 1e-9 else (1.0 if len(ids) == 1 else float("inf"))
    return {"poblacion": P, "p25_renta": round(p25, 2), "provincias": provs,
            "diametro_km": round(diam, 1), "radio_rms_km": round(rms, 1),
            "elongacion": (round(elong, 2) if math.isfinite(elong) else None),
            "centroide": [round(clat, 5), round(clon, 5)]}


def percentil(vals: list[float], q: float) -> float:
    if not vals:
        return 0.0
    s = sorted(vals)
    pos = (len(s) - 1) * q
    i = int(math.floor(pos))
    j = min(i + 1, len(s) - 1)
    return s[i] + (s[j] - s[i]) * (pos - i)


def escribir_legible(distritos: list[dict], U: dict[str, Unidad], ruta: Path, lo: int, hi: int):
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("AOCD v2 — Distritos electorales (arts. 16 y 17)\n")
        f.write(f"Total: {len(distritos)} distritos | rango {fmt(lo)}–{fmt(hi)} hab.\n")
        f.write("=" * 78 + "\n\n")
        for d in distritos:
            f.write(f"DISTRITO #{d['distrito']:03d} {d['nombre']} | {fmt(d['poblacion'])} hab | "
                    f"P25: {fmt(d['p25_renta'])}€ | Provincias: {', '.join(d['provincias'])} | "
                    f"diámetro {d['diametro_km']} km | radio RMS {d['radio_rms_km']} km\n")
            if d["excepcion"]:
                f.write(f"  EXCEPCIÓN: {d['excepcion']}\n")
            if d["justificacion_cruce"]:
                f.write(f"  CRUCE PROVINCIAL: {d['justificacion_cruce']}\n")
            f.write(f"Unidades ({len(d['municipios'])}):\n")
            for u in sorted(d["municipios"], key=lambda u: -U[u].pob):
                f.write(f"  {u} {U[u].nombre} ({fmt(U[u].pob)} hab, {fmt(U[u].renta)}€)\n")
            f.write("\n")


def escribir_informe(ruta: Path, res: dict, distritos: list[dict], notas: dict, infos: list[dict],
                     enlaces: list[dict], args, segundos: float):
    lo, hi = args.min, args.max
    L = []
    L.append("# AOCD v2 — Informe de ejecución\n")
    L.append(f"- Entrada: `{args.entrada}` ({res['n_unidades']} unidades, {fmt(res['poblacion_total'])} hab.)")
    L.append(f"- Rango: {fmt(lo)}–{fmt(hi)} hab. | semilla {args.semilla} | holgura de transferencia "
             f"{fmt(args.holgura)} hab./distrito | peso compacidad {args.peso_compacidad} €/km | tau {args.tau} €")
    L.append(f"- Tiempo de ejecución: {segundos:.1f} s\n")
    L.append("## Distritos\n")
    L.append(f"- Distritos: **{res['n_distritos']}** (objetivo teórico {fmt(res['poblacion_total'])}/"
             f"{fmt((lo + hi) / 2)} ≈ {res['poblacion_total'] / ((lo + hi) / 2):.0f})")
    L.append(f"- En rango [{fmt(lo)}, {fmt(hi)}]: **{res['en_rango']}**")
    L.append(f"- Fuera de rango: **{res['fuera_rango']}**, por motivo:")
    for motivo, n in sorted(res["fuera_por_motivo"].items(), key=lambda x: -x[1]):
        L.append(f"  - {n} — {motivo}")
    L.append(f"- Distritos sin contar ciudades que requieren subdivisión: {res['n_sin_ciudades']}; "
             f"de ellos en rango {res['en_rango']} ({res['pct_en_rango_sin_ciudades']:.1f} %)")
    L.append(f"- Población en distritos en rango: {fmt(res['pob_en_rango'])} "
             f"({100 * res['pob_en_rango'] / res['poblacion_total']:.1f} %)\n")
    L.append("## Diámetros (km, máxima distancia entre centroides de unidades)\n")
    dd = res["diametros"]
    L.append(f"- Mínimo {dd['min']} | P25 {dd['p25']} | mediana {dd['mediana']} | P75 {dd['p75']} | "
             f"P90 {dd['p90']} | máximo {dd['max']}")
    L.append(f"- Distritos con diámetro > 100 km: {dd['n_mas_100']}; > 150 km: {dd['n_mas_150']}; "
             f"> 200 km: {dd['n_mas_200']}")
    if res["grandes"]:
        L.append("- Distritos con diámetro > 150 km (todos listados):")
        for g in res["grandes"]:
            L.append(f"  - #{g['distrito']:03d} {g['nombre']}: {g['diametro_km']} km, {fmt(g['poblacion'])} hab., "
                     f"{g['n_unidades']} unidades, elongación {g['elongacion']}"
                     + (f" — excepción: {g['excepcion']}" if g["excepcion"] else ""))
    L.append("")
    L.append("## Cruces de frontera provincial\n")
    L.append(f"- Distritos con unidades de más de una provincia: **{res['n_multiprov']}**")
    for c in res["multiprov"]:
        L.append(f"  - #{c['distrito']:03d} {c['nombre']} ({', '.join(c['provincias'])}, "
                 f"{fmt(c['poblacion'])} hab.): {c['justificacion_cruce']}")
    L.append("")
    L.append("Transferencias aplicadas (R5, mínima población movida; nivel 0 = dentro de la provincia, "
             "1 = misma comunidad, 2 = otra comunidad):\n")
    for t in notas["transferencias"]:
        L.append(f"- [nivel {t.get('nivel', '?')}] {t['texto']}")
    if not notas["transferencias"]:
        L.append("- ninguna")
    L.append("")
    L.append("## P25 de renta por distrito (estimación poblacional sobre rentas medias de unidad)\n")
    p = res["p25"]
    L.append(f"- Mínimo **{fmt(p['min'])} €** (distrito #{p['argmin']:03d} {p['argmin_nombre']}) | "
             f"mediana {fmt(p['mediana'])} € | máximo {fmt(p['max'])} €")
    L.append(f"- Mínimo entre distritos en rango: {fmt(p['min_en_rango'])} €")
    L.append(f"- Comparación v1 (928 distritos): P25 mínimo 7.779 €\n")
    L.append("## Bloques factibles por suma sin partición contigua en rango\n")
    for i in notas.get("imposibles", []):
        if i["unidades"]:
            L.append(f"- {i['bloque']}: imposibilidad demostrable — {', '.join(i['unidades'])} no cabe(n) "
                     f"en ningún distrito contiguo en rango (todos sus vecinos son demasiado grandes)")
        else:
            L.append(f"- {i['bloque']}: no se encontró partición en rango (imposibilidad no demostrada)")
    L.append("")
    L.append("## Bloques municipales (municipios que caben solos, art. 16 restr. 3)\n")
    L.append(f"- Municipios resueltos como bloque propio: {len(notas.get('municipales', []))}")
    for m in notas.get("municipales", [])[:40]:
        L.append(f"  - {m['bloque']}: {fmt(m['poblacion'])} hab., {m['unidades']} unidades")
    if len(notas.get("municipales", [])) > 40:
        L.append(f"  - … (+{len(notas['municipales']) - 40})")
    if notas.get("provincias_sin_bloques_municipales"):
        L.append(f"- Provincias reconstruidas sin bloques municipales por falta de solución: "
                 f"{', '.join(notas['provincias_sin_bloques_municipales'])}")
    L.append("")
    L.append("## Excepciones (art. 16, restr. 1 y 4)\n")
    L.append(f"- Unidades > máximo sin subunidades (requieren subdivisión por secciones): {len(notas['ciudades'])}")
    L.append(f"- Bloques artefacto (provincia factible, resto infactible por las ciudades apartadas): "
             f"{len(notas['artefactos'])}")
    for a in notas["artefactos"]:
        L.append(f"  - {a['bloque']}: {fmt(a['poblacion'])} hab., {a['unidades']} unidades; "
                 f"unidades sin subdividir adyacentes: {', '.join(a['ciudades']) or '—'}")
    L.append(f"- Territorios aislados ó sin donante viable: {len(notas['aislados'])}")
    for a in notas["aislados"]:
        L.append(f"  - {a['bloque']}: {fmt(a['poblacion'])} hab. ({a['tipo']})")
    L.append("")
    L.append("## Adyacencias artificiales (unidades sin vecinos en la geometría)\n")
    for e in enlaces:
        if e["con"]:
            L.append(f"- {e['unidad']} {e['nombre']} → {e['con']} {e['nombre_con']} ({e['km']} km)")
        else:
            L.append(f"- {e['unidad']} {e['nombre']}: sin unidad de su provincia a menos de "
                     f"{args.radio_aislados} km (queda aislada)")
    L.append("")
    L.append("## Bloques resueltos\n")
    L.append("| Bloque | Tipo | Unidades | Nodos | Población | K | Factible | Refinados | Mejoras P25 | s |")
    L.append("|---|---|---:|---:|---:|---:|---|---:|---:|---:|")
    for i in sorted(infos, key=lambda x: x["bloque"]):
        if i["tipo"] == "ciudad":
            continue
        L.append(f"| {i['bloque']} | {i['tipo']} | {i['unidades']} | {i['nodos']} | {fmt(i['poblacion'])} | "
                 f"{i['K']} | {'sí' if i['factible'] else 'NO'} | {i['refinados']} | {i['mejoras_p25']} | "
                 f"{i['segundos']:.1f} |")
    L.append("")
    L.append("## Verificación\n")
    L.append(f"- Unidades asignadas exactamente una vez: {'sí' if res['asignacion_ok'] else 'NO'}")
    L.append(f"- Distritos no contiguos (BFS sobre `vecinos`): {res['no_contiguos']}")
    L.append(f"- Suma de poblaciones de distritos = población total: {'sí' if res['suma_ok'] else 'NO'}")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main(argv=None):
    ap = argparse.ArgumentParser(description="AOCD v2 (arts. 16 y 17)")
    ap.add_argument("--entrada", default="data/secciones_unificadas.json")
    ap.add_argument("--min", type=int, default=MIN_HAB_DEFECTO, help="población mínima por distrito")
    ap.add_argument("--max", type=int, default=MAX_HAB_DEFECTO, help="población máxima por distrito")
    ap.add_argument("--semilla", type=int, default=42)
    ap.add_argument("--salida", default="output", help="directorio de salida")
    ap.add_argument("--holgura", type=int, default=0,
                    help="holgura por distrito exigida al donante/receptor en transferencias (R5); "
                         "0 = literal del art. 16 (cruzar solo si no existe ningún reparto en rango)")
    ap.add_argument("--comunidades", default="data/provincia_comunidad.csv",
                    help="tabla provincia -> comunidad autónoma (escalón autonómico de la restr. 3)")
    ap.add_argument("--sin-bloques-municipales", action="store_true",
                    help="no tratar como bloque propio los municipios que caben solos en el rango")
    ap.add_argument("--radio-aislados", type=float, default=30.0,
                    help="km máximos para enlazar artificialmente una unidad sin vecinos")
    ap.add_argument("--peso-compacidad", type=float, default=100.0,
                    help="€ de P25 (softmin) que vale 1 km de radio RMS medio en la optimización")
    ap.add_argument("--peso-comp-eq", type=float, default=150.0,
                    help="habitantes equivalentes por km de radio RMS en el equilibrado")
    ap.add_argument("--tau", type=float, default=250.0, help="temperatura del softmin de P25 (€)")
    ap.add_argument("--iter-eq", type=int, default=300, help="iteraciones de equilibrado por nodo")
    ap.add_argument("--iter-opt", type=int, default=150, help="iteraciones de optimización por nodo")
    ap.add_argument("--max-iter", type=int, default=200_000, help="tope de iteraciones por fase y bloque")
    ap.add_argument("--reinicios", type=int, default=3)
    ap.add_argument("--reinicios-extra", type=int, default=6,
                    help="reinicios adicionales si ningún K da partición en rango")
    ap.add_argument("--tiempo-bloque", type=float, default=150.0,
                    help="segundos máximos de reintentos adicionales por bloque")
    ap.add_argument("--lloyd", type=int, default=3)
    ap.add_argument("--rondas-reparacion", type=int, default=8)
    ap.add_argument("--sin-transferencias", action="store_true",
                    help="no cruzar provincias: los bloques estructurales quedan como excepción")
    ap.add_argument("--solo-provincias", default="",
                    help="depuración: códigos de provincia separados por comas")
    args = ap.parse_args(argv)

    t_ini = time.time()
    log("AOCD v2 — Artículos 16 y 17")
    U = cargar_unidades(args.entrada)
    if args.solo_provincias:
        provs = set(args.solo_provincias.split(","))
        U = {k: v for k, v in U.items() if v.prov in provs}
        for u in U.values():
            u.vecinos = [v for v in u.vecinos if v in U]
    log(f"Unidades: {len(U)} | población {fmt(sum(u.pob for u in U.values()))}")
    enlaces = reparar_aislados(U, args.radio_aislados)
    for e in enlaces:
        log(f"  Aislada: {e['unidad']} {e['nombre']} -> {e['con']} {e['nombre_con']} ({e['km']} km)")

    ca_de = cargar_comunidades(args.comunidades)
    bloques, notas = construir_bloques(U, args.min, args.max, args.holgura,
                                       transferir=not args.sin_transferencias,
                                       carve=not args.sin_bloques_municipales, ca_de=ca_de)
    tipos = Counter(b.tipo for b in bloques)
    log(f"Bloques: {len(bloques)} {dict(tipos)}")

    params = Params(iter_eq=args.iter_eq, iter_opt=args.iter_opt, max_iter=args.max_iter,
                    reinicios=args.reinicios, reinicios_extra=args.reinicios_extra,
                    tiempo_bloque=args.tiempo_bloque, lloyd=args.lloyd,
                    rondas_reparacion=args.rondas_reparacion, peso_comp_eq=args.peso_comp_eq,
                    peso_compacidad=args.peso_compacidad, tau=args.tau)

    distritos: list[dict] = []
    infos: list[dict] = []
    orden = sorted(bloques, key=lambda b: (b.prov, b.tipo != "normal", b.nombre))
    notas["imposibles"] = []
    for b in orden:
        rng = random.Random(f"{args.semilla}-{b.nombre}")
        lista, info = resolver_bloque(b, U, params, rng)
        if b.tipo == "normal" and not info["factible"]:
            imp = unidades_sin_distrito_valido(b.unidades, U, b.lo, b.hi)
            info["imposibles"] = [f"{U[u].nombre} ({fmt(U[u].pob)})" for u in imp]
            notas["imposibles"].append({"bloque": b.nombre, "unidades": info["imposibles"]})
        infos.append(info)
        if b.tipo != "ciudad":
            log(f"  {b.nombre:<34} {b.tipo:<11} K={b.K:<3} unidades={len(b.unidades):<4} "
                f"factible={'sí' if info['factible'] else 'NO'} mejorasP25={info['mejoras_p25']} "
                f"({info['segundos']:.1f}s)")
        cruce = " | ".join(c["texto"] for c in b.cruces) or None
        for j, ids in enumerate(lista):
            m = metricas_distrito(ids, U)
            en_rango = args.min <= m["poblacion"] <= args.max
            if b.tipo == "ciudad":
                exc = b.motivo
            elif en_rango:
                exc = None
            elif b.motivo:
                exc = b.motivo
            else:
                imp = info.get("imposibles") or []
                exc = (f"Fuera de rango ({fmt(m['poblacion'])} hab.): el bloque {b.nombre} admite K={b.K} "
                       f"por población total, pero no se encontró partición contigua en rango con la "
                       f"granularidad de las unidades disponibles (desviación mínima encontrada)")
                if imp:
                    exc += (f". Imposibilidad demostrable: {', '.join(imp[:4])} no cabe(n) en ningún "
                            f"distrito en rango con sus vecinos")
            provs_d = m["provincias"]
            d = {"distrito": None,
                 "nombre": f"{b.nombre} {j + 1}" if len(lista) > 1 else b.nombre,
                 "municipios": ids,
                 **m,
                 "en_rango": en_rango,
                 "excepcion": exc,
                 "justificacion_cruce": (cruce if len(provs_d) > 1 else None),
                 "provincia_principal": b.prov,
                 "bloque": b.nombre, "tipo_bloque": b.tipo, "n_unidades": len(ids)}
            distritos.append(d)
    distritos.sort(key=lambda d: (d["provincia_principal"], d["tipo_bloque"] == "ciudad", d["nombre"]))
    for i, d in enumerate(distritos):
        d["distrito"] = i

    # Verificación global.
    asignadas = Counter(u for d in distritos for u in d["municipios"])
    asignacion_ok = (set(asignadas) == set(U) and all(v == 1 for v in asignadas.values()))
    no_contiguos = [d["distrito"] for d in distritos
                    if not es_conexo(set(d["municipios"]), lambda a: U[a].vecinos)]
    pob_total = sum(u.pob for u in U.values())
    suma_ok = sum(d["poblacion"] for d in distritos) == pob_total

    en_rango = [d for d in distritos if d["en_rango"]]
    fuera = [d for d in distritos if not d["en_rango"]]
    fuera_por_motivo = Counter()
    for d in fuera:
        if d["tipo_bloque"] == "ciudad":
            fuera_por_motivo["Unidad > máximo sin subunidades: requiere subdivisión por secciones censales"] += 1
        elif d["tipo_bloque"] == "artefacto":
            fuera_por_motivo["Bloque artefacto: provincia factible, resto infactible por las ciudades apartadas"] += 1
        elif d["tipo_bloque"] == "aislado":
            fuera_por_motivo["Territorio aislado (isla, Ceuta, Melilla): imposibilidad geográfica"] += 1
        elif d["tipo_bloque"] == "sin_donante":
            fuera_por_motivo["Bloque estructural sin transferencia viable"] += 1
        else:
            fuera_por_motivo["Bloque factible en el que el equilibrado no encontró partición en rango"] += 1
    diams = [d["diametro_km"] for d in distritos]
    grandes = sorted([d for d in distritos if d["diametro_km"] > 150], key=lambda d: -d["diametro_km"])
    multiprov = [d for d in distritos if len(d["provincias"]) > 1]
    p25s = [d["p25_renta"] for d in distritos]
    imin = min(range(len(distritos)), key=lambda i: p25s[i])
    n_ciudades = sum(1 for d in distritos if d["tipo_bloque"] == "ciudad")
    res = {
        "n_unidades": len(U), "poblacion_total": pob_total, "n_distritos": len(distritos),
        "en_rango": len(en_rango), "fuera_rango": len(fuera), "fuera_por_motivo": dict(fuera_por_motivo),
        "n_sin_ciudades": len(distritos) - n_ciudades,
        "pct_en_rango_sin_ciudades": 100.0 * len(en_rango) / max(1, len(distritos) - n_ciudades),
        "pob_en_rango": sum(d["poblacion"] for d in en_rango),
        "diametros": {"min": round(min(diams), 1), "p25": round(percentil(diams, 0.25), 1),
                      "mediana": round(percentil(diams, 0.5), 1), "p75": round(percentil(diams, 0.75), 1),
                      "p90": round(percentil(diams, 0.9), 1), "max": round(max(diams), 1),
                      "n_mas_100": sum(1 for x in diams if x > 100),
                      "n_mas_150": sum(1 for x in diams if x > 150),
                      "n_mas_200": sum(1 for x in diams if x > 200)},
        "grandes": [{k: g[k] for k in ("distrito", "nombre", "diametro_km", "poblacion", "n_unidades",
                                        "elongacion", "excepcion")} for g in grandes],
        "n_multiprov": len(multiprov),
        "multiprov": [{k: d[k] for k in ("distrito", "nombre", "provincias", "poblacion", "justificacion_cruce")}
                      for d in multiprov],
        "p25": {"min": min(p25s), "argmin": distritos[imin]["distrito"], "argmin_nombre": distritos[imin]["nombre"],
                "mediana": percentil(p25s, 0.5), "max": max(p25s),
                "min_en_rango": (min(d["p25_renta"] for d in en_rango) if en_rango else None)},
        "asignacion_ok": asignacion_ok, "no_contiguos": no_contiguos, "suma_ok": suma_ok,
        "n_ciudades": n_ciudades, "segundos": None,
    }
    segundos = time.time() - t_ini
    res["segundos"] = round(segundos, 1)

    out = Path(args.salida)
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "aocd_v2_resultado.json", "w", encoding="utf-8") as f:
        json.dump(distritos, f, ensure_ascii=False, indent=1)
    escribir_legible(distritos, U, out / "distritos_legible.txt", args.min, args.max)
    escribir_informe(out / "INFORME.md", res, distritos, notas, infos, enlaces, args, segundos)
    with open(out / "resumen.json", "w", encoding="utf-8") as f:
        json.dump({"resumen": res, "notas": notas, "bloques": infos, "enlaces": enlaces,
                   "args": vars(args)}, f, ensure_ascii=False, indent=1)

    log(f"Distritos: {len(distritos)} | en rango {len(en_rango)} | fuera {len(fuera)} | "
        f"multiprovincia {len(multiprov)} | no contiguos {len(no_contiguos)}")
    log(f"Diámetro mediana {res['diametros']['mediana']} km | máx {res['diametros']['max']} km | "
        f">150 km: {res['diametros']['n_mas_150']}")
    log(f"P25 mínimo {fmt(res['p25']['min'])} € (#{res['p25']['argmin']} {res['p25']['argmin_nombre']}) | "
        f"mediana {fmt(res['p25']['mediana'])} € | máx {fmt(res['p25']['max'])} €")
    log(f"Salida en {out} | {segundos:.1f} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
