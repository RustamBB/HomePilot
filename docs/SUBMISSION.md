# Devpost submission pack — HomePilot AI (copy/paste ready)

**Deadline: Oct 23, 2026, 12:00 PM Pacific.** Submit early; do not rely on last-minute video upload.

## 1. Entry
- **Primary track:** Alexa+ — self-hosted MCP server (spec 2025-11-25, Streamable HTTP) driven through a web-simulated Alexa+ experience.
- **Mini challenge:** AWS Builder (Strands Agents SDK + Amazon Bedrock + DynamoDB). See honesty notes in §5 before ticking this box.
- **Open Source mini challenge:** NOT claimed. It needs a *new, additional* open-source project or a contribution to a public repo made during the window, with its own URL/description. Optional quick route if time allows: fork the MCP Python SDK or Strands repo, push the doc fix for the deprecated `streamablehttp_client` name (see friction log), and enter that branch URL.

## 2. Title / tagline
HomePilot AI - The Household Coordination Agent
Turn family chaos into a coordinated plan - without another app everyone has to maintain.

## 3. Project description
**Inspiration.** Family organisation tools assume the hard part is storing information. The hard part is the invisible thinking: noticing what needs doing, checking everyone's availability, delegating, following up. HomePilot targets that coordination layer.

**What it does.** You describe the situation once in plain language ("Tomorrow our child has the doctor at 9. I start work at 8:30, Ali has class at 10, we're out of milk, and the science project is due Monday"). HomePilot extracts the commitments, reads household state through MCP tools, runs a deterministic conflict engine, and proposes who should own what, with the reasoning shown (Sam can't take the appointment because work starts 8:30; Ali can, reaching class at 10:00 with no spare time). Nothing is saved until a family member confirms. Each person then sees only their own next actions; every change is audited and undoable. If no adult is free, confirmation is blocked and options are offered instead of silently rescheduling anyone.

**How we built it.** Web simulator of an Alexa+ experience -> FastAPI gateway -> agent -> **self-hosted MCP server (Python MCP SDK, Streamable HTTP, protocol 2025-11-25, 19 tools)** -> domain engine -> state store. The agent has two interchangeable brains: a Strands Agents + Amazon Bedrock agent that discovers and calls the MCP tools, and a deterministic offline extractor used for reproducible demos and tests. Conflict detection and ownership are plain code, not LLM judgement. Write tools only stage drafts; `confirm_plan` is human-only and is never exposed to the agent. State is persisted to DynamoDB (or a JSON file / memory). Task text is sanitised and treated as data; households are isolated by id.

**Challenges.** Making the agent useful without being over-autonomous (draft vs commit split enforced at the tool layer, not by prompt); keeping a demo deterministic when model wording varies (LLM extracts, rules decide); MCP SDK transport/version details (see friction log).

**Accomplishments.** One message -> multi-step, constraint-aware plan with explanations; hard-conflict gate; 21 automated tests including an end-to-end run over real Streamable HTTP, a Strands agent run over MCP, and DynamoDB persistence; `make rehearse` completes five consecutive clean golden-scenario runs.

**What we learned.** Coordination is about turning information into shared responsibility. Putting policy (what needs confirmation, who may commit) in code behind the tool boundary is far sturdier than prompt rules.

**What's next.** Permissioned calendar/email integrations, location-aware errands, Ring arrival events, AgentCore Memory for preferences, Cognito auth, richer household memory.

## 4. Pre-existing work
Everything in this repository was created during the hackathon window (first commit Oct 4, 2026). No prior code was reused.

## 5. Honesty notes — verify before submitting
- **Live Bedrock call:** the Strands agent is tested over real MCP with a scripted model; it has **not** been run against Bedrock. Run `HOMEPILOT_AGENT=bedrock` once and confirm `/api/health` shows `"agent":"bedrock"` before claiming it in the video or ticking AWS Builder. If it fails, either fix it or enter without AWS Builder and describe the demo as running the offline agent.
- **AWS deployment:** `Dockerfile` and `infra/template.yaml` are untested. DynamoDB is tested only against a mock. Only describe what you actually ran.
- **Hosted URL:** none yet. A judge can still run locally (README), which satisfies "repo has everything needed".
- Don't narrate "Bedrock and Strands orchestrate…" (demo script 2:38) unless the recorded run really used Bedrock.

## 6. Repository access (pick one)
- **Public:** repo already has an MIT `LICENSE`. Nothing else needed.
- **Private:** Settings -> Collaborators -> add `testing@devpost.com`, `knmeiss`, `giolaq`, `anishamalde`, `mosesroth`, `emersonsklar`. Add them at submission time (invites expire after 7 days).
- Alexa+ code-evidence: `services/mcp/homepilot_mcp/server.py` (the MCP server), `services/agent/homepilot_agent/mcp_client.py` (Streamable HTTP client), `tests/test_e2e_mcp.py`.

## 7. Product feedback (per tool)
*Written from real experience this build; edit once you've used Bedrock/AWS.*

**MCP Python SDK (`mcp` 1.28) + Streamable HTTP** — used for the server (FastMCP) and the client. *Worked well:* decorating plain functions gave 19 typed tools with JSON schemas from type hints and Pydantic models; protocol 2025-11-25 negotiated out of the box; testing by spawning the server and connecting a real client was easy. *Needs work:* `streamablehttp_client` is deprecated in favour of `streamable_http_client` while docs/examples still use the old name; list return values arrive wrapped as `{"result": [...]}` in `structuredContent` but dicts do not (undocumented); DNS-rebinding protection rejects non-localhost Host headers with little guidance for container/load-balancer deployments. *Onboarding:* ~15 minutes to first tool call. *Again?* Yes — the typed-tool ergonomics are excellent.

**Strands Agents SDK** — used for the Bedrock agent: `MCPClient` to load MCP tools, tool allow-listing, `Agent.invoke_async`. *Worked well:* MCP tools plug in directly; a custom `Model` subclass made it easy to test the full tool-calling loop without a model. *Needs work:* the stream-event format needed for a fake model is only discoverable from source; a documented test double would help. *Again?* Yes.

**Amazon Bedrock / DynamoDB / App Runner / CloudWatch** — *Status:* [fill in after running]. DynamoDB integration (single item per household, JSON state) written and tested with moto; Bedrock and App Runner not yet exercised. State exactly this if unchanged.

**Devpost / hackathon resources** — [add your own notes].

## 8. Friction log
See `docs/friction_log.csv` (attach it). Add any Bedrock/AWS snags before submitting — up to 10% judging bonus.

## 9. Final checklist
- [ ] Ran Bedrock mode at least once (or decided not to claim AWS Builder)
- [ ] `make test` and `make rehearse` green on a fresh clone
- [ ] Video <3:00, public, English, shows MCP tool trace + confirm + per-person views (`docs/DEMO.md`)
- [ ] README placeholders (video/hosted URLs) filled
- [ ] Repo public (MIT) or private with reviewers added
- [ ] Track + mini challenge selected; product feedback + friction log pasted
- [ ] Brand note: "HomePilot" is a working title; similar names exist
