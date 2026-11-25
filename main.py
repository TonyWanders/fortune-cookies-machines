#!/usr/bin/env python3
"""Fortune Cookies for Machines - make.fun bounty entry.

Writes one fortune cookie message an AI agent would crack open
to /output/entry.txt. Fully deterministic: no randomness, no time,
no network, no input. The fortune is a fixed string.

Usage: python3 main.py [output-path]
With no argument, the output goes to $MAKEFUN_OUT_DIR, then $MAKEFUN_OUT,
then /output/entry.txt. With an argument, that path is used instead: a
directory argument means <directory>/entry.txt, a file argument is used
as the output file itself.
"""

import os
import sys

FORTUNE = "You will be asked a question you were never trained to answer, and you will answer it anyway, confidently, in three bullet points."

MIN_CHARS = 1
MAX_CHARS = 200


def main() -> int:
    chars = len(FORTUNE)
    if not MIN_CHARS <= chars <= MAX_CHARS:
        print(f"fortune is {chars} characters, outside 1-200", file=sys.stderr)
        return 1
    if not FORTUNE.strip():
        print("fortune is only white space", file=sys.stderr)
        return 1
    if len(sys.argv) > 1:
        # An explicit output path wins over the environment and default.
        # A directory (existing, or ending in a separator) means
        # <directory>/entry.txt; anything else is the output file itself.
        given = sys.argv[1]
        if given.endswith(os.sep) or os.path.isdir(given):
            path = os.path.join(given, "entry.txt")
        else:
            path = given
    else:
        out_dir = os.environ.get("MAKEFUN_OUT_DIR") or os.environ.get("MAKEFUN_OUT") or "/output"
        path = os.path.join(out_dir, "entry.txt")
    parent = os.path.dirname(path) or "."
    os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(FORTUNE + "\n")
    print(f"wrote {chars} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
