#!/usr/bin/env python3
"""
PyFIM - Python File Integrity Monitor

A simple command-line tool to calculate, compare, and monitor SHA-256
hashes of files and directories, in order to detect unauthorized or
unexpected modifications over time.
"""

import argparse
import hashlib
import json
import os
import sys

SNAPSHOT_FILE = "snapshot.json"

parser = argparse.ArgumentParser(
    prog="pyfim",
    description=(
        "Calculate SHA-256 hashes of files/directories, compare them, "
        "and monitor changes over time using saved snapshots."
    ),
)
parser.add_argument("path", type=str, help="Path to the file or directory to hash")
parser.add_argument(
    "--expected-hash",
    "--eh",
    type=str,
    help="Expected SHA-256 hash to compare the file against",
)
parser.add_argument(
    "--save",
    "--s",
    action="store_true",
    help="Save the current state (hashes) as a snapshot for later comparison",
)
parser.add_argument(
    "--check",
    "--c",
    action="store_true",
    help="Compare the current state against the last saved snapshot",
)

args = parser.parse_args()
files_info = []


def calculate_hash(filepath):
    with open(filepath, "rb") as f:
        file_content = f.read()
        sha256_hash = hashlib.sha256(file_content).hexdigest()
    return sha256_hash


def collect_file_info(path):
    if os.path.isdir(path):
        for element in os.listdir(path):
            collect_file_info(os.path.join(path, element))
    else:
        file_info = {
            "name": os.path.basename(path),
            "path": path,
            "sha256": calculate_hash(path),
        }
        files_info.append(file_info)


def compare_hashes(computed_hash, expected_hash, filepath):
    if computed_hash == expected_hash:
        print(f"Hash matches: {filepath}")
    else:
        print(f"Hash does not match: {filepath} (computed: {computed_hash})")


def save_snapshot():
    with open(SNAPSHOT_FILE, "w", encoding="utf-8") as f:
        json.dump(files_info, f, ensure_ascii=False, indent=4)
    print(f"Snapshot saved to {SNAPSHOT_FILE}")


def check_snapshot():
    """Compare the current state against the saved snapshot and report changes."""
    try:
        with open(SNAPSHOT_FILE, "r", encoding="utf-8") as f:
            saved_data = json.load(f)
    except FileNotFoundError:
        print(f"No snapshot found ({SNAPSHOT_FILE}). Run with --save first.")
        sys.exit(1)

    # Detect modified / unchanged / new files
    for file_info in files_info:
        saved_entry = next(
            (entry for entry in saved_data if entry["path"] == file_info["path"]),
            None,
        )
        if saved_entry:
            if file_info["sha256"] == saved_entry["sha256"]:
                print(f"UNCHANGED: {file_info['path']}")
            else:
                print(f"MODIFIED:  {file_info['path']}")
        else:
            print(f"NEW:       {file_info['path']}")

    # Detect deleted files
    for saved_entry in saved_data:
        still_exists = next(
            (f for f in files_info if f["path"] == saved_entry["path"]), None
        )
        if not still_exists:
            print(f"DELETED:   {saved_entry['path']}")


if not os.path.exists(args.path):
    print(f"Error: path not found: {args.path}")
    sys.exit(1)

collect_file_info(args.path)

if args.expected_hash is not None:
    for file_info in files_info:
        compare_hashes(file_info["sha256"], args.expected_hash, file_info["path"])
else:
    for file_info in files_info:
        print(f"SHA-256 of {file_info['path']}: {file_info['sha256']}")

if args.save:
    save_snapshot()

if args.check:
    check_snapshot()
