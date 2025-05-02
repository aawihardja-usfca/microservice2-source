#!/usr/bin/env python3
import os
import argparse
import sys

def combine_files(root_dir, output_path):
    """
    Recursively walks root_dir, skipping hidden directories,
    and writes each file's contents into output_path with a header.
    """
    with open(output_path, 'w', encoding='utf-8') as out_f:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Remove hidden directories from traversal
            dirnames[:] = [d for d in dirnames if not d.startswith('.')]
            
            for fname in filenames:
                # Skip hidden files
                if fname.startswith('.'):
                    continue

                file_path = os.path.join(dirpath, fname)
                try:
                    if file_path.endswith('.tf') or file_path.endswith('.yaml'):
                        with open(file_path, 'r', encoding='utf-8') as in_f:
                            # Write a header with the file’s relative path
                            rel_path = os.path.relpath(file_path, root_dir)
                            out_f.write(f"--- {rel_path} ---\n")
                            out_f.write(in_f.read())
                            out_f.write("\n\n")
                except Exception as e:
                    # Report errors but continue
                    print(f"Warning: could not read {file_path}: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(
        description="Recursively concatenate all files under a directory into one .txt, "
                    "skipping hidden directories/files.")
    parser.add_argument(
        "root_dir",
        help="Root directory to recurse into.")
    parser.add_argument(
        "-o", "--output",
        default="combined.txt",
        help="Path to the output text file (default: combined.txt).")
    args = parser.parse_args()

    if not os.path.isdir(args.root_dir):
        print(f"Error: '{args.root_dir}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    combine_files(args.root_dir, args.output)
    print(f"All files under '{args.root_dir}' have been combined into '{args.output}'.")

if __name__ == "__main__":
    main()
