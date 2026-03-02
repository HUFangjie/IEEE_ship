from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .oa_downloader import download_pdf


def _safe_id(doi: str | None, title: str, year: int) -> str:
    if doi:
        return doi.replace("/", "_")
    return hashlib.sha1(f"{title}{year}".encode()).hexdigest()


def bibtex_from_paper(paper: dict) -> str:
    key = (paper.get("doi") or paper.get("id", "paper")).replace("/", "_")
    authors = " and ".join(paper.get("authors", []))
    return (
        f"@article{{{key},\n"
        f"  title={{{paper.get('title','')}}},\n"
        f"  author={{{authors}}},\n"
        f"  journal={{IEEE Transactions on Information Forensics and Security}},\n"
        f"  year={{{paper.get('year','')}}},\n"
        f"  doi={{{paper.get('doi','')}}},\n"
        f"  url={{{paper.get('xplore_url','')}}}\n"
        "}\n"
    )


async def write_liked_bundle(library_path: str, paper: dict, summary_json: dict, summary_md: str) -> tuple[str, str | None]:
    safe_id = _safe_id(paper.get("doi"), paper["title"], paper["year"])
    out_dir = Path(library_path) / "TIFS" / str(paper["year"]) / safe_id
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "meta.json").write_text(json.dumps(paper, ensure_ascii=False, indent=2))
    (out_dir / "summary.json").write_text(json.dumps(summary_json, ensure_ascii=False, indent=2))
    (out_dir / "summary.md").write_text(summary_md)
    (out_dir / "cite.bib").write_text(bibtex_from_paper(paper))

    error = None
    if paper.get("is_oa") == 1 and paper.get("pdf_url"):
        error = await download_pdf(paper["pdf_url"], out_dir / "paper.pdf")
    else:
        (out_dir / "download_instructions.md").write_text(
            "Open link via institution and download manually.\n"
            f"Xplore URL: {paper.get('xplore_url','')}\n"
        )

    return str(out_dir), error
