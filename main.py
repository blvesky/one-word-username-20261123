"""Write the entrant's own make.fun handle to /output/entry.txt.

The competition gate requires /output/entry.txt to be UTF-8 text of
1 to 30 characters, not only whitespace. The entry is the entrant's
own make.fun handle, sent as a single word with nothing else.
"""

import os
import tempfile

ENTRY = "daring-lark-71"
OUTPUT_PATH = "/output/entry.txt"
MIN_CHARS = 1
MAX_CHARS = 30


def validate(text):
    """Enforce the competition gate before anything is written."""
    if not isinstance(text, str):
        raise TypeError("entry must be text")
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        raise ValueError(
            "entry must be %d to %d characters, got %d"
            % (MIN_CHARS, MAX_CHARS, len(text))
        )
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if any(ch.isspace() for ch in text):
        raise ValueError("entry must be a single word with no spaces")
    text.encode("utf-8")  # must be valid UTF-8 text
    return text


def write_atomic(path, text):
    """Write via a temp file in the same directory, then rename, so a
    reader never sees a half-written entry."""
    directory = os.path.dirname(path)
    os.makedirs(directory, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=directory, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def main():
    write_atomic(OUTPUT_PATH, validate(ENTRY))


if __name__ == "__main__":
    main()
