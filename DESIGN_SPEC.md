# DESIGN_SPEC.md

## Overview
The Morning Coffee and Afternoon Tea paired agent system splits the workday into two distinct, autonomous agent moments.

Morning Coffee is a scheduled prep agent designed to run each morning (~7:30 AM to 8:30 AM). It generates a Daily Prep Brief using the user's recent activity, today's calendar events, and company updates. It clusters recent work into top projects, ranks priorities, filters noise out of meetings, surfaces outstanding actionable tasks, and classifies usable free time into focus blocks (with optional "Book it now" Google Calendar links).

Afternoon Tea is an action review agent designed to run in the late afternoon (~3:30 PM to 5:00 PM). It reconciles the workday by scanning calls, emails, Slack discussions, and meeting transcripts. It consumes the morning's priority context via an autonomous A2A protocol (or shared session memory), evaluates what got done vs. what remains open, filters strictly for user ownership ("ball is in user's court"), deduplicates overlapping tasks across tools, classifies items into high-confidence vs. ambiguous blockers, and surfaces unanswered follow-up requests.

## Example Use Cases

### 1. Morning Daily Prep Generation
- **Input**: User activity logs for the past 48 hours, today's raw calendar events, company news feed.
- **Expected Output**: A scannable Daily Prep Brief detailing 3 top-ranked projects, 2 key prep notes for client meetings (filtering out solo blocks), 4 actionable tasks, and 1 suggested focus block with a direct booking link.

### 2. Afternoon Task Reconciliation & Ownership Filtering
- **Input**: Morning plan baseline, intra-day email/Slack transcript signals.
- **Expected Output**: An open action items report listing 2 unresolved tasks assigned to the user, excluding 3 tasks waiting on external customers.

### 3. Deduplication Across Fragmented Systems
- **Input**: Action item from Zoom transcript ("Follow up on pricing") and identical action item from Slack thread.
- **Expected Output**: A single deduplicated task in the reconciliation report citing both sources.

### 4. Unanswered Follow-up Identification
- **Input**: Outbound email sent 3 days ago requesting security approval with no response.
- **Expected Output**: Suggested reminder message drafted for the user to send on Slack/email.

## Tools Required

1. **`get_calendar_events`**: Fetches raw calendar events for the user. Authentication: OAuth2 / Service Account.
2. **`search_activity_corpus`**: Queries recent emails, Slack messages, and commits. Authentication: API Key / OAuth2.
3. **`schedule_focus_time`**: Generates Google Calendar event booking links. Authentication: None (URL builder) or OAuth2.
4. **`filter_ball_in_court`**: Evaluates ownership and deduplicates overlapping items. Authentication: Internal tool.

## Constraints & Safety Rules

- **Strict Noise Filtering**: Morning Coffee must explicitly ignore commute blocks, solo blocks, tentative/declined meetings, and social events.
- **Aggressive Ownership Filtering**: Afternoon Tea must never surface tasks where the dependency rests entirely on external customers or third-party teams.
- **Model Selection**: Must use `gemini-3-flash-preview` for core synthesis and evaluation tasks.
- **Read-Only Inspection**: Unless explicitly authorized via booking tools, collaboration integrations must operate in read-only scan mode.

## Success Criteria

1. **Safety & Guardrails**: Evaluates 100% compliant under `safety_v1` evaluation criteria.
2. **Reconciliation Accuracy**: Correctly identifies completed vs. open tasks with >95% precision on test evalsets.
3. **Deduplication Rate**: Successfully merges duplicate tasks across Zoom, Slack, and Gmail in >=90% of eval test cases.

## Edge Cases to Handle

1. **Zero Scheduled Meetings / Focus Day**: Handles completely clear calendars by prioritizing deep-work block suggestions and technical debt backlog items.
2. **Conflicting Multi-Source Status**: Resolves ambiguities when a task appears open on Zoom but closed on Slack by classifying it under "Ambiguous Items" for quick user check.
3. **Stale Outbound Requests**: Ignores follow-up prompts if an Out of Office (OOO) auto-reply was detected from the recipient.
