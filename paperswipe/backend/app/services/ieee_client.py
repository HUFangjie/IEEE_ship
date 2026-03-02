from __future__ import annotations

import asyncio
from datetime import datetime

import httpx


class IEEEClient:
    BASE_URL = "https://ieeexploreapi.ieee.org/api/v1/search/articles"

    def __init__(self, api_key: str):
        self.api_key = api_key

    async def search(self, query: str, publication: str, year_from: int, year_to: int, limit: int) -> list[dict]:
        if not self.api_key:
            raise ValueError("IEEE_API_KEY is required for Metadata API mode")
        params = {
            "apikey": self.api_key,
            "format": "json",
            "max_records": min(limit, 100),
            "start_record": 1,
            "querytext": query,
            "publication_title": "IEEE Transactions on Information Forensics and Security"
            if publication == "TIFS"
            else publication,
        }
        results = []
        async with httpx.AsyncClient(timeout=15) as client:
            for _ in range(3):
                try:
                    await asyncio.sleep(0.3)
                    resp = await client.get(self.BASE_URL, params=params)
                    resp.raise_for_status()
                    data = resp.json()
                    for a in data.get("articles", [])[:limit]:
                        pub_year = int(str(a.get("publication_year", "0"))[:4] or 0)
                        if pub_year < year_from or pub_year > year_to:
                            continue
                        results.append(
                            {
                                "source": "IEEE",
                                "publication": publication,
                                "title": a.get("title", "Untitled"),
                                "authors": [x.get("full_name") for x in a.get("authors", {}).get("authors", []) if x.get("full_name")],
                                "abstract": a.get("abstract", ""),
                                "doi": a.get("doi"),
                                "year": pub_year or datetime.utcnow().year,
                                "published_date": a.get("publication_date"),
                                "xplore_url": a.get("html_url") or a.get("pdf_url") or "",
                                "pdf_url": a.get("pdf_url"),
                                "is_oa": 1 if str(a.get("access_type", "")).lower() in {"open access", "ephemera"} else 0,
                            }
                        )
                    return results[:limit]
                except Exception:
                    await asyncio.sleep(1.5)
        return []
