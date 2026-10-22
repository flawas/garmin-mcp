---
name: ultra-trail
description: Analysiert die Vorbereitung und Einheiten für Ultra- und Trailläufe. Dazu gehören Time on Feet, Höhenmeter, Kilometer-Effort, steigungsbereinigte Pace, Longrun- und Back-to-back-Progression, Ermüdung in späten Phasen, Gehanteile, Nachtläufe und Verpflegungsbedarf. Verwenden bei "Ultra", "Trail", "Höhenmeter", "Time on Feet", "Back-to-back", "Bergtraining" oder "Vorbereitung 50/80/100 km".
---

# Ultra & Trail

Bei Ultras zählen nicht Pace und Kilometer, sondern **Zeit auf den Beinen, Höhenmeter und Ermüdungsresistenz**. Ziel ist eine Einschätzung, ob die Vorbereitung zur Zieldistanz und zum Profil passt.

## 1. Rahmen klären

Folgendes muss bekannt sein. Fehlt etwas, fragst du kurz nach:
- Zielrennen mit Distanz, Höhenmetern, Datum und erwarteter Dauer
- Gelände und ob Nachtabschnitte dazugehören
- Frühere Ultras, falls vorhanden

## 2. Daten holen

- `list_activities` ohne Typfilter über 12–16 Wochen. Relevant sind `running`, `trail_running` und `hiking`, denn Wandern mit Höhenmetern zählt als spezifisches Training. Bei Bedarf paginierst du.
- `activity_streams` für die längsten 2–3 Einheiten, mit `resolution_seconds` 60.

## 3. Kennzahlen

| Kennzahl | Berechnung | Einordnung |
|---|---|---|
| Time on Feet | Summe `duration_min` aus Laufen, Trail und Wandern pro Woche | wichtiger als km |
| Höhenmeter pro Woche | Summe `elevationGain` | im Peak etwa das 0,5- bis 1-fache der Renn-Höhenmeter pro Woche |
| Kilometer-Effort | km + Hm/100 pro Einheit bzw. Woche | vergleicht flache und steile Einheiten fair |
| Längste Einheit | Maximum Dauer und Kilometer-Effort | im Peak etwa 50–60 % der erwarteten Rennzeit, höchstens etwa 5–6 h |
| Back-to-back | zwei lange Einheiten an aufeinanderfolgenden Tagen | ab etwa 6 Wochen vor dem Rennen alle 2–3 Wochen sinnvoll |
| Steigungsbereinigte Pace | Pace pro Kilometer-Effort, also Dauer / (km + Hm/100) | Trend zeigt die Fitness im Gelände |

## 4. Ermüdungsresistenz (einzelne Langeinheit oder Rennen)

Teile `series` in Drittel nach Distanz:
- **Effizienz pro Drittel:** Pace pro Kilometer-Effort im Verhältnis zur HF. Fällt die Effizienz im letzten Drittel um mehr als 10 %, fehlt Ermüdungsresistenz oder Energie.
- **HF-Verlauf:** Bei Ultras sinkt die HF oft spät bei gleicher Anstrengung. Das deutet auf zentrale oder energetische Ermüdung hin, nicht auf Fitness.
- **Gehanteil:** Anteil der Zeit mit Speed unter etwa 1,7 m/s (Gehtempo), getrennt nach steil und flach, ermittelt über `altitude`-Differenzen. Gehen in Steigungen ist Strategie, Gehen im Flachen ist Ermüdung.
- **Pausen:** Differenz zwischen `total_elapsed_time` und `total_timer_time` bzw. Lücken in `t_s`, also Verpflegungsstopps.
- **Kadenz** im letzten Drittel: Wert ×2, ein Abfall zeigt muskuläre Ermüdung.
- **Nachtabschnitte:** Anhand von `startTimeLocal` + Zeit erkennen und prüfen, ob die Pace nachts überproportional fällt.

## 5. Verpflegung und Rennplanung

- Energieverbrauch pro Stunde aus `calories` / Dauer. Das ist eine grobe Garmin-Schätzung.
- Kohlenhydrate als Richtwert: 60–90 g pro Stunde, nur was im Training getestet ist. Flüssigkeit 400–800 ml pro Stunde je nach Hitze, Natrium beachten.
- Zeitplan pro Verpflegungsposten: Distanz und Höhenmeter der Abschnitte nimmst du aus dem Rennprofil (per Websuche, wenn nötig). Die Abschnittszeit rechnest du über die eigene steigungsbereinigte Pace mit 10–20 % Ermüdungsaufschlag in der zweiten Rennhälfte.

## 6. Antwort

1. **Stand:** auf Kurs, knapp oder Lücke, im Verhältnis zum Zielrennen.
2. **Tabelle** der Wochenwerte der letzten 8–12 Wochen mit Time on Feet, Höhenmetern und Kilometer-Effort.
3. **Grafik:** Time on Feet und Höhenmeter pro Woche.
4. **Ermüdungsanalyse** der letzten langen Einheit, wenn vorhanden.
5. **Nächste Schritte:** 3–5 Schwerpunkte, zum Beispiel Back-to-back, Bergtraining, Nachtlauf oder Verpflegung testen.

## Datenfakten

- `list_activities` liefert `distance_km`, `duration_min`, `elevationGain` (m), `averageHR`, `calories` und `activityTrainingLoad`.
- In `activity_streams` sind die Felder in `series` `t_s` (Bruttozeit), `distance` (m), `altitude` (m), `heart_rate`, `speed_mps` und `cadence` (pro Bein, ×2 ergibt Schritte pro Minute).
- Kalorien, Load und Training Effect sind Garmin-Schätzungen. Stelle keine medizinischen Diagnosen.
