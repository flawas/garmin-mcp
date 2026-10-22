---
name: running-load
description: Überwacht die Laufbelastung zur Verletzungsprävention und für einen sauberen Aufbau. Dazu gehören Wochenkilometer, Steigerungsrate, Akut-zu-chronisch-Verhältnis, Longrun-Anteil, Intensitätsverteilung, Kadenz-Trend und Zusatzbelastung durch andere Sportarten. Verwenden bei "Laufbelastung", "steigere ich zu schnell", "wie viele km soll ich laufen", "Verletzungsrisiko", "Umfang erhöhen" oder "Laufumfang".
---

# Lauf-Belastung

Ziel ist eine Antwort auf die Frage, ob der Nutzer sein Laufen gerade sinnvoll dosiert, und was er an Umfang verträgt. Die meisten Laufverletzungen entstehen durch zu schnelle Steigerung, nicht durch zu viel Umfang an sich.

## 1. Daten holen

- `list_activities` über 12 Wochen mit `activity_type="running"`. Das liefert auch Trail- und Laufband-Läufe, bei mehr als 50 Einträgen paginierst du.
- `list_activities` ohne Filter über die letzten 4 Wochen, um die Gesamtbelastung durch Unihockey, Rad, Wandern und Kraft zu sehen.
- Optional `profile` für die HF-Zonen.

## 2. Bereinigen

- Läufe unter 1,5 km und unter 8 Minuten sind meist Einlaufen, etwa vor Unihockey-Matches, oder Fehlstarts. Du zählst sie zu den Kilometern, aber nicht als Einheit und nicht in Pace- oder Kadenz-Statistiken.
- Laufband-Distanzen ohne Kalibrierung sind unsicher und werden so markiert.
- Trail: Für die Belastung rechnest du mit Kilometer-Effort, also km + Höhenmeter/100.

## 3. Kennzahlen

Rechne mit Code, sofern verfügbar.

| Kennzahl | Berechnung | Bewertung |
|---|---|---|
| Wochenkilometer | Summe `distance_km` pro Kalenderwoche; Wochen ohne Lauf mit 0 km aufführen | Trend über 12 Wochen |
| Steigerungsrate | Woche gegenüber dem Schnitt der 3 Vorwochen | > +10–15 % gelb, > +30 % rot (Ausnahme: Rückkehr auf früheres Niveau nach kurzer Pause) |
| ACWR Laufen | km der letzten 7 Tage / (km der letzten 28 Tage / 4) | 0.8–1.3 sicher, 1.3–1.5 erhöht, > 1.5 hoch. Werte unter 0.8 sind im Taper, in der Entlastungswoche oder nach einem Rennen gewollt. Gefährlich wird erst der Wiedereinstieg mit einem Sprung zurück auf das alte Niveau |
| Longrun-Anteil | längster Lauf der Woche / Wochenkilometer | > 40 % ist ein Risiko, der Longrun ist dann zu dominant. Bei nur 1–2 Läufen pro Woche ist der Anteil zwangsläufig hoch. Dann ist die Botschaft „häufiger laufen“, nicht „Longrun kürzen“ |
| Längster Lauf | Maximum der letzten 4 Wochen | ein Sprung über +20–25 % zum bisherigen Longrun ist zu viel |
| Laufhäufigkeit | Läufe pro Woche | gleich viele km auf mehr Läufe verteilen ist schonender |
| Intensität | Anteil `trainingEffectLabel` `RECOVERY`/`AEROBIC_BASE` an der Laufzeit | Ziel etwa 80 % locker. Sind viele lockere Läufe mit Tempo-HF gelabelt, ist das ein Hinweis, dass „locker“ zu schnell gelaufen wird |
| Kadenz | `averageRunningCadenceInStepsPerMinute` (bereits beide Beine) | ein Abfall bei gleichem Tempo deutet auf Ermüdung hin |
| Gesamtbelastung | `activityTrainingLoad` aller Sportarten pro Woche | Unihockey-Matches und harte Radeinheiten belasten Beine und Sehnen zusätzlich |

## 4. Empfehlung

- **Nächste Woche:** einen konkreten Kilometerkorridor nennen, begründet mit Steigerungsrate und ACWR, dazu die Länge des Longruns.
- **Aufbauregeln als Richtwerte:** +5–10 % pro Woche, alle 3–4 Wochen eine Entlastungswoche mit −20–30 %, Longrun höchstens etwa 30–35 % des Wochenumfangs und höchstens etwa 2,5–3 h, ausser im Ultra-Training.
- Gibt es Schmerzsignale aus dem Chat oder auffällige Kadenz- oder Pace-Muster, empfiehlst du Umfang reduzieren und Abklärung, nicht „durchziehen“.
- Steht ein Rennen an, passt du die Empfehlung an Aufbau, Peak oder Taper an.

## 5. Antwort

1. **Status:** Ampel und ein Satz.
2. **Grafik:** Wochenkilometer der letzten 12 Wochen, als Balken. Optional mit einer Linie für den 4-Wochen-Schnitt.
3. **Tabelle** der Kennzahlen mit Bewertung.
4. **Empfehlung** für die nächsten 1–2 Wochen.

## Datenfakten

- `list_activities` liefert `distance_km`, `duration_min`, `elevationGain`, `averageSpeed` (m/s), `averageHR`, `activityTrainingLoad` und `trainingEffectLabel`.
- In `activity_streams` ist `cadence` pro Bein angegeben, Schritte pro Minute ergeben sich mit ×2.
- Unihockey wird meist als `field_hockey` erfasst.
- Load und Training Effect sind Garmin-Schätzungen. Stelle keine medizinischen Diagnosen.
