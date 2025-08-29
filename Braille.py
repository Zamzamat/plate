input_file = "words_with_braille8.txt"
output_file = "words_with_braille8_short.txt"

with open(input_file, "r", encoding="utf-8") as f:
    lines = [line.rstrip("\n") for line in f]

with open(output_file, "w", encoding="utf-8") as f:
    for line in lines:
        parts = line.split()
        if not parts:
            continue

        # last column = full Braille-8
        braille8 = parts[-1]
        # take only first 4 characters
        short_braille = braille8[:4]

        # rebuild line with proper alignment
        # join everything except last col, then add full + short col aligned
        prefix = " ".join(parts[:-1])
        f.write(f"{prefix:<50}{braille8:<15}{short_braille:<5}\n")

print(f"✅ Done! File saved as {output_file}")
