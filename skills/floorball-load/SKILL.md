---
name: floorball-load
description: Ordnet Unihockey-Trainings und -Matches (bei Garmin meist als Feldhockey erfasst) als intervallartige Belastung ein. Dazu gehören Intensität, Sprints und Zeit in hohen Zonen, Turnier- und Doppelbelastung, Erholungsbedarf und die Abstimmung mit dem Ausdauertraining. Verwenden bei "Unihockey", "Floorball", "Match", "Turnier", "wie hart war das Training" oder "Unihockey und Laufen kombinieren".
---

# Unihockey-Belastung

Unihockey ist intermittierende Hochintensität: kurze Sprints, Richtungswechsel und Wechselpausen. Die Durchschnitts-HF unterschätzt die Belastung deshalb. Ziel ist, die Einheiten richtig einzuordnen und das Ausdauertraining darum herum zu planen.

## 1. Einheiten finden

- `list_activities` ohne Typfilter über 4–8 Wochen.
- Unihockey ist meist als `activityType` `field_hockey` erfasst, weil Garmin kein Unihockey-Profil hat. Seltener taucht es als `floorball`, `team_sport`, `indoor_cardio` oder `other` auf, mit Namen wie „Unihockey“, „Training“ oder „Match“. Bei Unklarheit fragst du einmal nach und merkst dir die Antwort für das Gespräch.
- Kurze Läufe unter 1,5 km kurz vor einer Unihockey-Einheit gehören als Einlaufen dazu.
- Mehrere Einheiten am selben Tag oder Wochenende deuten auf ein Turnier oder eine Doppelrunde hin und werden als Block betrachtet.

## 2. Pro Einheit auswerten

Aus `list_activities` nimmst du `duration_min`, `averageHR`, `maxHR`, `activityTrainingLoad`, `aerobicTrainingEffect`, `anaerobicTrainingEffect` und `trainingEffectLabel`. Ein Anaerob-Effekt ab etwa 2.5 steht für intensive Spielbelastung.

Für Details holst du `activity_streams` mit `resolution_seconds` 5–10 und dazu die Zonen aus `profile`:
- **Zeit in Zone 4 und Zone 5** in Minuten und Prozent.
- **Hochintensive Spitzen:** Anzahl der Phasen über der Zone-5-Grenze, die mindestens 10 s dauern. Das ist eine Näherung für die Anzahl harter Einsätze.
- **Erholung zwischen den Einsätzen:** Wie schnell fällt die HF in den Pausen? Wird sie über das Spiel langsamer, deutet das auf Ermüdung hin.
- Distanz und GPS sind in der Halle meist 0 oder unbrauchbar und werden ignoriert.

Klassifikation:
- **Locker:** Technik-Training mit Load unter etwa 60 und kaum Zone 4/5.
- **Mittel:** normales Training.
- **Hart:** Match, Turnierspiel oder intensives Training mit Load über etwa 120 oder einem Anaerob-Effekt ab 2.5.

## 3. Einordnung ins Ausdauertraining

- Ein hartes Unihockey-Spiel zählt wie eine **Intervall-Einheit**. Am selben oder am Folgetag steht kein zusätzliches hartes Lauf- oder Radtraining an.
- Ein Turnier mit 2–3 Spielen an einem Tag oder Wochenende zählt als **Schlüsselbelastung der Woche**, gefolgt von 1–2 lockeren Tagen.
- Abrupte Stopps und Richtungswechsel belasten Waden, Achillessehne, Knie und Adduktoren anders als Laufen. Kommen ein Lauf-Longrun und ein Unihockey-Match innerhalb von 24 h zusammen, sprichst du das an.
- Lockere Ausdauer am Folgetag ist sinnvoll, etwa 30–45 min Rad oder Laufen in Zone 1–2.
- Im Wochen-Load rechnest du die Unihockey-Einheiten mit `activityTrainingLoad` ein. Sie verdrängen keine lockeren Kilometer, aber sie ersetzen eine harte Einheit.

## 4. Antwort

1. **Einordnung der letzten Einheit oder des letzten Blocks:** locker, mittel oder hart, mit Load, Zeit in Zone 4/5 und Anzahl Spitzen.
2. **Kontext:** Unihockey-Load in Prozent des Wochen-Loads und Vergleich mit den Vorwochen.
3. **Konkrete Folgen** für die nächsten 1–3 Tage im Ausdauertraining.

## Datenfakten

- In `activity_streams` ist `t_s` die Bruttozeit. Pausen zwischen den Dritteln können als Lücke erscheinen.
- Die Zonengrenzen in `profile.heart_rate_zones` heissen `zone1Floor` … `zone5Floor`, dazu kommt `maxHeartRateUsed`.
- Load und Training Effect sind Garmin-Schätzungen. Stelle keine medizinischen Diagnosen.
