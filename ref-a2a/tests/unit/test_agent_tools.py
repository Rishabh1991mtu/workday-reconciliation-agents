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

from app.tools import (
    filter_ball_in_court_tasks,
    get_calendar_events,
    scan_collaboration_activity,
    schedule_focus_time,
    search_recent_work,
)


def test_morning_tools() -> None:
    cal_res = get_calendar_events("2026-06-17")
    assert cal_res["status"] == "success"
    assert len(cal_res["events"]) == 4

    work_res = search_recent_work("all")
    assert work_res["status"] == "success"
    assert len(work_res["projects"]) == 2

    focus_res = schedule_focus_time(60)
    assert focus_res["status"] == "success"
    assert "booking_url" in focus_res


def test_afternoon_tools() -> None:
    scan_res = scan_collaboration_activity("today")
    assert scan_res["status"] == "success"
    assert len(scan_res["signals"]) == 4

    filter_res = filter_ball_in_court_tasks(scan_res["signals"])
    assert filter_res["status"] == "success"
    assert len(filter_res["ball_in_court"]) == 1
    assert len(filter_res["follow_ups_needed"]) == 1
