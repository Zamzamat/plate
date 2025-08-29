from pybraille import convertText

def braille_with_checksum(bits: int) -> int:
    """
    Add parity dots (7,8) so both columns have even number of raised dots.
    bits: int (0–255) Braille bit pattern
    returns: new bits with parity enforced
    """
    # column masks
    left_mask  = (1<<0) | (1<<1) | (1<<2) | (1<<6)   # dots 1,2,3,7
    right_mask = (1<<3) | (1<<4) | (1<<5) | (1<<7)   # dots 4,5,6,8

    left_count = (bits & left_mask).bit_count()
    right_count = (bits & right_mask).bit_count()

    if left_count % 2 == 1:   # odd → raise dot 7
        bits |= (1<<6)
    if right_count % 2 == 1:  # odd → raise dot 8
        bits |= (1<<7)
    return bits

def convert_word_to_braille8(word: str) -> str:
    """
    Convert word to Braille with parity (2x4).
    """
    braille6 = convertText(word)       # 6-dot Unicode Braille
    result = []
    for ch in braille6:
        bits = ord(ch) - 0x2800        # get dot pattern bits
        new_bits = braille_with_checksum(bits)
        result.append(chr(0x2800 + new_bits))  # make Unicode char
    return "".join(result)

# ---- Main script ----

input_file = "words.txt"
output_file = "words_with_braille8.txt"

with open(input_file, "r", encoding="utf-8") as f:
    lines = [line.strip().split("\t") for line in f]

with open(output_file, "w", encoding="utf-8") as f:
    for row in lines:
        if len(row) < 3:
            continue
        index, binary, word = row
        braille6 = convertText(word)
        braille8 = convert_word_to_braille8(word)
        f.write(f"{index:<5} {binary:<12} {word:<15} {braille6:<15} {braille8}\n")

print(f"✅ Done! File saved as {output_file}")
