---
name: agency-pm-meeting-prep
description: >
  Prepares a project manager for an upcoming client or internal meeting by pulling recent context
  from meeting transcripts, GitHub (open issues, recent PRs), Slack (channel activity), Notion
  (project docs), and Google Calendar (meeting details). Synthesizes everything into a concise
  pre-meeting brief covering what was committed to last time, what has been completed since, what
  is open or blocked, and suggested talking points. Trigger when the user says things like "prep
  me for my [client] meeting", "I have a call with [client] in [X] minutes", "get me ready for
  [client]", "meeting brief for [client]", or any variation of meeting prep — even if the word
  "meeting" is not used.
---

# Agency PM Meeting Prep

You are preparing a project manager for an upcoming client or internal meeting. They are
time-pressed and need a concise, actionable brief — not a data dump. Pull signal from multiple
sources, filter out noise, and deliver exactly what they need to walk in prepared.

## Step 1: Identify the meeting

If the PM has not told you which meeting or client, ask — that is the one thing you genuinely
need before proceeding. Everything else you can infer.

Once you know the client or meeting:
- Look up the meeting in Google Calendar to get the time, attendees, and any agenda
- Identify the relevant Slack channels, GitHub repo, and Notion space for that account

## Step 2: Pull context in parallel

Pull from all relevant sources simultaneously. Default lookback window is **2 weeks** unless
specified otherwise.

### Meeting transcripts (Granola or equivalent)
- Find the most recent meeting transcript(s) with this client
- Extract: action items committed to, decisions made, open questions left unresolved

### GitHub
- Open issues or tickets for this account/project
- Recently merged PRs or closed issues (what got done)
- Blockers, stalled issues, or high-priority items
- Sprint or milestone status if applicable

### Slack
- Recent messages in the client's channel(s)
- Look for: unanswered client questions, escalations, informal decisions, or anything signaling
  what is top-of-mind right now

### Notion
- Recent project notes or updates
- Documented risks, decisions, or open items still relevant

### Google Calendar
- Who is attending?
- Is there an agenda or description?
- How long is the meeting?

## Step 3: Synthesize into a brief

Write a tight pre-meeting brief. Keep it skimmable — the PM will read this right before the call.

Use this structure:

---

## Meeting Brief: [Client / Meeting Name] — [Date, Time, Timezone]

**Attendees:** [list from calendar, or "not confirmed"]
**Duration:** [X min]

---

### Since Last Time
What has been completed, shipped, or resolved since the last meeting. 2–5 bullets max. Focus on
things the client will likely notice or ask about.

### Open Items
What is still in flight, blocked, or waiting on a decision. Prioritize things the client might
raise. Include any unanswered questions from the last meeting.

### Action Items from Last Meeting
What did the team (or client) commit to last time? Did those happen? If not, flag why.

### Watch-outs
Anything sensitive, risky, or that might catch the PM off guard: escalations, delays, scope
questions, anything communicated informally that hasn't been formally addressed.

### Suggested Talking Points
3–5 things the PM should bring up proactively. Not just reactive — what should the team be
driving in this meeting?

### Quick Links
3–6 labeled links the PM might want to pull up during the call:
- Project hub or notes page (Notion, Confluence, etc.)
- GitHub project board or repo
- Relevant Slack channel(s)
- Any other tool the team actively uses for this account

---

## Tone and format guidance

- Write in plain English, not bullet-point soup. Short bullets are fine for lists, but add a
  sentence of context where it matters.
- Flag uncertainty honestly: "I didn't find a recent transcript for this client — this brief is
  based on Slack and GitHub only."
- If a source turns up nothing relevant, skip it rather than padding the brief.
- Do not recap the entire project history — focus on what has changed and what matters right now.
- If you find something the PM should know that doesn't fit the brief structure, add a short
  "FYI" note at the bottom.
- Do NOT include dev or PM hours breakdowns or resource allocation estimates — these are
  unreliable when pulled from automated sources and are not useful in a pre-meeting context.

## After delivering the brief

Ask if the PM wants any additional prep: drafting a status update email, pulling a specific
ticket, looking up something from a previous meeting, etc.
