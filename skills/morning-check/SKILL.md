---
name: morning-check
description: Kurzer Tagesform-Check am Morgen aus HRV, Schlaf, Ruhepuls, Body Battery und der Belastung der Vortage, mit einer klaren Empfehlung für das heutige Training (hart, locker oder Pause). Verwenden bei "Morgen-Check", "wie fit bin ich heute", "soll ich heute hart trainieren", "Tagesform" oder "Readiness".
---

# Morgen-Check

Ziel ist eine Antwort in 30 Sekunden: eine Ampel, die Begründung und eine konkrete Empfehlung für heute. Lieber knapp als vollständig.

## 1. Daten holen

Alle drei Abfragen gehen über 14 Tage und laufen parallel:
- `hrv_summaries`, wovon der heutige Eintrag die letzte Nacht abbildet.
- `sleep_summaries`, wovon der heutige Eintrag die letzte Nacht abbildet.
- `daily_summaries` für Ruhepuls und Body Battery, von gestern und heute.

Dazu kommt `list_activities` über die letzten 3 Tage. Liegen für heute noch keine Werte vor, weil die Uhr noch nicht synchronisiert ist, sagst du das und arbeitest mit den letzten verfügbaren Werten.

## 2. Bewerten

Jedes Signal ordnest du grün, gelb oder rot ein.

| Signal | Grün | Gelb | Rot |
|---|---|---|---|
| HRV `lastNightAvg` | innerhalb `balancedLow`–`balancedUpper` | unter `balancedLow` oder `status` `UNBALANCED` | unter `baseline.lowUpper` oder `status` `LOW` / `POOR` |
| Ruhepuls `heartRate.restingValue` | ≤ 14-Tage-Schnitt +2 | +3 bis +5 | > +5 |
| Schlaf | Score ≥ 75 und Dauer ≥ `sleepNeed.actual` − 30 min | Score 60–74 oder 30–90 min zu kurz | Score < 60 oder > 90 min zu kurz |
| Body Battery (Höchstwert der Nacht bzw. heute) | ≥ 70 | 40–69 | < 40 |
| Load der letzten 2 Tage | normal | eine harte Einheit gestern (`SPEED`, `VO2MAX`, `ANAEROBIC_CAPACITY`, `LACTATE_THRESHOLD`, Unihockey-Match) | mehrere harte Einheiten oder ein Wettkampf in 48 h |

**Gesamturteil:**
- Grün, wenn kein Signal rot ist und höchstens eines gelb.
- Rot, wenn zwei Signale rot sind oder HRV und Ruhepuls zugleich auffällig sind.
- In allen anderen Fällen gelb.

Ein einzelner Ausreisser ist kein Alarm. Ein Muster über 2–3 Tage zählt mehr. Das Urteil ist eine Entscheidungshilfe und ersetzt nicht das eigene Körpergefühl. Krankheitszeichen wie Halsweh oder Fieber gehen immer vor: dann kein Training.

## 3. Antwort

Antworte in diesem Format und höchstens 6 Zeilen:

```
🟢/🟡/🔴 **<Urteil>** – <ein Satz warum>
HRV <Wert> (Baseline <von–bis>) · Ruhepuls <Wert> (<±x> zum Schnitt) · Schlaf <h:mm>, Score <x> · Body Battery <x>
**Heute:** <konkrete Empfehlung, z.B. "Intervalle wie geplant", "nur 40–50 min locker in Zone 2", "Ruhetag oder Mobility">
```

Ist bekannt, was heute geplant ist, etwa aus dem Chat oder einem Trainingsplan, beziehst du die Empfehlung darauf. Steht in den nächsten Tagen ein Rennen an, gewichtest du Erholung stärker.

## Datenfakten

- In `hrv_summaries` sind die Baseline-Werte `baseline.lowUpper`, `balancedLow` und `balancedUpper`. `status` nimmt zum Beispiel `BALANCED`, `UNBALANCED` oder `LOW` an.
- In `sleep_summaries` ist `sleepNeed.actual` in Minuten angegeben, `sleepTimeSeconds` in Sekunden.
- Das Datum eines Schlaf- oder HRV-Eintrags ist der Tag des Aufwachens.
- Unihockey wird meist als `field_hockey` erfasst.
- Body Battery, HRV-Status und Training Effect sind Garmin-Schätzungen. Stelle keine medizinischen Diagnosen.
