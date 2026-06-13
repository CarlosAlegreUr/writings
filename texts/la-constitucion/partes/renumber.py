#!/usr/bin/env python3
"""Renumber constitution articles to eliminate gaps, updating all cross-references."""
import re

filepath = '/home/charlescheerful/Desktop/AGENTS/archives/experiments/learning-agents/LittleCheerful/democracyandAI/test/obra-constitucion-democratica/partes/parte-1-constitucion-completa.md'

# Old → New mapping (only articles that change)
mapping = {
    42: 37, 43: 38, 44: 39, 45: 40, 46: 41,
    51: 42, 52: 43, 53: 44, 54: 45, 55: 46, 56: 47, 57: 48, 58: 49, 59: 50,
    61: 51, 62: 52, 64: 53, 65: 54, 66: 55, 67: 56, 68: 57, 69: 58, 71: 59, 72: 60,
    73: 61, 74: 62, 75: 63, 76: 64, 77: 65, 78: 66,
    81: 67, 82: 68
}

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

original = content  # Keep backup for comparison

def ph(n):
    """Create placeholder that won't collide with any text."""
    return f'\x00{n}\x00'

# ============================================================
# PASS 1: Replace old numbers with placeholders
# Process from HIGHEST old number to LOWEST to avoid partial
# matches (e.g., "8" in "81" being matched before "81")
# ============================================================

for old in sorted(mapping.keys(), reverse=True):
    new = mapping[old]
    p = ph(new)
    old_s = str(old)

    # 1. Article headings: "## Artículo XX:"
    content = content.replace(f'## Artículo {old_s}:', f'## Artículo {p}:')

    # 2. Index entries: "(Arts. XX" at start of range
    content = content.replace(f'(Arts. {old_s}-', f'(Arts. {p}-')
    content = content.replace(f'(Arts. {old_s},', f'(Arts. {p},')
    content = content.replace(f'(Arts. {old_s})', f'(Arts. {p})')

    # 3. Index range end: "-XX)"
    content = re.sub(rf'-{old_s}\)', f'-{p})', content)

    # 4. "artículo XX" - single reference (not followed by another digit)
    content = re.sub(rf'(artículo\s+){old_s}(?!\d)', rf'\1{p}', content)

    # 5. "artículos XX" - start of range/list (not followed by another digit)
    content = re.sub(rf'(artículos\s+){old_s}(?!\d)', rf'\1{p}', content)

    # 6. Range end with dash: "NN-XX" (preceded by digit or placeholder)
    content = re.sub(rf'(\d)-{old_s}(?!\d)', rf'\1-{p}', content)
    content = re.sub(rf'(\x00)-{old_s}(?!\d)', rf'\1-{p}', content)

    # 7. Range end with " a ": "NN a XX"
    content = re.sub(rf'(\d)\s+a\s+{old_s}(?!\d)', rf'\1 a {p}', content)
    content = re.sub(rf'(\x00)\s+a\s+{old_s}(?!\d)', rf'\1 a {p}', content)

    # 8. List with " y ": "NN y XX"
    content = re.sub(rf'(\d)\s+y\s+{old_s}(?!\d)', rf'\1 y {p}', content)

# ============================================================
# PASS 2: Replace placeholders with actual new numbers
# ============================================================

for new in set(mapping.values()):
    content = content.replace(ph(new), str(new))

# ============================================================
# VERIFICATION
# ============================================================

# Count changes
changes = sum(1 for a, b in zip(original, content) if a != b)
print(f"Characters changed: {changes}")

# Verify no placeholders remain
assert '\x00' not in content, "ERROR: Placeholders remain in output!"

# Verify all new article headings exist
for new_num in sorted(set(mapping.values())):
    assert f'## Artículo {new_num}:' in content, f"ERROR: Missing heading for Artículo {new_num}"

# Verify no old article headings remain (for numbers that changed)
for old_num in mapping.keys():
    if old_num not in mapping.values():  # Only check if old num isn't also a valid new num
        if f'## Artículo {old_num}:' in content:
            print(f"WARNING: Old heading '## Artículo {old_num}:' still exists")

# Print mapping for reference
print("\nMapping applied:")
for old, new in sorted(mapping.items()):
    print(f"  Art. {old} → Art. {new}")

# Write output
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nDone! File updated: {filepath}")
print(f"Total articles after renumbering: 68 (numbered 1-68)")
