# Garmin Connect für Claude

Mit diesem Repo kann Claude deine eigenen Garmin-Daten über die **Garmin Connect Personal API** lesen und analysieren: Aktivitäten samt FIT-Verläufen, Schlaf, HRV, Body Battery, Stress, Gewicht und Tageswerte. Der Zugriff ist read-only.

Das Repo enthält zwei Teile:

| Teil | Datei | Inhalt |
|---|---|---|
| **Desktop Extension** | `garmin-connect.mcpb` | Der MCP-Server mit allen Tools. Der API-Key wird in den Claude-Einstellungen eingetragen und ist dort sichtbar und änderbar |
| **Plugin** (Marketplace `flawas`) | `.claude-plugin/`, `skills/` | Der Skill *training-analysis*, der Claude die Auswertung der Daten zeigt (optional) |

## Installation

1. **API-Key erstellen** unter <https://connect.garmin.com/app/settings/personalApiToken> → *Create Key*. Der Key wird nur einmal angezeigt.
2. **Extension installieren:** [`garmin-connect.mcpb`](https://github.com/flawas/garmin-mcp/raw/main/garmin-connect.mcpb) herunterladen und doppelklicken, oder in Claude Desktop unter *Einstellungen → Extensions* installieren.
3. **Key eintragen:** Den Key im Konfigurationsdialog der Extension einfügen. Er wird maskiert und sicher gespeichert. Später findest du ihn unter *Einstellungen → Extensions → Garmin Connect → Konfigurieren*, wo du ihn auch ersetzen kannst.
4. **Skill (optional):** Den Marketplace `https://github.com/flawas/garmin-mcp` hinzufügen und das Plugin *garmin-connect* installieren.

Claude Desktop installiert Python und die Abhängigkeiten beim ersten Start selbst über uv.

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

Token-Cache und FIT-Downloads liegen auf macOS unter `~/Library/Caches/garmin-connect-mcp`.

## Fehlerbehebung

| Meldung | Lösung |
|---|---|
| `Garmin Personal API Key fehlt oder ist ungültig` | Neuen Key erstellen und unter *Einstellungen → Extensions → Garmin Connect → Konfigurieren* ersetzen. Keys laufen nach der gewählten Dauer ab |
| `Garmin ist nicht erreichbar` | Internetverbindung, VPN oder Proxy prüfen |

## Entwicklung

- Die Extension wird mit `npx @anthropic-ai/mcpb pack . garmin-connect.mcpb` gebaut. `.mcpbignore` hält Plugin, Skill und README aus dem Paket.
- Bei Änderungen die Version in `manifest.json`, `pyproject.toml` und `.claude-plugin/plugin.json` gemeinsam erhöhen und das Paket neu bauen.

Die Personal API ist für den persönlichen Zugriff auf die eigenen Daten gedacht. Dieses Projekt steht in keiner Verbindung zu Garmin.
