from __future__ import annotations

import json

import httpx


SYSTEM_PROMPT = """You summarize research paper abstracts. Only use abstract facts. If missing, use 'Not specified in abstract'. Output strict JSON only with keys: one_liner, problem, core_idea, threat_model_or_assumptions, experiments, results, limitations, relevance_to_query, tags."""


def default_summary(user_query: str) -> dict:
    return {
        "one_liner": "Not specified in abstract",
        "problem": "Not specified in abstract",
        "core_idea": "Not specified in abstract",
        "threat_model_or_assumptions": "Not specified in abstract",
        "experiments": "Not specified in abstract",
        "results": "Not specified in abstract",
        "limitations": ["Not specified in abstract"],
        "relevance_to_query": {"score": 50, "why": f"Potentially related to {user_query}."},
        "tags": ["TIFS"],
    }


async def summarize_openai(api_key: str, model: str, payload: dict) -> tuple[dict, str]:
    if not api_key:
        s = default_summary(payload.get("user_query", "query"))
        return s, render_markdown(s, payload)
    body = {
        "model": model,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ],
        "temperature": 0.2,
    }
    async with httpx.AsyncClient(timeout=25) as client:
        resp = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json=body,
        )
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
        data = json.loads(content)
        return data, render_markdown(data, payload)


def render_markdown(summary: dict, payload: dict) -> str:
    return (
        f"# {payload.get('title', 'Paper')}\n\n"
        f"- **One-liner**: {summary.get('one_liner','')}\n"
        f"- **Problem**: {summary.get('problem','')}\n"
        f"- **Method**: {summary.get('core_idea','')}\n"
        f"- **Results**: {summary.get('results','')}\n"
        f"- **Limitations**: {summary.get('limitations','')}\n"
    )


async def summarize_kimi(api_key: str, model: str, payload: dict) -> tuple[dict, str]:
    if not api_key:
        s = default_summary(payload.get("user_query", "query"))
        return s, render_markdown(s, payload)
    body = {
        "model": model,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ],
        "temperature": 0.2,
    }
    async with httpx.AsyncClient(timeout=25) as client:
        resp = await client.post(
            "https://api.moonshot.cn/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json=body,
        )
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
        data = json.loads(content)
        return data, render_markdown(data, payload)
