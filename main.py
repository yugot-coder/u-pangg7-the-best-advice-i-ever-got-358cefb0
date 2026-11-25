"""The Best Advice I Ever Got — make.fun entry.

Writes one sentence (<= 200 characters) to /output/entry.txt
(or ./entry.txt when /output does not exist).
Standard library only; deterministic: two runs are byte-identical.
"""

import hashlib
import os
import sys

TEXT = (
    "My father pressed his last twenty into my hand the morning I left "
    "for the city and said, \"Spend it on food, not pride \u2014 hunger "
    "passes, but a debt to a stranger follows you home.\""
)


def check_gate(text: str) -> None:
    """Validate the gate: UTF-8, 1-200 chars, one sentence, not whitespace."""
    if not text or not text.strip():
        raise ValueError("entry is empty or only whitespace")
    if len(text) > 200:
        raise ValueError(f"entry is {len(text)} characters, over the 200 limit")
    text.encode("utf-8")  # raises if not valid UTF-8-encodable
    # One sentence: exactly one terminal punctuation mark at the end
    # (allowing a closing quote after it), and no other sentence-ending
    # punctuation inside.
    stripped = text.rstrip("\"'\u201d")
    if stripped[-1] not in ".!?":
        raise ValueError("entry does not end with sentence punctuation")
    inner = stripped[:-1]
    if any(ch in inner for ch in ".!?"):
        raise ValueError("entry contains more than one sentence")


def main() -> int:
    check_gate(TEXT)
    data = TEXT.encode("utf-8")
    out_dir = "/output" if os.path.isdir("/output") else "."
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(data)
    print(f"wrote {path} ({len(TEXT)} chars)")
    print(f"sha256: {hashlib.sha256(data).hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
