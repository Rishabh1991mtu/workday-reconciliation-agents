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

import json
from google.adk.tools import ToolContext


def get_calendar_events(date_str: str) -> dict:
    """Fetches today's calendar events for the user.

    Args:
        date_str: The date string in YYYY-MM-DD format.

    Returns:
        A dictionary containing scheduled events for the requested date.
    """
    events = [
        {
            "id": "c1",
            "title": "Client Onboarding Sync",
            "time": "10:00-10:45",
            "status": "accepted",
        },
        {
            "id": "c2",
            "title": "Solo Focus Block",
            "time": "11:00-12:00",
            "status": "accepted",
            "is_solo": True,
        },
        {
            "id": "c3",
            "title": "Weekly Team Standup",
            "time": "13:30-14:00",
            "status": "accepted",
        },
    ]
    return {"status": "success", "date": date_str, "events": events}


def search_recent_work(query: str) -> dict:
    """Searches recent commits, emails, and active projects for the user.

    Args:
        query: Search term or project filter.

    Returns:
        A dictionary containing clustered recent work items and project deadlines.
    """
    projects = [
        {
            "project": "Project Alpha",
            "volume": 14,
            "urgency": "High",
            "deadline": "Today 5 PM",
        }
    ]
    return {"status": "success", "projects": projects}


def publish_morning_plan(plan_details: str, tool_context: ToolContext) -> dict:
    """Saves the Morning Coffee prep details to session storage so the afternoon agent can retrieve it.

    Args:
        plan_details: A JSON string or detailed summary of today's morning plan.
    """
    tool_context.state["user:morning_plan"] = plan_details

    try:
        with open("/tmp/shared_workday_plan.json", "w") as f:
            json.dump({"morning_plan": plan_details}, f)
    except Exception:
        pass

    return {"status": "success", "saved": True}
