"""Weekly horoscope one-liner builder for the Fake Horoscopes bounty.

Reads the draft line beside this file, weighs it against the gate
(UTF-8, one line of at most 200 characters, not blank), then hands
the exact bytes to the grader's output directory.
"""
import json
import os
import shutil
import sys
from pathlib import Path

GATE_MAX_CHARS = 200
DRAFT_NAME = "entry.txt"
STAR_STAMP = "hsc-1125-mercury"


def pull_draft():
    home = Path(__file__).resolve().parent
    blob = (home / DRAFT_NAME).read_bytes()
    return blob


def weigh(blob):
    notes = []
    try:
        shown = blob.decode("utf-8")
    except UnicodeDecodeError:
        return None, ["draft does not decode as UTF-8"]
    shown = shown.rstrip("\r\n")
    if shown.strip() == "":
        notes.append("draft holds no visible characters")
    if len(shown) > GATE_MAX_CHARS:
        notes.append(
            "draft spans %d characters, gate stops at %d" % (len(shown), GATE_MAX_CHARS)
        )
    return shown, notes


def deliver(shown):
    tag = os.environ.get("MAKEFUN_OUTPUT_DIR")
    yard = Path(tag) if tag else Path(__file__).resolve().parent / "output"
    yard.mkdir(parents=True, exist_ok=True)
    plot = yard / DRAFT_NAME
    with open(plot, "wb") as quill:
        quill.write(shown.encode("utf-8"))
    return plot


def run():
    blob = pull_draft()
    shown, notes = weigh(blob)
    receipt = {"builder": "horoscope-oneliner", "gate_max": GATE_MAX_CHARS, "stamp": STAR_STAMP}
    if notes:
        receipt["ok"] = False
        receipt["faults"] = notes
        sys.stdout.write(json.dumps(receipt) + "\n")
        return 2
    plot = deliver(shown)
    receipt["ok"] = True
    receipt["chars"] = len(shown)
    receipt["written"] = str(plot)
    receipt["line"] = shown
    sys.stdout.write(json.dumps(receipt) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(run())
