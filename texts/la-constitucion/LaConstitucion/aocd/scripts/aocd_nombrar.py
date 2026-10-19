#!/usr/bin/env python3
"""
AOCD — Nombres propios para los distritos del resultado (output/aocd_v2_resultado.json).
Reglas automáticas: ciudad partida -> ciudad + distrito municipal dominante (ó sector por
orientación si no se conoce el nombre del distrito municipal); resto -> comarca(s) agrarias
dominantes + municipio principal + provincia. Nombres únicos, máximo 10 palabras.
Escribe output/nombres_distritos.{json,csv,md} y añade `nombre_propio` a
output/interactivo/distritos.geojson si existe. Ejecutar desde aocd/.
"""
import csv, json, math, collections, re
from pathlib import Path

PROV = {"01":"Álava","02":"Albacete","03":"Alicante","04":"Almería","05":"Ávila","06":"Badajoz","07":"Baleares","08":"Barcelona","09":"Burgos","10":"Cáceres","11":"Cádiz","12":"Castellón","13":"Ciudad Real","14":"Córdoba","15":"A Coruña","16":"Cuenca","17":"Girona","18":"Granada","19":"Guadalajara","20":"Gipuzkoa","21":"Huelva","22":"Huesca","23":"Jaén","24":"León","25":"Lleida","26":"La Rioja","27":"Lugo","28":"Madrid","29":"Málaga","30":"Murcia","31":"Navarra","32":"Ourense","33":"Asturias","34":"Palencia","35":"Las Palmas","36":"Pontevedra","37":"Salamanca","38":"Tenerife","39":"Cantabria","40":"Segovia","41":"Sevilla","42":"Soria","43":"Tarragona","44":"Teruel","45":"Toledo","46":"Valencia","47":"Valladolid","48":"Bizkaia","49":"Zamora","50":"Zaragoza","51":"Ceuta","52":"Melilla"}
# Distritos municipales conocidos (código INE de distrito -> nombre)
DM = {
 "28079": {1:"Centro",2:"Arganzuela",3:"Retiro",4:"Salamanca",5:"Chamartín",6:"Tetuán",7:"Chamberí",8:"Fuencarral-El Pardo",9:"Moncloa-Aravaca",10:"Latina",11:"Carabanchel",12:"Usera",13:"Puente de Vallecas",14:"Moratalaz",15:"Ciudad Lineal",16:"Hortaleza",17:"Villaverde",18:"Villa de Vallecas",19:"Vicálvaro",20:"San Blas-Canillejas",21:"Barajas"},
 "08019": {1:"Ciutat Vella",2:"Eixample",3:"Sants-Montjuïc",4:"Les Corts",5:"Sarrià-Sant Gervasi",6:"Gràcia",7:"Horta-Guinardó",8:"Nou Barris",9:"Sant Andreu",10:"Sant Martí"},
 "46250": {1:"Ciutat Vella",2:"l'Eixample",3:"Extramurs",4:"Campanar",5:"la Saïdia",6:"el Pla del Real",7:"l'Olivereta",8:"Patraix",9:"Jesús",10:"Quatre Carreres",11:"Poblats Marítims",12:"Camins al Grau",13:"Algirós",14:"Benimaclet",15:"Rascanya",16:"Benicalap",17:"Pobles del Nord",18:"Pobles de l'Oest",19:"Pobles del Sud"},
 "41091": {1:"Casco Antiguo",2:"Macarena",3:"Nervión",4:"Cerro-Amate",5:"Sur",6:"Triana",7:"Norte",8:"San Pablo-Santa Justa",9:"Este-Alcosa-Torreblanca",10:"Bellavista-La Palmera",11:"Los Remedios"},
 "29067": {1:"Centro",2:"Este",3:"Ciudad Jardín",4:"Bailén-Miraflores",5:"Palma-Palmilla",6:"Cruz de Humilladero",7:"Carretera de Cádiz",8:"Churriana",9:"Campanillas",10:"Puerto de la Torre",11:"Teatinos-Universidad"},
 "48020": {1:"Deusto",2:"Uribarri",3:"Otxarkoaga-Txurdinaga",4:"Begoña",5:"Ibaiondo",6:"Abando",7:"Errekalde",8:"Basurto-Zorroza"},
}
MINUSC = {"de","del","la","las","los","y","el","en","a","e","o","ó","i"}
def tc(s):
    """Nombre de comarca del MAPA (en mayúsculas) a formato título."""
    out = []
    for i, w in enumerate(s.lower().split()):
        if "-" in w:
            w = "-".join(x.capitalize() for x in w.split("-"))
        elif w in MINUSC and i > 0:
            pass
        else:
            w = w[0].upper() + w[1:] if w else w
        w = re.sub(r"([/(])([a-záéíóúñ])", lambda m: m.group(1) + m.group(2).upper(), w)
        out.append(w)
    return " ".join(out)

ART = {"el","la","los","las","a","o","as","os","els","les","l'","es","sa","ses"}
def nombre_mun(s):
    """'Prat de Llobregat, El' -> 'El Prat de Llobregat' (formato INE con artículo pospuesto)."""
    if ", " in s:
        base, art = s.rsplit(", ", 1)
        if art.lower() in ART:
            return f"{art} {base}" if not art.endswith("'") else f"{art}{base}"
    return s

def sector(dx, dy, radio):
    if math.hypot(dx, dy) < radio: return "Centro"
    ang = (math.degrees(math.atan2(dy, dx)) + 360) % 360
    nombres = ["Este","Noreste","Norte","Noroeste","Oeste","Suroeste","Sur","Sureste"]
    return nombres[int(((ang + 22.5) % 360) // 45)]

def main():
    r = json.load(open("output/aocd_v2_resultado.json", encoding="utf-8"))
    S = json.load(open("data/secciones_unificadas.json", encoding="utf-8"))
    com = {}
    with open("data/municipio_comarca.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            com[row["comarca_id"]] = tc(row["comarca_nombre"].strip())
    # centroides de municipios (ponderados) para sectores
    mx = collections.defaultdict(lambda: [0.0, 0.0, 0])
    for u, v in S.items():
        m = mx[v["municipio"]]; m[0] += v["lon"] * v["poblacion"]; m[1] += v["lat"] * v["poblacion"]; m[2] += v["poblacion"]
    cen = {m: (a / p, b / p) for m, (a, b, p) in mx.items() if p}
    nombres = {}
    fichas = []
    for d in r:
        us = d["municipios"]
        pm = collections.Counter(); nom = {}; pdm = collections.Counter(); pc = collections.Counter()
        for u in us:
            v = S[u]; pm[v["municipio"]] += v["poblacion"]; nom[v["municipio"]] = nombre_mun(v["nombre"].split(" sección")[0])
            pdm[v["distrito_municipal"]] += v["poblacion"]; pc[v.get("comarca")] += v["poblacion"]
        P = d["poblacion"] or 1
        prov = PROV.get(d.get("provincia_principal") or d["provincias"][0], d["provincias"][0])
        muns = pm.most_common()
        m1, p1 = muns[0]
        if len(muns) == 1 or p1 / P >= 0.85:
            # distrito de ciudad (partida)
            ciudad = nom[m1]
            dms = [(int(k[5:7]), p) for k, p in pdm.most_common() if k.startswith(m1)]
            if m1 in DM and dms:
                dom = [DM[m1].get(k, f"distrito {k}") for k, p in dms if p / P >= 0.25][:2] or [DM[m1].get(dms[0][0], f"distrito {dms[0][0]}")]
                nombre = f"{ciudad}: {' y '.join(dom)}"
            else:
                lon = sum(S[u]["lon"] * S[u]["poblacion"] for u in us) / P
                lat = sum(S[u]["lat"] * S[u]["poblacion"] for u in us) / P
                cx, cy = cen[m1]
                sec = sector((lon - cx) * math.cos(math.radians(lat)), lat - cy, 0.012)
                nombre = f"{ciudad} {sec}"
            if len(muns) > 1 and p1 / P < 0.95:
                nombre += f" y {nom[muns[1][0]]}"
            tipo = "ciudad"
        else:
            cs = [(com.get(c, c or "?"), p) for c, p in pc.most_common()]
            principales = [c for c, p in cs if p / P >= 0.3][:2] or [cs[0][0]]
            base = " y ".join(principales)
            if p1 / P >= 0.35 and nom[m1] not in base:
                nombre = f"{base}: {nom[m1]}"
            else:
                nombre = base
            if prov.lower() not in nombre.lower():
                nombre += f" ({prov})"
            tipo = "comarcal"
        if d["excepcion"] and "aislado" in (d["excepcion"] or ""):
            base_exc = cs[0][0] if not (len(muns)==1 or p1/P>=0.85) else nom[m1]
            nombre = base_exc if base_exc.lower() == prov.lower() else f"{base_exc} ({prov})"
        nombre = re.sub(r"\s+", " ", nombre).strip()
        nombres[d["distrito"]] = nombre
        fichas.append({"distrito": d["distrito"], "nombre": nombre, "poblacion": d["poblacion"], "provincias": d["provincias"],
                       "municipios_principales": "; ".join(f"{nom[m]} ({p:,})".replace(",", ".") for m, p in muns[:3]), "tipo": tipo})
    # unicidad: añadir ordinal romano
    cnt = collections.Counter(nombres.values()); seen = collections.Counter()
    ROM = ["I","II","III","IV","V","VI","VII","VIII","IX","X","XI","XII"]
    for d in sorted(nombres):
        n = nombres[d]
        if cnt[n] > 1:
            seen[n] += 1; nombres[d] = f"{n} {ROM[seen[n]-1]}"
    for f_ in fichas: f_["nombre"] = nombres[f_["distrito"]]
    # límite de 10 palabras
    for d, n in nombres.items():
        if len(n.split()) > 10: nombres[d] = " ".join(n.split()[:10])
    Path("output").mkdir(exist_ok=True)
    json.dump({str(k): v for k, v in sorted(nombres.items())}, open("output/nombres_distritos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    with open("output/nombres_distritos.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["distrito","nombre","poblacion","provincias","municipios_principales","tipo"]); w.writeheader()
        for f_ in sorted(fichas, key=lambda x: x["distrito"]):
            w.writerow({**f_, "provincias": "+".join(f_["provincias"])})
    with open("output/nombres_distritos.md", "w", encoding="utf-8") as f:
        f.write("# Nombres de los 469 distritos (automáticos, provisionales)\n\n| Nº | Nombre | Hab. | Municipios ó barrios principales |\n|---|---|---:|---|\n")
        for f_ in sorted(fichas, key=lambda x: (x["provincias"][0], x["distrito"])):
            f.write(f"| {f_['distrito']} | {f_['nombre']} | {f_['poblacion']:,} | {f_['municipios_principales']} |\n".replace(",", "."))
    g = Path("output/interactivo/distritos.geojson")
    if g.exists():
        gj = json.load(open(g, encoding="utf-8"))
        for ft in gj["features"]: ft["properties"]["nombre_propio"] = nombres[ft["properties"]["distrito"]]
        json.dump(gj, open(g, "w", encoding="utf-8"), ensure_ascii=False)
    print("nombres:", len(nombres), "| únicos:", len(set(nombres.values())))

if __name__ == "__main__":
    main()
