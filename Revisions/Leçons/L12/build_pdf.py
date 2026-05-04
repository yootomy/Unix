#!/usr/bin/env python3
"""Génère le PDF des notes de révision L12 (Shell + Virtualisation).

Pipeline : notes.md -> HTML (markdown lib) -> PDF (WeasyPrint) avec style.css.
Lance : python3 build_pdf.py  (depuis le venv .venv).
"""

from pathlib import Path
import sys

import markdown
from weasyprint import HTML, CSS

HERE = Path(__file__).resolve().parent
SRC_MD = HERE / "notes.md"
SRC_CSS = HERE / "style.css"
OUT_PDF = HERE / "notes_revision_L12.pdf"


def main() -> int:
    if not SRC_MD.exists():
        sys.stderr.write(f"Source introuvable: {SRC_MD}\n")
        return 1
    if not SRC_CSS.exists():
        sys.stderr.write(f"CSS introuvable: {SRC_CSS}\n")
        return 1

    md_text = SRC_MD.read_text(encoding="utf-8")

    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "sane_lists", "toc", "attr_list"],
        output_format="html5",
    )
    body_html = md.convert(md_text)

    full_html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Notes de révision — L12</title>
</head>
<body>
{body_html}
</body>
</html>
"""

    HTML(string=full_html, base_url=str(HERE)).write_pdf(
        target=str(OUT_PDF),
        stylesheets=[CSS(filename=str(SRC_CSS))],
    )

    size_kb = OUT_PDF.stat().st_size / 1024
    print(f"OK -> {OUT_PDF}  ({size_kb:.1f} Kio)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
