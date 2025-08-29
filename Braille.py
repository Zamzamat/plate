# make_aligned_braille_table.py
# pip install pybraille wcwidth

from pybraille import convertText
from wcwidth import wcswidth

def braille_with_checksum(bits: int) -> int:
    # enforce even parity per column: add dot7 (left), dot8 (right)
    left_mask  = (1<<0) | (1<<1) | (1<<2) | (1<<6)   # 1,2,3,7
    right_mask = (1<<3) | (1<<4) | (1<<5) | (1<<7)   # 4,5,6,8
    if (bits & left_mask).bit_count() % 2 == 1:
        bits |= (1<<6)
    if (bits & right_mask).bit_count() % 2 == 1:
        bits |= (1<<7)
    return bits

def to_braille8(word: str) -> str:
    b6 = convertText(word)
    out = []
    for ch in b6:
        bits = ord(ch) - 0x2800
        out.append(chr(0x2800 + braille_with_checksum(bits)))
    return "".join(out)

def dots_numbers(bits: int) -> str:
    # e.g. 1+7 raised => "17"
    return "".join(str(i+1) for i in range(8) if bits & (1<<i))

def dispw(s: str) -> int:
    w = wcswidth(s)
    return 0 if w < 0 else w

def pad_cell(s: str, width: int) -> str:
    return s + " " * max(0, width - dispw(s))

INPUT  = "words.txt"                 # format: index binary word (space-separated)
OUTPUT = "words_with_braille_all.txt"
SEP    = "  "                        # two spaces between columns

# Build rows: [index, binary, word, braille6, braille8, short_b8, numbers_first4]
rows = []
with open(INPUT, "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) < 3:
            continue
        idx, binary, word = parts[0], parts[1], parts[2]

        b6  = convertText(word)
        b8  = to_braille8(word)
        short_b8 = " ".join(list(b8[:4]))  # first 4 Braille8 cells, space-separated

        # last column: ONLY the first 4 cells' dot-numbers (space-separated)
        nums_first4 = " ".join(
            dots_numbers(ord(ch) - 0x2800) for ch in b8[:4]
        )

        rows.append([idx, binary, word, b6, b8, short_b8, nums_first4])

# Compute display-width-based column widths (no header)
num_cols = len(rows[0]) if rows else 0
col_w = [0]*num_cols
for row in rows:
    for i, cell in enumerate(row):
        col_w[i] = max(col_w[i], dispw(cell))

# Write aligned table (no column names)
with open(OUTPUT, "w", encoding="utf-8") as out:
    for row in rows:
        out.write(SEP.join(pad_cell(cell, col_w[i]) for i, cell in enumerate(row)) + "\n")

print(f"✅ Aligned table saved to {OUTPUT}")
