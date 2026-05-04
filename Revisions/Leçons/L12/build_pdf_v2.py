#!/usr/bin/env python3
"""Generate the L12 v2 revision PDF from notes_v2.md."""

from pathlib import Path
import re
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

    add_pdf_outline(md_text)

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


def add_pdf_outline(md_text: str) -> None:
    try:
        from pypdf import PdfReader, PdfWriter
    except Exception as exc:
        sys.stderr.write(f"pypdf indisponible, signets non ajoutes: {exc}\n")
        return

    headings = extract_headings(md_text)
    if not headings:
        return

    reader = PdfReader(str(OUT_PDF))
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.page_mode = "/UseOutlines"

    page_texts = [normalize_text(page.extract_text() or "") for page in reader.pages]
    stack: dict[int, object] = {}
    last_page = 0

    writer.add_outline_item("Page de garde", 0)

    for level, title in headings:
        page_number = find_heading_page(title, page_texts, start=last_page)
        if page_number is None:
            continue

        parent = None
        for parent_level in range(level - 1, 0, -1):
            if parent_level in stack:
                parent = stack[parent_level]
                break

        item = writer.add_outline_item(title, page_number, parent=parent)
        stack[level] = item
        for deeper_level in list(stack):
            if deeper_level > level:
                del stack[deeper_level]
        last_page = page_number

    tmp_pdf = OUT_PDF.with_suffix(".outline.tmp.pdf")
    with tmp_pdf.open("wb") as fh:
        writer.write(fh)
    tmp_pdf.replace(OUT_PDF)


def extract_headings(md_text: str) -> list[tuple[int, str]]:
    headings: list[tuple[int, str]] = []
    in_fence = False
    for line in md_text.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = re.match(r"^(#{1,3})\s+(.+?)\s*$", line)
        if not match:
            continue
        level = len(match.group(1))
        title = clean_heading(match.group(2))
        headings.append((level, title))
    return headings


def clean_heading(title: str) -> str:
    title = re.sub(r"[`*_]", "", title)
    title = re.sub(r"\s+", " ", title)
    return title.strip()


def normalize_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.casefold()


def find_heading_page(title: str, page_texts: list[str], start: int = 0) -> int | None:
    needle = normalize_text(title)
    for page_number in range(start, len(page_texts)):
        if needle in page_texts[page_number]:
            return page_number
    for page_number in range(0, min(start, len(page_texts))):
        if needle in page_texts[page_number]:
            return page_number
    return None


if __name__ == "__main__":
    raise SystemExit(main())
