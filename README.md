
# CRM Agent — AI-Powered Marketing Assistant

An experimental CRM agent that uses LangGraph, LangChain adapters, and an MCP-based toolset to analyze customer data, build targeted email campaigns, and run supervised marketing workflows.

Key features:
- Smart customer segmentation using RFM (Recency, Frequency, Monetary)
- Human-in-the-loop protected tool calls for sensitive actions (create/send campaigns)
- Streamlit-based UI for interactive conversations with the assistant
- Configurable MCP servers for custom tools and integrations

Files of interest:
- [src/nova/graph.py](src/nova/graph.py) — application graph and agent orchestration
- [src/nova/prompts.py](src/nova/prompts.py) — system prompt and DB schema description
- [frontend/ui.py](frontend/ui.py) — Streamlit UI that runs the assistant
- [src/nova/my_mcp/config.py](src/nova/my_mcp/config.py) — MCP configuration loader
- [db/generate_data_tables.py](db/generate_data_tables.py) — helper to generate sample CSVs

Requirements
-----------
- Python 3.13+
- PostgreSQL (e.g., Supabase) for production use
- API credentials for your chosen LLM (Gemini in examples)
- See `pyproject.toml` for the main dependencies

Quick start
-----------
1. Clone repository and install dependencies (project uses `uv` in examples — adapt to your tooling):

```bash
git clone <repo-url>
cd CRM-ai-agent
uv sync
```

2. Copy and edit environment variables:

```bash
cp .env.example .env
# Edit .env to set GEMINI_API_KEY, DATABASE_URL, and any MCP server env vars
```

3. Prepare sample data (optional):

```bash
python db/generate_data_tables.py
```

4. Start the Streamlit UI:

```bash
# from project root
python -m streamlit run frontend/ui.py
```

Or (if you use `uv`):

```bash
uv run python -m streamlit run frontend/ui.py
```

Running the agent locally
-------------------------
- The agent graph is constructed in [src/nova/graph.py](src/nova/graph.py). To generate the visualization (PNG), run:

```bash
python -m src.nova.graph
```

- The Streamlit UI sends messages to the graph using the `AgentState` model. Protected tool calls (e.g., `create_campaign`, `send_campaign_email`) trigger a human review interrupt.

Configuration
-------------
- Update `.env` with your LLM API key and database URL.
- MCP servers are configured in [src/nova/my_mcp/mcp_config.json](src/nova/my_mcp/mcp_config.json). The loader at [src/nova/my_mcp/config.py](src/nova/my_mcp/config.py) resolves env vars and relative paths.

Data model
----------
This project expects the following tables (see `prompts.py` for full schema): `customers`, `transactions`, `items`, `rfm`, `marketing_campaigns`, and `campaign_emails`.

Examples and suggested prompts
------------------------------
- "Display top 5 customers by revenue"
- "Create a re-engagement campaign for customers inactive over 6 months"
- "Draft personalized appreciation emails for Champions" 

Development notes
-----------------
- The LangGraph graph composes LLM calls and MCP tool calls via a `StateGraph`.
- `ralph_system_prompt` (in [src/nova/prompts.py](src/nova/prompts.py)) contains DB schema, email guidelines, and marketing rules the assistant follows.
- Add or customize tools by editing your MCP servers and their server-side handlers (see `mcp_config.json` and your MCP server implementations).

Security and human oversight
---------------------------
- Tool calls that perform side effects are protected by default and require manual approval via the Streamlit UI interrupt flow.
- Keep secret keys out of source control; use `.env` and platform secrets for production.

Next steps
----------
- Verify environment variables in `.env` and `mcp_config.json`.
- Start the Streamlit UI and test sample prompts.
- Extend MCP servers with custom marketing actions as needed.

License
-------
This repository does not include a license file. Add one (for example, MIT) if you intend to publish.

