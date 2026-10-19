#!/usr/bin/env python3
"""
AOCD — Lector mínimo de ficheros PC-Axis (.px) del INE.

Solo cubre lo que necesitan los scripts del AOCD: cabecera por bloques
(KEYWORD o KEYWORD("variable")), VALUES/CODES de cada variable y el bloque
DATA en orden fila-mayor (STUB primero, HEADING después, última variable
la más rápida), que es el orden estándar de PC-Axis.

Uso:
    px = leer_px(ruta)
    px['stub'], px['heading']         -> listas de nombres de variable
    px['values'][var], px['codes'][var]
    for combinacion, valor in iterar_datos(px): ...
        combinacion = tupla de valores (uno por variable, orden STUB+HEADING)
        valor = float o None (".." / "." / "-" = sin dato)

Ejecútese con `python3 -I`; no hace imports fuera de la librería estándar.
"""

import re

_RE_KEYWORD = re.compile(r'^([A-Z][A-Z0-9\-]*)(?:\("((?:[^"]|"")*)"\))?=', re.M)
_RE_QUOTED = re.compile(r'"((?:[^"]|"")*)"')


def _bloques(texto):
    """Devuelve lista de (keyword, variable|None, contenido) en orden."""
    matches = list(_RE_KEYWORD.finditer(texto))
    bloques = []
    for i, m in enumerate(matches):
        fin = matches[i + 1].start() if i + 1 < len(matches) else len(texto)
        contenido = texto[m.end():fin].strip()
        if contenido.endswith(';'):
            contenido = contenido[:-1]
        bloques.append((m.group(1), m.group(2), contenido))
    return bloques


def _lista_entrecomillada(contenido):
    return [v.replace('""', '"') for v in _RE_QUOTED.findall(contenido)]


def leer_px(ruta, encoding='iso-8859-15'):
    with open(ruta, 'r', encoding=encoding, newline='') as f:
        texto = f.read()
    px = {'meta': {}, 'values': {}, 'codes': {}, 'stub': [], 'heading': [], 'data': None}
    for kw, var, cont in _bloques(texto):
        if kw == 'DATA':
            px['data'] = cont
        elif kw == 'VALUES':
            px['values'][var] = _lista_entrecomillada(cont)
        elif kw == 'CODES':
            px['codes'][var] = _lista_entrecomillada(cont)
        elif kw == 'STUB':
            px['stub'] = _lista_entrecomillada(cont)
        elif kw == 'HEADING':
            px['heading'] = _lista_entrecomillada(cont)
        else:
            px['meta'][(kw, var)] = cont
    if px['data'] is None:
        raise ValueError(f'{ruta}: sin bloque DATA')
    return px


def _parse_valor(tok):
    if tok.startswith('"'):
        tok = tok.strip('"')
    if tok in ('..', '.', '-', '...', '....', ''):
        return None
    try:
        return float(tok.replace(',', '.'))
    except ValueError:
        return None


def iterar_datos(px):
    """Itera (tupla_de_valores, valor) en orden fila-mayor STUB+HEADING."""
    variables = px['stub'] + px['heading']
    listas = [px['values'][v] for v in variables]
    tokens = px['data'].split()
    esperados = 1
    for l in listas:
        esperados *= len(l)
    if len(tokens) != esperados:
        raise ValueError(f'DATA tiene {len(tokens)} valores, se esperaban {esperados} '
                         f'({" x ".join(str(len(l)) for l in listas)})')
    tam = [len(l) for l in listas]
    n = len(tam)
    idx = [0] * n
    for tok in tokens:
        yield tuple(listas[k][idx[k]] for k in range(n)), _parse_valor(tok)
        # incrementar índice mixto (última variable la más rápida)
        k = n - 1
        while k >= 0:
            idx[k] += 1
            if idx[k] < tam[k]:
                break
            idx[k] = 0
            k -= 1
