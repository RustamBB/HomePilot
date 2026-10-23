## Inspiration

Family organisation tools assume the hard part is *storing* information. It isn't. The hard part is the invisible thinking: noticing what needs doing, remembering deadlines, checking who is free, deciding who should do what, and following up. Research on cognitive household labour describes this planning and anticipation as a distinct burden, and in community discussions families keep describing abandoned shared calendars and one person quietly becoming the household project manager.

The pain point is not "we need another calendar." It is "someone still has to think for the calendar." HomePilot targets that thinking work.

## What it does

You describe the situation once, in plain language:

> *"Tomorrow our child has the doctor at 9. I start work at 8:30, Ali has class at 10, we are out of milk, and the science project is due Monday."*

HomePilot extracts the commitments, reads the household through MCP tools, checks constraints with a deterministic conflict engine, and proposes a plan with reasons:

- Sam can't take the appointment, because work starts at 8:30.
- Ali can, and still reaches class at 10:00 after 15 minutes of travel.
- Milk goes to Ali, who is already out. The science project goes to Sam, which balances the load.

**Nothing is saved until a family member confirms.** Each person then sees only their own next actions, every change is audited and undoable, and if no adult is free, confirmation is blocked and options are offered instead of silently rescheduling anyone.

## How I built it

Web simulator of an Alexa+ experience → FastAPI gateway → agent → **self-hosted MCP server** (Python MCP SDK, Streamable HTTP, protocol 2025-11-25, 19 tools) → domain engine → state store.

- **Two interchangeable agent brains.** A Strands Agents + Amazon Bedrock agent discovers and calls the MCP tools. A deterministic offline extractor produces the same structured commitments for reproducible demos and tests.
- **Rules decide, the model communicates.** Overlap and travel-time checks, ownership, and the daily brief are plain code. For a person $p$ attending an event $e$ and then a later commitment $n$, the check is

  $$\text{start}(n) - \text{end}(e) \;\ge\; \max\big(\text{travel}(e),\,\text{travel}(n)\big)$$

  and the plan reports the spare time $\text{start}(n) - \text{end}(e) - \text{travel}$ (zero in the golden scenario, which is why the explanation says "no spare time").
- **Policy lives at the tool boundary.** Write tools only *stage drafts*. `confirm_plan` is human-only and is never exposed to the agent, so no prompt can talk the model into committing state.
- **Safety.** Task text is sanitised and treated as data, households are isolated by id, health items are reminders only, and every state change is audited and undoable.
- **State.** Pluggable persistence: in memory, a JSON file, or DynamoDB.
- **Quality.** 21 automated tests, including an end-to-end run over real Streamable HTTP, a Strands agent run over MCP, and DynamoDB persistence; `make rehearse` completes five consecutive clean golden-scenario runs.

## Challenges

- **Useful without being over-autonomous.** I separated *drafting* from *committing* and enforced it in the tool layer rather than the prompt.
- **A deterministic demo from a variable model.** The model extracts; code decides. That keeps the outcome stable even when wording varies.
- **Honest ambiguity.** When two adults are free, HomePilot presents a *suggestion* and the alternatives instead of pretending one owner is objectively best.
- **SDK details.** The deprecated `streamablehttp_client` name, the way list results arrive wrapped in `structuredContent`, and host checks when serving MCP outside localhost. All are recorded in the friction log.

## What I learned

Household coordination is less about collecting more information and more about lowering the cost of turning information into shared responsibility. Putting policy (what needs confirmation, who may commit) in code behind the tool boundary is far sturdier than writing rules into a prompt, and testing agent loops with a scripted model against a real MCP server catches real integration bugs without needing a live LLM.

## What's next

Permissioned calendar and email integrations, location-aware errands, Ring arrival events, AgentCore Memory for household preferences, Cognito authentication, and a hosted deployment on App Runner with DynamoDB (the container and CloudFormation template are written but not yet deployed).

## Honest status

The Strands agent is verified over real MCP with a scripted model; the live Amazon Bedrock call and the AWS deployment have not yet been exercised. "HomePilot" is a working title; similar names exist.
