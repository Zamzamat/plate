# fixed16_braille_table.py
# pip install pybraille wcwidth

from pybraille import convertText
from wcwidth import wcwidth, wcswidth

WIDTH = 16       # each column's visual width
SEP   = " "      # 1-space gutter between columns

def braille_with_checksum(bits: int) -> int:
    # add dot7/8 to make each column even parity
    left_mask  = (1<<0)|(1<<1)|(1<<2)|(1<<6)   # 1,2,3,7
    right_mask = (1<<3)|(1<<4)|(1<<5)|(1<<7)   # 4,5,6,8
    if (bits & left_mask).bit_count() % 2:  bits |= (1<<6)
    if (bits & right_mask).bit_count() % 2: bits |= (1<<7)
    return bits

def to_braille8(word: str) -> str:
    b6 = convertText(word)
    out = []
    for ch in b6:
        bits = ord(ch) - 0x2800
        out.append(chr(0x2800 + braille_with_checksum(bits)))
    return "".join(out)

def dots_numbers(bits: int) -> str:
    return "".join(str(i+1) for i in range(8) if bits & (1<<i))

def fit_display_width(s: str, target: int) -> str:
    """Return s clipped/padded to *display* width = target."""
    # clip by display width
    acc = []
    w = 0
    for ch in s:
        cw = wcwidth(ch)
        if cw is None or cw < 0:
            cw = 1
        if w + cw > target:
            break
        acc.append(ch)
        w += cw
        if w == target:
            break
    out = "".join(acc)
    # pad if short
    pad = target - (wcswidth(out) if wcswidth(out) >= 0 else len(out))
    if pad > 0:
        out += " " * pad
    return out

INPUT  = "words.txt"                 # format: index binary word
OUTPUT = "words_fixed16.txt"

rows = []
with open(INPUT, "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) < 3:
            continue
        idx, binary, word = parts[0], parts[1], parts[2]

        b6  = convertText(word)           # Braille6
        b8  = to_braille8(word)           # Braille8 w/ parity
        sb8 = " ".join(list(b8[:4]))      # ShortBraille8 (first 4 cells, spaced)
        nums4 = " ".join(dots_numbers(ord(ch)-0x2800) for ch in b8[:4])  # first 4 cells only

        rows.append([idx, binary, word, b6, b8, sb8, nums4])

with open(OUTPUT, "w", encoding="utf-8") as out:
    for r in rows:
        cells16 = [fit_display_width(c, WIDTH) for c in r]
        out.write(SEP.join(cells16) + "\n")

print(f"✅ Aligned (fixed 16) table saved to {OUTPUT}")
