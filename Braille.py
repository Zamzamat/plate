from pybraille import convertText

def braille_with_checksum(bits: int) -> int:
    """ Add parity dots (7,8) so both columns have even raised dots. """
    left_mask  = (1<<0) | (1<<1) | (1<<2) | (1<<6)   # dots 1,2,3,7
    right_mask = (1<<3) | (1<<4) | (1<<5) | (1<<7)   # dots 4,5,6,8

    left_count  = (bits & left_mask).bit_count()
    right_count = (bits & right_mask).bit_count()

    if left_count % 2 == 1:
        bits |= (1<<6)  # set dot 7
    if right_count % 2 == 1:
        bits |= (1<<7)  # set dot 8
    return bits

def convert_word_to_braille8(word: str) -> str:
    """ Convert word into Braille-8 (with parity). """
    braille6 = convertText(word)
    result = []
    for ch in braille6:
        bits = ord(ch) - 0x2800
        new_bits = braille_with_checksum(bits)
        result.append(chr(0x2800 + new_bits))
    return "".join(result)

def braille_dots(bits: int) -> str:
    """ Return list of raised dots numbers as string (e.g., '17'). """
    dots = []
    for i in range(8):
        if bits & (1<<i):
            dots.append(str(i+1))  # dots are 1-based
    return "".join(dots)

# ---- Main script ----
input_file = "words.txt"
output_file = "words_with_braille_all.txt"

with open(input_file, "r", encoding="utf-8") as f:
    lines = [line.strip().split() for line in f]

with open(output_file, "w", encoding="utf-8") as f:
    for row in lines:
        if len(row) < 3:
            continue
        index, binary, word = row

        # Braille 6-dot
        braille6 = convertText(word)

        # Braille 8-dot with parity
        braille8 = convert_word_to_braille8(word)

        # Short Braille8 (first 4 chars, with spaces)
        short_braille8 = " ".join(list(braille8[:4]))

        # Numbers of raised dots (concatenate for all characters)
        raised = []
        for ch in braille8:
            bits = ord(ch) - 0x2800
            raised.append(braille_dots(bits))
        braille8_numbers = " ".join(raised)

        # Write with double tabs between columns
        f.write(
            f"{index}\t\t{binary}\t\t{word}\t\t{braille6}\t\t{braille8}\t\t{short_braille8}\t\t{braille8_numbers}\n"
        )

print(f"✅ Done! Saved as {output_file}")
