#!/usr/bin/env python3
"""
Shift all article numbers >= 14 (old numbering) by +1 in both Part 1 and Part 2.
The new Article 14 (Autodeterminación Territorial) has already been inserted manually.
This script renames old 14->15, 15->16, ..., 68->69.

Uses null-byte placeholder technique to avoid collisions (same as renumber.py).
"""

import re
import os

BASE = os.path.dirname(os.path.abspath(__file__))
FILES = [
    os.path.join(BASE, "parte-1-constitucion-completa.md"),
    os.path.join(BASE, "parte-2-argumentacion.md"),
]

# Old numbers to shift: 14 through 68, mapped to 15 through 69
# Process from highest to lowest to avoid collisions... but we'll use placeholders anyway
OLD_MIN = 14
OLD_MAX = 68

# Build mapping: old -> new
mapping = {}
for old in range(OLD_MIN, OLD_MAX + 1):
    mapping[old] = old + 1

# We need to handle various patterns:
# "Artículo 14" -> "Artículo 15"
# "artículo 14" -> "artículo 15"
# "artículos 14" -> "artículos 15"
# "Artículos 14" -> "Artículos 15"
# "artículos 6-7" -> no change (both < 14)
# "artículos 39-41" -> "artículos 40-42"
# Also handle ranges like "14-15" that appear after artículo/artículos

def replace_article_numbers(text):
    """Replace article numbers in text using null-byte placeholders."""

    total_changes = 0

    # Step 1: Replace all old numbers with null-byte placeholders
    # Handle range patterns first: "artículos X-Y" or "artículos X a Y"
    # Then single patterns: "artículo X"

    # We'll use a function-based replacement

    def replace_single_num(match):
        """Replace a single article number reference."""
        nonlocal total_changes
        prefix = match.group(1)  # "Artículo ", "artículo ", "artículos ", etc.
        num = int(match.group(2))
        suffix = match.group(3)  # rest

        if num in mapping:
            total_changes += 1
            return f"{prefix}\x00{mapping[num]}\x00{suffix}"
        return match.group(0)

    # Pattern for "artículo(s) X" - handles single numbers
    # Also need to handle ranges like "artículos 43-45" and "artículos 6 y 7"

    # First pass: handle range patterns "artículos X-Y"
    def replace_range(match):
        nonlocal total_changes
        prefix = match.group(1)
        num1 = int(match.group(2))
        separator = match.group(3)  # "-" or " a " or " y "
        num2 = int(match.group(4))
        suffix = match.group(5)

        new1 = mapping.get(num1, num1)
        new2 = mapping.get(num2, num2)

        changed = (new1 != num1) or (new2 != num2)
        if changed:
            total_changes += 1

        return f"{prefix}\x00{new1}\x00{separator}\x00{new2}\x00{suffix}"

    # Range pattern: artículo/artículos followed by number-separator-number
    text = re.sub(
        r'([Aa]rtículos?\s+)(\d+)(\s*[-–]\s*|\s+a\s+|\s+y\s+)(\d+)(\b)',
        replace_range,
        text
    )

    # Second pass: handle single number patterns (that weren't already replaced)
    # Need to avoid matching numbers already wrapped in null bytes
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

    # Third pass: handle "## Artículo XX:" headers
    # These were already caught by the pattern above, but let's make sure

    # Step 2: Remove null-byte placeholders
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

print("\nDone. New article 14 (Autodeterminación Territorial) is in place.")
print("Old articles 14-68 are now 15-69.")
