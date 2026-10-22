---
name: race-readiness
description: Bereitet einen bevorstehenden Wettkampf mit den eigenen Garmin-Daten vor. Dazu gehören ein Taper- und Formcheck (Belastung, HRV, Schlaf, Ruhepuls), eine realistische Zielzeit aus den letzten Einheiten und ein Pacing-Plan pro Abschnitt. Verwenden bei Fragen wie "bin ich bereit für den Marathon", "welche Zielzeit ist realistisch", "Pacing-Plan für Sonntag" oder "wie soll ich die letzten Tage vor dem Rennen trainieren".
---

# Race-Readiness & Pacing

Ziel ist eine ehrliche Einschätzung vor einem Rennen. Sie besteht aus drei Teilen: Wie fit ist der Nutzer, wie erholt ist er, und wie sollte er das Rennen einteilen?

## 1. Rahmen klären

Folgendes muss bekannt sein. Fehlt etwas, fragst du kurz nach:
- Distanz und Datum des Rennens, Name und Strecke. Höhenprofil und Rundenstruktur recherchierst du per Websuche, wenn sie unbekannt sind.
- Ein eigenes Zeitziel, falls vorhanden.

Die Tage bis zum Rennen rechnest du ab dem heutigen Datum.

## 2. Daten holen

- `list_activities` über die letzten 12 Wochen mit `activity_type="running"`. Bei Triathlon kommen alle Typen dazu.
- `list_activities` ohne Typfilter über mindestens 90 Tage für die Formberechnung. Mit kürzerer Historie wird CTL unterschätzt.
- `hrv_summaries` und `sleep_summaries` über die letzten 14 Tage, `daily_summaries` über die letzten 14 Tage für den Ruhepuls.
- `profile` für die HF-Zonen und die Laktatschwelle (`lactateThresholdHeartRateUsed`).
- Bei Bedarf `activity_streams` der 1–3 aussagekräftigsten Einheiten, also Tempo- oder Schwellenläufe und Longruns.

## 3. Fitness einschätzen

**Umfang und Longrun.** Berechne Kilometer pro Woche (Mittel der letzten 4 und 8 Wochen), den längsten Lauf der letzten 8 Wochen und die Anzahl der Läufe über 25 km. Läufe unter 1,5 km lässt du weg, das sind meist Einlaufen oder Fehlstarts.

**Leistungsindikatoren.** Wähle die besten Anstrengungen der letzten 6–8 Wochen: Rennen, Schwellen- oder Tempoläufe (`trainingEffectLabel` `LACTATE_THRESHOLD` oder `TEMPO`, oder hohe HF über längere Zeit). Lockere Läufe eignen sich nicht als Prognosebasis.

**Prognose.** Rechne mit der Riegel-Formel T2 = T1 × (D2 / D1)^k:
- k = 1.06 für Distanzen bis zum Halbmarathon.
- Für den Marathon gilt k = 1.06 nur bei solider Vorbereitung, das heisst mehrere Longruns ab 30 km und etwa 50 km pro Woche oder mehr. Fehlen diese, rechnest du mit k = 1.08–1.10 und gibst eine Spanne an.
- Basiert die Prognose auf einem Trainingslauf statt einem Rennen, schlägst du 2–4 % auf.
- Aerobe Effizienz als Plausibilitätscheck: Wie schnell läuft der Nutzer bei einer HF knapp unter der Schwelle? Der Marathon wird typischerweise bei 85–92 % der Laktatschwellen-HF gelaufen.

Rechne mit mehreren Bezugsleistungen, etwa dem Schwellenlauf und dem längsten harten Lauf, und vergleiche die Ergebnisse. Liegen sie weit auseinander, nimmst du die vorsichtigere Basis. Gib eine **realistische Spanne** und eine **Empfehlung** an, keine Scheingenauigkeit auf die Sekunde. Nennt der Nutzer ein Ziel, ordnest du es ein: ambitioniert, realistisch oder konservativ.

## 4. Taper- und Erholungscheck

Als Tagesbelastung dient die Summe von `activityTrainingLoad` pro Tag über alle Sportarten.
- **Form:** CTL ist der exponentielle 42-Tage-Schnitt der Tagesbelastung, ATL der 7-Tage-Schnitt, Form = CTL − ATL. Am Renntag sollte die Form leicht positiv sein. Diese Kennzahlen sind Annäherungen und so zu benennen.
- **Belastung der letzten 7 Tage im Vergleich zu den Wochen davor.** Im Taper sinkt der Umfang auf 40–60 %, die Intensität bleibt in kurzen Dosen erhalten. Ein tiefes Akut-zu-chronisch-Verhältnis ist hier gewollt und kein Warnsignal.
- **Erholungssignale:** HRV `lastNightAvg` relativ zur Baseline (`balancedLow`/`balancedUpper`) und zum `status`, Ruhepuls relativ zum 14-Tage-Schnitt (ab +5 Schlägen auffällig), Sleep Score und Schlafdauer relativ zu `sleepNeed.actual`.
- Andere Sportarten wie Unihockey (`field_hockey`), Rad oder Wandern zählen mit. Harte Intervall- und Spielbelastung in den letzten 3–4 Tagen vor dem Rennen ist ein Risiko, das du ansprichst.

## 5. Pacing-Plan

- Grundsatz: gleichmässig oder leicht negativ. Die ersten 3–5 km laufen 5–10 s/km langsamer als die Zielpace.
- Plane pro Abschnitt, also pro 5 km und beim Marathon zusätzlich die Halbmarathon-Durchgangszeit. Gib Pace und Durchgangszeit an und passe Steigungen an: etwa +10–15 s/km pro 1 % Steigung, und die Pace nicht bergab „zurückholen“.
- Als HF-Leitplanke gibst du eine Obergrenze für die erste Hälfte an. Beim Marathon liegt sie etwa im oberen Bereich von Zone 3 bzw. bei rund 88–90 % der Laktatschwelle.
- Verpflegung beim Marathon: 60–90 g Kohlenhydrate pro Stunde ab etwa Minute 30–40, Wasser nach Durst. Was im Training nicht getestet wurde, wird am Renntag nicht verwendet.

## 6. Antwort

1. **Ampel:** Bereit, Bereit mit Vorbehalten oder Risiko, jeweils mit 2–3 Gründen.
2. **Zielzeit:** Spanne und Empfehlung, mit der Herleitung in einem Satz.
3. **Pacing-Tabelle:** Abschnitt, Pace, Durchgangszeit, Hinweis.
4. **Die letzten Tage:** Was der Nutzer bis zum Rennen noch tun und lassen sollte, konkret pro Tag, wenn weniger als 7 Tage bleiben.

## Datenfakten

- `list_activities`: `distance_km`, `duration_min`, `movingDuration_min`, `averageSpeed` (m/s), `averageHR`, `maxHR`, `elevationGain`, `activityTrainingLoad`, `trainingEffectLabel`. Der Filter `running` liefert auch `trail_running` und `treadmill_running`.
- `activity_streams`: In `laps` sind meist Auto-Laps à 1 km. Das Feld `t_s` in `series` ist Bruttozeit inklusive Pausen, deshalb rechnest du Pace über Distanz oder Laps. `cadence` ist pro Bein angegeben, Schritte pro Minute ergeben sich mit ×2.
- Garmin-Werte wie VO2max, Training Effect, Load und Body Battery sind Schätzungen. Stelle keine medizinischen Diagnosen.
