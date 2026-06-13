#!/usr/bin/env python3
import re
import sys

filepath = '/home/charlescheerful/Desktop/AGENTS/previous-experimentation/learning-agents/LittleCheerful/democracyandAI/test/obra-constitucion-democratica/partes/parte-1-constitucion-completa.md'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"File read: {len(content)} characters")

# ============================================================
# STEP 1: Extract Art 37 body
# ============================================================
art37_header = '## Artículo 37: Garantía de Anulación Popular'
art37_pos = content.find(art37_header)
if art37_pos == -1:
    print("ERROR: Cannot find Art 37 header")
    sys.exit(1)

# Find body (between header+blank line and "---")
header_end = content.find('\n\n', art37_pos) + 2
body_end = content.find('\n\n---\n', header_end)
if body_end == -1:
    # Try alternate pattern
    body_end = content.find('\n---\n', header_end)
    if body_end == -1:
        print("ERROR: Cannot find end of Art 37 body")
        sys.exit(1)

art37_body = content[header_end:body_end].strip()
print(f"Art 37 body extracted: {len(art37_body)} chars")
print(f"Preview: {art37_body[:150]}...")

# ============================================================
# STEP 2: Remove Art 37 from current position
# ============================================================
# Find Art 38 header (next section after Art 37)
art38_header = '## Artículo 38:'
art38_pos = content.find(art38_header, art37_pos + 1)
if art38_pos == -1:
    print("ERROR: Cannot find Art 38 header")
    sys.exit(1)

# Remove from Art 37 header position to Art 38 header position
content = content[:art37_pos] + content[art38_pos:]
print(f"Removed Art 37 from its original position")

# ============================================================
# STEP 3: Insert as new Art 13 before "Fin del Título I"
# ============================================================
fin_t1 = '**Fin del Título I**'
fin_t1_pos = content.find(fin_t1)
if fin_t1_pos == -1:
    print("ERROR: Cannot find 'Fin del Título I'")
    sys.exit(1)

# Use placeholder to protect from renumbering
new_section = f"""## Artículo __NEWART13__: Garantía de Anulación Popular

{art37_body}

---

"""

content = content[:fin_t1_pos] + new_section + content[fin_t1_pos:]
print("Inserted new Art 13 (with placeholder)")

# ============================================================
# STEP 4: Renumber all article references
# ============================================================
def renumber(num):
    """37->13, 13-36->num+1, others->no change"""
    if num == 37:
        return 13
    elif 13 <= num <= 36:
        return num + 1
    return num

# Comprehensive regex for article references
# Handles: artículo(s) X, X-Y, X a Y, X y Y
ref_pattern = re.compile(
    r'([Aa]rtículos?)(\s+)(\d+)'
    r'(?:'
    r'(\s*-\s*)(\d+)'
    r'|(\s+a\s+)(\d+)'
    r'|(\s+y\s+)(\d+)'
    r')?'
)

def ref_replacer(m):
    word = m.group(1)
    space = m.group(2)
    n1 = int(m.group(3))
    new_n1 = renumber(n1)
    
    if m.group(5) is not None:  # dash range
        sep = m.group(4)
        n2 = int(m.group(5))
        return f"{word}{space}{new_n1}{sep}{renumber(n2)}"
    elif m.group(7) is not None:  # "a" range
        sep = m.group(6)
        n2 = int(m.group(7))
        return f"{word}{space}{new_n1}{sep}{renumber(n2)}"
    elif m.group(9) is not None:  # "y" range
        sep = m.group(8)
        n2 = int(m.group(9))
        return f"{word}{space}{new_n1}{sep}{renumber(n2)}"
    else:  # single
        return f"{word}{space}{new_n1}"

content = ref_pattern.sub(ref_replacer, content)
print("Article references renumbered")

# ============================================================
# STEP 5: Replace placeholder
# ============================================================
content = content.replace('__NEWART13__', '13')
print("Placeholder replaced")

# ============================================================
# STEP 6: Update index
# ============================================================
content = content.replace(
    'FUNDAMENTOS (Arts. 1-12)',
    'FUNDAMENTOS (Arts. 1-13)'
)
content = content.replace(
    'ORGANIZACIÓN DE PODERES (Arts. 13-35)',
    'ORGANIZACIÓN DE PODERES (Arts. 14-36)'
)
# Handle both old and current name for Title III
content = content.replace(
    'BOOTSTRAP DEMOCRÁTICO (Arts. 36-41)',
    'PROCESO DE ARRANQUE (Arts. 37-38)'
)
content = content.replace(
    'PROCESO DE ARRANQUE (Arts. 36-41)',
    'PROCESO DE ARRANQUE (Arts. 37-38)'
)
# Also handle if it was partially updated
content = content.replace(
    'PROCESO DE ARRANQUE (Arts. 36-38)',
    'PROCESO DE ARRANQUE (Arts. 37-38)'
)
print("Index updated")

# ============================================================
# STEP 7: Write back
# ============================================================
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

# ============================================================
# VERIFICATION
# ============================================================
print("\n=== VERIFICATION ===")
headers = re.findall(r'## Artículo (\d+):', content)
header_nums = sorted([int(h) for h in headers])
print(f"Article headers: {header_nums}")
print(f"Total articles: {len(header_nums)}")

# Check key articles
checks = [
    ('## Artículo 13: Garantía de Anulación Popular', 'New Art 13 (Garantia)'),
    ('## Artículo 14: Separación de Poderes', 'Old Art 13 -> Art 14 (Separacion)'),
    ('## Artículo 15: Igualdad ante la Ley', 'Old Art 14 -> Art 15 (Igualdad)'),
    ('## Artículo 29: Poder Judicial', 'Old Art 28 -> Art 29 (Judicial)'),
    ('## Artículo 37: Proceso de Arranque', 'Old Art 36 -> Art 37 (Arranque)'),
    ('## Artículo 38: Transición', 'Art 38 (Transicion, unchanged)'),
]

for pattern, desc in checks:
    if pattern in content:
        print(f"  OK {desc}")
    else:
        print(f"  FAIL {desc} - NOT FOUND")

# Check key cross-references
ref_checks = [
    ('artículo 14)', 'Clausulas petreas ref to Separacion (was 13)'),
    ('artículo 13.', 'Art 37 (Arranque) ref to Garantia (was 37)'),
    ('artículos 22-24', 'Exception control ref (was 21-23)'),
]

for pattern, desc in ref_checks:
    if pattern in content:
        print(f"  OK {desc}")
    else:
        print(f"  ? {desc} - pattern not found (check manually)")

print("\nDone!")
