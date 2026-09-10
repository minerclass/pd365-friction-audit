#!/usr/bin/env python3
"""Generate the public participant deck from the facilitator source.

The facilitator source carries per-slide notes in `data-notes` attributes,
a notes side panel, and an `N` key binding. None of that belongs in the
public build: some notes plan for contingencies that read poorly beside a
partner's event listing.

    python tools/build_participant_deck.py <source.html> deck/index.html

The source is an artifact-style fragment: a bare <title>, <link> and
<style> followed by body content, with no <html>/<head>/<body> wrapper.
This script strips the notes, then wraps the fragment into a standalone
document for GitHub Pages.

The export button needs no change. It already falls back to "use your
browser's print dialogue" when `window.claude` is absent, which is always
the case outside the artifact host.
"""
import io
import os
import re
import sys

SKELETON = (
    '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    '<meta name="color-scheme" content="light dark">\n'
    '<link rel="icon" href="data:,">\n'
    '<style>*{box-sizing:border-box}html{color-scheme:light dark}'
    'body{margin:0;font:14px/1.5 system-ui,sans-serif;background:#f4f6f8}'
    'img{max-width:100%}[hidden]{display:none!important}</style>\n'
    '__HEAD__\n</head>\n<body>\n__BODY__\n</body>\n</html>\n'
)

# Each pair is (pattern, replacement, is_regex). Order matters: markup first,
# then the JavaScript that referenced it.
STRIPS = [
    (r'\s*data-notes="[^"]*"', '', True),
    (r'<aside class="notes".*?</aside>\s*', '', True),
    (r'\s*<button class="cbtn wide" id="notesBtn"[^>]*>Notes</button>', '', True),
    ('var notesEl = document.getElementById("notes");\n'
     '  var notesText = document.getElementById("notesText");\n'
     '  var notesBtn = document.getElementById("notesBtn");\n'
     '  var notesOpen = false;\n', '  var notesOpen = false;\n', False),
    (r'\n  function paintNotes\(\)\{.*?\n  \}\n', '\n  function paintNotes(){}\n', True),
    (r'\n  function toggleNotes\(force\)\{.*?\n  \}\n'
     r'  notesBtn\.addEventListener\("click", function\(\)\{ toggleNotes\(\); \}\);\n',
     '\n  function toggleNotes(){}\n', True),
    ('else if (e.key === "n" || e.key === "N"){ toggleNotes(); }\n    ', '', False),
    ('if (menuOpen) toggleMenu(false); else if (notesOpen) toggleNotes(false); return;',
     'if (menuOpen) toggleMenu(false); return;', False),
    ('<kbd>N</kbd> facilitator notes &nbsp; ', '', False),
    ('if (notesOpen) paintNotes();\n    tickTimer();', 'tickTimer();', False),
]


def split_head(src):
    """Lift <title>, <link> and <style> out of the fragment into a head block."""
    head, body = [], src
    for pattern in (r'<title>.*?</title>\s*', r'<link\b[^>]*>\s*', r'<style>.*?</style>\s*'):
        head.extend(m.strip() for m in re.findall(pattern, body, flags=re.S))
        body = re.sub(pattern, '', body, flags=re.S)
    return "\n".join(head), body.strip()


def build(src_path, out_path):
    src = io.open(src_path, encoding="utf-8").read()
    slides_before = src.count('class="slide')

    for pattern, replacement, is_regex in STRIPS:
        if is_regex:
            src = re.sub(pattern, replacement, src, flags=re.S)
        else:
            if pattern not in src:
                print("  warning: strip pattern not found: %s..." % pattern[:60])
            src = src.replace(pattern, replacement)

    for leaked in ("data-notes", "notesBtn", "notesText", 'id="notes"'):
        if leaked in src:
            raise SystemExit("refusing to write: %r survived the strip" % leaked)

    head, body = split_head(src)
    out = SKELETON.replace("__HEAD__", head).replace("__BODY__", body)

    if out.count('class="slide') != slides_before:
        raise SystemExit("refusing to write: slide count changed during build")

    directory = os.path.dirname(out_path)
    if directory:
        try:
            os.makedirs(directory)
        except OSError:
            pass
    io.open(out_path, "w", encoding="utf-8").write(out)
    print("wrote %s (%d slides, %d bytes)" % (out_path, slides_before, len(out)))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    build(sys.argv[1], sys.argv[2])
