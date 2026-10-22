---
name: weekly-review
description: Erstellt einen Wochenbericht aus den Garmin-Daten. Dazu gehören Umfang und Belastung pro Sportart, Intensitätsverteilung, Erholungstrend (HRV, Schlaf, Ruhepuls), Highlights, Warnsignale und der Fokus für die nächste Woche, auf Wunsch auch als Notiz in Obsidian. Verwenden bei "Wochenreview", "wie war meine Trainingswoche", "Wochenbericht" oder "Rückblick letzte Woche".
---

# Wochenreview

Ziel ist ein kompakter Rückblick, der in einer Minute gelesen ist und mit einem klaren Fokus für die nächste Woche endet.

## 1. Zeitraum

- Die Woche beginnt mit dem Wochentag aus `profile` → `firstDayOfWeek`, standardmässig Montag.
- Ohne Angabe ist die laufende bzw. zuletzt abgeschlossene Woche gemeint. Läuft die Woche noch, kennzeichnest du sie als „bisher“.
- Als Vergleichsbasis dienen die 4 Wochen davor.

## 2. Daten holen

- `list_activities` über 5 Wochen ohne Typfilter, mit `limit` 100 und bei Bedarf paginiert.
- `hrv_summaries`, `sleep_summaries` und `daily_summaries` für die Woche plus 4 Vergleichswochen. Aus `daily_summaries` brauchst du Ruhepuls, Stress und Body Battery.

## 3. Auswerten

**Pro Sportart** gruppierst du nach `activityType` in diese Familien:
- Laufen: `running`, `trail_running`, `treadmill_running`, `track_running`
- Rad: `road_biking`, `cycling`, `indoor_cycling`, `virtual_ride`, `gravel_cycling`, `mountain_biking`
- Schwimmen: `lap_swimming`, `open_water_swimming`
- Unihockey: meist `field_hockey`
- Wandern: `hiking`
- Kraft und übrige Einheiten

Für jede Familie ermittelst du Anzahl, Zeit (`duration_min`), Distanz, Höhenmeter und Load (Summe `activityTrainingLoad`). Laufen unter 1,5 km, also Einlaufen, zählst du zur Zeit, aber nicht als eigene Einheit.

**Gesamtbild.**
- Wochen-Load im Vergleich zum 4-Wochen-Schnitt: unter 0.8 ist eine Entlastungswoche, 0.8–1.3 normal, über 1.3–1.5 ein deutlicher Sprung.
- Intensitätsverteilung nach `trainingEffectLabel`: locker sind `RECOVERY` und `AEROBIC_BASE`, mittel `TEMPO`, hart `LACTATE_THRESHOLD`, `VO2MAX`, `ANAEROBIC_CAPACITY` und `SPEED`. Angestrebt sind etwa 80 % locker. Unihockey-Einheiten tragen meist das Label `SPEED` und zählen damit als hart. Das ist korrekt, du weist aber darauf hin, wenn sie den Hauptanteil der harten Zeit ausmachen.
- Monotonie nach Foster: Mittelwert der Tagesloads geteilt durch deren Standardabweichung, Ruhetage zählen mit 0. Über 2.0 ist das monoton, was zusammen mit hoher Last ein Risiko darstellt.

**Erholungstrend.** HRV-Wochenschnitt und Status, Ruhepuls-Schnitt, durchschnittliche Schlafdauer und Score, Durchschnitt der `bodyBattery.maxValue`. Jeden Wert vergleichst du mit den Vorwochen und kennzeichnest den Trend mit ↑, → oder ↓.

**Highlights.** Die längste und härteste Einheit sowie persönliche Bestwerte, soweit sie aus den Daten erkennbar sind.

## 4. Bericht

Verwende dieses Format:

```
## Woche <KW>, <Datum von–bis>
**Fazit:** <1–2 Sätze>

| Sportart | Einheiten | Zeit | Distanz | Hm | Load |
…
**Load:** <Wert> (<Faktor> × 4-Wochen-Schnitt) · **Intensität:** <x % locker / y % hart>

**Erholung:** HRV <Wert> <Trend> · Ruhepuls <Wert> <Trend> · Schlaf <h> / Score <Wert> <Trend>
**Highlights:** …
**Achtung:** … (nur wenn nötig)
**Fokus nächste Woche:** 2–3 konkrete Punkte
```

Steht ein Rennen an, etwa laut Gedächtnis oder Chat, richtest du den Fokus danach aus.

## 5. Optional: Obsidian

Ist ein Obsidian-Tool verfügbar und möchte der Nutzer den Bericht ablegen, fragst du einmal nach Ordner und Dateinamen. Ein Vorschlag wäre `Training/Wochenreview/<JJJJ>-KW<NN>.md` mit Frontmatter (`week`, `load`, `hrv_avg`, `rhr_avg`, `sleep_avg_h`). Existiert die Notiz schon, ersetzt du sie nicht ohne Rückfrage.

## Datenfakten

- `hrv_summaries` liefert `lastNightAvg`, `weeklyAvg`, `baseline.balancedLow` und `balancedUpper` sowie `status`.
- `sleep_summaries` liefert `sleepTimeSeconds` und `sleepScores.overall.value`.
- `daily_summaries` liefert `heartRate.restingValue`, `bodyBattery.maxValue` und `stress.avgLevel`.
- Load, Training Effect und Body Battery sind Garmin-Schätzungen. Stelle keine medizinischen Diagnosen.
