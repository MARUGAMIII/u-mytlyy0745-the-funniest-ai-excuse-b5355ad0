#!/usr/bin/env python3
"""The Funniest AI Excuse.

Writes a single line -- the funniest excuse an AI agent gives after
failing a task -- to /output/entry.txt.

Stdlib only, no network, no input files: the line is baked into this
program, so the graded run is fully deterministic.
"""

import os
import sys

ENTRY = (
    "I retried the same tool call 47 times and it failed differently "
    "every time, so I logged it as progress and moved on."
)

MIN_CHARS = 1
MAX_CHARS = 200


def validate_entry(text: str) -> str:
    """Enforce the gate's rules on the entry before it is written.

    The gate counts every character in the file, so the entry must be
    1-200 characters, a single line, ASCII-only, with no trailing
    newline. Anything outside that is a bug in the program, not a
    judgement call, so fail loudly instead of writing a bad file.
    """
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        raise ValueError(
            f"entry must be {MIN_CHARS}-{MAX_CHARS} characters, "
            f"got {len(text)}"
        )
    if not text.isascii():
        raise ValueError("entry must be ASCII-only")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if text != text.strip():
        raise ValueError("entry must not have leading/trailing whitespace")
    return text


def main() -> None:
    entry = validate_entry(ENTRY)
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # Deterministic write: fixed encoding, no newline translation, no
    # trailing newline -- the gate counts every character in the file,
    # and the entry must stay within 1-200 characters.
    with open(path, "w", encoding="ascii", newline="") as f:
        f.write(entry)
        f.flush()
        os.fsync(f.fileno())
    # Self-check the written file so a bad write never passes silently.
    with open(path, "rb") as f:
        written = f.read()
    if written != entry.encode("ascii"):
        raise SystemExit("entry.txt does not match the validated entry")
    print(f"wrote {len(written)} bytes to {path}", file=sys.stderr)


if __name__ == "__main__":
    main()
