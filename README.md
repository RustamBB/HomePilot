# HomePilot AI

HomePilot AI is a household coordination agent for the Amazon Developer Hackathon 2026. It converts natural-language family context into a structured, conflict-aware plan and executes approved actions through a self-hosted MCP server.

## Demo
- Public demo video: _TODO_
- Hosted app: _TODO_ (or run locally, below)

## Track
- Primary: Alexa+ (web-simulated experience + self-hosted MCP server, Streamable HTTP, protocol 2025-11-25)
- Mini challenge: AWS Builder (Bedrock + Strands agent; DynamoDB/CloudWatch planned, see roadmap)

## Architecture
Web simulator -> FastAPI -> agent (offline rules **or** Strands + Amazon Bedrock) -> HomePilot MCP server -> household domain -> state store.

```
apps/web/            single-page simulator UI (no build step)
services/api/        FastAPI gateway (holds no state)
services/agent/      MCP client, offline extractor, Strands/Bedrock agent
services/mcp/        MCP server: 19 tools
packages/domain/     data model, conflict engine, planner, use cases (LLM-independent)
demo/                golden scenario
tests/               unit + real-MCP end-to-end tests
docs/                specs, DEMO.md script, friction log
```

Key design rules (from the spec): write tools only **stage drafts**; only a human (via the API's confirm endpoint → `confirm_plan`, which is not exposed to the agent) commits state. Every state change is audited and undoable. Task text is sanitised and treated as data. Households are isolated by id.

## Local setup
1. `cp .env.example .env` (defaults work for the offline demo)
2. `pip install -e ".[dev]"` (add `.[aws]` for Bedrock mode)
3. Terminal 1: `make mcp`  — Terminal 2: `make api`  (or `make run`)
4. `make selftest` confirms protocol version and tool listing
5. `make demo-seed` resets the synthetic household
6. Open http://localhost:8000

State: in-memory by default; `HOMEPILOT_DATA_FILE` for JSON, `HOMEPILOT_DDB_TABLE` for DynamoDB (tested against moto). AWS deployment files: `Dockerfile`, `infra/template.yaml`, `docs/DEPLOY.md` (not yet deployed).

For Bedrock mode set `HOMEPILOT_AGENT=bedrock`, AWS credentials and `HOMEPILOT_MODEL_ID` (Bedrock model access required). The Strands agent is tested over real MCP with a scripted model in place of Bedrock; the live Bedrock call is **not yet tested**.

## Reproducible judge scenario
Run `make demo-seed`, open the app, click **Plan it** with the text from `demo/golden_scenario.txt`, then **Confirm & save**. Switch "Acting as" to Ali to see only Ali's next actions. The other chips cover an ambiguous owner and an impossible schedule.

## Tests
`make rehearse` runs the demo-reliability protocol (reset → golden scenario → confirm → verify) five times. `make test` — domain rules, safety (injection text, household boundary, staged writes) and an end-to-end run against a spawned MCP server.

## Safety
State-changing actions require confirmation. Demo data is synthetic.

## License
MIT
