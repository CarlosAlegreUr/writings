#!/usr/bin/env python3
"""
Renumber articles: old 4-71 → new 5-72 (shift +1)
For insertion of new Art 4 (Sujetos Constitucionales)
"""
import re

def renumber(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    count = 0

    def incr(num_str):
        nonlocal count
        n = int(num_str)
        if n >= 4:
            count += 1
            return f'\x00{n+1}\x00'
        return num_str

    # Replace article header numbers: ## Artículo N:
    def repl_header(m):
        return m.group(1) + incr(m.group(2)) + m.group(3)
    text = re.sub(r'(## Artículo )(\d+)(:)', repl_header, text)

    # Replace inline article references
    def repl_inline(m):
        return m.group(1) + incr(m.group(2))
    text = re.sub(r'([Aa]rtículos?\s+)(\d+)', repl_inline, text)
    text = re.sub(r'(Arts?\.\s+)(\d+)', repl_inline, text)

    # Replace range continuations after placeholders
    def repl_range(m):
        return m.group(1) + incr(m.group(2))

    for _ in range(5):
        text = re.sub(r'(\x00[-–]\s*)(\d+)', repl_range, text)
        text = re.sub(r'(\x00\s+a\s+)(\d+)', repl_range, text)
        text = re.sub(r'(\x00\s+y\s+)(\d+)', repl_range, text)
        text = re.sub(r'(\x00,\s*)(\d+)', repl_range, text)

    text = text.replace('\x00', '')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

    return count

p1 = renumber('obra-constitucion-democratica/partes/parte-1-constitucion-completa.md')
p2 = renumber('obra-constitucion-democratica/partes/parte-2-argumentacion.md')
print(f"Part 1: {p1} replacements")
print(f"Part 2: {p2} replacements")
