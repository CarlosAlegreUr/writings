#!/usr/bin/env python3
"""
Reorder Part 2 (argumentación) to match new constitution structure.
Updates article references and reorganizes título/section order.
"""
import re
import sys

INPUT = 'parte-2-argumentacion.md'
OUTPUT = 'parte-2-argumentacion-v2.md'

OLD_TO_NEW = {
    1: 1, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 9, 8: 10, 9: 11, 10: 12,
    11: 13, 12: 14, 13: 15, 14: 16, 15: 6, 16: 7, 17: 18,
    18: 8, 19: 19, 20: 20, 21: 21, 22: 22, 23: 23, 24: 24,
    25: 25, 26: 37, 27: 38, 28: 26, 29: 27, 30: 28, 31: 29,
    32: 30, 33: 31, 34: 32, 35: 33, 36: 34, 37: 35, 38: 36,
    39: 17, 40: 40, 41: 41, 42: 42, 43: 43, 44: 44, 45: 64,
    46: 65, 47: 66, 48: 67, 49: 68, 50: 69, 51: 70, 52: 53,
    53: 54, 54: 55, 55: 56, 56: 57, 57: 58, 58: 59, 59: 60,
    60: 61, 61: 62, 62: 63, 63: 47, 64: 48, 65: 49, 66: 50,
    67: 51, 68: 52, 69: 45, 70: 46,
}


def update_references(text):
    """Update all article number references using two-pass tokenization."""
    def tokenize_single(m):
        return m.group(1) + f'§OLD{m.group(2)}§'

    result = text
    result = re.sub(r'([Aa]rtículos?\s+)(\d+)', tokenize_single, result)
    for _ in range(10):
        prev = result
        result = re.sub(r'(§OLD\d+§\s*(?:,\s*|y\s+|a\s+|-\s*))(\d+)(?!\d)', tokenize_single, result)
        if result == prev:
            break
    result = re.sub(r'(Arts?\.\s+)(\d+)', tokenize_single, result)
    for _ in range(5):
        prev = result
        result = re.sub(r'(§OLD\d+§\s*(?:,\s*|y\s+|a\s+|-\s*))(\d+)(?!\d)', tokenize_single, result)
        if result == prev:
            break

    def detokenize(m):
        old_num = int(m.group(1))
        new_num = OLD_TO_NEW.get(old_num)
        if new_num is None:
            print(f"  WARNING: No mapping for article {old_num}")
            return str(old_num)
        return str(new_num)

    result = re.sub(r'§OLD(\d+)§', detokenize, result)

    # Fix merged articles: "Artículos 1-1" → "Artículo 1"
    result = re.sub(r'Artículos\s+(\d+)-\1\b', r'Artículo \1', result)

    # Update Título VI references
    result = result.replace('conforme al Título VI', 'conforme al artículo 53')
    result = result.replace('del Título VI', 'sobre estados de excepción')

    return result


def split_sections(content):
    """Split content into sections by H1 (#) and H2 (##) headers.
    Returns list of (level, header_line, body_text) tuples."""
    lines = content.split('\n')
    sections = []
    current_header = None
    current_level = 0
    current_body = []

    for line in lines:
        h1_match = re.match(r'^# (.+)$', line)
        h2_match = re.match(r'^## (.+)$', line)

        if h1_match and not line.startswith('##'):
            # Save previous
            if current_header is not None:
                sections.append((current_level, current_header, '\n'.join(current_body)))
            current_header = line
            current_level = 1
            current_body = []
        elif h2_match:
            if current_header is not None:
                sections.append((current_level, current_header, '\n'.join(current_body)))
            current_header = line
            current_level = 2
            current_body = []
        else:
            current_body.append(line)

    # Save last section
    if current_header is not None:
        sections.append((current_level, current_header, '\n'.join(current_body)))

    return sections


def main():
    with open(INPUT, 'r', encoding='utf-8') as f:
        content = f.read()

    print("Parsing sections...")
    sections = split_sections(content)
    print(f"  Found {len(sections)} sections")

    # Build a dict by header for easy lookup
    sec_dict = {}
    for i, (level, header, body) in enumerate(sections):
        key = header.strip()
        sec_dict[key] = (level, header, body)
        print(f"  [{i}] L{level}: {key[:80]}")

    # Define new order
    # Each entry is the exact header string from the old file
    new_order = [
        # Pre-título content
        '# LA CONSTITUCIÓN DEMOCRÁTICA',
        '# INTRODUCCIÓN: FILOSOFÍA DE DISEÑO',
        '## El problema que resuelve esta Constitución',
        '## Mentalidad defensiva',
        '## Marco del coste de corrupción',
        '## Trilema democrático',
        '## Influencias teóricas conscientes',
        '# QUÉ ES DEMOCRACIA Y POR QUÉ UNA DEMOCRACIA',
        '## Definición',
        '## Argumentos a favor y en contra de la democracia',

        # TÍTULO I: PRINCIPIOS FUNDAMENTALES (was FUNDAMENTOS)
        ('INJECT', '---\n---\n\n# TÍTULO I: PRINCIPIOS FUNDAMENTALES\n'),
        '## Artículos 1-2: Soberanía Popular y Jerarquía de Legitimidad',
        '## Artículo 3: Niveles de Consenso',
        '## Artículo 4: Sujetos Constitucionales',
        '## Artículo 5: Sufragio Universal',
        '## Artículos 6 y 14: Secreto, Verificabilidad del Voto y Voto Remoto',
        '## Artículo 15: Garantía de Anulación Popular',
        '## Artículo 16: Derecho a la Autodeterminación Territorial',
        # Art 18 (Igualdad) moved here from old Título II
        '## Artículo 18: Igualdad ante la Ley',

        # TÍTULO II: SISTEMA ELECTORAL (new)
        ('INJECT', '\n---\n---\n\n# TÍTULO II: SISTEMA ELECTORAL\n'),
        '## Artículo 7: Distritos Uninominales',
        '## Artículos 8-9: Revocabilidad y el umbral del 75%',
        '## Artículo 10: Doble Vuelta Electoral',
        '## Artículo 11: Tamaño de Distritos y AOCD',
        '## Artículo 12: Ciclo de 21 años',
        '## Artículo 13: Financiación Electoral',

        # TÍTULO III: PROCESO DE ARRANQUE (same)
        '# TÍTULO III: PROCESO DE ARRANQUE',
        '## La analogía hardware/software',
        '## ¿Por qué es necesario?',
        '## ¿Por qué no puede reactivarse?',

        # TÍTULO IV: SEPARACIÓN Y CONTRAPESOS (was ORGANIZACIÓN DE PODERES)
        ('INJECT', '\n---\n---\n\n# TÍTULO IV: SEPARACIÓN Y CONTRAPESOS DE LOS PODERES\n'),
        '## Artículo 17: Separación de Poderes',
        '## Artículos 19-21: Poder Legislativo',
        '## Artículos 22-23: Poder Ejecutivo',
        '## Artículo 24: Sucesión Presidencial',
        '## Artículos 28-31: Ministerios y Presupuesto',
        '## Artículos 32-38: Poder Judicial',
        '## Artículos 26-27: Autodestrucción Mutua',
        '## Incumplimiento Grave del Ejecutivo',
        # Control de Legitimidad (from old Título IV)
        '## ¿Por qué control difuso y no un Tribunal Constitucional centralizado?',
        '## Responsabilidad penal bidireccional',
        '## Anulación Popular de decisiones judiciales (artículo 44)',
        # Fiscal (from old Título VIII)
        '## ¿Por qué la transparencia presupuestaria es constitucional?',
        '## Derecho de auditoría ciudadana',
        # FFAA (from old Título VII)
        '## Control civil del ejército',
        '## ¿Por qué el 85% (N5) para declarar guerra?',
        '## Amputación de una mano por operaciones secretas desastrosas',
        '## Separación de ramas militares',
        # Estados de Excepción (from old Título VI)
        '## El problema estructural',
        '## Consenso creciente e intervalos decrecientes',
        '## Declaración falsa de estado de excepción',
        '## Seis límites no suspendibles',
        '## Prohibición de decretos fuera de estados de excepción',

        # TÍTULO V: REFORMA Y PROTECCIÓN CONSTITUCIONAL (was PROTECCIONES FUNDAMENTALES)
        ('INJECT', '\n---\n---\n\n# TÍTULO V: REFORMA Y PROTECCIÓN CONSTITUCIONAL\n'),
        '## ¿Por qué estas once cláusulas pétreas específicas?',
        '## Asimetría temporal',
        '## Artículo 49: Los mecanismos prevalecen sobre los derechos',
        '## Artículo 47: Reforma ordinaria y protección contra bypass',

        # FIN
        '# FIN DE LA PARTE 2',
    ]

    # Build output
    print("\nBuilding output...")
    output_parts = []
    used_headers = set()

    for item in new_order:
        if isinstance(item, tuple) and item[0] == 'INJECT':
            output_parts.append(item[1])
            continue

        if item in sec_dict:
            level, header, body = sec_dict[item]
            output_parts.append(f'\n{header}\n{body}')
            used_headers.add(item)
        else:
            print(f"  WARNING: Section not found: {item[:80]}")

    # Check for unused sections
    for key in sec_dict:
        if key not in used_headers:
            # Skip old título headers that were replaced
            if key.startswith('# TÍTULO '):
                continue
            print(f"  UNUSED SECTION: {key[:80]}")

    # Join and update references
    output = '\n'.join(output_parts) if not output_parts else ''.join(output_parts)

    # Clean up excessive blank lines
    output = re.sub(r'\n{4,}', '\n\n\n', output)

    print("Updating references...")
    output = update_references(output)

    # Write
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(output)

    # Verification
    print("\nVerification:")
    refs = re.findall(r'§OLD\d+§', output)
    print(f"  Untranslated references: {len(refs)}")
    old_titulo_refs = re.findall(r'Título (?:VII|VIII)', output)
    print(f"  Old Título VII/VIII refs: {len(old_titulo_refs)}")
    titulo_vi_body = re.findall(r'conforme al Título VI', output)
    print(f"  'conforme al Título VI' refs: {len(titulo_vi_body)}")

    print("\nDone!")


if __name__ == '__main__':
    main()
