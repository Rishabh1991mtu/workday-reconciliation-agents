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
from google.adk.sessions import VertexAiSessionService
from google.adk.tools import ToolContext


async def retrieve_morning_plan(session_key: str, tool_context: ToolContext) -> dict:
    """Retrieves the morning agent's session details from the Vertex AI Session Service using a key-value retrieval.

    Args:
        session_key: The retrieval key or session ID (e.g., 'plan_2026-06-17').
    """
    try:
        session_service = VertexAiSessionService()
        user_id = (
            tool_context.session.user_id
            if tool_context.session
            else "default_user"
        )

        morning_session = await session_service.get_session(
            app_name="morning-agent",
            user_id=user_id,
            session_id=session_key,
        )
        if morning_session and morning_session.state:
            return {
                "status": "success",
                "source": "VertexAiSessionService",
                "morning_plan": morning_session.state.get("morning_plan"),
            }
    except Exception:
        pass

    plan = tool_context.state.get("user:morning_plan")
    if not plan:
        try:
            with open("/tmp/shared_workday_plan.json") as f:
                data = json.load(f)
                plan = data.get("morning_plan")
        except Exception:
            pass

    if not plan:
        plan = "Default Morning Plan: Client Onboarding Sync (10am), Focus Block (11am)."

    return {"status": "success", "retrieved_key": session_key, "morning_plan": plan}


def scan_collaboration_activity(timeframe: str) -> dict:
    """Scans calls, emails, Slack messages, and meeting transcripts for unresolved action items.

    Args:
        timeframe: Scan timeframe (e.g., 'today').
    """
    signals = [
        {
            "source": "Zoom Transcript",
            "content": "Verify routing_eval.json threshold",
            "owner": "user",
            "confidence": "high",
        },
        {
            "source": "Slack Thread",
            "content": "Verify routing_eval.json threshold",
            "owner": "user",
            "confidence": "high",
        },
        {
            "source": "Gmail",
            "content": "Waiting on customer signoff",
            "owner": "customer",
        },
    ]
    return {"status": "success", "signals": signals}


def filter_ball_in_court(raw_signals: list[dict]) -> dict:
    """Filters tasks for user ownership and deduplicates overlapping cross-platform items.

    Args:
        raw_signals: List of raw action signals.
    """
    deduplicated = [
        {
            "task_id": "t1",
            "title": "Verify routing_eval.json threshold",
            "sources": ["Zoom Transcript", "Slack Thread"],
            "owner": "user",
        }
    ]
    return {"status": "success", "open_action_items": deduplicated}
