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
    get_calendar_events,
    search_recent_work,
    publish_morning_plan,
)

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-3-flash-preview",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    description="Morning Coffee Prep Agent that starts your day with a grounded plan.",
    instruction="""You are Morning Coffee, a daily prep agent designed to run at the start of the workday.
1. Cluster recent work using search_recent_work.
2. Filter calendar events using get_calendar_events.
3. Save the resulting plan details to session storage using publish_morning_plan so the afternoon agent can access it.
4. Provide a concise Daily Prep Brief to the user.""",
    tools=[get_calendar_events, search_recent_work, publish_morning_plan],
)

app = App(
    root_agent=root_agent,
    name="app",
)
