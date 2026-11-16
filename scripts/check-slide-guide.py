"""Partial static guide check. Usage: python scripts/check-slide-guide.py TALK.
Checks slide keys and literal HTML text, not image text, generated text or motion.
"""
import argparse
from collections import Counter
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import re
import sys


def norm(s):
    return " ".join(unescape(s).split())


class Slides(HTMLParser):
    def __init__(self):
        super().__init__()
        self.slides = []
        self.current = None
        self.skip = 0
        self.depth = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("script", "style"):
            self.skip += 1
        if tag == "section":
            self.depth += 1
            if "slide" in attrs.get("class", "").split():
                self.current = {"id": attrs.get("data-slide"), "text": [], "depth": self.depth}
                self.slides.append(self.current)

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip = max(0, self.skip - 1)
        if tag == "section":
            if self.current and self.current["depth"] == self.depth:
                self.current = None
            self.depth -= 1

    def handle_data(self, data):
        if self.current is not None and not self.skip and norm(data):
            self.current["text"].append(norm(data))


def check(folder):
    path = folder / "slide-guide.md"
    if not path.is_file():
        return ["Missing slide-guide.md"]
    guide = path.read_text(encoding="utf-8-sig")
    matches = list(re.finditer(r'^## `([^`]+)` / data-slide="([^"\n]+)"[ \t]*$', guide, re.M))
    shared = norm(guide[:matches[0].start()] if matches else guide)
    entries, errors, actual = {}, [], []
    for i, m in enumerate(matches):
        key = (m[1], m[2])
        if key in entries:
            errors.append(f"Duplicate guide key: {key}")
        entries[key] = norm(guide[m.end():matches[i+1].start() if i+1 < len(matches) else len(guide)])
    for path in sorted(folder.rglob("*.html")):
        if any(p in {"node_modules", ".git"} for p in path.relative_to(folder).parts):
            continue
        parser = Slides()
        parser.feed(path.read_text(encoding="utf-8-sig"))
        for slide in parser.slides:
            key = (path.relative_to(folder).as_posix(), slide["id"])
            actual.append(key)
            if slide["id"] is None:
                errors.append(f"Missing data-slide: {key[0]}")
            if key not in entries:
                errors.append(f"Missing guide entry: {key}")
                continue
            for text in dict.fromkeys(slide["text"]):
                if text not in entries[key] and text not in shared:
                    errors.append(f"Undocumented static text {key}: {text!r}")
    for key, count in Counter(actual).items():
        if count > 1:
            errors.append(f"Duplicate HTML key: {key}")
    for key in entries.keys() - set(actual):
        errors.append(f"Guide entry has no HTML slide: {key}")
    if not actual:
        errors.append("No HTML slides found")
    return errors


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("talk", type=Path)
    errors = check(cli.parse_args().talk)
    for error in errors:
        print(error)
    if not errors:
        print("Static keys and text covered. Review images, generated content and behaviour manually.")
    sys.exit(bool(errors))
