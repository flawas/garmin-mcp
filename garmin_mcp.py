"""Garmin Connect Personal API als MCP-Server (Claude Desktop Extension „Garmin Connect“).

Stellt die eigenen Garmin-Daten (Aktivitäten, Schlaf, HRV, Body Battery, Stress …)
als read-only Tools bereit. Der API-Key kommt aus den Extension-Einstellungen
(Umgebungsvariable GARMIN_PERSONAL_API_KEY); das Bearer-Token wird gecacht und erneuert.
Abhängigkeiten: pyproject.toml.
"""

from __future__ import annotations

import io
import logging
import os
import sys
import zipfile
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

import fitdecode
import requests
from garmin_personal_api import (
    GarminPersonalApiClient,
    PersonalApiAuthenticator,
)
from garmin_personal_api.errors import GarminPersonalApiError, HttpError
from mcp.server.mcpserver import MCPServer

# stdout gehört dem MCP-Protokoll – Logs nur nach stderr.
logging.basicConfig(stream=sys.stderr, level=logging.WARNING)

# Token-Cache und FIT-Downloads
DATA_DIR = Path(
    os.environ.get("GARMIN_MCP_DATA_DIR")
    or ("~/Library/Caches/garmin-connect-mcp" if sys.platform == "darwin" else "~/.cache/garmin-connect-mcp")
).expanduser()
CACHE_DIR = DATA_DIR / "activities"
TOKEN_CACHE_FILE = DATA_DIR / "bearer-token.json"
KEY_PORTAL = "https://connect.garmin.com/app/settings/personalApiToken"
KEY_HINT = (
    "Garmin Personal API Key fehlt oder ist ungültig. In Claude Desktop unter Einstellungen → "
    "Extensions → Garmin Connect → Konfigurieren eintragen und die Extension neu aktivieren. "
    f"Neuen Key erstellen: {KEY_PORTAL} → Create Key."
)
MAX_LIST_LEN = 40  # längere Arrays (Zeitreihen) werden standardmässig zusammengefasst

mcp = MCPServer(
    name="garmin",
    instructions=(
        "Read-only Zugriff auf die eigenen Garmin-Connect-Daten des Nutzers. "
        "Meldet ein Tool einen fehlenden oder ungültigen API-Key, den mitgelieferten Hinweis "
        "weitergeben; den Nutzer nie bitten, den Key in den Chat zu schreiben. "
        "Datumsangaben immer als YYYY-MM-DD. Für Trends zuerst Range-Tools "
        "(daily_summaries, sleep_summaries, hrv_summaries, body_battery, list_activities) "
        "nutzen; Tageszeitreihen nur mit include_timeseries=true holen, wenn wirklich nötig. "
        "Für Laps, Pace, Herzfrequenz- und Leistungsverläufe einer Einheit activity_streams verwenden."
    ),
)


# --------------------------------------------------------------------------- Auth


def _api_key() -> str:
    """Key aus den Extension-Einstellungen."""
    key = os.environ.get("GARMIN_PERSONAL_API_KEY", "").strip()
    if not key or key.startswith("${"):
        raise GarminPersonalApiError("No personal API key configured")
    return key


class _Garmin:
    """Hält Client und Token; erneuert bei 401 einmal automatisch."""

    def __init__(self) -> None:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self._auth = PersonalApiAuthenticator(bearer_token_cache_file=TOKEN_CACHE_FILE)
        self._client: GarminPersonalApiClient | None = None

    def _token(self, force: bool = False) -> str:
        return self._auth.obtain_token(_api_key(), force_refresh=force).access_token


    def client(self) -> GarminPersonalApiClient:
        if self._client is None:
            self._client = GarminPersonalApiClient(self._token())
        else:
            # obtain_token liefert gecachtes Token oder holt bei <1h Restlaufzeit ein neues
            self._client.update_bearer_token(self._token())
        return self._client

    def call(self, fn_name: str, *args: Any, **kwargs: Any) -> Any:
        try:
            return getattr(self.client(), fn_name)(*args, **kwargs)
        except HttpError as exc:
            if exc.status_code != 401:
                raise
            self.client().update_bearer_token(self._token(force=True))
            return getattr(self.client(), fn_name)(*args, **kwargs)


garmin = _Garmin()


# Fehler, die ein Tool als Ergebnis meldet statt abzustürzen
TOOL_ERRORS = (GarminPersonalApiError, requests.RequestException, OSError, ValueError)


def _error(exc: Exception) -> dict:
    if isinstance(exc, requests.RequestException):
        return {"error": "Garmin ist nicht erreichbar (Netzwerk/Proxy)", "detail": str(exc)[:300]}
    if isinstance(exc, HttpError):
        out = {"error": f"Garmin API HTTP {exc.status_code}", "detail": exc.response_text[:500]}
        if exc.method == "POST" and exc.status_code in (400, 401, 403):
            out["hint"] = KEY_HINT  # Token-Austausch abgelehnt → Key falsch, abgelaufen oder gelöscht
        return out
    msg = str(exc)
    if "API key" in msg or "api key" in msg.lower():
        return {"error": msg, "hint": KEY_HINT}
    return {"error": msg}


def _run(fn_name: str, *args: Any, timeseries: bool = False, **kwargs: Any) -> Any:
    try:
        data = garmin.call(fn_name, *args, **kwargs)
    except TOOL_ERRORS as exc:
        return _error(exc)
    return data if timeseries else _trim(data)


def _trim(obj: Any) -> Any:
    """Ersetzt lange Arrays durch eine kurze Zusammenfassung, damit der Kontext klein bleibt."""
    if isinstance(obj, dict):
        return {k: _trim(v) for k, v in obj.items()}
    if isinstance(obj, list):
        if len(obj) > MAX_LIST_LEN and not all(isinstance(x, dict) and _is_summary(x) for x in obj):
            return {"_omitted_series": len(obj), "hint": "include_timeseries=true für Rohdaten"}
        return [_trim(x) for x in obj]
    return obj


def _is_summary(d: dict) -> bool:
    # Tages-/Aktivitäts-Datensätze (mit Datum) nie wegkürzen, nur Messreihen
    return any(k in d for k in ("calendarDate", "activityId", "date", "startTimeLocal"))


def _today() -> str:
    return date.today().isoformat()


def _days_ago(n: int) -> str:
    return (date.today() - timedelta(days=n)).isoformat()


# --------------------------------------------------------------------------- Profil


@mcp.tool()
def profile() -> Any:
    """Profil-Einstellungen (Gewicht, Grösse, VO2max, Laktatschwelle, Einheiten) und Herzfrequenzzonen."""
    return {
        "profile": _run("get_user_profile_settings"),
        "heart_rate_zones": _run("get_heart_rate_zones"),
    }


# --------------------------------------------------------------------------- Tageswerte (Ranges)


@mcp.tool()
def daily_summaries(start_date: str | None = None, end_date: str | None = None) -> Any:
    """Tageszusammenfassungen pro Tag: Schritte, Kalorien, Ruhepuls, Stress, Body Battery,
    Intensitätsminuten, Etagen usw. Standard: letzte 7 Tage."""
    return _run("get_daily_summaries", start_date or _days_ago(6), end_date or _today())


@mcp.tool()
def sleep_summaries(start_date: str | None = None, end_date: str | None = None) -> Any:
    """Schlaf-Zusammenfassung pro Nacht (Dauer, Phasen, Sleep Score). Standard: letzte 14 Tage."""
    return _run("get_daily_sleep_summaries", start_date or _days_ago(13), end_date or _today())


@mcp.tool()
def hrv_summaries(start_date: str | None = None, end_date: str | None = None) -> Any:
    """HRV pro Nacht (Mittelwert, 7-Tage-Schnitt, Baseline, Status). Standard: letzte 28 Tage."""
    return _run("get_daily_hrv_summaries", start_date or _days_ago(27), end_date or _today())


@mcp.tool()
def body_battery(start_date: str | None = None, end_date: str | None = None) -> Any:
    """Body Battery pro Tag (Aufladung, Verbrauch, Höchst-/Tiefstwert). Standard: letzte 7 Tage."""
    return _run("get_daily_body_battery", start_date or _days_ago(6), end_date or _today())


@mcp.tool()
def stress(start_date: str | None = None, end_date: str | None = None) -> Any:
    """Durchschnittlicher Stress pro Tag. Standard: letzte 28 Tage."""
    return _run("get_daily_stress", start_date or _days_ago(27), end_date or _today())


@mcp.tool()
def steps(start_date: str | None = None, end_date: str | None = None) -> Any:
    """Schritte und Schrittziel pro Tag. Standard: letzte 28 Tage."""
    return _run("get_daily_steps", start_date or _days_ago(27), end_date or _today())


@mcp.tool()
def weight(start_date: str | None = None, end_date: str | None = None) -> Any:
    """Gewichtsmessungen (inkl. Körperzusammensetzung, falls vorhanden). Standard: letzte 90 Tage."""
    return _run("get_weight_measurements", start_date or _days_ago(89), end_date or _today())


@mcp.tool()
def wellness_activity_summaries(start_date: str | None = None, end_date: str | None = None) -> Any:
    """Wellness-Aktivitätsübersicht pro Tag. Standard: letzte 7 Tage."""
    return _run("get_wellness_activity_summaries", start_date or _days_ago(6), end_date or _today())


# --------------------------------------------------------------------------- Einzeltage


@mcp.tool()
def sleep_day(date: str | None = None, include_timeseries: bool = False) -> Any:
    """Detaillierter Schlaf einer Nacht (Phasen, Atmung, HF, HRV, Sleep Score inkl. Faktoren).
    `date` = Datum des Aufwachens. Zeitreihen nur mit include_timeseries=true."""
    return _run("get_daily_sleep", date or _today(), timeseries=include_timeseries)


@mcp.tool()
def hrv_day(date: str | None = None, include_timeseries: bool = False) -> Any:
    """HRV einer Nacht mit Einzelmessungen (Zeitreihe nur mit include_timeseries=true)."""
    return _run("get_daily_hrv", date or _today(), timeseries=include_timeseries)


@mcp.tool()
def heart_rate_day(date: str | None = None, include_timeseries: bool = False) -> Any:
    """Herzfrequenz eines Tages (Ruhepuls, Min/Max; Verlauf nur mit include_timeseries=true)."""
    return _run("get_daily_heart_rate", date or _today(), timeseries=include_timeseries)


@mcp.tool()
def fitness_age(date: str | None = None) -> Any:
    """Fitness-Alter und beeinflussende Faktoren."""
    return _run("get_fitness_age", date or _today())


@mcp.tool()
def spo2_day(date: str | None = None) -> Any:
    """Pulsoximetrie (SpO2) und Höhenakklimatisierung eines Tages."""
    return _run("get_daily_spo2", date or _today())


# --------------------------------------------------------------------------- Aktivitäten

_ACTIVITY_FIELDS = (
    "activityId", "activityName", "startTimeLocal", "activityType", "distance", "duration",
    "movingDuration", "elevationGain", "averageSpeed", "averageHR", "maxHR", "averagePower",
    "normPower", "averageRunningCadenceInStepsPerMinute", "aerobicTrainingEffect",
    "anaerobicTrainingEffect", "activityTrainingLoad", "vO2MaxValue", "calories",
    "trainingEffectLabel", "locationName",
)


def _slim_activity(a: dict) -> dict:
    out = {k: a[k] for k in _ACTIVITY_FIELDS if k in a and a[k] is not None}
    if isinstance(out.get("activityType"), dict):
        out["activityType"] = out["activityType"].get("typeKey")
    if out.get("distance"):
        out["distance_km"] = round(out.pop("distance") / 1000, 2)
    for k in ("duration", "movingDuration"):
        if out.get(k):
            out[f"{k}_min"] = round(out.pop(k) / 60, 1)
    if out.get("averageSpeed") and out.get("activityType") in ("running", "trail_running", "treadmill_running"):
        out["avg_pace_min_per_km"] = _pace(out["averageSpeed"])
    return out


def _pace(mps: float | None) -> str | None:
    if not mps:
        return None
    sec = 1000 / mps
    return f"{int(sec // 60)}:{int(sec % 60):02d}"


@mcp.tool()
def list_activities(
    start_date: str | None = None,
    end_date: str | None = None,
    activity_type: str | None = None,
    limit: int = 50,
    start: int = 0,
) -> Any:
    """Aktivitäten (kompakt) im Zeitraum, neueste zuerst. Standard: letzte 30 Tage.
    activity_type z.B. running, cycling, trail_running, lap_swimming, strength_training.
    Für mehr als `limit` Einträge mit `start` paginieren."""
    data = _run(
        "search_activities",
        start=start,
        limit=min(limit, 200),
        start_date=start_date or _days_ago(29),
        end_date=end_date or _today(),
        activity_type=activity_type,
        timeseries=True,
    )
    if isinstance(data, list):
        return {"count": len(data), "activities": [_slim_activity(a) for a in data]}
    return data


@mcp.tool()
def activity_details(activity_id: int) -> Any:
    """Vollständige Zusammenfassung einer Aktivität (Splits-Summary, Trainingseffekt, Gerät usw.)."""
    return _run("get_activity", activity_id)


@mcp.tool()
def activity_workouts(activity_id: int) -> Any:
    """Geplante/strukturierte Workouts, die mit einer Aktivität verknüpft sind."""
    return _run("get_activity_workouts", activity_id)


@mcp.tool()
def activity_streams(activity_id: int, resolution_seconds: int = 30) -> Any:
    """Lädt die Original-FIT-Datei und liefert Session-Werte, alle Laps und einen auf
    `resolution_seconds` heruntergerechneten Verlauf (HF, Pace/Speed, Leistung, Kadenz, Höhe).
    Ideal für Intervall-, Pacing-, Drift- und Zonen-Analysen. Datei wird lokal gecacht."""
    try:
        raw = _download(activity_id)
    except TOOL_ERRORS as exc:
        return _error(exc)
    try:
        return _parse_fit(raw, max(1, resolution_seconds))
    except (zipfile.BadZipFile, fitdecode.FitError) as exc:
        return {"error": f"Aktivitätsdatei nicht lesbar: {exc}"}


def _download(activity_id: int) -> bytes:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path = CACHE_DIR / f"{int(activity_id)}.zip"
    if path.exists():
        return path.read_bytes()
    content = garmin.call("download_activity", activity_id)
    path.write_bytes(content)
    return content


_SESSION_FIELDS = (
    "sport", "sub_sport", "start_time", "total_elapsed_time", "total_timer_time", "total_distance",
    "avg_heart_rate", "max_heart_rate", "avg_speed", "enhanced_avg_speed", "avg_power",
    "normalized_power", "avg_cadence", "total_ascent", "total_descent", "total_calories",
    "total_training_effect", "total_anaerobic_training_effect", "training_load_peak",
)
_LAP_FIELDS = (
    "start_time", "total_timer_time", "total_distance", "avg_heart_rate", "max_heart_rate",
    "avg_speed", "enhanced_avg_speed", "avg_power", "avg_cadence", "total_ascent", "intensity",
)
_RECORD_FIELDS = (
    "heart_rate", "enhanced_speed", "speed", "power", "cadence", "enhanced_altitude", "altitude",
    "distance",
)


def _jsonable(v: Any) -> Any:
    if isinstance(v, datetime):
        return v.isoformat()
    if isinstance(v, float):
        return round(v, 3)
    if isinstance(v, (int, str)) or v is None:
        return v
    return str(v)


def _fields(frame: fitdecode.FitDataMessage, names: tuple[str, ...]) -> dict:
    out = {}
    for n in names:
        if frame.has_field(n):
            v = frame.get_value(n)
            if v is not None:
                out[n] = _jsonable(v)
    return out


def _parse_fit(zip_bytes: bytes, step: int) -> dict:
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        fit_names = [n for n in zf.namelist() if n.lower().endswith(".fit")]
        if not fit_names:
            return {"error": "Keine FIT-Datei im Download (evtl. manuell erfasste Aktivität)",
                    "files": zf.namelist()}
        fit = zf.read(fit_names[0])

    sessions, laps, records = [], [], []
    with fitdecode.FitReader(io.BytesIO(fit)) as reader:
        for frame in reader:
            if not isinstance(frame, fitdecode.FitDataMessage):
                continue
            if frame.name == "session":
                sessions.append(_fields(frame, _SESSION_FIELDS))
            elif frame.name == "lap":
                laps.append(_fields(frame, _LAP_FIELDS))
            elif frame.name == "record" and frame.has_field("timestamp"):
                records.append((frame.get_value("timestamp"), _fields(frame, _RECORD_FIELDS)))

    for lap in laps:
        speed = lap.get("enhanced_avg_speed") or lap.get("avg_speed")
        if speed:
            lap["pace_min_per_km"] = _pace(speed)

    return {
        "session": sessions,
        "laps": laps,
        "series": _downsample(records, step),
        "series_resolution_seconds": step,
        "record_count": len(records),
    }


def _downsample(records: list[tuple[datetime, dict]], step: int) -> list[dict]:
    """Mittelt Messpunkte in Zeitfenstern von `step` Sekunden."""
    if not records:
        return []
    t0 = records[0][0]
    buckets: dict[int, list[dict]] = {}
    for ts, vals in records:
        buckets.setdefault(int((ts - t0).total_seconds()) // step, []).append(vals)
    out = []
    for idx in sorted(buckets):
        rows = buckets[idx]
        point: dict[str, Any] = {"t_s": idx * step}
        for key in _RECORD_FIELDS:
            nums = [r[key] for r in rows if isinstance(r.get(key), (int, float))]
            if nums:
                point[key] = round(sum(nums) / len(nums), 2) if key != "distance" else round(max(nums), 1)
        speed = point.pop("enhanced_speed", None) or point.get("speed")
        point.pop("speed", None)
        if speed:
            point["speed_mps"] = speed
            point["pace_min_per_km"] = _pace(speed)
        if "enhanced_altitude" in point:
            point["altitude"] = point.pop("enhanced_altitude")
        out.append(point)
    return out


# --------------------------------------------------------------------------- Fallback


@mcp.tool()
def raw_get(path: str, params: dict[str, str] | None = None, include_timeseries: bool = False) -> Any:
    """Beliebiger GET-Aufruf an die Personal API für Endpoints ohne eigenes Tool
    (siehe Swagger-Doku), z.B. path='/usersummary-service/stats/hydration/daily/2026-10-01/2026-10-21'."""
    if not path.startswith("/") or ".." in path or "://" in path:
        return {"error": "path muss ein relativer API-Pfad sein, der mit / beginnt"}
    return _run("get", path, params=params, timeseries=include_timeseries)


def main() -> None:
    mcp.run("stdio")


if __name__ == "__main__":
    main()
