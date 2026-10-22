---
name: race-debrief
description: Analysiert ein absolviertes Rennen oder einen Wettkampf aus den Garmin-Daten. Dazu gehören Splits, Pace-Einbruch, HF-Drift, Kadenz, Pausen, der Vergleich mit Plan und früheren Rennen sowie die Lehren für das nächste Rennen. Verwenden bei "wie lief mein Marathon", "Analyse meines Rennens", "wo habe ich Zeit verloren" oder "Race-Debrief".
---

# Race-Debrief

Ziel ist eine sachliche Nachanalyse mit 2–4 konkreten Lehren. Lob gehört dazu, wo es verdient ist. Schwächen benennst du klar und ohne Beschönigung.

## 1. Rennen finden

- `list_activities` im passenden Zeitraum. Das Rennen erkennst du am Datum, am Namen, an der Distanz oder als längste bzw. schnellste Einheit. Bei Unklarheit fragst du nach.
- `activity_details` für das Rennen, `activity_streams` mit `resolution_seconds` 30–60.
- Zum Vergleich holst du frühere Rennen über ähnliche Distanzen und den Pacing-Plan, falls er im Chat oder im Gedächtnis vorliegt.

## 2. Analysieren

**Splits.** Nimm die Laps, meist Auto-Laps à 1 km. Stimmen die Laps nicht, berechnest du Splits pro km aus `series.distance`.
- Erste gegen zweite Hälfte: Ein Positive Split zeigt sich an der Differenz in Sekunden und Prozent. Bis 2 % gelten als gut eingeteilt, über 5 % als deutlicher Einbruch.
- Ab welchem Kilometer fällt die Pace dauerhaft um mehr als 10 s/km unter den Schnitt der ersten Hälfte? Diesen Punkt nennst du „den Hammer“.
- Die Startphase vergleichst du mit der Zielpace bzw. dem Rennschnitt. Ein zu schneller Start ist der häufigste Fehler.

**Herzfrequenz.**
- Kardiale Drift: Pace/HF der ersten Hälfte gegen die zweite (Decoupling in %). Unter 5 % ist das sehr gut. Steigt die HF bei gleicher Pace, deutet das auf Hitze, Dehydrierung oder zu wenig Ausdauerbasis hin. Sinken HF und Pace gemeinsam, spricht das eher für muskuläre Ermüdung oder Energiemangel.
- Die Zeitanteile in den HF-Zonen ermittelst du über die Zonen aus `profile`.

**Weitere Signale.**
- Kadenz: Wert in `series` ×2 ergibt Schritte pro Minute. Ein Abfall um mehr als 5 % im letzten Drittel zeigt muskuläre Ermüdung.
- Pausen: Die Differenz zwischen `total_elapsed_time` und `total_timer_time` in `session` sowie Lücken in `t_s` zeigen Verpflegungs-, Toiletten- oder Gehpausen.
- Höhe: Liegen Einbrüche an Steigungen? Dafür nimmst du `altitude` aus `series`.

**Vorlauf.** In den 7 Tagen vor dem Rennen schaust du auf Belastung, HRV, Schlaf und Ruhepuls. War der Nutzer erholt?

## 3. Antwort

1. **Ergebnis in einem Satz:** Zeit, Pace, Vergleich mit Ziel und Prognose.
2. **Split-Tabelle**, pro 5 km verdichtet, sowie eine Grafik von Pace und HF über die Distanz, wenn möglich.
3. **Was gut lief**, 1–3 Punkte.
4. **Wo Zeit verloren ging**, mit Ursache, soweit die Daten sie stützen. Spekulationen kennzeichnest du als solche.
5. **Lehren für das nächste Rennen:** 2–4 konkrete Massnahmen für Training, Pacing und Verpflegung.
6. **Erholung:** Bei Marathon und Ultra empfiehlst du Erholungstage. Faustregel: etwa ein lockerer Tag pro 10 km Renndistanz bevor wieder intensiv trainiert wird. Den Ruhepuls- und HRV-Verlauf der Folgetage beobachtest du, wenn schon Daten vorliegen.

## Datenfakten

- In `activity_streams` sind `session` die Rennsummen, `laps` die Rundenwerte (`total_timer_time`, `total_distance`, `avg_heart_rate`, `pace_min_per_km`) und `series` der Verlauf. Das Feld `t_s` in `series` ist Bruttozeit inklusive Pausen. `cadence` ist pro Bein angegeben, Schritte pro Minute ergeben sich mit ×2.
- Bei Rad-Abschnitten heisst das Geschwindigkeitsfeld `speed_mps`. Rechne dort in km/h statt Pace.
- Training Effect und Load sind Garmin-Schätzungen. Stelle keine medizinischen Diagnosen.
