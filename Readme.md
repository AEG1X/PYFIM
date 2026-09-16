# PyFIM — Python File Integrity Monitor

A small command-line tool to calculate SHA-256 hashes of files and
directories, compare them against a known value, and detect unauthorized
or unexpected changes over time by saving and re-checking snapshots.

Built as a learning project while studying cybersecurity (EPITA), with no
external dependencies — pure Python standard library.

## Features

- Calculate the SHA-256 hash of a single file or every file in a directory
  (recursively)
- Compare a computed hash against a known/expected reference hash
- Save a snapshot of a directory's current state (`--save`, `--s`)
- Check a directory against its last saved snapshot (`--check`, `--c`) and report:
  - `UNCHANGED` — file content is identical to the snapshot
  - `MODIFIED` — file content has changed since the snapshot
  - `NEW` — file wasn't present in the snapshot
  - `DELETED` — file was in the snapshot but no longer exists
- Clear error handling for invalid paths

## Requirements

- Python 3.7+
- No third-party dependencies

## Installation

```bash
git clone https://github.com/AEG1X/pyfim.git
cd pyfim
```

## Usage

Hash a single file:

```bash
python3 pyfim.py path/to/file.txt
```

Hash every file in a directory (recursively):

```bash
python3 pyfim.py path/to/directory
```

Compare a file against a known/expected hash:

```bash
python3 pyfim.py path/to/file.txt --expected-hash <sha256_hash>
```

Save a snapshot of a directory's current state:

```bash
python3 pyfim.py path/to/directory --save
```

Check the directory against the last saved snapshot:

```bash
python3 pyfim.py path/to/directory --check
```

## How it works

Every file has a unique SHA-256 fingerprint (hash) based on its exact
content — changing even a single byte produces a completely different
hash. `--save` records the current hash of every file in a directory into
`snapshot.json`. Running `--check` later recomputes the current hashes and
compares them against that snapshot to report exactly what changed.

This is a simplified version of the technique used by File Integrity
Monitoring (FIM) tools such as Tripwire or AIDE, commonly used to detect
tampering or unauthorized modifications on sensitive files and systems.

## Possible improvements

- Configurable snapshot file path (`--snapshot-file`)
- Ignore patterns (e.g. skip `.git`, `__pycache__`)
- Support for other hash algorithms (SHA-1, MD5, BLAKE2)
- Export check results as JSON/CSV for automation

## Author & credits

Code written by Aegis. This README was drafted with the help of Claude
(Anthropic).

## License

MIT — see [LICENSE](LICENSE).
