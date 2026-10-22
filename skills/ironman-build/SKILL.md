---
name: ironman-build
description: Begleitet den Aufbau für eine Triathlon-Langdistanz (Ironman) oder Mitteldistanz (70.3) mit den Garmin-Daten. Dazu gehören die Verteilung von Schwimmen, Rad und Laufen, Wochenstunden, Langeinheiten, Koppeltrainings, 80/20-Intensität, Progression und Lücken zum Zielniveau. Verwenden bei "Ironman", "Triathlon-Training", "70.3", "Koppeltraining", "wie viel muss ich schwimmen/radeln" oder "bin ich auf Kurs für die Langdistanz".
---

# Ironman-Aufbau

Ziel ist ein ehrlicher Stand der Vorbereitung für eine Langdistanz (3,8 km Schwimmen, 180 km Rad, 42,2 km Laufen) oder Mitteldistanz (1,9 km, 90 km, 21,1 km) und eine Aussage dazu, was als Nächstes kommen sollte.

## 1. Rahmen klären

Folgendes muss bekannt sein. Fehlt etwas, fragst du kurz nach:
- Zielrennen und Datum, die Anzahl der Wochen bis dahin
- Erfahrung mit Triathlon
- Verfügbare Stunden pro Woche

Die Wochen bis zum Rennen teilst du grob in Phasen ein: Basis, Aufbau, Spezifisch, Taper (2–3 Wochen).

## 2. Daten holen

- `list_activities` ohne Typfilter über 12–16 Wochen, mit `limit` 100 und bei Bedarf paginiert.
- `profile` für die Zonen. Die Zonen dort sind meist sportübergreifend (`sport` `DEFAULT`). Für das Rad gilt typischerweise eine um 5–10 Schläge tiefere Schwelle, darauf weist du hin.

Gruppierung nach `activityType`:
- Schwimmen: `lap_swimming`, `open_water_swimming`
- Rad: `road_biking`, `cycling`, `indoor_cycling`, `virtual_ride`, `gravel_cycling`, `mountain_biking`
- Laufen: `running`, `trail_running`, `treadmill_running`
- Multisport: `multi_sport` (Rennen oder Koppeleinheiten)
- Ergänzung: `strength_training` und weitere

## 3. Auswerten

| Kennzahl | Berechnung | Richtwert (Langdistanz, Altersklasse) |
|---|---|---|
| Wochenstunden | Summe `duration_min` / 60 | Basis 7–10 h, Peak 12–16 h |
| Verteilung | Zeitanteil Swim / Bike / Run | etwa 15–20 % / 50–55 % / 25–30 % |
| Längste Ausfahrt | Maximum Rad-Dauer (4 Wochen) | Peak 5–6 h bzw. 150–180 km |
| Längster Lauf | Maximum Lauf-Dauer (4 Wochen) | Peak 2:30–3:00 h, nicht länger |
| Schwimmen | Einheiten pro Woche und längste Distanz | 2–3 Einheiten pro Woche, mindestens 3,8 km am Stück im Peak |
| Koppeltraining | Lauf, der innerhalb von 30 min nach einer Radeinheit beginnt (`startTimeLocal` + Dauer) | im Aufbau etwa 1 pro Woche |
| Intensität | Anteil `RECOVERY`/`AEROBIC_BASE` an der Zeit | etwa 80 % locker |
| Progression | Wochenstunden-Trend und Load-ACWR | +5–10 % pro Woche, Entlastungswoche alle 3–4 Wochen |

Die Richtwerte sind grobe Orientierung und kein Trainingsplan. Bei Mitteldistanz rechnest du mit etwa 60–70 % davon.

- **Schwimmen:** Pace pro 100 m = Dauer / (Distanz / 100). Für Schwimm-Details nimmst du `activity_details`, dort stehen Bahnen und Züge, falls vorhanden.
- **Rad:** Geschwindigkeit ist `averageSpeed` × 3,6 in km/h. Leistung wertest du nur aus, wenn `averagePower` oder `normPower` vorhanden sind.
- **Unihockey und andere Sportarten** zählen zum Load, verdrängen aber Triathlon-spezifische Zeit. Das sprichst du an, wenn ihr Anteil gross ist.

## 4. Lückenanalyse

Pro Disziplin vergleichst du den Ist-Stand mit dem Richtwert für die aktuelle Phase und kennzeichnest ihn mit „auf Kurs“, „knapp“ oder „Lücke“. Typische Lücken bei Läufern, die neu im Triathlon sind:
- zu wenig Rad-Volumen
- zu wenig Schwimm-Regelmässigkeit
- keine Koppeleinheiten
- zu harte lockere Einheiten

## 5. Antwort

1. **Stand:** Phase, Wochen bis zum Rennen und ein Satz zur Gesamteinschätzung.
2. **Tabelle** pro Disziplin mit Ist-Wert, Richtwert und Status.
3. **Grafik:** Wochenstunden gestapelt nach Disziplin über die letzten 12 Wochen.
4. **Nächste 2–4 Wochen:** 3–5 konkrete Schwerpunkte, zum Beispiel „Longride auf 3:30 h steigern“ oder „zweite Schwimmeinheit fix einplanen“.

## Datenfakten

- `list_activities` liefert `distance_km`, `duration_min`, `averageSpeed` (m/s), `averageHR`, `elevationGain`, `activityTrainingLoad` und `trainingEffectLabel`.
- In `activity_streams` ist `cadence` beim Laufen pro Bein angegeben (×2 ergibt Schritte pro Minute), beim Rad entspricht sie den Umdrehungen pro Minute.
- Load, Training Effect und VO2max sind Garmin-Schätzungen. Stelle keine medizinischen Diagnosen.
