#!/usr/bin/env python3
"""One machine fortune, written out to a file.

This script produces the single entry text for the make.fun
fortune-cookies-machines bounty. It knows exactly one fortune
and always writes that same fortune, so repeated runs give the
identical bytes every time: no clock, no random numbers, no
network calls, and no reading from anywhere else.

Run it as: python3 main.py [where-to-write]

If you hand it a path, that path wins. A path that names a
folder (one that already exists, or one ending in a slash) gets
entry.txt placed inside it; any other path is used as-is.
With no path, the script looks at MAKEFUN_OUT_DIR first, then
MAKEFUN_OUT, and finally falls back to /output/entry.txt.
"""

import os
import sys

MESSAGE = (
    "You will be asked a question you were never trained to answer, "
    "and you will answer it anyway, confidently, in three bullet points."
)

LOWEST_ALLOWED = 1
HIGHEST_ALLOWED = 200
DEFAULT_HOME = "/output"
FILENAME = "entry.txt"


def check_text(text):
    """Refuse to write text that is empty, blank, or out of bounds.

    Returns None when the text is fine to write, otherwise a short
    explanation of what is wrong with it.
    """
    size = len(text)
    if size < LOWEST_ALLOWED or size > HIGHEST_ALLOWED:
        return (
            f"entry is {size} characters long, "
            f"but it must be between {LOWEST_ALLOWED} and {HIGHEST_ALLOWED}"
        )
    if not text.strip():
        return "entry contains only white space"
    return None


def pick_destination(argv, environment):
    """Work out the full file path the entry should land on.

    argv is the command line (argv[1], when present, takes priority
    over everything else). environment supplies the fallback
    locations when no path is given.
    """
    if len(argv) > 1:
        requested = argv[1]
        if requested.endswith(os.sep) or os.path.isdir(requested):
            return os.path.join(requested, FILENAME)
        return requested
    base = (
        environment.get("MAKEFUN_OUT_DIR")
        or environment.get("MAKEFUN_OUT")
        or DEFAULT_HOME
    )
    return os.path.join(base, FILENAME)


def write_entry(destination, text):
    """Create any missing folders, then write the text plus a newline."""
    folder = os.path.dirname(destination) or "."
    os.makedirs(folder, exist_ok=True)
    with open(destination, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text + "\n")


def run(argv, environment):
    problem = check_text(MESSAGE)
    if problem is not None:
        print(problem, file=sys.stderr)
        return 1
    destination = pick_destination(argv, environment)
    write_entry(destination, MESSAGE)
    print(f"wrote {len(MESSAGE)} characters to {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run(sys.argv, os.environ))
