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
    retrieve_morning_plan,
    scan_collaboration_activity,
    filter_ball_in_court,
)

_, project_id = google.auth.default()
os.environ["CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-3-flash-preview",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    description="Afternoon Tea Reconciliation Agent that closes your workday.",
    instruction="""You are Afternoon Tea, a late-day action review agent designed to reconcile the workday.
1. Retrieve the morning session details and plan using retrieve_morning_plan with key 'user:morning_plan'.
2. Scan collaboration activity using scan_collaboration_activity.
3. Filter tasks for ownership ('ball in court') using filter_ball_in_court.
4. Output a comprehensive Open Action Items Report reconciling completed work vs open items.""",
    tools=[retrieve_morning_plan, scan_collaboration_activity, filter_ball_in_court],
)

app = App(
    root_agent=root_agent,
    name="app",
)
