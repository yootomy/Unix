#!/usr/bin/env python3
"""Generate the L12 v2 revision PDF from notes_v2.md."""

from pathlib import Path
import subprocess
import sys
import tempfile

import markdown

HERE = Path(__file__).resolve().parent
SRC_MD = HERE / "notes_v2.md"
SRC_CSS = HERE / "style_v2.css"
OUT_PDF = HERE.parent.parent / "notes_revision_L12_v2.pdf"


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

    css_text = SRC_CSS.read_text(encoding="utf-8")
    full_html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Notes de revision L12 v2</title>
<style>
{css_text}
</style>
</head>
<body>
{body_html}
</body>
</html>
"""

    try:
        from weasyprint import HTML, CSS

        HTML(string=full_html, base_url=str(HERE)).write_pdf(
            target=str(OUT_PDF),
            stylesheets=[CSS(filename=str(SRC_CSS))],
        )
    except Exception as exc:
        sys.stderr.write(f"WeasyPrint indisponible, fallback navigateur: {exc}\n")
        render_with_browser(full_html)

    size_kb = OUT_PDF.stat().st_size / 1024
    print(f"OK -> {OUT_PDF}  ({size_kb:.1f} Kio)")
    return 0


def render_with_browser(full_html: str) -> None:
    browser = find_browser()
    if browser is None:
        raise RuntimeError("Aucun navigateur Chromium/Edge trouve pour generer le PDF")

    OUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="notes_l12_v2_") as tmpdir:
        html_path = Path(tmpdir) / "notes_v2.html"
        html_path.write_text(full_html, encoding="utf-8")
        cmd = [
            str(browser),
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={OUT_PDF}",
            html_path.as_uri(),
        ]
        result = subprocess.run(cmd, cwd=str(HERE), text=True, capture_output=True)
        if result.returncode != 0:
            sys.stderr.write(result.stdout)
            sys.stderr.write(result.stderr)
            raise RuntimeError(f"Echec generation PDF via navigateur: code {result.returncode}")


def find_browser() -> Path | None:
    candidates = [
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


if __name__ == "__main__":
    raise SystemExit(main())
