# align_bip39_braille.py
# pip install pybraille wcwidth

from pybraille import convertText
from wcwidth import wcswidth

def braille_with_checksum(bits: int) -> int:
    left_mask  = (1<<0)|(1<<1)|(1<<2)|(1<<6)   # 1,2,3,7
    right_mask = (1<<3)|(1<<4)|(1<<5)|(1<<7)   # 4,5,6,8
    if (bits & left_mask).bit_count() % 2:  bits |= (1<<6)  # dot 7
    if (bits & right_mask).bit_count() % 2: bits |= (1<<7)  # dot 8
    return bits

def to_braille8(word: str) -> str:
    return "".join(chr(0x2800 + braille_with_checksum(ord(c)-0x2800))
                   for c in convertText(word))

def dots_numbers(bits: int) -> str:
    return "".join(str(i+1) for i in range(8) if bits & (1<<i))

def dispw(s: str) -> int:
    w = wcswidth(s);  return 0 if w < 0 else w

def pad(s: str, w: int) -> str:
    return s + " " * max(0, w - dispw(s))

INPUT  = "words.txt"                 # "index binary word"
OUTPUT = "words_with_braille_all.txt"
SEP    = "  "                        # two spaces between columns

rows = []
with open(INPUT, "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) < 3: continue
        idx, binary, word = parts[0], parts[1], parts[2]

        b6  = convertText(word)              # Braille6
        b8  = to_braille8(word)              # Braille8 with parity
        sb8 = " ".join(list(b8[:4]))         # ShortBraille8
        nums4 = " ".join(dots_numbers(ord(ch)-0x2800) for ch in b8[:4])  # only first 4 cells

        rows.append([idx, binary, word, b6, b8, sb8, nums4])

# compute column widths by *display width* (Unicode-aware)
W = [0]*len(rows[0])
for r in rows:
    for i, cell in enumerate(r):
        W[i] = max(W[i], dispw(cell))

with open(OUTPUT, "w", encoding="utf-8") as out:
    for r in rows:
        out.write(SEP.join(pad(cell, W[i]) for i, cell in enumerate(r)) + "\n")

print(f"Aligned table saved to {OUTPUT}")
