import io
import zipfile

import pytest
import requests

from mcp_server_garmin_connect import server

from .conftest import Seq, http_error

EXPECTED_TOOLS = {
    "profile",
    "daily_summaries",
    "sleep_summaries",
    "hrv_summaries",
    "body_battery",
    "stress",
    "steps",
    "weight",
    "wellness_activity_summaries",
    "sleep_day",
    "hrv_day",
    "heart_rate_day",
    "fitness_age",
    "spo2_day",
    "list_activities",
    "activity_details",
    "activity_workouts",
    "activity_streams",
    "raw_get",
}


async def test_all_tools_registered():
    tools = await server.mcp.list_tools()
    assert {t.name for t in tools} == EXPECTED_TOOLS


def test_list_activities_is_compact(garmin):
    _, client = garmin
    client.responses["search_activities"] = [
        {
            "activityId": 1,
            "activityName": "Rigi Lauf",
            "activityType": {"typeKey": "running"},
            "distance": 10500.0,
            "duration": 3300.0,
            "averageSpeed": 3.18,
            "averageHR": 151,
            "irrelevant": "x",
        }
    ]
    result = server.list_activities(start_date="2026-10-01", end_date="2026-10-21")
    act = result["activities"][0]
    assert result["count"] == 1
    assert act["activityType"] == "running"
    assert act["distance_km"] == 10.5
    assert act["duration_min"] == 55.0
    assert act["avg_pace_min_per_km"] == "5:14"
    assert "irrelevant" not in act


def test_long_series_are_trimmed_unless_requested(garmin):
    _, client = garmin
    client.responses["get_daily_sleep"] = lambda: {
        "dailySleepDTO": {"calendarDate": "2026-10-21"},
        "sleepHeartRate": [{"value": 50, "startGMT": i} for i in range(300)],
    }
    trimmed = server.sleep_day("2026-10-21")
    assert trimmed["sleepHeartRate"]["_omitted_series"] == 300
    full = server.sleep_day("2026-10-21", include_timeseries=True)
    assert len(full["sleepHeartRate"]) == 300


def test_daily_records_are_never_trimmed(garmin):
    _, client = garmin
    days = [{"calendarDate": f"2026-09-{d:02d}", "steps": d} for d in range(1, 31)] * 2
    client.responses["get_daily_steps"] = days
    assert len(server.steps("2026-08-01", "2026-09-30")) == 60


def test_expired_token_is_refreshed_once(garmin):
    auth, client = garmin
    client.responses["get_daily_hrv_summaries"] = Seq(http_error(401), {"hrvSummaries": []})
    assert server.hrv_summaries() == {"hrvSummaries": []}
    assert auth.forced == 1


def test_missing_key_gives_settings_hint(garmin, monkeypatch):
    monkeypatch.delenv("GARMIN_PERSONAL_API_KEY")
    result = server.stress()
    assert result["error"] == "No personal API key configured"
    assert "Einstellungen" in result["hint"]


@pytest.mark.parametrize("value", ["", "   ", "${user_config.garmin_api_key}"])
def test_placeholder_or_empty_key_counts_as_missing(garmin, monkeypatch, value):
    monkeypatch.setenv("GARMIN_PERSONAL_API_KEY", value)
    assert "hint" in server.steps()


def test_rejected_key_gives_hint(garmin):
    auth, _ = garmin
    auth.fail_with = http_error(401, method="POST")
    result = server.profile()["profile"]
    assert result["error"] == "Garmin API HTTP 401"
    assert "hint" in result


def test_network_error_is_reported_not_raised(garmin):
    _, client = garmin
    client.responses["get_daily_steps"] = requests.ConnectionError("offline")
    assert "nicht erreichbar" in server.steps()["error"]


@pytest.mark.parametrize("path", ["https://evil.example/x", "relative/path", "/a/../b"])
def test_raw_get_rejects_unsafe_paths(garmin, path):
    assert "error" in server.raw_get(path)


def test_raw_get_passes_params(garmin):
    _, client = garmin
    client.responses["get"] = {"ok": True}
    assert server.raw_get("/usersummary-service/x", {"a": "1"}) == {"ok": True}
    assert client.calls[-1] == ("get", ("/usersummary-service/x",), {"params": {"a": "1"}})


def _fit_zip() -> bytes:
    from fit_tool.fit_file_builder import FitFileBuilder
    from fit_tool.profile.messages.file_id_message import FileIdMessage
    from fit_tool.profile.messages.lap_message import LapMessage
    from fit_tool.profile.messages.record_message import RecordMessage
    from fit_tool.profile.messages.session_message import SessionMessage
    from fit_tool.profile.profile_type import FileType, Manufacturer, Sport

    builder = FitFileBuilder(auto_define=True)
    file_id = FileIdMessage()
    file_id.type = FileType.ACTIVITY
    file_id.manufacturer = Manufacturer.GARMIN.value
    t0 = 1_760_000_000_000
    file_id.time_created = t0
    builder.add(file_id)
    for i in range(600):
        rec = RecordMessage()
        rec.timestamp = t0 + i * 1000
        rec.heart_rate = 140 + i // 60
        rec.speed = 3.3
        rec.distance = 3.3 * i
        rec.cadence = 85
        builder.add(rec)
    for k in range(2):
        lap = LapMessage()
        lap.start_time = t0 + k * 300_000
        lap.timestamp = t0 + (k + 1) * 300_000
        lap.total_timer_time = 300
        lap.total_distance = 990
        lap.avg_heart_rate = 142 + 5 * k
        lap.enhanced_avg_speed = 3.3
        builder.add(lap)
    session = SessionMessage()
    session.timestamp = t0 + 600_000
    session.start_time = t0
    session.sport = Sport.RUNNING
    session.total_timer_time = 600
    session.total_distance = 1980
    builder.add(session)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("123_ACTIVITY.fit", builder.build().to_bytes())
    return buf.getvalue()


def test_activity_streams_parses_fit(garmin):
    _, client = garmin
    client.responses["download_activity"] = _fit_zip()
    result = server.activity_streams(987654321, resolution_seconds=60)
    assert result["session"][0]["sport"] == "running"
    assert [lap["pace_min_per_km"] for lap in result["laps"]] == ["5:03", "5:03"]
    assert len(result["series"]) == 10
    first = result["series"][0]
    assert first["t_s"] == 0 and first["pace_min_per_km"] == "5:03"
    assert result["series"][-1]["heart_rate"] == 149.0
    # zweiter Aufruf kommt aus dem Cache
    client.responses["download_activity"] = AssertionError("nicht erneut laden")
    assert server.activity_streams(987654321)["record_count"] == 600


def test_activity_streams_handles_broken_download(garmin):
    _, client = garmin
    client.responses["download_activity"] = b"kein zip"
    assert "nicht lesbar" in server.activity_streams(111)["error"]
