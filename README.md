# Garmin Connect für Claude

Ein Claude-Plugin, mit dem Claude deine eigenen Garmin-Daten über die **Garmin Connect Personal API** lesen und analysieren kann: Aktivitäten samt FIT-Verläufen, Schlaf, HRV, Body Battery, Stress, Gewicht und Tageswerte. Der Zugriff ist read-only.

Das Repo ist ein Plugin-Marketplace (`flawas`) mit dem Plugin `garmin-connect`.

## Voraussetzungen

- macOS oder Linux mit **uv** (`brew install uv`). Ohne uv genügt auch Python ≥ 3.12 im PATH.
- Ein **Garmin Personal API Key**: <https://connect.garmin.com/app/settings/personalApiToken> → *Create Key*. Der Key wird nur einmal angezeigt.

## Installation

1. Den Marketplace in Claude per GitHub-Link hinzufügen: `https://github.com/flawas/garmin-mcp`.
   In Claude Code lauten die Befehle `/plugin marketplace add flawas/garmin-mcp` und `/plugin install garmin-connect@flawas`.
2. Das Plugin **Garmin Connect** installieren und den API-Key in den Plugin-Einstellungen eintragen.

Beim ersten Start werden die Abhängigkeiten automatisch installiert. Danach startet der Server in etwa einer Sekunde.

## Tools

| Tool | Inhalt | Standard-Zeitraum |
|---|---|---|
| `profile` | Profil, VO2max, Laktatschwelle, HF-Zonen | – |
| `daily_summaries` | Schritte, Kalorien, Ruhepuls, Stress, Body Battery, Intensitätsminuten | 7 Tage |
| `sleep_summaries` | Schlaf pro Nacht inkl. Score | 14 Tage |
| `hrv_summaries` | HRV pro Nacht, Baseline, Status | 28 Tage |
| `body_battery` | Body Battery pro Tag | 7 Tage |
| `stress`, `steps` | Tageswerte | 28 Tage |
| `weight` | Gewicht / Körperzusammensetzung | 90 Tage |
| `wellness_activity_summaries` | Wellness-Aktivität pro Tag | 7 Tage |
| `sleep_day`, `hrv_day`, `heart_rate_day` | Detail eines Tages | heute |
| `fitness_age`, `spo2_day` | Fitness-Alter, SpO2 | heute |
| `list_activities` | Aktivitäten kompakt (Distanz, Pace, HF, Trainingseffekt, Load) | 30 Tage |
| `activity_details`, `activity_workouts` | Volle Details einer Aktivität | – |
| `activity_streams` | FIT-Datei → Session, Laps, Verlauf (HF, Pace, Leistung, Kadenz, Höhe) | – |
| `raw_get` | Beliebiger GET-Endpoint aus der [Swagger-Doku](https://developer.garmin.com/gc-developer-program/personal/swagger-docs/) | – |

Der Skill **training-analysis** zeigt Claude, wie es die Tools kombiniert und Kennzahlen wie aerobe Effizienz, kardiale Drift, Belastungsverhältnis und Erholungsstatus berechnet.

## Fehlerbehebung

| Meldung | Lösung |
|---|---|
| `Weder uv noch Python >= 3.12 gefunden` | `brew install uv` ausführen und Claude neu starten |
| `Garmin Personal API Key fehlt oder ist ungültig` | Neuen Key erstellen und in den Plugin-Einstellungen eintragen. Keys laufen nach der gewählten Laufzeit ab |

## Entwicklung

- Bei jeder Änderung `version` in `.claude-plugin/plugin.json` erhöhen, sonst bleiben installierte Plugins auf der alten Version.
- Abhängigkeiten an zwei Stellen synchron halten: im PEP-723-Block in `garmin_mcp.py` und in `requirements.txt`.

Die Personal API ist für den persönlichen Zugriff auf die eigenen Daten gedacht. Dieses Projekt steht in keiner Verbindung zu Garmin.
