---
name: training-analysis
description: Allgemeine Analyse der eigenen Garmin-Daten (Training, Erholung, Schlaf, HRV, Belastung) mit den Tools der Garmin-Connect-Extension. Verwenden bei Fragen zu einzelnen Einheiten, Trends und Vergleichen über Zeiträume, Schlaf, HRV, Ruhepuls, Body Battery oder Stress, sofern kein spezialisierter Garmin-Skill passt (race-readiness, race-debrief, weekly-review, morning-check, running-load, floorball-load, ironman-build, ultra-trail).
---

# Garmin-Trainingsanalyse

Die Daten kommen ausschliesslich über die Tools der Desktop Extension „Garmin Connect“ (MCP-Server `garmin`). Alle Tools sind read-only. Datumswerte werden immer als `YYYY-MM-DD` übergeben, und "heute" ergibt sich aus dem aktuellen Datum.

## Vorgehen

1. **Zeitraum klären.** Ohne Angabe gelten für Trends 4 Wochen und für Vergleiche zwei gleich lange Perioden.
2. **Zuerst Range-Tools verwenden**, weil sie wenig Kontext kosten:
   - Training: `list_activities`, bei Bedarf gefiltert mit `activity_type` wie `running`, `trail_running`, `cycling` oder `lap_swimming`
   - Erholung: `hrv_summaries`, `sleep_summaries`, `body_battery`, `daily_summaries`, `stress`
   - Schwellen und Zonen: `profile`
3. **Dann gezielt vertiefen**, nur für die Einheiten oder Tage, um die es geht:
   - Eine einzelne Einheit analysierst du mit `activity_streams`. Das Tool liefert Laps und einen Verlauf mit HF, Pace, Leistung, Kadenz und Höhe. Für Intervalle passt `resolution_seconds` 5–15, für lange Einheiten 30–60.
   - Für eine einzelne Nacht nimmst du `sleep_day` oder `hrv_day`. `include_timeseries=true` setzt du nur, wenn der Verlauf wirklich gebraucht wird.
4. **Rechnen statt schätzen.** Bei mehr als einer Handvoll Werten rechnest du Mittelwerte, Trends und Korrelationen mit Code, sofern ein Code-Tool verfügbar ist.
5. **Antworten** mit den wichtigsten Zahlen, einer kurzen Einordnung und höchstens 1–3 konkreten Empfehlungen. Bei Trends über Zeit lohnt sich ein Diagramm.

## Einheiten

- `averageSpeed` und `speed_mps` sind in m/s. Die Pace in min/km ist 1000 / speed / 60. Die Tools liefern `pace_min_per_km` meist schon mit.
- Rohdauern sind in Sekunden, Distanzen in Metern. `list_activities` rechnet bereits in `distance_km` und `duration_min` um.
- Schlafdauern sind in Sekunden, HRV-Werte (RMSSD) in Millisekunden.
- Kadenz: `averageRunningCadenceInStepsPerMinute` in `list_activities` zählt beide Beine. `cadence` in `activity_streams` zählt beim Laufen pro Bein, für Schritte pro Minute nimmst du ×2.
- In `activity_streams` ist `t_s` in `series` die Bruttozeit inklusive Pausen. Pace und Splits rechnest du deshalb über Distanz oder `laps`.

## Datenbesonderheiten

- `activity_type="running"` liefert auch `trail_running` und `treadmill_running`. Andere Sportarten fragst du ohne Filter ab und gruppierst sie nach `activityType`.
- Unihockey wird meist als `field_hockey` (Feldhockey) erfasst.
- Läufe unter 1,5 km sind meist Einlaufen, etwa vor Unihockey, oder Fehlstarts. Sie gehören nicht in Pace- oder Kadenz-Statistiken.
- Der Eintrag eines Tages in `sleep_summaries` und `hrv_summaries` beschreibt die Nacht davor, das Datum ist der Tag des Aufwachens.

## Bewährte Kennzahlen

- **Aerobe Effizienz (EF):** Geschwindigkeit bzw. Leistung geteilt durch die durchschnittliche HF. Sinnvoll ist der Vergleich nur zwischen ähnlichen, lockeren Einheiten auf ähnlichem Terrain. Steigt EF, verbessert sich die aerobe Fitness.
- **Kardiale Drift (Decoupling):** EF der ersten Hälfte verglichen mit der zweiten Hälfte, berechnet aus `activity_streams`. Unter 5 % gilt als gute aerobe Basis.
- **Belastungsverhältnis (ACWR):** Die Summe von `activityTrainingLoad` der letzten 7 Tage im Verhältnis zum Wochenschnitt der letzten 28 Tage. Werte über etwa 1.5 zeigen einen sprunghaften Anstieg der Belastung an.
- **Erholungsstatus:** Liegt die HRV-Nacht unter der Baseline, steigt der Ruhepuls und sinkt der Sleep Score zugleich, ist das ein Ermüdungssignal. Mehrere Signale über mehrere Tage sind aussagekräftiger als ein einzelner Ausreisser.
- **Zeit in Zonen:** Die HF-Werte aus `activity_streams` werden den Zonen aus `profile` zugeordnet.

## Spezialisierte Skills

Für diese Fragen gibt es eigene Skills mit genaueren Vorgaben. Nutze sie, wenn sie passen:
- Rennvorbereitung und Pacing → `race-readiness`
- Rennanalyse → `race-debrief`
- Wochenbericht → `weekly-review`
- Tagesform → `morning-check`
- Laufumfang und Verletzungsrisiko → `running-load`
- Unihockey → `floorball-load`
- Triathlon → `ironman-build`
- Ultra und Trail → `ultra-trail`

## Grenzen

- Garmin-Werte wie VO2max, Training Effect und Body Battery sind Schätzungen. Benenne sie auch so.
- Stelle keine medizinischen Diagnosen. Bei auffälligen Werten wie einem dauerhaft stark erhöhten Ruhepuls, Rhythmusauffälligkeiten oder sehr niedriger SpO2 empfiehlst du eine ärztliche Abklärung.
- Meldet ein Tool einen fehlenden oder ungültigen API-Key, gibst du den `hint` weiter: Der Key wird in Claude Desktop unter Einstellungen → Extensions → Garmin Connect eingetragen. Bitte den Nutzer nie, den Key in den Chat zu schreiben.
- Fehlen die Garmin-Tools ganz, ist die Desktop Extension „Garmin Connect“ nicht installiert oder deaktiviert.
