#!/usr/bin/env python3


import sys
import os
import argparse

def convert_frequency(freq, unit="mhz"):
    if unit == "hz":
        return int(freq * 1_000_000)  # MHz to Hz
    elif unit == "khz":
        return int(freq * 1_000)  # MHz to kHz
    elif unit == "ghz":
        return freq / 1_000  # MHz to GHz
    return freq  # Default to MHz

def parse_data(input_data):
    rows = []
    tags = set()
    for line in input_data:
        columns = line.split('\t')
        if len(columns) < 8:
            continue  # Skip malformed lines

        try:
            freq = float(columns[0])  # Frequency in MHz
            converted_freq = convert_frequency(freq, unit="hz")
            name = columns[4].strip()
            if not name:
                continue  # Skip entries without a name
            mode = columns[6].strip()
            mode = "Narrow FM" if mode == "FMN" else mode
            bandwidth = ""  # Default to empty
            if mode == "Narrow FM" or mode.startswith("AM"):
                bandwidth = "10000"
            elif mode in {"LSB", "USB"}:
                bandwidth = "2700"
            tags_field = columns[7].strip().replace(" ", "")  # Remove spaces around commas

            row = f"{converted_freq}; {name}             ; {mode}                  ;      {bandwidth}; {tags_field}"
            rows.append(row)

            if tags_field:
                tags.update(tags_field.split(","))
        except ValueError:
            continue  # Skip rows with invalid data

    return rows, tags

def write_bookmarks(output_file, rows, tags, overwrite=False):
    if overwrite or not os.path.exists(output_file):
        with open(output_file, "w") as f:
            for tag in tags:
                f.write(f"{tag} ; #c0c0c0\n")
            f.write("\n")  # Add an empty line between tags and data

    with open(output_file, "a") as f:
        for row in rows:
            f.write(row + "\n")

def main():
    parser = argparse.ArgumentParser(
        description="Parse radio frequency data from a text file and format it for GQRX bookmarks.",
        epilog="Example usage: python formatter.py input.txt output.csv --new"
    )
    parser.add_argument("input_file", help="Input text file containing radio frequency data in tab-delimited format.")
    parser.add_argument("output_file", help="Output CSV file for GQRX bookmarks.")
    parser.add_argument(
        "--new", 
        action="store_true", 
        help="Overwrite the output file if it exists. By default, new entries are appended."
    )
    args = parser.parse_args()

    with open(args.input_file, "r") as f:
        input_data = f.readlines()

    rows, tags = parse_data(input_data)
    write_bookmarks(args.output_file, rows, tags, overwrite=args.new)

if __name__ == "__main__":
    main()

