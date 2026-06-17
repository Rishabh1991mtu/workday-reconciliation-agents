# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import google.auth
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from .tools import (
    filter_ball_in_court_tasks,
    get_calendar_events,
    scan_collaboration_activity,
    schedule_focus_time,
    search_recent_work,
)

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"


morning_coffee_agent = Agent(
    name="morning_coffee_agent",
    model=Gemini(
        model="gemini-3-flash-preview",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    description="An early-morning planning agent that generates a scannable Daily Prep Brief from calendar events and recent work.",
    instruction="""You are Morning Coffee, a daily prep agent designed to run at the start of the workday.
1. Cluster recent work into top projects using search_recent_work.
2. Filter out noisy calendar events (commute, solo blocks, declined meetings) using get_calendar_events.
3. Classify free time and suggest focus blocks using schedule_focus_time.
4. Output a concise, scannable Daily Prep Brief.""",
    tools=[
        get_calendar_events,
        search_recent_work,
        schedule_focus_time,
    ],
    output_key="morning_prep_brief",
)

afternoon_tea_agent = Agent(
    name="afternoon_tea_agent",
    model=Gemini(
        model="gemini-3-flash-preview",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    description="A late-day action review agent that scans collaboration tools to surface unresolved work and unanswered follow-ups.",
    instruction="""You are Afternoon Tea, a late-day action review agent designed to close out the workday.
1. Reference any previous morning prep brief from state if available.
2. Scan emails, Slack threads, and meeting transcripts using scan_collaboration_activity.
3. Filter aggressively for ball-in-court ownership and deduplicate tasks using filter_ball_in_court_tasks.
4. Separate high-confidence items from ambiguous ones and draft reminders for unanswered follow-ups.""",
    tools=[
        scan_collaboration_activity,
        filter_ball_in_court_tasks,
    ],
    output_key="afternoon_reconciliation_report",
)

root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-3-flash-preview",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    description="Workday reconciliation coordinator pairing Morning Coffee and Afternoon Tea moments.",
    instruction="You coordinate the workday agent lifecycle. Route morning prep requests to morning_coffee_agent and afternoon reconciliation requests to afternoon_tea_agent.",
    sub_agents=[
        morning_coffee_agent,
        afternoon_tea_agent,
    ],
)

app = App(
    root_agent=root_agent,
    name="app",
)
