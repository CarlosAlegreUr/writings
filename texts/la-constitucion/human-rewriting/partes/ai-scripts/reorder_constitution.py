#!/usr/bin/env python3
"""
Reorder constitution articles according to new structure.
No content changes - only structural reordering + reference updates.
"""
import re
import sys

INPUT_FILE = 'parte-1-constitucion-completa.md'
OUTPUT_FILE = 'parte-1-constitucion-completa-v2.md'

# Old article number → New article number
OLD_TO_NEW = {
    1: 1, 2: 1,  # merged into 1
    3: 2, 4: 3, 5: 4, 6: 5, 7: 9, 8: 10, 9: 11, 10: 12,
    11: 13, 12: 14, 13: 15, 14: 16, 15: 6, 16: 7, 17: 18,
    18: 8, 19: 19, 20: 20, 21: 21, 22: 22, 23: 23, 24: 24,
    25: 25, 26: 37, 27: 38, 28: 26, 29: 27, 30: 28, 31: 29,
    32: 30, 33: 31, 34: 32, 35: 33, 36: 34, 37: 35, 38: 36,
    39: 17, 40: 40, 41: 41, 42: 42, 43: 43, 44: 44, 45: 64,
    46: 65, 47: 66, 48: 67, 49: 68, 50: 69, 51: 70, 52: 53,
    53: 54, 54: 55, 55: 56, 56: 57, 57: 58, 58: 59, 59: 60,
    60: 61, 61: 62, 62: 63, 63: 47, 64: 48, 65: 49, 66: 50,
    67: 51, 68: 52, 69: 45, 70: 46,
    'XX': 39,
}

# New structure: list of (old_art_key, new_art_num)
# old_art_key is str: '1', '2', ..., '70', 'XX', '1+2' (merged)
STRUCTURE = [
    # --- TÍTULO I: PRINCIPIOS FUNDAMENTALES ---
    ('TITULO', 'I', 'PRINCIPIOS FUNDAMENTALES'),
    ('1+2', 1),
    ('3', 2),
    ('4', 3),
    ('5', 4),
    ('6', 5),
    ('15', 6),
    ('16', 7),
    ('18', 8),
    ('FIN_TITULO', 'I'),

    # --- TÍTULO II: SISTEMA ELECTORAL ---
    ('TITULO', 'II', 'SISTEMA ELECTORAL'),
    ('7', 9),
    ('8', 10),
    ('9', 11),
    ('10', 12),
    ('11', 13),
    ('12', 14),
    ('13', 15),
    ('14', 16),
    ('FIN_TITULO', 'II'),

    # --- TÍTULO III: PROCESO DE ARRANQUE ---
    ('TITULO', 'III', 'PROCESO DE ARRANQUE'),
    ('39', 17),
    ('FIN_TITULO', 'III'),

    # --- TÍTULO IV: SEPARACIÓN Y CONTRAPESOS DE LOS PODERES ---
    ('TITULO', 'IV', 'SEPARACIÓN Y CONTRAPESOS DE LOS PODERES'),
    ('17', 18),  # opening article before subtítulos

    ('SUBTITULO', '1', 'Poder Legislativo'),
    ('19', 19),
    ('20', 20),
    ('21', 21),

    ('SUBTITULO', '2', 'Poder Ejecutivo'),
    ('22', 22),
    ('23', 23),
    ('24', 24),
    ('25', 25),
    ('28', 26),
    ('29', 27),
    ('30', 28),
    ('31', 29),

    ('SUBTITULO', '3', 'Poder Judicial'),
    ('32', 30),
    ('33', 31),
    ('34', 32),
    ('35', 33),
    ('36', 34),
    ('37', 35),
    ('38', 36),

    ('SUBTITULO', '4', 'Equilibrio entre Poderes'),
    ('26', 37),
    ('27', 38),
    ('XX', 39),

    ('SUBTITULO', '5', 'Control de Legitimidad Judicial'),
    ('40', 40),
    ('41', 41),
    ('42', 42),
    ('43', 43),

    ('SUBTITULO', '6', 'Anulación Popular'),
    ('44', 44),

    ('SUBTITULO', '7', 'Control Fiscal y Transparencia'),
    ('69', 45),
    ('70', 46),

    ('SUBTITULO', '8', 'Fuerzas Armadas'),
    ('63', 47),
    ('64', 48),
    ('65', 49),
    ('66', 50),
    ('67', 51),
    ('68', 52),

    ('SUBTITULO', '9', 'Estados de Excepción'),
    ('52', 53),
    ('53', 54),
    ('54', 55),
    ('55', 56),
    ('56', 57),
    ('57', 58),
    ('58', 59),
    ('59', 60),
    ('60', 61),
    ('61', 62),
    ('62', 63),
    ('FIN_TITULO', 'IV'),

    # --- TÍTULO V: REFORMA Y PROTECCIÓN CONSTITUCIONAL ---
    ('TITULO', 'V', 'REFORMA Y PROTECCIÓN CONSTITUCIONAL'),
    ('45', 64),
    ('46', 65),
    ('47', 66),
    ('48', 67),
    ('49', 68),
    ('FIN_TITULO', 'V'),

    # --- TÍTULO VI: DERECHOS Y PROTECCIONES ---
    ('TITULO', 'VI', 'DERECHOS Y PROTECCIONES'),
    ('50', 69),
    ('51', 70),
    ('FIN_TITULO', 'VI'),
]


def parse_articles(content):
    """Parse the markdown file into individual articles."""
    # Split by article headers
    segments = re.split(r'(## Artículo (?:\d+|XX): [^\n]+)', content)

    articles = {}
    for i in range(1, len(segments), 2):
        header = segments[i]
        body = segments[i + 1] if i + 1 < len(segments) else ''

        match = re.match(r'## Artículo (\d+|XX): (.+)', header)
        art_num = match.group(1)
        art_title = match.group(2)

        # Clean body: remove structural markers from end
        body_lines = body.split('\n')
        while body_lines and body_lines[-1].strip() in ('', '---') or \
              (body_lines and (
                  body_lines[-1].startswith('**Fin del Título') or
                  body_lines[-1].startswith('# TÍTULO') or
                  body_lines[-1].startswith('# FIN DE LA CONSTITUCIÓN')
              )):
            body_lines.pop()

        # Clean leading blank lines and separators
        while body_lines and body_lines[0].strip() in ('', '---'):
            body_lines.pop(0)

        clean_body = '\n'.join(body_lines).strip()

        articles[art_num] = {
            'title': art_title,
            'body': clean_body,
        }

    return articles


def merge_articles_1_2(articles):
    """Merge articles 1 and 2 into a single article."""
    art1 = articles['1']
    art2 = articles['2']

    merged = {
        'title': 'Soberanía Popular y Jerarquía de Legitimidad',
        'body': art1['body'] + '\n\n' + art2['body'],
    }

    articles['1+2'] = merged
    del articles['1']
    del articles['2']
    return articles


def update_references(text, old_to_new):
    """Update all article number references in text using two-pass tokenization."""

    # Pass 1: Tokenize - replace numbers in article references with §OLDX§ tokens
    # This prevents conflicts when e.g. old 5→4 and old 4→3

    # Handle "artículo X" and "Artículo X" (but NOT in "## Artículo X:" headers)
    # The headers won't be in the text we process (they're separate)

    def tokenize_single(m):
        prefix = m.group(1)
        num = m.group(2)
        return prefix + f'§OLD{num}§'

    result = text

    # Pattern: artículo(s) followed by a number (case insensitive for the a)
    result = re.sub(r'((?:[Aa]rtículos?)\s+)(\d+)', tokenize_single, result)

    # Handle continuation numbers in sequences: §OLDX§ y Y, §OLDX§-Y, §OLDX§ a Y, §OLDX§, Y
    for _ in range(10):
        prev = result
        result = re.sub(
            r'(§OLD\d+§\s*(?:,\s*|y\s+|a\s+|-\s*))(\d+)(?!\d)',
            tokenize_single,
            result
        )
        if result == prev:
            break

    # Handle "(artículo X)" format in cláusulas pétreas
    # Already handled by the general pattern above

    # Handle "Arts. X-Y" in index format
    result = re.sub(r'(Arts?\.\s+)(\d+)', tokenize_single, result)
    for _ in range(5):
        prev = result
        result = re.sub(
            r'(§OLD\d+§\s*(?:,\s*|y\s+|a\s+|-\s*))(\d+)(?!\d)',
            tokenize_single,
            result
        )
        if result == prev:
            break

    # Pass 2: Detokenize - replace §OLDX§ with new number
    def detokenize(m):
        old_num_str = m.group(1)
        old_num = int(old_num_str) if old_num_str != 'XX' else 'XX'
        new_num = old_to_new.get(old_num)
        if new_num is None:
            print(f"  WARNING: No mapping for article {old_num}")
            return old_num_str
        return str(new_num)

    result = re.sub(r'§OLD(\d+|XX)§', detokenize, result)

    return result


def update_titulo_references(text):
    """Update Título references that changed."""
    # "Título VI" (old: estados de excepción) → no longer a separate título
    # Replace with reference to specific article (Art 53 new = principle article)

    # "conforme al Título VI" → "conforme al artículo 53"
    text = text.replace('conforme al Título VI', 'conforme al artículo 53')

    # "de este Título" in old Art 63 context → will be handled per-article
    # "los artículos 64 a 68 de este Título" → already renumbered to 48-52
    # Just remove "de este Título" since it's now in a subtítulo
    text = text.replace(' de este Título', '')

    # Título III stays the same
    # Título IV references stay correct (old IV content is within new IV)

    return text


def build_index():
    """Build the new index."""
    return """# ÍNDICE

- **TÍTULO I:** PRINCIPIOS FUNDAMENTALES (Arts. 1-8)
- **TÍTULO II:** SISTEMA ELECTORAL (Arts. 9-16)
- **TÍTULO III:** PROCESO DE ARRANQUE (Art. 17)
- **TÍTULO IV:** SEPARACIÓN Y CONTRAPESOS DE LOS PODERES (Arts. 18-63)
  - Subtítulo 1: Poder Legislativo (Arts. 19-21)
  - Subtítulo 2: Poder Ejecutivo (Arts. 22-29)
  - Subtítulo 3: Poder Judicial (Arts. 30-36)
  - Subtítulo 4: Equilibrio entre Poderes (Arts. 37-39)
  - Subtítulo 5: Control de Legitimidad Judicial (Arts. 40-43)
  - Subtítulo 6: Anulación Popular (Art. 44)
  - Subtítulo 7: Control Fiscal y Transparencia (Arts. 45-46)
  - Subtítulo 8: Fuerzas Armadas (Arts. 47-52)
  - Subtítulo 9: Estados de Excepción (Arts. 53-63)
- **TÍTULO V:** REFORMA Y PROTECCIÓN CONSTITUCIONAL (Arts. 64-68)
- **TÍTULO VI:** DERECHOS Y PROTECCIONES (Arts. 69-70)"""


def build_output(articles, structure, old_to_new):
    """Build the complete output file."""

    # File header
    header = """# LA CONSTITUCIÓN DEMOCRÁTICA

**Texto Constitucional Completo**

**Total de artículos:** 70
**Estructura:** 6 Títulos

---

"""
    header += build_index()

    output_parts = [header]

    for item in structure:
        if item[0] == 'TITULO':
            _, num, name = item
            output_parts.append(f'\n\n---\n---\n\n# TÍTULO {num}: {name}\n')

        elif item[0] == 'SUBTITULO':
            _, num, name = item
            output_parts.append(f'\n---\n\n**SUBTÍTULO {num}: {name.upper()}**\n')

        elif item[0] == 'FIN_TITULO':
            _, num = item
            output_parts.append(f'\n---\n\n**Fin del Título {num}**\n')

        else:
            old_key, new_num = item
            art = articles[old_key]

            # Update references in body
            updated_body = update_references(art['body'], old_to_new)
            updated_body = update_titulo_references(updated_body)

            # Build article block
            art_block = f'\n## Artículo {new_num}: {art["title"]}\n\n{updated_body}\n\n---\n'
            output_parts.append(art_block)

    # Footer
    output_parts.append('\n---\n\n# FIN DE LA CONSTITUCIÓN DEMOCRÁTICA\n')

    return ''.join(output_parts)


def main():
    print("Reading input file...")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    print("Parsing articles...")
    articles = parse_articles(content)
    print(f"  Found {len(articles)} articles")

    # Verify we have all expected articles
    expected = [str(i) for i in range(1, 71)] + ['XX']
    for e in expected:
        if e not in articles:
            print(f"  MISSING: Article {e}")
            sys.exit(1)
    print("  All articles found ✓")

    print("Merging articles 1 and 2...")
    articles = merge_articles_1_2(articles)
    print(f"  Now {len(articles)} articles")

    # Verify structure references all articles
    art_keys_in_structure = [item[0] for item in STRUCTURE if item[0] not in ('TITULO', 'SUBTITULO', 'FIN_TITULO')]
    for key in articles:
        if key not in art_keys_in_structure:
            print(f"  WARNING: Article {key} not in structure!")
    for key in art_keys_in_structure:
        if key not in articles:
            print(f"  ERROR: Structure references article {key} but not in articles!")
            sys.exit(1)
    print(f"  Structure references {len(art_keys_in_structure)} articles ✓")

    print("Building output...")
    output = build_output(articles, STRUCTURE, OLD_TO_NEW)

    print(f"Writing to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(output)

    # Verification
    print("\nVerification:")
    art_count = output.count('## Artículo ')
    print(f"  Article count: {art_count}")

    # Check for remaining §OLD tokens
    remaining = re.findall(r'§OLD\d+§', output)
    if remaining:
        print(f"  WARNING: {len(remaining)} untranslated references: {remaining[:5]}")
    else:
        print("  No untranslated references ✓")

    # Check for old título references
    old_titulo_refs = re.findall(r'Título (?:VII|VIII)', output)
    if old_titulo_refs:
        print(f"  WARNING: Old título references found: {old_titulo_refs}")
    else:
        print("  No old título references ✓")

    print("\nDone!")


if __name__ == '__main__':
    main()
