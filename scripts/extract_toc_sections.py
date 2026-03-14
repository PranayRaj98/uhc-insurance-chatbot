import os
import re
from pathlib import Path

from pypdf import PdfReader
from tqdm import tqdm


DATA_DIR = Path("./data/uhc_policies")


def extract_toc_sections_from_page_text(text: str) -> list[str]:
    """
    Given the text of a page that includes a Table of Contents,
    extract probable section titles.
    """
    lines = [ln.strip() for ln in text.splitlines()]

    sections: list[str] = []
    in_toc = False

    for line in lines:
        if not in_toc:
            # Look for the heading that starts the TOC
            if "table of contents" in line.lower():
                in_toc = True
            continue

        # Once we're in the TOC block, stop if we hit an obviously unrelated heading
        if line.lower().startswith("references"):
            break
        if not line:
            # allow occasional blank lines, but don't collect them
            continue

        # Heuristic 1: lines that look like "Section Title ..... 3"
        m = re.match(r"^(.*?)(?:\s?\.{2,}\s*|\s{2,})(\d+)$", line)
        if m:
            title = m.group(1).strip()
            if title:
                sections.append(title)
            continue

        # Heuristic 2: lines that look like numbered headings "1. Introduction"
        m2 = re.match(r"^\d+(\.\d+)*\s+(.*)$", line)
        if m2:
            title = m2.group(2).strip()
            if title:
                sections.append(title)
            continue

    return sections


def extract_unique_toc_sections(data_dir: Path) -> set[str]:
    """
    Iterate all PDFs in data_dir, extract TOC sections, and return unique set.
    """
    pdf_files = sorted(data_dir.glob("*.pdf"))
    print(f"Found {len(pdf_files)} PDF files under '{data_dir}'.")

    unique_sections: set[str] = set()

    for pdf_path in tqdm(pdf_files, desc="Processing PDFs"):
        try:
            reader = PdfReader(str(pdf_path))
        except Exception as e:
            print(f"[ERROR] Failed to open {pdf_path.name}: {e}")
            continue

        pdf_sections: set[str] = set()

        for page_index, page in enumerate(reader.pages):
            try:
                text = page.extract_text() or ""
            except Exception as e:
                print(f"[WARN] Failed to extract text from {pdf_path.name} page {page_index}: {e}")
                continue

            if "table of contents" not in text.lower():
                continue

            sections = extract_toc_sections_from_page_text(text)
            if sections:
                pdf_sections.update(sections)

        if pdf_sections:
            print(f"\n[PDF] {pdf_path.name} - found {len(pdf_sections)} TOC sections.")
            for s in sorted(pdf_sections):
                print(f"    - {s}")

        unique_sections.update(pdf_sections)

    return unique_sections


if __name__ == "__main__":
    if not DATA_DIR.exists():
        print(f"Data directory '{DATA_DIR}' does not exist. "
              f"Make sure PDFs are downloaded to './data/uhc_policies'.")
        raise SystemExit(1)

    sections = extract_unique_toc_sections(DATA_DIR)

    print("\n========== UNIQUE TOC SECTIONS ACROSS ALL PDFs ==========\n")
    for s in sorted(sections):
        print(f"- {s}")

    print(f"\nTotal unique sections: {len(sections)}")

