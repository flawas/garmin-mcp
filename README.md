# Garmin Connect MCP Server

<!-- mcp-name: io.github.flawas/garmin-mcp -->

Ein [Model Context Protocol](https://modelcontextprotocol.io) Server für deine **eigenen Garmin-Connect-Daten** über die [Garmin Connect Personal API](https://developer.garmin.com/gc-developer-program/personal/personal-api/): Aktivitäten samt FIT-Verläufen, Schlaf, HRV, Body Battery, Stress, Gewicht und Tageswerte. Der Zugriff ist read-only.

Dazu gehört ein optionales Claude-Plugin mit Analyse-Skills für Tagesform, Wochenreview, Rennen, Laufbelastung, Unihockey, Ironman sowie Ultra und Trail.

### Tools

| Tool | Inhalt | Standard-Zeitraum |
|---|---|---|
| `profile` | Profil-Einstellungen und HF-Zonen | – |
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

Lange Zeitreihen werden standardmässig gekürzt, damit der Chat-Kontext nicht vollläuft. Mit `include_timeseries=true` bekommst du die Rohdaten.

## API-Key

Erstelle unter <https://connect.garmin.com/app/settings/personalApiToken> einen Key mit *Create Key*. Er wird nur einmal angezeigt und läuft nach der gewählten Dauer ab (30 Tage bis 1 Jahr). Der Server liest ihn aus der Umgebungsvariable `GARMIN_PERSONAL_API_KEY`.

## Installation

### Claude Desktop (Extension, empfohlen)

1. Lade `garmin-connect.mcpb` aus dem [neuesten Release](https://github.com/flawas/garmin-mcp/releases/latest) herunter und doppelklicke die Datei.
2. Trag den API-Key im Konfigurationsdialog ein. Er ist danach unter *Einstellungen → Extensions → Garmin Connect* sichtbar und änderbar.

Python und die Abhängigkeiten installiert Claude Desktop selbst.

### Mit uvx (jeder MCP-Client)

Voraussetzung ist [uv](https://docs.astral.sh/uv/). Das Paket wird beim Start automatisch von PyPI geladen.

```json
{
  "mcpServers": {
    "garmin": {
      "command": "uvx",
      "args": ["mcp-server-garmin-connect"],
      "env": { "GARMIN_PERSONAL_API_KEY": "<dein-key>" }
    }
  }
}
```

In Claude Code genügt ein Befehl:

```bash
claude mcp add garmin -e GARMIN_PERSONAL_API_KEY=<dein-key> -- uvx mcp-server-garmin-connect
```

### Mit pip

```bash
pip install mcp-server-garmin-connect
GARMIN_PERSONAL_API_KEY=<dein-key> mcp-server-garmin-connect
```

### Mit Docker

```bash
docker build -t mcp-server-garmin-connect .
docker run -i --rm -e GARMIN_PERSONAL_API_KEY=<dein-key> mcp-server-garmin-connect
```

### Skills (optional, Claude)

Füge den Plugin-Marketplace `https://github.com/flawas/garmin-mcp` hinzu und installiere das Plugin *garmin-connect*. In Claude Code geht das mit `/plugin install garmin-connect --marketplace flawas/garmin-mcp`.

| Skill | Wofür |
|---|---|
| `morning-check` | Tagesform-Ampel aus HRV, Schlaf, Ruhepuls und Body Battery mit Empfehlung für heute |
| `weekly-review` | Wochenbericht nach Sportart, optional als Obsidian-Notiz |
| `race-readiness` | Taper- und Formcheck, realistische Zielzeit, Pacing-Plan |
| `race-debrief` | Rennanalyse: Splits, Einbruch, HF-Drift, Kadenz, Lehren |
| `running-load` | Laufumfang, Steigerungsrate, ACWR, Verletzungsrisiko |
| `floorball-load` | Unihockey (bei Garmin als Feldhockey erfasst) als Intervallbelastung einordnen |
| `ironman-build` | Triathlon-Aufbau: Verteilung, Langeinheiten, Koppeltrainings, Lücken |
| `ultra-trail` | Time on Feet, Höhenmeter, Kilometer-Effort, Ermüdungsresistenz |
| `training-analysis` | Allgemeine Analysen und Basis für alle anderen Skills |

## Konfiguration

| Variable | Pflicht | Bedeutung |
|---|---|---|
| `GARMIN_PERSONAL_API_KEY` | ja | Personal API Key |
| `GARMIN_MCP_DATA_DIR` | nein | Ordner für Token-Cache und FIT-Downloads. Standard ist `~/Library/Caches/garmin-connect-mcp` auf macOS und `~/.cache/garmin-connect-mcp` sonst |

## Debugging

Mit dem [MCP Inspector](https://github.com/modelcontextprotocol/inspector):

```bash
npx @modelcontextprotocol/inspector uvx mcp-server-garmin-connect
# aus dem Repo heraus:
npx @modelcontextprotocol/inspector uv run mcp-server-garmin-connect
```

| Meldung | Lösung |
|---|---|
| `Garmin Personal API Key fehlt oder ist ungültig` | Neuen Key erstellen und in der Extension bzw. in `GARMIN_PERSONAL_API_KEY` ersetzen |
| `Garmin ist nicht erreichbar` | Internetverbindung, VPN oder Proxy prüfen |

## Entwicklung

```bash
uv sync                         # Umgebung inkl. Dev-Tools
uv run pytest                   # Tests
uv run ruff check . && uv run ruff format --check .
uv run pyright                  # Typen
npx @anthropic-ai/mcpb pack . garmin-connect.mcpb   # Desktop Extension lokal bauen
```

Aufbau des Repos:

```
src/mcp_server_garmin_connect/   MCP-Server (Python-Paket, Einstiegspunkt mcp-server-garmin-connect)
tests/                           pytest
server.json                      Eintrag für die MCP Registry
manifest.json, .mcpbignore       Claude Desktop Extension (.mcpb)
.claude-plugin/, skills/         Claude-Plugin mit Analyse-Skills
.github/workflows/               CI und Release
```

### Release

1. Die Version in `pyproject.toml`, `manifest.json` und `server.json` (zweimal: oben und im PyPI-Paket) gleich setzen. Die CI prüft das. Bei Skill-Änderungen zusätzlich `.claude-plugin/plugin.json` erhöhen.
2. `git tag v<version> && git push origin v<version>`
3. Der Release-Workflow testet, baut, veröffentlicht auf PyPI, erstellt das GitHub-Release mit der `.mcpb`, trägt deren SHA-256 in `server.json` ein und veröffentlicht in der [MCP Registry](https://registry.modelcontextprotocol.io).

Vor dem ersten Release ist eine einmalige Einrichtung nötig:
- **PyPI Trusted Publishing:** Auf <https://pypi.org/manage/account/publishing/> einen *pending publisher* anlegen mit PyPI-Projekt `mcp-server-garmin-connect`, Owner `flawas`, Repository `garmin-mcp`, Workflow `release.yml` und Environment `pypi`.
- **GitHub:** In den Repo-Einstellungen unter *Environments* das Environment `pypi` anlegen.
- Für die MCP Registry ist nichts einzurichten. Die Anmeldung läuft über GitHub OIDC für den Namensraum `io.github.flawas`.

## Hinweis

Die Garmin Connect Personal API ist für den persönlichen Zugriff auf die eigenen Daten gedacht, nicht für kommerzielle Anwendungen mit mehreren Nutzern. Dieses Projekt steht in keiner Verbindung zu Garmin.

## Lizenz

MIT, siehe [LICENSE](LICENSE).
