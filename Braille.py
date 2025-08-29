# align_words_braille.py
# pip install pybraille wcwidth

from pybraille import convertText
from wcwidth import wcswidth

def braille_with_checksum(bits: int) -> int:
    """Add parity dots (7,8) so both columns have even raised dots."""
    left_mask  = (1<<0) | (1<<1) | (1<<2) | (1<<6)   # dots 1,2,3,7
    right_mask = (1<<3) | (1<<4) | (1<<5) | (1<<7)   # dots 4,5,6,8
    if (bits & left_mask).bit_count() % 2 == 1:
        bits |= (1<<6)  # dot 7
    if (bits & right_mask).bit_count() % 2 == 1:
        bits |= (1<<7)  # dot 8
    return bits

def to_braille8(word: str) -> str:
    """6-dot → add parity → 8-dot Unicode."""
    b6 = convertText(word)
    out = []
    for ch in b6:
        bits = ord(ch) - 0x2800
        out.append(chr(0x2800 + braille_with_checksum(bits)))
    return "".join(out)

def dots_numbers(bits: int) -> str:
    """Return raised dot numbers (e.g., '17') for one cell."""
    return "".join(str(i+1) for i in range(8) if bits & (1<<i))

def display_width(s: str) -> int:
    """Unicode display width (handles wide glyphs like Braille)."""
    w = wcswidth(s)
    return 0 if w < 0 else w

def pad_cell(s: str, width: int) -> str:
    """Left-pad s to the given *display* width with spaces."""
    pad = width - display_width(s)
    return s + (" " * max(pad, 0))

INPUT  = "words.txt"                 # format: index binary word
OUTPUT = "words_with_braille_all.txt"
SEP    = "  "                        # inter-column spacing (two spaces)

# Build rows
rows = []
with open(INPUT, "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) < 3:
            continue
        idx, binary, word = parts[0], parts[1], parts[2]

        b6  = convertText(word)
        b8  = to_braille8(word)
        b8s = " ".join(list(b8[:4]))  # first 4 cells, spaced

        # per-cell dot numbers for Braille8
        nums = " ".join(dots_numbers(ord(ch)-0x2800) for ch in b8)

        rows.append([idx, binary, word, b6, b8, b8s, nums])

# Column headers (optional; comment out if you don’t want them)
headers = ["Index", "Binary", "Word", "Braille6", "Braille8", "ShortBraille8", "Braille8NumbersRaised"]
rows_with_header = [headers] + rows

# Compute display-width-based column widths
num_cols = len(rows_with_header[0])
col_w = [0]*num_cols
for row in rows_with_header:
    for i, cell in enumerate(row):
        col_w[i] = max(col_w[i], display_width(cell))

# Write aligned table
with open(OUTPUT, "w", encoding="utf-8") as out:
    for r, row in enumerate(rows_with_header):
        out.write(SEP.join(pad_cell(cell, col_w[i]) for i, cell in enumerate(row)) + "\n")
        if r == 0:  # underline header
            out.write("-" * (sum(col_w) + len(SEP)*(num_cols-1)) + "\n")

print(f"✅ Aligned table saved to {OUTPUT}")
