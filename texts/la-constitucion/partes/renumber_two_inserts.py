#!/usr/bin/env python3
"""
Renumber articles for two insertions:
- New Article 3 (Consensus Levels) → old 3-21 shift by +1
- New Article 23 (Presidential Succession) → old 22-69 shift by +2

Uses null-byte placeholder technique to avoid collisions.
"""

import re
import os

BASE = os.path.dirname(os.path.abspath(__file__))
FILES = [
    os.path.join(BASE, "parte-1-constitucion-completa.md"),
    os.path.join(BASE, "parte-2-argumentacion.md"),
]

# Build mapping: old -> new
mapping = {}
for old in range(3, 22):   # 3-21 → +1
    mapping[old] = old + 1
for old in range(22, 70):  # 22-69 → +2
    mapping[old] = old + 2

def replace_article_numbers(text):
    """Replace article numbers in text using null-byte placeholders."""
    total_changes = 0

    # First pass: handle range patterns "artículo/artículos X-Y" or "X a Y" or "X y Y"
    def replace_range(match):
        nonlocal total_changes
        prefix = match.group(1)
        num1 = int(match.group(2))
        separator = match.group(3)
        num2 = int(match.group(4))
        suffix = match.group(5)

        new1 = mapping.get(num1, num1)
        new2 = mapping.get(num2, num2)

        changed = (new1 != num1) or (new2 != num2)
        if changed:
            total_changes += 1

        return f"{prefix}\x00{new1}\x00{separator}\x00{new2}\x00{suffix}"

    text = re.sub(
        r'([Aa]rtículos?\s+)(\d+)(\s*[-–]\s*|\s+a\s+|\s+y\s+)(\d+)(\b)',
        replace_range,
        text
    )

    # Second pass: handle single number patterns
    def replace_single(match):
        nonlocal total_changes
        prefix = match.group(1)
        num = int(match.group(2))
        suffix = match.group(3)

        if num in mapping:
            total_changes += 1
            return f"{prefix}\x00{mapping[num]}\x00{suffix}"
        return match.group(0)

    text = re.sub(
        r'([Aa]rtículos?\s+)(\d+)(\b)',
        replace_single,
        text
    )

    # Remove null-byte placeholders
    text = text.replace('\x00', '')

    return text, total_changes


for filepath in FILES:
    filename = os.path.basename(filepath)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content, changes = replace_article_numbers(content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"{filename}: {changes} references updated")

print("\nDone. Old 3-21 are now 4-22. Old 22-69 are now 24-71.")
print("Slots 3 and 23 are free for new articles.")
