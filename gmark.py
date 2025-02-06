#!/usr/bin/env python3

import argparse
import re
import sys

# Define allowed modulation modes (for reference, but not enforced)
ALLOWED_MODES = {
    "Narrow FM", "AM", "USB", "LSB", "CW-U", "CW-L", "WFM (stereo)",
    "WFM (mono)", "WFM (oirt)", "AM-Sync", "Raw I/Q"
}

# Function to parse input file and extract frequencies
def parse_input_file(input_file):
    frequencies = []
    with open(input_file, 'r') as file:
        for line in file:
            # Match frequency, name, modulation, and bandwidth
            match = re.match(r'(\d+\.?\d*)\s*;\s*(.*?)\s*;\s*(.*?)\s*;\s*(\d+)\s*;\s*(.*)', line.strip())
            if match:
                freq, name, mod, bw, tags = match.groups()
                # Convert frequency to Hz
                freq_hz = int(float(freq) * 1e6)
                # Allow any modulation mode (no validation)
                frequencies.append((freq_hz, name, mod, int(bw), tags))
    return frequencies

# Function to write frequencies to the output file
def write_frequencies(output_file, frequencies, tag, replace_tags=False, extra_tags=None):
    header = []
    freq_section = []
    try:
        with open(output_file, 'r') as file:
            lines = file.readlines()
            in_header = True
            for line in lines:
                if line.startswith("# Frequency"):
                    in_header = False
                if in_header:
                    header.append(line.strip())
                else:
                    freq_section.append(line.strip())
    except FileNotFoundError:
        # If file doesn't exist, create a new one
        header = ["# Tag name ; color", f"{tag} ; #0000FF"]
        freq_section = []

    # Append new frequencies
    for freq in frequencies:
        freq_hz, name, mod, bw, tags = freq
        if replace_tags:
            tags = tag
        if extra_tags:
            tags = f"{tags},{extra_tags}" if tags else extra_tags
        freq_section.append(f"{freq_hz} ; {name} ; {mod} ; {bw} ; {tags}")

    # Write to output file
    with open(output_file, 'w') as file:
        file.write("\n".join(header) + "\n")
        file.write("\n".join(freq_section) + "\n")


# Easter egg: --fuck
def fuck():
    print(r"""
 ___________________
< fuck donald trump >
 -------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\\
                ||----w |
                ||     ||
    """)

# Main function
def main():
    parser = argparse.ArgumentParser(description="Format and append frequencies to a bookmarks.csv file.")
    parser.add_argument("input_file", nargs="?", help="Input text file containing frequencies.")
    parser.add_argument("output_file", nargs="?", help="Output CSV file.")
    parser.add_argument("--new", action="store_true", help="Create a new file instead of appending.")
    parser.add_argument("--replace", action="store_true", help="Replace all tags with a custom tag.")
    parser.add_argument("--tags", help="Extra tags to append to all frequencies (comma-separated).")
    parser.add_argument("--fuck", action="store_true", help=argparse.SUPPRESS)  # Easter egg

    # If no arguments are provided, print usage and exit
    if len(sys.argv) == 1:
        parser.print_help()
        print("\nUse --help for more information.")
        sys.exit(0)

    args = parser.parse_args()

    # Handle Easter eggs
    if args.fuck:
        fuck()
        sys.exit(0)

    # Check if input and output files are provided
    if not args.input_file or not args.output_file:
        print("Error: Input and output files are required.")
        parser.print_help()
        sys.exit(1)

    # Parse input file
    frequencies = parse_input_file(args.input_file)

    # Determine tag
    tag = "NationalInterop"  # Default tag
    if args.replace:
        tag = args.tags.split(",")[0] if args.tags else tag

    # Determine extra tags
    extra_tags = None
    if args.tags and not args.replace:
        extra_tags = args.tags

    # Write frequencies to output file
    if args.new:
        # Create a new file
        with open(args.output_file, 'w') as file:
            file.write("# Tag name ; color\n")
            file.write(f"{tag} ; #0000FF\n")
            file.write("# Frequency ; Name ; Modulation ; Bandwidth ; Tags\n")
        print(f"Created new file: {args.output_file}")

    # Append frequencies
    write_frequencies(args.output_file, frequencies, tag, args.replace, extra_tags)
    print(f"Frequencies appended to: {args.output_file}")

if __name__ == "__main__":
    main()
