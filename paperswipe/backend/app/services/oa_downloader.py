from __future__ import annotations

from pathlib import Path

import httpx


async def download_pdf(pdf_url: str, output_path: Path) -> str | None:
    if not pdf_url:
        return "Missing pdf_url"
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.get(pdf_url)
            r.raise_for_status()
            output_path.write_bytes(r.content)
        return None
    except Exception as exc:
        return str(exc)
