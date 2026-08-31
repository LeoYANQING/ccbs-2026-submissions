#!/usr/bin/env python3
"""Assemble the week's extension-by-audience skeleton.

Usage:
    python3 tools/assemble_extension.py week5 [--out week5/extension_skeleton.html]

Scans <week>/*_ext.html, extracts each submission's title, author and body content,
and writes ONE skeleton HTML page: every micro-essay placed in order, each wrapped in
a section with author attribution, plus assembly notes at the top. The skeleton is a
*starting point* — the TA then hands it to an AI agent with the instruction to weave
the essays into one coherent themed long-form writeup (keep authors; keep conflicts
and opposing views visibly in conversation), reviews the result, and ships it as the
week's extension-by-audience page to the main course site
(assets/ccbs/2026fall/weekN/extension/index.html).

Stdlib only. Run with any Python 3.9+.
"""

import re
import sys
from html.parser import HTMLParser
from pathlib import Path


class Page(HTMLParser):
    """Collect <title>, meta author, and the inner HTML of <body>."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.author = ""
        self.in_title = False
        self.depth = 0            # 1 = we are inside <body>
        self.body_chunks = []
        self.void = {"meta", "link", "br", "hr", "img", "input", "source", "wbr"}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self.in_title = True
        if tag == "meta" and a.get("name", "").lower() == "author":
            self.author = a.get("content", "").strip()
        if tag == "body":
            self.depth = 1
        elif self.depth:
            self.depth += 1
            if tag not in self.void:
                self.body_chunks.append(f"<{tag}>")

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if self.depth:
            self.body_chunks.append(f"</{tag}>")
            if tag == "body":
                self.depth = 0
            else:
                self.depth = max(1, self.depth - 1)

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.depth:
            self.body_chunks.append(data)

    @property
    def body(self):
        return "".join(self.body_chunks).strip()


def author_from_filename(path: Path) -> str:
    m = re.match(r"week\d+_(.+)_ext\.html$", path.name)
    return (m.group(1).replace("_", " ").title() if m else path.stem)


def main() -> int:
    args = list(sys.argv[1:])
    out = None
    if "--out" in args:
        i = args.index("--out")
        if i + 1 < len(args):
            out = Path(args[i + 1])
            del args[i:i + 2]
    week = Path(args[0]) if args else Path(".")
    out = out or (week / "extension_skeleton.html")
    entries = sorted(week.glob("*_ext.html"))
    if not entries:
        print(f"no *_ext.html files found in {week}", file=sys.stderr)
        return 1

    sections = []
    for p in entries:
        page = Page()
        try:
            page.feed(p.read_text(encoding="utf-8", errors="replace"))
        except OSError as e:
            print(f"skip {p.name}: {e}", file=sys.stderr)
            continue
        title = (page.title or f"{p.stem}").strip()
        author = (page.author or author_from_filename(p)).strip()
        sections.append((p.name, author, title, page.body))

    head = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Week {week.name} — Extension by the audience (skeleton)</title>
<style>
  :root {{ --ink:#1a1a1a; --muted:#566; --accent:#1f4e79; --line:#d8dee4; --bg:#fff; --soft:#f6f8fa; }}
  @media (prefers-color-scheme: dark) {{
    :root {{ --ink:#e8e8e8; --muted:#9aa; --accent:#8ab4e8; --line:#3a4652; --bg:#15191d; --soft:#1e242a; }}
  }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--ink); font-family:"Segoe UI",Roboto,Arial,sans-serif; line-height:1.6; }}
  .wrap {{ max-width:820px; margin:0 auto; padding:40px 22px 80px; }}
  h1 {{ font-size:1.6rem; color:var(--accent); }}
  .notes {{ background:var(--soft); border:1px solid var(--line); border-radius:6px; padding:12px 16px; font-size:.9rem; }}
  article {{ margin-top:34px; }}
  article h2 {{ font-size:1.1rem; color:var(--accent); }}
  .byline {{ color:var(--muted); font-size:.9rem; }}
</style>
</head>
<body>
<div class="wrap">
<h1>Week {week.name} — Extension by the audience</h1>
<div class="notes"><strong>Assembly notes (delete before publishing):</strong> this is a
skeleton with each student's micro-essay placed in order. Weave them into ONE coherent
themed long-form writeup with an AI agent: give each piece a home in a shared argument
(or a deliberate turn/contrast), keep author attribution, keep conflicting positions
visibly in conversation with each other, and fix any internal contradictions in the
editorial voice (not by erasing them). Then review, retitle, and publish as the week's
extension-by-audience page.</div>
"""

    body = "\n".join(
        f"""
<article>
<h2>{esc(title)}</h2>
<p class="byline">{esc(author)} · ({esc(name)})</p>
{body_html}
</article>"""
        for name, author, title, body_html in sections
    )

    tail = "\n</div>\n</body>\n</html>\n"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(head + body + tail, encoding="utf-8")
    print(f"wrote {out} from {len(sections)} submissions")
    for name, author, title, _ in sections:
        print(f"  - {name}  [{author}]  {title[:60]}")
    return 0


def esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


if __name__ == "__main__":
    raise SystemExit(main())
