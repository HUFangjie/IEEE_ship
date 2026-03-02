# PaperSwipe for IEEE TIFS (MVP)

本项目实现本地部署的论文筛选工具：基于 IEEE Metadata API 拉取 TIFS 元数据 + 摘要，生成结构化总结，并提供 Tinder 风格 Like/Skip。

## 合规说明
- **不抓取 IEEE Xplore HTML 页面**，只使用 IEEE Metadata API。
- **仅对 OA 论文自动下载 PDF**；非 OA 只保存链接并生成人工下载说明。
- 外部调用实现了 timeout/retry（指数退避）与基础速率限制。

## 1. 申请 API Key
- IEEE API：到 IEEE Developer Portal 申请 Metadata API key。
- LLM API：OpenAI（默认）或 Gemini。

## 2. 启动
```bash
cp .env.example .env
# 填入 IEEE_API_KEY, OPENAI_API_KEY 等
docker compose up --build
```

- 前端：http://localhost:3000
- 后端：http://localhost:8000/docs

## 3. 使用流程
1. 打开 `/settings` 保存 IEEE / LLM key 和 library 路径。
2. 回到首页 `/`，设置 query（默认 federated learning）、年份范围、limit，点击 **Fetch & Start**。
3. 在 `/swipe` 页面进行 Like/Skip。
4. Like 后入库到 `library/TIFS/<year>/<doi_or_hash>/`：
   - `meta.json`
   - `summary.json`
   - `summary.md`
   - `cite.bib`
   - OA 时 `paper.pdf`，否则 `download_instructions.md`
5. 在 `/liked` 页面筛选 tag/year 并导出 bib/csv。

## API 概览
- `GET/POST /api/settings`
- `POST /api/search`
- `GET /api/jobs`, `GET /api/jobs/{job_id}`
- `GET /api/papers/queue`
- `POST /api/swipe`
- `GET /api/liked`
- `POST /api/export/bib`, `POST /api/export/csv`

## TODO
- RSS/ToC 备选模式（无 IEEE key 时）
- Gemini summarizer 直连
- 拖拽手势增强
