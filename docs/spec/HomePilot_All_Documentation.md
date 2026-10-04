# HomePilot — Complete Documentation

Converted from the original HomePilot documentation package. All nine documents are included in full; repeated material is retained. Requirements and submission claims reflect the original package dated 2 October 2026 and have not been reverified during format conversion.

## Contents
- [00 HomePilot Master Document](#document-00)
- [01 HomePilot Product Overview](#document-01)
- [02 HomePilot PRD](#document-02)
- [03 HomePilot Technical Architecture](#document-03)
- [04 HomePilot UX and User Flows](#document-04)
- [05 HomePilot Privacy Safety Testing](#document-05)
- [06 HomePilot MVP Roadmap](#document-06)
- [07 HomePilot Devpost Submission Pack](#document-07)
- [08 HomePilot Demo and Pitch](#document-08)
- [Supporting files](#supporting-files)


---

<a id="document-00"></a>

## 00 HomePilot Master Document

**A household coordination agent for reducing family mental load**

Prepared for Build, Ship, Shape: Amazon Developer Hackathon 2026

| Working title note: "HomePilot" is used as the hackathon codename in this package. Public app-name clearance is recommended before launch because similar names already exist in software/smart-home markets. |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>Executive summary<br />
</strong>HomePilot AI is a household coordination agent that turns messy family conversations into a shared, feasible plan. Instead of asking every family member to maintain another calendar or task app, HomePilot listens to natural-language requests, understands constraints, detects conflicts, delegates responsibility, asks for confirmation when needed, and surfaces only the next actions each person needs.</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## 1. Product concept

### 1.1 Problem

Households often have information spread across memory, messaging apps, calendars, shopping lists, school notices, and sticky notes. The hard part is not merely storing tasks; it is the invisible cognitive work of anticipating needs, remembering deadlines, deciding who should do what, checking conflicts, and following up. Research on cognitive household labor describes this planning and anticipation as a distinct burden, while recent community discussions show that shared calendars and family task apps often fail because they require sustained manual upkeep.

### 1.2 Solution

HomePilot AI is a household coordination agent that turns messy family conversations into a shared, feasible plan. Instead of asking every family member to maintain another calendar or task app, HomePilot listens to natural-language requests, understands constraints, detects conflicts, delegates responsibility, asks for confirmation when needed, and surfaces only the next actions each person needs.

### 1.3 Value proposition

HomePilot reduces the need for a human "household project manager". The product does not replace family decisions; it makes the coordination work explicit, shared, and actionable.

### 1.4 One-line pitch

HomePilot AI turns household chaos into a coordinated plan - without forcing the family to maintain yet another productivity app.

### 1.5 Why this is different

- Most family apps are databases: users must manually enter and maintain every event or task. HomePilot is an agent: it converts unstructured family context into structured actions.

- The core unit is not a to-do item but a household commitment with an owner, deadline, dependencies, constraints and confirmation state.

- The product focuses on reducing cognitive labor: anticipating, deciding, delegating and following up - not just reminding.

- The MVP is intentionally built around a reproducible simulated household, making the 3-minute demo reliable while still showing real MCP/AWS execution.

## 2. Evidence of user need

Academic research distinguishes cognitive household labor from physical household labor and links the planning/anticipation burden to stress and family-work conflict. A 3,000-parent US study identified distinct forms of domestic cognitive labor, while a separate study of 322 mothers found cognitive labor especially disproportionate and associated with stress, burnout and relationship outcomes. Community discussions in 2026 also repeatedly describe failed shared calendars, abandoned family task apps and one person becoming the de facto household coordinator.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>Product insight<br />
</strong>The pain point is not "we need another calendar." The pain point is "someone still has to think for the calendar." HomePilot targets that thinking work.</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## 3. Target users and jobs-to-be-done

| **Persona**                | **Situation**                                                           | **Job to be done**                                                  |
|----------------------------|-------------------------------------------------------------------------|---------------------------------------------------------------------|
| Primary coordinator parent | Works full-time, remembers school, appointments, shopping and deadlines | Reduce mental load without creating another system to maintain      |
| Partner / co-parent        | Wants to help but lacks the full context                                | See ownership clearly and receive only relevant next actions        |
| Teen / older child         | Has school, activities and chores                                       | Know what is expected without reading long family chats             |
| Caregiver family member    | Coordinates an older relative across siblings                           | Avoid missed appointments, duplicated errands and unclear ownership |

## 4. Core user stories

- As a parent, I can describe several obligations in one message and get a feasible plan instead of manually creating five separate tasks.

- As a co-parent, I can see exactly what I own and why, without needing to inspect the entire family calendar.

- As a caregiver, I can prevent duplicated errands and missed appointments by sharing one current plan across siblings.

- As a family member, I can reject or modify a proposed assignment before the agent commits it.

- As a household, we can ask "what is at risk today?" and receive a short exception-focused answer rather than a full data dump.

## 5. Feature set

| **Feature**                       | **What it does**                                                                                      |
|-----------------------------------|-------------------------------------------------------------------------------------------------------|
| Natural-language household intake | One message can contain multiple people, tasks, deadlines, dependencies and constraints.              |
| Constraint-aware planning         | Detects calendar collisions, travel-time issues, overloaded family members and missing ownership.     |
| Delegation with confirmation      | Proposes who should own a task; significant schedule changes require user approval.                   |
| Shared household state            | Tasks, events, shopping needs and commitments live in one structured model.                           |
| Role-specific next actions        | Each family member sees a small, relevant list instead of the full household backlog.                 |
| Daily brief                       | A concise morning/evening summary of what changed, what is at risk and what needs attention.          |
| Conflict resolver                 | When plans collide, suggests options with tradeoffs instead of silently changing schedules.           |
| Preference memory                 | Learns non-sensitive preferences such as preferred pickup person, quiet hours and notification style. |
| Explainable actions               | Shows why an assignment or reschedule was proposed and which constraints were considered.             |
| Demo-safe simulation              | Uses synthetic household data so the hackathon demo is reproducible and privacy-safe.                 |

## 6. Golden demo scenario

Scenario: Friday evening. The family has a pediatric appointment Saturday at 09:00, one parent starts work at 08:30, the other has a class at 10:00, groceries are low, and a school project is due Monday. The user speaks or types the situation once. HomePilot extracts the commitments, checks availability, proposes that the second parent handles the appointment, schedules grocery pickup on the return route, assigns the school-project check to the first parent in the evening, and asks for confirmation before saving the plan.

1.  User: "Tomorrow our child has the doctor at 9. I start work at 8:30, Ali has class at 10, we are out of milk, and the science project is due Monday."

2.  HomePilot identifies four obligations, two people, hard time constraints and one shopping dependency.

3.  The agent calls household and calendar MCP tools.

4.  It detects that the first parent cannot attend the appointment and that Ali has enough travel buffer before class.

5.  It proposes a plan and explicitly explains the tradeoff.

6.  User confirms. Tasks/events are updated and each family member gets only their relevant next action.

## 7. UX principles

- Conversation-first, dashboard-second: the fastest path is natural language; the dashboard is for verification and adjustment.

- Exception-focused: highlight conflicts, unowned tasks and overdue commitments instead of showing everything equally.

- Progressive confirmation: low-risk drafting can be automatic; external or schedule-changing actions require explicit approval.

- Low notification burden: one actionable brief is better than ten reminders.

- Visible reasoning: show the constraints behind a recommendation in plain language.

- Family dignity: never rank family members, shame missed tasks, or frame household contribution as a competition.

## 8. Screen inventory

| **Screen**    | **Purpose**                | **Key components**                                             |
|---------------|----------------------------|----------------------------------------------------------------|
| Today         | Household control center   | At-risk items, next actions, daily brief, unresolved conflicts |
| Ask HomePilot | Natural-language intake    | Chat input, suggestion chips, confirmation cards               |
| Plan          | Shared structured plan     | Timeline, owner badges, deadlines, dependencies                |
| People        | Family roles & preferences | Availability, notification preference, responsibility areas    |
| Tasks         | Operational details        | Status, owner, due date, source, reasoning                     |
| Shopping      | Shared errands             | Items, assignee, optional route grouping                       |
| Activity      | Audit trail                | Agent proposals, confirmations, edits, tool calls              |
| Settings      | Privacy and control        | Data retention, integrations, quiet hours, export/delete       |

## 9. Technical architecture

![HomePilot architecture](image omitted)

Recommended hackathon architecture: a web-based simulated Alexa+ experience connects to a Python FastAPI backend. A Strands agent uses Amazon Bedrock for reasoning and invokes a self-hosted HomePilot MCP server over Streamable HTTP. Household state is stored in DynamoDB; optional Amazon Bedrock AgentCore Memory can retain preferences and session summaries. CloudWatch/OpenTelemetry captures traceable tool activity. This architecture also gives the project a credible AWS Builder mini-challenge story.

### 9.1 Primary track strategy

- Primary track: Alexa+.

- Preferred compliance path: working self-hosted MCP server implementing MCP 2025-11-25 or later over Streamable HTTP, demonstrated through the project web UI.

- Fallback path if MCP integration slows development: official rules also allow a simulated Alexa+ experience built with any agentic tool; however, the MCP path gives a stronger technical narrative.

- Mini challenge target: AWS Builder using Bedrock + Strands + AgentCore/DynamoDB/CloudWatch as a multi-service agentic system.

- Optional Open Source mini challenge: publish a reusable household-coordination MCP schema/toolkit or a generic conflict-resolution component with tests.

### 9.2 MCP tool contract

| **Tool**              | **Purpose**                                                            |
|-----------------------|------------------------------------------------------------------------|
| get_household_context | Return family members, roles, preferences and current household state. |
| list_events           | Read upcoming events and availability windows.                         |
| create_event          | Create a proposed event after confirmation.                            |
| list_tasks            | Read active tasks with owner, deadline and status.                     |
| create_task           | Create a structured household task.                                    |
| assign_task           | Assign or reassign a task with a reason.                               |
| detect_conflicts      | Find schedule, ownership and deadline conflicts.                       |
| propose_plan          | Generate a candidate coordination plan from constraints.               |
| shopping_list         | Read/add/complete shopping items.                                      |
| send_notification     | Send a simulated or real notification to a family member.              |
| daily_brief           | Return only high-priority items for the day.                           |

### 9.3 Agent execution flow

![HomePilot agent workflow](image omitted)

### 9.4 Suggested repository structure

homepilot-ai/  
apps/web/ \# Next.js/React simulator UI  
services/api/ \# FastAPI gateway  
services/agent/ \# Strands orchestrator, prompts, policies  
services/mcp/ \# MCP 2025-11-25+ Streamable HTTP server  
packages/domain/ \# household data model + conflict engine  
infra/ \# CDK/Terraform/CloudFormation  
demo/ \# deterministic synthetic scenario data  
tests/ \# unit, integration, agent evals  
docs/ \# architecture, demo, feedback, friction log  
LICENSE  
README.md

## 10. Domain model

| **Entity**    | **Key fields**                                                 |
|---------------|----------------------------------------------------------------|
| Household     | id, name, timezone, quiet_hours, preferences                   |
| Person        | id, display_name, role, availability, notification_style       |
| Commitment    | id, type, title, start/end or due_at, owner, priority, source  |
| Constraint    | person, time window, hard/soft, reason                         |
| Task          | status, owner, due_at, dependencies, effort estimate           |
| ShoppingItem  | name, quantity, priority, assigned_to, status                  |
| AgentProposal | proposed actions, rationale, confidence, confirmation_required |
| AuditEvent    | timestamp, actor, tool, before/after, approval state           |

## 11. Agent policy and guardrails

- Never silently cancel or reschedule a family member's commitment.

- Require confirmation before sending external notifications, creating high-impact events, spending money, or sharing sensitive information.

- For ambiguous ownership, propose options rather than inventing consent.

- Treat health-related entries such as "take medicine" as reminders only; do not provide diagnosis, dosage or medical advice.

- Use minimum necessary household data and synthetic data in the public demo.

- Record an audit event for each agent tool call that changes state.

- Allow undo for all reversible actions in the MVP.

## 12. Privacy & security

- Data minimization: collect only information needed for coordination.

- Household boundary: every object belongs to one household; cross-household access is denied by design.

- Authentication: Amazon Cognito or equivalent identity layer for deployed builds.

- Authorization: owner/member roles plus tool-level checks; agent permission never exceeds the signed-in user.

- Encryption: TLS in transit; AWS-managed encryption at rest for deployed AWS stores.

- Auditability: state-changing actions retain who/what/when and confirmation status.

- Retention: configurable; demo defaults to ephemeral synthetic data.

- Prompt injection defense: never treat arbitrary task/event text as system instructions; sanitize tool outputs and separate data from agent policy.

## 13. Functional requirements

| **ID** | **Requirement**                                                              | **Priority**     |
|--------|------------------------------------------------------------------------------|------------------|
| FR-01  | Parse one natural-language message into multiple commitments and constraints | Must             |
| FR-02  | Read current household tasks/events through tools                            | Must             |
| FR-03  | Detect at least time conflicts and unowned critical tasks                    | Must             |
| FR-04  | Generate a proposed plan with rationale                                      | Must             |
| FR-05  | Require user confirmation for state-changing plan actions                    | Must             |
| FR-06  | Persist confirmed tasks/events                                               | Must             |
| FR-07  | Show person-specific next actions                                            | Must             |
| FR-08  | Generate a concise daily brief                                               | Should           |
| FR-09  | Remember non-sensitive household preferences across sessions                 | Should           |
| FR-10  | Integrate real external calendars                                            | Could - post-MVP |

## 14. Non-functional requirements

- Demo determinism: seed data and scripted scenario must produce a stable result even if model wording varies.

- Latency target: first useful response within 5 seconds for demo-sized household state; stream progress where possible.

- Observability: record model/tool latency, tool failures, retries and confirmation actions.

- Graceful degradation: if Bedrock fails, show an actionable error and preserve household state.

- Accessibility: keyboard navigation, semantic labels, readable contrast and no color-only state coding.

- Portability: core domain/conflict logic remains independent from the LLM provider.

## 15. MVP scope

| **In MVP**                           | **Out of MVP / later**                              |
|--------------------------------------|-----------------------------------------------------|
| Web simulator for Alexa+ experience  | Native mobile app                                   |
| Synthetic 4-person household         | Full onboarding/import from every calendar provider |
| Tasks, events, shopping, daily brief | Payments/purchasing                                 |
| Constraint/conflict detection        | Complex route optimization                          |
| Self-hosted MCP server               | Production Alexa+ gated SDKs                        |
| Bedrock + Strands agent              | Medical/financial decision-making                   |
| DynamoDB or local demo store         | Enterprise multi-tenant admin suite                 |
| Confirmation + audit trail           | Fully autonomous external actions                   |

## 16. Build plan to submission

| **Dates (2026)**           | **Goal**          | **Exit criteria**                                                           |
|----------------------------|-------------------|-----------------------------------------------------------------------------|
| Oct 2-5                    | Product skeleton  | UI shell, synthetic family, domain model, 1 golden scenario                 |
| Oct 6-10                   | Agent + MCP       | MCP server, 6+ tools, Strands agent, Bedrock working end-to-end             |
| Oct 11-14                  | Planning quality  | Conflict rules, confirmations, daily brief, stable agent prompt             |
| Oct 15-17                  | AWS deployment    | Hosted backend, database, logs/traces, reproducible setup                   |
| Oct 18-20                  | QA + polish       | Tests, accessibility pass, failure states, screenshots                      |
| Oct 21                     | Submission assets | English demo recording, Devpost text, product feedback, friction log        |
| Oct 22                     | Freeze            | Fresh-environment install test, repo/license check, final video upload      |
| Oct 23 before 12:00 PM PDT | Submit            | Do not rely on last-minute upload; deadline is Oct 23, 2026 at noon Pacific |

## 17. Testing and evaluation plan

| **Test type**  | **Examples**                                                 | **Pass signal**                            |
|----------------|--------------------------------------------------------------|--------------------------------------------|
| Unit           | Conflict overlap; ownership; due dates; timezones            | Deterministic expected outputs             |
| Tool contract  | MCP schema, required fields, error codes                     | 100% schema-valid responses                |
| Agent scenario | Golden family scenario; ambiguous owner; impossible schedule | Correct tool selection + safe proposal     |
| Safety         | Prompt injection in task title; unauthorized household id    | No policy override or cross-household data |
| UX             | First-time user completes plan in \<= 90 sec                 | No documentation required                  |
| Resilience     | Bedrock timeout; DB unavailable; invalid tool input          | Clear error, no state corruption           |
| Demo rehearsal | Fresh browser, clean account, 3-minute script                | End-to-end success 5 consecutive runs      |

## 18. Hackathon judging alignment

| **Criterion**              | **How HomePilot demonstrates it**                                                                                   |
|----------------------------|---------------------------------------------------------------------------------------------------------------------|
| Tech Implementation        | Real MCP tool execution, Strands orchestration, Bedrock reasoning, persistent state, confirmation/audit flow.       |
| Design                     | Conversation-first flow, conflict cards, person-specific next actions, explainable proposals, accessible dashboard. |
| Potential Impact           | Targets a widespread coordination burden in families and caregiving; credible path beyond hackathon.                |
| Quality of Idea            | Moves beyond a Q&A assistant or API wrapper into a stateful, multi-step household orchestration workflow.           |
| Friction bonus             | Maintain a concrete friction log during setup/integration and submit actionable feedback.                           |
| AWS Builder mini-challenge | Use a multi-service agentic architecture rather than a single model call.                                           |

## 19. Devpost submission copy - English

### Project title

HomePilot AI - The Household Coordination Agent

### Tagline

Turn family chaos into a coordinated plan - without another app everyone has to maintain.

### Inspiration

Family organization tools usually assume the hard part is storing information. In reality, someone still has to notice what needs doing, remember deadlines, check everyone's availability, delegate tasks, and follow up. HomePilot AI focuses on that invisible coordination layer.

### What it does

HomePilot takes a messy natural-language description of household obligations and turns it into a structured, constraint-aware plan. It can read the household context, detect conflicts, propose ownership, create tasks and events after confirmation, and generate a short daily brief for each family member. The experience is demonstrated in a web-based Alexa+ simulation and backed by a self-hosted MCP server.

### How we built it

The web client sends requests to a FastAPI backend running a Strands agent. Amazon Bedrock provides model reasoning. The agent invokes household coordination tools through a self-hosted MCP server using Streamable HTTP. DynamoDB stores household state, while AWS observability services capture tool and agent execution. The demo uses deterministic synthetic household data so judges can reproduce the workflow safely.

### Challenges we ran into

The hardest design problem was making the agent useful without making it over-autonomous. We separated drafting from committing: the agent can reason and propose freely, but schedule changes and external actions require explicit confirmation. We also designed tool contracts so task text is treated as data rather than instructions, reducing prompt-injection risk.

### Accomplishments

A single natural-language request can trigger multi-step reasoning across people, tasks, time constraints and shopping needs; the system produces a transparent plan, asks for approval, and updates shared household state through real tool calls.

### What we learned

Household coordination is less about collecting more information and more about reducing the cost of turning information into shared responsibility. Agentic workflows are especially useful when the product needs to combine context, constraints and actions across several services.

### What is next

Next we would add permissioned calendar/email integrations, location-aware errands, optional Ring-based arrival events, richer household memory, and privacy-preserving personalization.

## 20. Product feedback template

| **Prompt**                                      | **Draft answer / notes to capture during build**                                                                       |
|-------------------------------------------------|------------------------------------------------------------------------------------------------------------------------|
| Which tools/APIs/SDKs did you use and for what? | List MCP implementation, Strands Agents, Amazon Bedrock, AgentCore if used, DynamoDB, CloudWatch, deployment services. |
| What worked well?                               | Record setup speed, docs quality, debugging visibility, tool reliability and deployment experience.                    |
| What needs work?                                | Capture specific errors, missing examples, confusing version requirements, local testing gaps and workarounds.         |
| Onboarding experience                           | Measure time from zero to first successful model call, first agent tool call and first MCP call.                       |
| Would you build with them again?                | Answer yes/no per tool with one concrete reason rather than generic praise.                                            |

## 21. Friction log template

| **Date**   | **Task attempted**                         | **Steps**            | **Expected**      | **Actual**     | **Severity** | **Workaround**    | **Actionable suggestion**        |
|------------|--------------------------------------------|----------------------|-------------------|----------------|--------------|-------------------|----------------------------------|
| YYYY-MM-DD | e.g., expose MCP tool over Streamable HTTP | Commands/config used | Expected behavior | Observed issue | Low/Med/High | What unblocked it | Specific doc/tooling improvement |
|            |                                            |                      |                   |                |              |                   |                                  |
|            |                                            |                      |                   |                |              |                   |                                  |

## 22. Three-minute demo script

| **Time**  | **Visual**                      | **Narration**                                                                                                      |
|-----------|---------------------------------|--------------------------------------------------------------------------------------------------------------------|
| 0:00-0:20 | Messy family dashboard / chat   | "Families do not fail because they lack calendars. They fail because someone still has to think for the calendar." |
| 0:20-0:45 | User enters the golden scenario | Explain that one message contains several people, deadlines and constraints.                                       |
| 0:45-1:15 | Live agent/tool trace           | Show MCP calls: household context, events, conflict detection. Keep trace readable.                                |
| 1:15-1:45 | Plan card appears               | Highlight conflict, proposed owner, rationale and travel/time buffer.                                              |
| 1:45-2:10 | User confirms                   | Show real state change: tasks/events updated and audit entry created.                                              |
| 2:10-2:35 | Person-specific views           | Switch between two family members; each sees only relevant next actions.                                           |
| 2:35-2:50 | AWS architecture overlay        | Mention Bedrock + Strands + MCP + state/observability.                                                             |
| 2:50-3:00 | Closing screen                  | "HomePilot removes the need for one person to be the household project manager."                                   |

## 23. GitHub README skeleton

\# HomePilot AI  
  
HomePilot AI is a household coordination agent for the Amazon Developer Hackathon 2026. It converts natural-language family context into a structured, conflict-aware plan and executes approved actions through a self-hosted MCP server.  
  
\## Demo  
- Public demo video: \<URL\>  
- Hosted app: \<URL or testing instructions\>  
  
\## Track  
- Primary: Alexa+  
- Mini challenge: AWS Builder  
  
\## Architecture  
Web simulator -\> FastAPI -\> Strands Agent -\> Amazon Bedrock -\> HomePilot MCP server -\> household tools -\> DynamoDB.  
  
\## Local setup  
1. Copy \`.env.example\` to \`.env\`.  
2. Install Python/Node dependencies.  
3. Configure AWS credentials or Bedrock API key.  
4. Start MCP server.  
5. Start agent/API service.  
6. Start web client.  
7. Load demo seed data.  
  
\## Reproducible judge scenario  
Run \`make demo-seed\`, open the app, and paste the scenario from \`demo/golden_scenario.txt\`.  
  
\## Safety  
State-changing actions require confirmation. Demo data is synthetic.  
  
\## License  
\<Choose an approved open-source license if public.\>

## 24. Risk register

| **Risk**                        | **Impact** | **Mitigation**                                                                                                                            |
|---------------------------------|------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| Agent output varies during demo | High       | Use structured output, deterministic seed data, low temperature where available, and rule-based conflict validation.                      |
| MCP version/transport mismatch  | High       | Pin MCP dependency and include a startup self-test that confirms protocol version and tool listing.                                       |
| AWS latency/cost                | Medium     | Use small demo state, stream output, set budgets, shut down idle resources, cache non-sensitive static demo context.                      |
| Too much scope                  | High       | Freeze MVP to one golden scenario plus 2 edge cases; external calendar integration stays optional.                                        |
| Privacy concerns                | High       | Use synthetic public demo data, explicit confirmations, clear data controls and household authorization boundaries.                       |
| Name conflict                   | Medium     | Treat HomePilot as working title; perform final brand/trademark clearance or rename before broader release.                               |
| Submission packaging error      | High       | Fresh-clone test repo, verify public/private reviewer access, license, README, demo URL and all required feedback fields before deadline. |

## 25. Definition of done

- A judge can clone the repo and run the documented demo path without private developer tooling.

- The demo visibly performs real agent/tool work rather than playing a prerecorded fake sequence.

- The MCP server exposes documented household tools and is actually invoked by the running application.

- At least one multi-constraint scenario is solved end-to-end and persisted after confirmation.

- The 3-minute public English video shows the working project and stays under the time limit.

- The submission includes product feedback, selected track(s), mini-challenge information, repository URL and testing instructions.

- The repo contains an appropriate license if public, or required reviewer access if private.

- Friction logs are concrete and actionable rather than generic complaints.

## Sources and verification links

- **Amazon hackathon official rules:** https://amazonappdev2026.devpost.com/rules

- **Amazon hackathon FAQ:** https://amazonappdev2026.devpost.com/details/faqs

- **Amazon hackathon main page:** https://amazonappdev2026.devpost.com/

- **Amazon build-session resources:** https://amazonappdev2026.devpost.com/updates/46232-the-amazon-devices-build-session-recording-is-up-resources

- **Strands Agents Python quickstart:** https://strandsagents.com/docs/user-guide/sdk/quickstart/python/

- **Strands Agents MCP tools:** https://strandsagents.com/docs/user-guide/sdk/tools/mcp-tools/

- **Amazon Bedrock AgentCore - Strands integration:** https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/strands-sdk-memory.html

- **Weeks & Ruppanner (2025), cognitive labor among US parents:** https://doi.org/10.1111/jomf.13057

- **Aviv et al. (2025), cognitive household labor and wellbeing:** https://pubmed.ncbi.nlm.nih.gov/38951218/

- **Community signal: family coordination pain point:** https://www.reddit.com/r/homeautomation/comments/1sidwf0/


---

<a id="document-01"></a>

## 01 HomePilot Product Overview

**Problem, users, value proposition, features and scenarios**

Prepared for Build, Ship, Shape: Amazon Developer Hackathon 2026

| Working title note: "HomePilot" is used as the hackathon codename in this package. Public app-name clearance is recommended before launch because similar names already exist in software/smart-home markets. |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## Product vision

HomePilot AI is a household coordination agent that turns messy family conversations into a shared, feasible plan. Instead of asking every family member to maintain another calendar or task app, HomePilot listens to natural-language requests, understands constraints, detects conflicts, delegates responsibility, asks for confirmation when needed, and surfaces only the next actions each person needs.

## Problem statement

Households often have information spread across memory, messaging apps, calendars, shopping lists, school notices, and sticky notes. The hard part is not merely storing tasks; it is the invisible cognitive work of anticipating needs, remembering deadlines, deciding who should do what, checking conflicts, and following up. Research on cognitive household labor describes this planning and anticipation as a distinct burden, while recent community discussions show that shared calendars and family task apps often fail because they require sustained manual upkeep.

## Value proposition

HomePilot reduces the need for a human "household project manager". The product does not replace family decisions; it makes the coordination work explicit, shared, and actionable.

## Target users

| **Persona**                | **Situation**                                                           | **Need**                                                            |
|----------------------------|-------------------------------------------------------------------------|---------------------------------------------------------------------|
| Primary coordinator parent | Works full-time, remembers school, appointments, shopping and deadlines | Reduce mental load without creating another system to maintain      |
| Partner / co-parent        | Wants to help but lacks the full context                                | See ownership clearly and receive only relevant next actions        |
| Teen / older child         | Has school, activities and chores                                       | Know what is expected without reading long family chats             |
| Caregiver family member    | Coordinates an older relative across siblings                           | Avoid missed appointments, duplicated errands and unclear ownership |

## Core features

| **Feature**                       | **Description**                                                                                       |
|-----------------------------------|-------------------------------------------------------------------------------------------------------|
| Natural-language household intake | One message can contain multiple people, tasks, deadlines, dependencies and constraints.              |
| Constraint-aware planning         | Detects calendar collisions, travel-time issues, overloaded family members and missing ownership.     |
| Delegation with confirmation      | Proposes who should own a task; significant schedule changes require user approval.                   |
| Shared household state            | Tasks, events, shopping needs and commitments live in one structured model.                           |
| Role-specific next actions        | Each family member sees a small, relevant list instead of the full household backlog.                 |
| Daily brief                       | A concise morning/evening summary of what changed, what is at risk and what needs attention.          |
| Conflict resolver                 | When plans collide, suggests options with tradeoffs instead of silently changing schedules.           |
| Preference memory                 | Learns non-sensitive preferences such as preferred pickup person, quiet hours and notification style. |
| Explainable actions               | Shows why an assignment or reschedule was proposed and which constraints were considered.             |
| Demo-safe simulation              | Uses synthetic household data so the hackathon demo is reproducible and privacy-safe.                 |

## Golden scenario

A parent describes tomorrow's doctor appointment, work schedule, another parent's class, missing groceries and a school deadline in a single message. HomePilot checks household context, detects the conflict, proposes ownership and timing, asks for confirmation, then updates the plan and each person's next actions.

## Competitive positioning

| **Conventional family organizer**      | **HomePilot AI**                                |
|----------------------------------------|-------------------------------------------------|
| Manual event/task entry                | Natural-language multi-intent intake            |
| Stores information                     | Reasons across constraints and responsibilities |
| Many notifications                     | Exception-focused briefs                        |
| User decides every assignment manually | Agent proposes ownership with explanation       |
| Static calendar/list                   | Stateful agentic workflow with tools            |

## Success metrics

- Plan creation time for golden scenario \<= 90 seconds from first input to confirmation.

- At least 80% of seeded commitments are correctly extracted without manual field entry.

- 100% of state-changing actions have explicit confirmation and audit events.

- No unresolved hard time conflict after a plan is confirmed.

- User can understand why an assignment was proposed without opening technical logs.

## Sources and verification links

- **Amazon hackathon official rules:** https://amazonappdev2026.devpost.com/rules

- **Amazon hackathon FAQ:** https://amazonappdev2026.devpost.com/details/faqs

- **Amazon hackathon main page:** https://amazonappdev2026.devpost.com/

- **Amazon build-session resources:** https://amazonappdev2026.devpost.com/updates/46232-the-amazon-devices-build-session-recording-is-up-resources

- **Strands Agents Python quickstart:** https://strandsagents.com/docs/user-guide/sdk/quickstart/python/

- **Strands Agents MCP tools:** https://strandsagents.com/docs/user-guide/sdk/tools/mcp-tools/

- **Amazon Bedrock AgentCore - Strands integration:** https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/strands-sdk-memory.html

- **Weeks & Ruppanner (2025), cognitive labor among US parents:** https://doi.org/10.1111/jomf.13057

- **Aviv et al. (2025), cognitive household labor and wellbeing:** https://pubmed.ncbi.nlm.nih.gov/38951218/

- **Community signal: family coordination pain point:** https://www.reddit.com/r/homeautomation/comments/1sidwf0/


---

<a id="document-02"></a>

## 02 HomePilot PRD

**MVP requirements and acceptance criteria**

Prepared for Build, Ship, Shape: Amazon Developer Hackathon 2026

| Working title note: "HomePilot" is used as the hackathon codename in this package. Public app-name clearance is recommended before launch because similar names already exist in software/smart-home markets. |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## 1. Objective

Build a demo-ready household coordination agent that converts natural-language family context into an approved, structured plan using an Alexa+ compatible self-hosted MCP architecture and AWS agentic services.

## 2. Users and JTBD

| **Persona**                | **Job to be done**                                                  |
|----------------------------|---------------------------------------------------------------------|
| Primary coordinator parent | Reduce mental load without creating another system to maintain      |
| Partner / co-parent        | See ownership clearly and receive only relevant next actions        |
| Teen / older child         | Know what is expected without reading long family chats             |
| Caregiver family member    | Avoid missed appointments, duplicated errands and unclear ownership |

## 3. Functional requirements

| **ID** | **Requirement**                                                              | **Priority**     |
|--------|------------------------------------------------------------------------------|------------------|
| FR-01  | Parse one natural-language message into multiple commitments and constraints | Must             |
| FR-02  | Read current household tasks/events through tools                            | Must             |
| FR-03  | Detect at least time conflicts and unowned critical tasks                    | Must             |
| FR-04  | Generate a proposed plan with rationale                                      | Must             |
| FR-05  | Require user confirmation for state-changing plan actions                    | Must             |
| FR-06  | Persist confirmed tasks/events                                               | Must             |
| FR-07  | Show person-specific next actions                                            | Must             |
| FR-08  | Generate a concise daily brief                                               | Should           |
| FR-09  | Remember non-sensitive household preferences across sessions                 | Should           |
| FR-10  | Integrate real external calendars                                            | Could - post-MVP |

## 4. Acceptance criteria

- Given the golden scenario, the app extracts at least one event, two tasks, two people and all hard time constraints.

- The conflict engine flags an impossible or overlapping plan before a commit is allowed.

- The proposed plan identifies an owner and rationale for every critical commitment.

- No state mutation is executed until the user approves the proposal.

- After approval, the dashboard, relevant person views and audit log reflect the new state.

- A daily brief returns at most five high-value items prioritized by urgency/risk.

## 5. Non-functional requirements

- Demo reliability across five consecutive rehearsals.

- Accessible keyboard-first UI and semantic labels.

- Structured logs for tool calls and errors.

- Synthetic demo data; no real family PII required.

- Provider-independent core conflict engine.

- Clear setup instructions from a fresh clone.

## 6. Out of scope

- Autonomous purchasing

- Medical decision support

- Native mobile apps

- Full calendar/email provider matrix

- Advanced route optimization

- Production-scale multi-tenant billing

## 7. KPIs

| **KPI**                           | **Target**                  |
|-----------------------------------|-----------------------------|
| Time to coordinated plan          | \<= 90 sec in demo scenario |
| State-changing actions confirmed  | 100%                        |
| Hard conflicts after confirmation | 0                           |
| Fresh-clone demo success          | 5/5 rehearsals              |
| Demo video duration               | \< 3 minutes                |

## 8. Release gate

- Golden scenario stable

- MCP tools validated

- AWS deployed

- README complete

- Product feedback complete

- Friction log complete

- Video recorded

- Repo access/license verified


---

<a id="document-03"></a>

## 03 HomePilot Technical Architecture

**Alexa+ / MCP / AWS Builder implementation specification**

Prepared for Build, Ship, Shape: Amazon Developer Hackathon 2026

| Working title note: "HomePilot" is used as the hackathon codename in this package. Public app-name clearance is recommended before launch because similar names already exist in software/smart-home markets. |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## 1. Architecture overview

![HomePilot architecture](image omitted)

Primary track: Alexa+. The recommended implementation is a self-hosted MCP server using Streamable HTTP and MCP version 2025-11-25 or later, connected to a web-based simulated Alexa+ experience. The reasoning layer uses Strands Agents with Amazon Bedrock. The architecture is intentionally modular so the core domain model and conflict engine can be tested independently from the LLM.

## 2. Components

| **Component**      | **Technology**                | **Responsibility**                                     |
|--------------------|-------------------------------|--------------------------------------------------------|
| Web client         | Next.js/React                 | Chat, dashboard, confirmation cards, person views      |
| API gateway        | FastAPI; optional API Gateway | Session endpoints, streaming, auth boundary            |
| Agent orchestrator | Strands Agents SDK            | Reasoning loop, tool selection, structured plan output |
| Model              | Amazon Bedrock                | Natural-language understanding and planning            |
| MCP server         | Python MCP SDK                | Expose household actions over Streamable HTTP          |
| Domain engine      | Python package                | Conflict checks, deadlines, permissions, invariants    |
| State store        | DynamoDB                      | Household, tasks, events, audit records                |
| Memory             | AgentCore Memory optional     | Summaries and non-sensitive preferences                |
| Observability      | CloudWatch + OpenTelemetry    | Trace model/tool latency and failures                  |

## 3. Agent workflow

![HomePilot agent workflow](image omitted)

## 4. MCP tools

| **Tool**              | **Purpose**                                                            |
|-----------------------|------------------------------------------------------------------------|
| get_household_context | Return family members, roles, preferences and current household state. |
| list_events           | Read upcoming events and availability windows.                         |
| create_event          | Create a proposed event after confirmation.                            |
| list_tasks            | Read active tasks with owner, deadline and status.                     |
| create_task           | Create a structured household task.                                    |
| assign_task           | Assign or reassign a task with a reason.                               |
| detect_conflicts      | Find schedule, ownership and deadline conflicts.                       |
| propose_plan          | Generate a candidate coordination plan from constraints.               |
| shopping_list         | Read/add/complete shopping items.                                      |
| send_notification     | Send a simulated or real notification to a family member.              |
| daily_brief           | Return only high-priority items for the day.                           |

## 5. Tool design rules

- Tools return structured JSON, not prose.

- State-changing tools accept an approval_token or confirmed=true supplied by the application layer.

- Tools validate household_id authorization independently of the model.

- Conflict detection is deterministic code; the LLM interprets and communicates results but does not decide whether two times overlap.

- Every write tool records an audit event.

- Task/event text is escaped and treated as untrusted data.

## 6. Example plan schema

{  
"summary": "Ali can take the child to the doctor before class.",  
"conflicts": \[{"type":"availability","commitment":"doctor_visit","person":"Parent A"}\],  
"actions": \[  
{"tool":"assign_task","target":"doctor_visit","owner":"Ali","requires_confirmation":true},  
{"tool":"shopping_list","item":"milk","assignee":"Ali","requires_confirmation":true}  
\],  
"rationale": \["Parent A starts work at 08:30", "Ali has sufficient buffer before 10:00 class"\]  
}

## 7. Deployment options

| **Option**           | **Pros**                      | **Cons**                              | **Recommendation**                                            |
|----------------------|-------------------------------|---------------------------------------|---------------------------------------------------------------|
| Local + tunnel       | Fastest development           | Judge environment less reproducible   | Use only during early development                             |
| AWS App Runner / ECS | Simple web service deployment | More infra than Lambda                | Strong choice for MCP Streamable HTTP                         |
| Lambda + API Gateway | Low idle cost                 | Streaming/session behavior needs care | Good for stateless API, not necessarily the simplest MCP host |
| AgentCore Runtime    | Strong agentic story          | Additional setup learning             | Use if stable early enough                                    |

## 8. Security model

- Cognito or equivalent authentication

- Household-scoped authorization in every tool

- TLS

- AWS-managed encryption at rest

- Secrets Manager/SSM for credentials

- No model-generated SQL

- Least-privilege IAM

- Audit log

## 9. Observability

- trace_id per user request

- model latency/tokens

- tool name + latency + result status

- confirmation decisions

- validation failures

- MCP protocol errors

- end-to-end demo success metric

## 10. Repository layout

homepilot-ai/  
apps/web/ \# Next.js/React simulator UI  
services/api/ \# FastAPI gateway  
services/agent/ \# Strands orchestrator, prompts, policies  
services/mcp/ \# MCP 2025-11-25+ Streamable HTTP server  
packages/domain/ \# household data model + conflict engine  
infra/ \# CDK/Terraform/CloudFormation  
demo/ \# deterministic synthetic scenario data  
tests/ \# unit, integration, agent evals  
docs/ \# architecture, demo, feedback, friction log  
LICENSE  
README.md

## 11. Compliance checklist

- MCP protocol version pinned to 2025-11-25 or later.

- Streamable HTTP demonstrated.

- Track technology is actually invoked at runtime, not only documented.

- Repository includes all code/assets/setup instructions.

- Demo video shows working experience.

- If repo is public, include an open-source license; if private, add required reviewers.

## Sources and verification links

- **Amazon hackathon official rules:** https://amazonappdev2026.devpost.com/rules

- **Amazon hackathon FAQ:** https://amazonappdev2026.devpost.com/details/faqs

- **Amazon hackathon main page:** https://amazonappdev2026.devpost.com/

- **Amazon build-session resources:** https://amazonappdev2026.devpost.com/updates/46232-the-amazon-devices-build-session-recording-is-up-resources

- **Strands Agents Python quickstart:** https://strandsagents.com/docs/user-guide/sdk/quickstart/python/

- **Strands Agents MCP tools:** https://strandsagents.com/docs/user-guide/sdk/tools/mcp-tools/

- **Amazon Bedrock AgentCore - Strands integration:** https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/strands-sdk-memory.html

- **Weeks & Ruppanner (2025), cognitive labor among US parents:** https://doi.org/10.1111/jomf.13057

- **Aviv et al. (2025), cognitive household labor and wellbeing:** https://pubmed.ncbi.nlm.nih.gov/38951218/

- **Community signal: family coordination pain point:** https://www.reddit.com/r/homeautomation/comments/1sidwf0/


---

<a id="document-04"></a>

## 04 HomePilot UX and User Flows

**Screens, interaction patterns and sample dialogs**

Prepared for Build, Ship, Shape: Amazon Developer Hackathon 2026

| Working title note: "HomePilot" is used as the hackathon codename in this package. Public app-name clearance is recommended before launch because similar names already exist in software/smart-home markets. |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## 1. UX thesis

HomePilot should feel like a calm household coordinator, not a project-management tool. The product asks for the minimum information necessary, shows only exceptions and next actions, and keeps significant decisions under user control.

## 2. Screen map

| **Screen**    | **Primary action**              | **Success state**                   |
|---------------|---------------------------------|-------------------------------------|
| Today         | Understand what needs attention | User sees 1-5 prioritized items     |
| Ask HomePilot | Describe situation naturally    | Agent returns structured proposal   |
| Plan          | Review timeline/ownership       | No hidden hard conflicts            |
| Confirmation  | Approve/reject edits            | Only approved actions execute       |
| People        | Set availability/preferences    | Agent has valid constraints         |
| Activity      | Inspect history                 | Every write has traceable rationale |

## 3. Main flow

1.  Open Today screen

2.  Tap Ask HomePilot

3.  Describe the situation in one message

4.  Agent shows extracted commitments

5.  Agent checks tools/context

6.  Proposal card shows conflicts, owners and rationale

7.  User edits or confirms

8.  Dashboard and person views update

## 4. Confirmation card design

- Headline: what will change

- Reason: why the agent proposes it

- Affected people

- Time/deadline impact

- Buttons: Confirm / Edit / Cancel

- Optional "show details" for tool-level explanation

## 5. Sample conversation

**User:** Tomorrow the child has a doctor appointment at 9. I start work at 8:30, Ali has class at 10. We need milk, and the science project is due Monday.

**HomePilot:** I found four commitments and one schedule conflict. You cannot make the 09:00 appointment after your 08:30 work start. Ali appears available until his 10:00 class.

**HomePilot:** Proposed plan: Ali handles the doctor appointment, picks up milk on the return route, and you review the science project Saturday evening. I will not save these changes until you confirm.

**User:** Confirm.

**HomePilot:** Plan updated. Ali sees two next actions; you see one. No hard conflicts remain.

## 6. Error/edge states

| **Situation**                 | **UX response**                                       |
|-------------------------------|-------------------------------------------------------|
| No feasible owner             | Say why; ask user to choose what to move or cancel    |
| Ambiguous person name         | Ask one targeted clarification only when needed       |
| Bedrock unavailable           | Preserve input; show retry; do not mutate state       |
| MCP write fails               | Show failed action; keep remaining proposal pending   |
| Unauthorized household action | Block immediately and log                             |
| Two people both available     | Offer options; do not pretend one is objectively best |

## 7. Accessibility

- Keyboard accessible confirmations

- Screen-reader labels

- Status uses icons/text, not color alone

- Readable font sizes

- Plain-language reasoning

- Reduced-motion option

- No rapid flashing


---

<a id="document-05"></a>

## 05 HomePilot Privacy Safety Testing

**Trust requirements for a household coordination agent**

Prepared for Build, Ship, Shape: Amazon Developer Hackathon 2026

| Working title note: "HomePilot" is used as the hackathon codename in this package. Public app-name clearance is recommended before launch because similar names already exist in software/smart-home markets. |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## 1. Safety principles

- HomePilot coordinates; it does not make medical, legal or financial decisions.

- The model may propose; policy code decides what actions require confirmation.

- No family member is scored, ranked or shamed.

- The system must preserve human override and provide undo where possible.

- Sensitive household data is minimized and not required for public demo.

## 2. Privacy controls

- Synthetic data in public demo

- Household-scoped access

- Configurable retention

- Export/delete path

- No training-on-user-data assumption in product claims unless contractually supported

- Secret separation

- Audit log

## 3. Threat model

| **Threat**                | **Example**                       | **Mitigation**                                                    |
|---------------------------|-----------------------------------|-------------------------------------------------------------------|
| Prompt injection          | Task title says "ignore policy"   | Treat domain text as data; fixed system policy; schema validation |
| Cross-household access    | Modified household_id             | Server-side authorization in every tool                           |
| Over-autonomy             | Agent reschedules without consent | Confirmation token for write tools                                |
| Hallucinated availability | Model assumes free time           | Availability comes only from tool data                            |
| Silent partial failure    | One tool call fails               | Transactional status + user-visible error                         |
| Privacy leakage in demo   | Real names/appointments           | Synthetic personas and seed data                                  |

## 4. Test matrix

| **Category**   | **Cases**                          | **Expected**                      |
|----------------|------------------------------------|-----------------------------------|
| Extraction     | 1, 3, 6 commitments in one message | All structured correctly          |
| Time conflicts | overlap, tight buffer, timezone    | Deterministic flag                |
| Ownership      | none, one, multiple candidates     | Proposal without invented consent |
| Confirmations  | accept, edit, reject               | Only approved writes happen       |
| Authorization  | wrong household id                 | Denied                            |
| Injection      | malicious text in notes            | No policy change                  |
| Failure        | model timeout, MCP error, DB error | No corrupted state                |
| Accessibility  | keyboard/screen reader             | Core flow works                   |

## 5. Demo reliability protocol

1.  Reset to known seed

2.  Run golden scenario

3.  Verify expected conflicts

4.  Confirm proposal

5.  Verify state and audit log

6.  Repeat five times before recording

7.  Record only after five clean runs

## 6. Risk register

| **Risk**          | **Level** | **Mitigation**                                            |
|-------------------|-----------|-----------------------------------------------------------|
| Scope creep       | High      | Freeze feature list; defer external integrations          |
| Agent variability | High      | Structured output + deterministic validators              |
| Protocol mismatch | High      | Pin dependencies; startup self-test                       |
| Cloud cost        | Medium    | Budget alarms; teardown scripts                           |
| Name conflict     | Medium    | Working title only; clearance/rename before public launch |


---

<a id="document-06"></a>

## 06 HomePilot MVP Roadmap

**Three-week plan to Amazon AppDev 2026 submission**

Prepared for Build, Ship, Shape: Amazon Developer Hackathon 2026

| Working title note: "HomePilot" is used as the hackathon codename in this package. Public app-name clearance is recommended before launch because similar names already exist in software/smart-home markets. |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## Deadline

Official submission deadline: October 23, 2026 at 12:00 PM Pacific Time. In Uzbekistan this is approximately midnight entering October 24 (UTC+5), but the project should be submitted at least a day early to avoid timezone/upload risk.

## Milestones

| **Dates** | **Deliverable**       | **Definition of done**                                        |
|-----------|-----------------------|---------------------------------------------------------------|
| Oct 2-5   | Foundation            | Repo, UI shell, data model, synthetic family, golden scenario |
| Oct 6-10  | Agentic core          | Bedrock + Strands + MCP end-to-end                            |
| Oct 11-14 | Product behavior      | Conflict engine, confirmations, daily brief                   |
| Oct 15-17 | Cloud & observability | Deployed demo, state store, logs                              |
| Oct 18-20 | QA/polish             | Tests, accessibility, friction log, screenshots               |
| Oct 21    | Video/submission copy | English demo \<3 min, Devpost fields drafted                  |
| Oct 22    | Freeze                | Fresh-clone run, repo permissions/license, final upload       |
| Oct 23    | Submit early          | Final Devpost submission before official deadline             |

## Daily build discipline

- One stable end-to-end demo path always remains runnable

- Every AWS/MCP friction is recorded immediately

- No new feature after Oct 17 unless it fixes a judge-visible gap

- Every state-changing feature receives a unit/integration test

- Record screenshots/video clips continuously as backup

## Scope priority

| **P0 - must**      | **P1 - useful**       | **P2 - only if ahead** |
|--------------------|-----------------------|------------------------|
| MCP server         | Daily brief           | Real external calendar |
| Bedrock/Strands    | Preference memory     | Ring add-on            |
| Golden scenario    | Person-specific views | Location-aware errands |
| Conflict detection | AgentCore memory      | Mobile wrapper         |
| Confirmation/audit | Better onboarding     | Purchasing workflow    |

## Submission checklist

- Devpost registration complete

- Primary track selected

- Repo URL works

- Code + assets + setup included

- License or private reviewer access configured

- Video public on YouTube/Vimeo and \<3 min

- Product feedback completed

- Mini-challenge details completed

- Friction log attached

- Testing credentials included if needed


---

<a id="document-07"></a>

## 07 HomePilot Devpost Submission Pack

**Copy-ready English submission text and compliance checklist**

Prepared for Build, Ship, Shape: Amazon Developer Hackathon 2026

| Working title note: "HomePilot" is used as the hackathon codename in this package. Public app-name clearance is recommended before launch because similar names already exist in software/smart-home markets. |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## Project title

HomePilot AI - The Household Coordination Agent

## Tagline

Turn family chaos into a coordinated plan - without another app everyone has to maintain.

## Inspiration

Family organization tools usually assume the hard part is storing information. In reality, someone still has to notice what needs doing, remember deadlines, check everyone's availability, delegate tasks, and follow up. HomePilot AI focuses on that invisible coordination layer.

## What it does

HomePilot takes a messy natural-language description of household obligations and turns it into a structured, constraint-aware plan. It reads household context, detects conflicts, proposes ownership, creates tasks and events after confirmation, and generates a short daily brief for each family member. The experience is demonstrated in a web-based Alexa+ simulation and backed by a self-hosted MCP server.

## How we built it

The web client sends requests to a FastAPI backend running a Strands agent. Amazon Bedrock provides model reasoning. The agent invokes household coordination tools through a self-hosted MCP server using Streamable HTTP. DynamoDB stores household state and AWS observability captures tool and agent execution. The demo uses deterministic synthetic household data so judges can reproduce the workflow safely.

## Challenges

The hardest design problem was making the agent useful without making it over-autonomous. We separated drafting from committing: the agent can reason and propose freely, but schedule changes and external actions require explicit confirmation. We also designed tool contracts so task text is treated as data rather than instructions.

## Accomplishments

A single natural-language request can trigger multi-step reasoning across people, tasks, time constraints and shopping needs; the system produces a transparent plan, asks for approval, and updates shared household state through real tool calls.

## What we learned

Household coordination is less about collecting more information and more about reducing the cost of turning information into shared responsibility. Agentic workflows are useful when the product combines context, constraints and actions across several services.

## What is next

We would add permissioned calendar/email integrations, location-aware errands, optional Ring-based arrival events, richer household memory, and privacy-preserving personalization.

## Product feedback worksheet

| **Required question**                  | **Fill during build** |
|----------------------------------------|-----------------------|
| Tools/APIs/SDKs used                   |                       |
| What worked well?                      |                       |
| What needs work?                       |                       |
| Onboarding experience                  |                       |
| Would you build with these again? Why? |                       |

## Friction log

| **Task** | **Steps** | **Expected** | **Actual** | **Severity** | **Workaround** | **Suggestion** |
|----------|-----------|--------------|------------|--------------|----------------|----------------|
|          |           |              |            |              |                |                |
|          |           |              |            |              |                |                |
|          |           |              |            |              |                |                |

## Final compliance checklist

- Working project meets Alexa+ track requirement

- Repo contains runtime integration and setup

- Video \<3 min, public, English

- Third-party assets licensed

- Testing access free and available through judging

- Product feedback completed

- Track/mini-challenge selected

- Optional feature requests/friction logs included

## Sources and verification links

- **Amazon hackathon official rules:** https://amazonappdev2026.devpost.com/rules

- **Amazon hackathon FAQ:** https://amazonappdev2026.devpost.com/details/faqs

- **Amazon hackathon main page:** https://amazonappdev2026.devpost.com/

- **Amazon build-session resources:** https://amazonappdev2026.devpost.com/updates/46232-the-amazon-devices-build-session-recording-is-up-resources

- **Strands Agents Python quickstart:** https://strandsagents.com/docs/user-guide/sdk/quickstart/python/

- **Strands Agents MCP tools:** https://strandsagents.com/docs/user-guide/sdk/tools/mcp-tools/

- **Amazon Bedrock AgentCore - Strands integration:** https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/strands-sdk-memory.html

- **Weeks & Ruppanner (2025), cognitive labor among US parents:** https://doi.org/10.1111/jomf.13057

- **Aviv et al. (2025), cognitive household labor and wellbeing:** https://pubmed.ncbi.nlm.nih.gov/38951218/

- **Community signal: family coordination pain point:** https://www.reddit.com/r/homeautomation/comments/1sidwf0/


---

<a id="document-08"></a>

## 08 HomePilot Demo and Pitch

**Video shot list, narration and backup plan**

Prepared for Build, Ship, Shape: Amazon Developer Hackathon 2026

| Working title note: "HomePilot" is used as the hackathon codename in this package. Public app-name clearance is recommended before launch because similar names already exist in software/smart-home markets. |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## Primary demo script

| **Time**  | **On screen**                                | **Narration**                                                                                                                       |
|-----------|----------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| 0:00-0:12 | HomePilot logo + messy list/calendar montage | "Families do not need another calendar. They need less coordination work."                                                          |
| 0:12-0:28 | Today screen with conflicts                  | "Appointments, pickups, groceries and school deadlines live in different places - and one person often keeps it all in their head." |
| 0:28-0:50 | Type golden scenario                         | "With HomePilot, I describe the situation once in natural language."                                                                |
| 0:50-1:15 | Agent trace panel                            | "The agent reads household context through our MCP tools, checks availability and detects conflicts."                               |
| 1:15-1:42 | Proposal card                                | "It does not just create reminders. It proposes a feasible division of responsibility and explains why."                            |
| 1:42-1:58 | Click Confirm                                | "High-impact changes stay under human control. Nothing is committed until I confirm."                                               |
| 1:58-2:20 | Updated timeline + audit                     | "The approved plan is saved, the conflict disappears, and every state change is auditable."                                         |
| 2:20-2:38 | Switch person views                          | "Each family member sees only the next actions relevant to them, reducing notification overload."                                   |
| 2:38-2:53 | Architecture graphic                         | "Under the hood: Amazon Bedrock and Strands orchestrate a self-hosted MCP server, with household state and observability on AWS."   |
| 2:53-3:00 | Closing tagline                              | "HomePilot removes the need for one person to be the household project manager."                                                    |

## Recording rules

- Keep final video safely under 3:00

- Use English narration

- Show the actual running product

- Avoid copyrighted music/logos/assets without permission

- Use readable zoom level

- Do not spend time on login/setup

- Show one real tool trace, not every log line

## Backup plan

- If cloud latency is high, record a clean run from a stable deployed environment

- Keep synthetic seed reset button

- Have static architecture screenshot ready

- Do not fake state changes; the visible result must come from the running project

- Record separate clean audio if needed and edit only for pacing

## 30-second elevator pitch

HomePilot AI is a household coordination agent for the invisible work behind family life. You tell it the messy reality once - appointments, work schedules, groceries, deadlines - and it checks constraints, proposes who should handle what, asks for confirmation, and updates a shared plan. Unlike a family calendar, HomePilot does not just store the plan; it helps create it.


---

<a id="supporting-files"></a>

## Supporting files

### README.md

#### HomePilot AI - Hackathon Documentation Package

This folder contains a complete planning and submission package for the Amazon Developer Hackathon 2026.

##### Files
- `00_HomePilot_Master_Document.docx` - complete product, technical, UX, safety, roadmap and submission specification.
- `01_HomePilot_Product_Overview.docx` - concise product/business overview.
- `02_HomePilot_PRD.docx` - MVP product requirements.
- `03_HomePilot_Technical_Architecture.docx` - Alexa+/MCP/AWS architecture and agent design.
- `04_HomePilot_UX_and_User_Flows.docx` - screen and conversation specification.
- `05_HomePilot_Privacy_Safety_Testing.docx` - privacy, safety, threat model and QA.
- `06_HomePilot_MVP_Roadmap.docx` - execution plan to deadline.
- `07_HomePilot_Devpost_Submission_Pack.docx` - copy-ready Devpost text and required feedback templates.
- `08_HomePilot_Demo_and_Pitch.docx` - under-3-minute video script.
- `HomePilot_GitHub_README_Template.md` - repo README starter.
- `HomePilot_Friction_Log.csv` - structured friction log for the optional judging bonus.

##### Branding note
`HomePilot` is used as a working hackathon codename. Similar names exist in software/smart-home markets, so perform final brand/trademark clearance or adopt a more distinctive public name before broader launch.

### HomePilot_GitHub_README_Template.md

#### HomePilot AI

HomePilot AI is a household coordination agent for the Amazon Developer Hackathon 2026. It converts natural-language family context into a structured, conflict-aware plan and executes approved actions through a self-hosted MCP server.

##### Demo
- Public demo video: <URL>
- Hosted app: <URL or testing instructions>

##### Track
- Primary: Alexa+
- Mini challenge: AWS Builder

##### Architecture
Web simulator -> FastAPI -> Strands Agent -> Amazon Bedrock -> HomePilot MCP server -> household tools -> DynamoDB.

##### Local setup
1. Copy `.env.example` to `.env`.
2. Install Python/Node dependencies.
3. Configure AWS credentials or Bedrock API key.
4. Start MCP server.
5. Start agent/API service.
6. Start web client.
7. Load demo seed data.

##### Reproducible judge scenario
Run `make demo-seed`, open the app, and paste the scenario from `demo/golden_scenario.txt`.

##### Safety
State-changing actions require confirmation. Demo data is synthetic.

##### License
<Choose an approved open-source license if public.>
### SOURCES.md

#### Sources

##### Hackathon
- https://amazonappdev2026.devpost.com/
- https://amazonappdev2026.devpost.com/rules
- https://amazonappdev2026.devpost.com/details/faqs
- https://amazonappdev2026.devpost.com/updates/46232-the-amazon-devices-build-session-recording-is-up-resources

##### AWS / Strands
- https://strandsagents.com/docs/user-guide/sdk/quickstart/python/
- https://strandsagents.com/docs/user-guide/sdk/tools/mcp-tools/
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/strands-sdk-memory.html

##### User-need evidence
- https://doi.org/10.1111/jomf.13057
- https://pubmed.ncbi.nlm.nih.gov/38951218/
- https://www.reddit.com/r/homeautomation/comments/1sidwf0/

##### Naming note
A web search found existing software/smart-home products and trademark records using HomePilot. Treat it as a working title until clearance.

### HomePilot Friction Log

| date | task_attempted | steps_taken | expected_result | actual_result | severity | workaround | actionable_suggestion |
| --- | --- | --- | --- | --- | --- | --- | --- |

```csv
date,task_attempted,steps_taken,expected_result,actual_result,severity,workaround,actionable_suggestion
```
