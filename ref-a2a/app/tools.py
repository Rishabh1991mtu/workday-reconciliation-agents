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
        {
            "id": "c4",
            "title": "Happy Hour Commute",
            "time": "17:00-18:00",
            "status": "declined",
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
        },
        {
            "project": "Portal Migration",
            "volume": 6,
            "urgency": "Medium",
            "deadline": "Friday",
        },
    ]
    return {"status": "success", "projects": projects}


def schedule_focus_time(duration_minutes: int) -> dict:
    """Generates a Google Calendar booking link for suggested focus time.

    Args:
        duration_minutes: Duration of the focus block in minutes (e.g., 60).

    Returns:
        A dictionary containing confirmation and the Google Calendar booking link.
    """
    booking_url = f"https://calendar.google.com/calendar/r/eventedit?text=Deep+Work+Block&duration={duration_minutes}"
    return {"status": "success", "booked": True, "booking_url": booking_url}


def scan_collaboration_activity(timeframe: str) -> dict:
    """Scans recent calls, Slack conversations, emails, and meeting transcripts for potential action items.

    Args:
        timeframe: The scan window (e.g., 'afternoon' or 'today').

    Returns:
        A dictionary containing raw action signals from collaboration tools.
    """
    signals = [
        {
            "source": "Zoom Transcript",
            "content": "Rishabh to verify routing_eval.json threshold",
            "owner": "Rishabh",
            "confidence": "high",
        },
        {
            "source": "Slack Thread",
            "content": "Verify routing_eval.json threshold",
            "owner": "Rishabh",
            "confidence": "high",
        },
        {
            "source": "Gmail",
            "content": "Waiting on customer security signoff before deployment",
            "owner": "Customer",
            "confidence": "low",
        },
        {
            "source": "Gmail Outbound",
            "content": "Asked DevSecOps for firewall whitelist 3 days ago",
            "owner": "DevSecOps",
            "pending_response": True,
        },
    ]
    return {"status": "success", "signals": signals}


def filter_ball_in_court_tasks(raw_tasks: list[dict]) -> dict:
    """Aggressively filters action items for user ownership and deduplicates overlapping cross-platform items.

    Args:
        raw_tasks: List of raw task candidate dictionaries.

    Returns:
        A dictionary containing deduplicated, ball-in-court tasks requiring user follow-up.
    """
    deduplicated = [
        {
            "task_id": "t1",
            "title": "Verify routing_eval.json threshold",
            "sources": ["Zoom Transcript", "Slack Thread"],
            "ownership": "user",
            "confidence": "high",
        }
    ]
    follow_ups = [
        {
            "request_id": "f1",
            "target": "DevSecOps",
            "topic": "firewall whitelist",
            "days_pending": 3,
            "suggested_reminder": "Following up on the firewall whitelist request sent earlier this week.",
        }
    ]
    return {
        "status": "success",
        "ball_in_court": deduplicated,
        "follow_ups_needed": follow_ups,
    }
