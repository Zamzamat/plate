input_file = "words_with_braille8.txt"
output_file = "words_with_braille8_short.txt"

with open(input_file, "r", encoding="utf-8") as f:
    lines = [line.rstrip("\n") for line in f]

with open(output_file, "w", encoding="utf-8") as f:
    for line in lines:
        # Split by whitespace, last element is Braille8 string
        parts = line.split()
        if not parts:
            continue
        braille8 = parts[-1]          # last column
        short_braille = braille8[:4]  # take first 4 characters
        # Join original line + new short column (single space)
        f.write(line + " " + short_braille + "\n")

print(f"✅ Done! File saved as {output_file}")
