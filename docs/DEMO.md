# 3-minute demo (docs 08) — run it for real, no faked state

Prep: `make mcp` + `make api`, `make demo-seed`, open http://localhost:8000, run `make rehearse` five times first.

| Time | On screen | Say |
|---|---|---|
| 0:00-0:12 | Title / messy-list montage | "Families do not need another calendar. They need less coordination work." |
| 0:12-0:28 | Today tab | "Appointments, pickups, groceries and deadlines live in different places — one person keeps it in their head." |
| 0:28-0:50 | Paste `demo/golden_scenario.txt` | "I describe the situation once, in natural language." |
| 0:50-1:15 | Click Plan it; trace panel | "The agent reads household context through our MCP tools, checks availability and detects conflicts." |
| 1:15-1:42 | Proposal card | "It proposes a feasible division of responsibility and explains why." |
| 1:42-1:58 | Click Confirm & save | "Nothing is committed until I confirm." |
| 1:58-2:20 | Plan + Activity tabs | "The plan is saved and every state change is auditable." |
| 2:20-2:38 | Switch Acting-as to Ali | "Each family member sees only their own next actions." |
| 2:38-2:53 | Architecture graphic | "Bedrock and Strands orchestrate a self-hosted MCP server; state and observability on AWS." |
| 2:53-3:00 | Tagline | "HomePilot removes the need for one person to be the household project manager." |

Bonus beats if time: "Impossible schedule" chip (Confirm is disabled until the conflict is resolved).
Record in `HOMEPILOT_AGENT=bedrock` mode once the Bedrock path is verified — the 2:38 line is only true then.
