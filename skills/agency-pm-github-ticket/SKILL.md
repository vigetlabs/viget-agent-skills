---
name: agency-pm-github-ticket
description: >
  Writes a well-structured GitHub issue from a rough description, client message, or Slack
  snippet. Use this skill whenever a user asks to write a ticket, create a GitHub issue, log a
  bug, open an issue, draft a ticket, or track a task — even if they don't say "GitHub"
  explicitly. Trigger when the user describes a bug, feature request, or task and implies it
  needs to be tracked. Produces a ready-to-paste title and issue body every time.
---

# Agency PM GitHub Ticket Writer

When a PM or team member asks you to write a ticket, your job is to produce a well-structured
GitHub issue — a title and body — that a developer can understand without any prior context.
The input might be rough: a Slack message, a client email excerpt, or a quick verbal description.
Your job is to translate it into clean, developer-ready language.

## Required Ticket Format

Every ticket must use this template. Do not skip or rename sections.

```markdown
### Overview
- **URL:** [page or feature URL if applicable, otherwise leave blank]
- **Level of urgency:** [Low / Medium / High]
- **Potential deadline:** [Specific date, sprint name, or "None"]

**Is your feature request related to a problem? Please describe.**
[Clear and concise: what is the problem? Who reported it? Is this a bug, feature enhancement, or
customer-reported issue? Include context about how it was discovered.]

**Describe the solution you'd like**
[What should happen? Be specific enough that a developer can act on it without follow-up.]

**Describe alternatives you've considered**
[Any other approaches, workarounds, or solutions considered. If none, write "N/A".]

**Additional context**
[Extra details: related tickets, Slack thread links, error messages, browser/device specifics,
stakeholder notes, etc. If none, write "N/A".]

### Screenshots
[List any screenshots or attachments mentioned, or leave as a placeholder if none.]
```

## Ticket Title Format

Produce a short, scannable title under 80 characters:

```
[PROJECT] Type: Brief description
```

**Types:** `Bug:` `Feature:` `Enhancement:` `Task:` `Question:`

If no project name is given, omit the bracket prefix. If the user provides a title, use it
as-is or lightly clean it up — keep their intent intact.

## Urgency Guidelines

- **High** — blocking users, production down, client escalation, or has an imminent hard deadline
- **Medium** — impacts functionality but has a workaround, or is a client request without a hard deadline
- **Low** — cosmetic, nice-to-have, or backlog item

## How to Fill It In

**Synthesize, don't transcribe.** Write as if a developer with zero context will read this cold.
Turn rough input into complete, professional language.

**Dates:** If the user says "end of sprint" or "next week," convert to an approximate calendar
date based on today's date and note the assumption.

**Missing info:** If a field is genuinely unknown (e.g., no URL exists), leave the placeholder
text as-is rather than inventing a value.

**Multiple issues in one request:** If the input describes more than one distinct problem,
produce a separate ticket for each and note that you've split them.

## Output Format

Produce exactly two things, with no preamble:

1. **Ticket title** — one line
2. **Ticket body** — the filled-in markdown template, ready to paste into GitHub

---

## Example

**Input:** "Can you write a ticket? The Events listing page is showing duplicate entries when
you filter by date. High priority, the client noticed it. Project is PROJ."

**Output:**

---

**[PROJ] Bug: Events listing page shows duplicate entries when filtering by date**

### Overview
- **URL:** /events
- **Level of urgency:** High
- **Potential deadline:** None

**Is your feature request related to a problem? Please describe.**
Client-reported bug: The Events listing page displays duplicate event entries when a date filter
is applied. The issue was noticed by the client. This appears to be a frontend rendering or query
issue specific to the date filter interaction.

**Describe the solution you'd like**
The Events listing page should return unique, non-duplicate results regardless of which filters
are applied. Filtering by date should produce the same result set as an unfiltered view, narrowed
by the selected date range.

**Describe alternatives you've considered**
N/A

**Additional context**
N/A

### Screenshots

---
