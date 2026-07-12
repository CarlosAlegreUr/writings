#!/usr/bin/env python3
"""Renumber articles in La Constitución Democrática after structural changes.

Changes applied:
- Art 24 split into 24 + 24B
- Art 27 merged into Art 25
- Arts 39+40 merged into Art 39
- Art 42 split into 42 + 42B + 42C
- Arts 43+44+45 merged into Art 43
- Arts 47+48+49 merged into Art 47
- Art 56 split into 56 + 56B

Result: 72 → 70 articles with sequential numbering.
"""

import re
import sys

# Mapping from current/referenced number to new number
MAPPING = {
    "1": "1", "2": "2", "3": "3", "4": "4", "5": "5",
    "6": "6", "7": "7", "8": "8", "9": "9", "10": "10",
    "11": "11", "12": "12", "13": "13", "14": "14", "15": "15",
    "16": "16", "17": "17", "18": "18", "19": "19", "20": "20",
    "21": "21", "22": "22", "23": "23", "24": "24",
    "24B": "25",
    "25": "26", "26": "27", "27": "26",
    "28": "28", "29": "29", "30": "30", "31": "31", "32": "32",
    "33": "33", "34": "34", "35": "35", "36": "36", "37": "37",
    "38": "38", "39": "39", "40": "39",
    "41": "40", "42": "41",
    "42B": "42", "42C": "43",
    "43": "44", "44": "44", "45": "44",
    "46": "45", "47": "46", "48": "46", "49": "46",
    "50": "47", "51": "48", "52": "49", "53": "50", "54": "51",
    "55": "52", "56": "53",
    "56B": "54",
    "57": "55", "58": "56", "59": "57", "60": "58",
    "61": "59", "62": "60", "63": "61", "64": "62",
    "65": "63", "66": "64", "67": "65", "68": "66",
    "69": "67", "70": "68", "71": "69", "72": "70",
}

def m(n):
    """Map article number string to new number."""
    return MAPPING.get(n, n)

def map_range_expanded(start_str, end_str):
    """Map a range by expanding all articles and finding new min/max."""
    start = int(re.match(r'(\d+)', start_str).group(1))
    end = int(re.match(r'(\d+)', end_str).group(1))
    new_nums = set()
    for i in range(start, end + 1):
        mapped = MAPPING.get(str(i))
        if mapped:
            new_nums.add(int(mapped))
    if not new_nums:
        return start_str, end_str
    return str(min(new_nums)), str(max(new_nums))

changes = []

def renumber(text):
    # 1. Replace article headers: ## Artículo XX: or ## Artículo XXB:
    def repl_header(match):
        old_num = match.group(1)
        new_num = m(old_num)
        if old_num != new_num:
            changes.append(f"  Header: Art {old_num} → Art {new_num}")
        return f"## Artículo {new_num}:"
    text = re.sub(r'## Artículo (\d+[BC]?):', repl_header, text)

    # 2. Handle "artículos X a Y" ranges
    def repl_range_a(match):
        prefix = match.group(1)  # "artículos" or "Artículos"
        old_s, old_e = match.group(2), match.group(3)
        new_s, new_e = map_range_expanded(old_s, old_e)
        if new_s == new_e:
            singular = prefix.replace("ículos", "ículo")
            result = f"{singular} {new_s}"
        else:
            result = f"{prefix} {new_s} a {new_e}"
        if f"{prefix} {old_s} a {old_e}" != result:
            changes.append(f"  Range-a: {prefix} {old_s} a {old_e} → {result}")
        return result
    text = re.sub(r'([Aa]rtículos) (\d+[BC]?) a (\d+[BC]?)', repl_range_a, text)

    # 3. Handle "artículos X-Y" dash ranges
    def repl_range_dash(match):
        prefix = match.group(1)
        old_s, old_e = match.group(2), match.group(3)
        new_s, new_e = map_range_expanded(old_s, old_e)
        if new_s == new_e:
            singular = prefix.replace("ículos", "ículo")
            result = f"{singular} {new_s}"
        else:
            result = f"{prefix} {new_s}-{new_e}"
        if f"{prefix} {old_s}-{old_e}" != result:
            changes.append(f"  Range-dash: {prefix} {old_s}-{old_e} → {result}")
        return result
    text = re.sub(r'([Aa]rtículos) (\d+[BC]?)-(\d+[BC]?)', repl_range_dash, text)

    # 4. Handle "artículos X, Y y Z" lists
    def repl_list3(match):
        prefix = match.group(1)
        a, b, c = m(match.group(2)), m(match.group(3)), m(match.group(4))
        nums = list(dict.fromkeys([a, b, c]))
        if len(nums) == 1:
            result = f"{prefix.replace('ículos', 'ículo')} {nums[0]}"
        elif len(nums) == 2:
            result = f"{prefix} {nums[0]} y {nums[1]}"
        else:
            result = f"{prefix} {nums[0]}, {nums[1]} y {nums[2]}"
        if match.group(0) != result:
            changes.append(f"  List3: {match.group(0)} → {result}")
        return result
    text = re.sub(r'([Aa]rtículos) (\d+[BC]?), (\d+[BC]?) y (\d+[BC]?)', repl_list3, text)

    # 5. Handle "artículos X y Y" pairs
    def repl_list2(match):
        prefix = match.group(1)
        a, b = m(match.group(2)), m(match.group(3))
        if a == b:
            result = f"{prefix.replace('ículos', 'ículo')} {a}"
        else:
            result = f"{prefix} {a} y {b}"
        if match.group(0) != result:
            changes.append(f"  List2: {match.group(0)} → {result}")
        return result
    text = re.sub(r'([Aa]rtículos) (\d+[BC]?) y (\d+[BC]?)', repl_list2, text)

    # 6. Handle single "artículo X" references
    def repl_single(match):
        prefix = match.group(1)
        old = match.group(2)
        new = m(old)
        if old != new:
            changes.append(f"  Single: {prefix} {old} → {prefix} {new}")
        return f"{prefix} {new}"
    text = re.sub(r'([Aa]rtículo) (\d+[BC]?)\b', repl_single, text)

    # 7. Handle index format "Arts. X-Y"
    def repl_index(match):
        old_s, old_e = match.group(1), match.group(2)
        new_s, new_e = map_range_expanded(old_s, old_e)
        if new_s == new_e:
            result = f"Art. {new_s}"
        else:
            result = f"Arts. {new_s}-{new_e}"
        if f"Arts. {old_s}-{old_e}" != result:
            changes.append(f"  Index: Arts. {old_s}-{old_e} → {result}")
        return result
    text = re.sub(r'Arts\. (\d+[BC]?)-(\d+[BC]?)', repl_index, text)

    # 8. Fix grammar: when plural "artículos" collapsed to singular "artículo",
    #    the preceding "los" must become "el", with contractions
    text = re.sub(r'\blos artículo\b', 'el artículo', text)
    text = re.sub(r'\bLos artículo\b', 'El artículo', text)
    # Handle contractions: "a el" → "al", "de el" → "del"
    text = re.sub(r'\ba el artículo\b', 'al artículo', text)
    text = re.sub(r'\bA el artículo\b', 'Al artículo', text)
    text = re.sub(r'\bde el artículo\b', 'del artículo', text)
    text = re.sub(r'\bDe el artículo\b', 'Del artículo', text)

    # 9. Update article count
    text = text.replace("**Total de artículos:** 72", "**Total de artículos:** 70")

    return text


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 renumber_final.py <file1> [file2] ...")
        sys.exit(1)

    for filepath in sys.argv[1:]:
        changes.clear()
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()

        new_text = renumber(text)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_text)

        print(f"\n{'='*60}")
        print(f"Renumbered: {filepath}")
        print(f"Changes: {len(changes)}")
        for c in changes:
            print(c)
