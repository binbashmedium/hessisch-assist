# Frankfurt Assist

Frankfurt Assist ist ein Home Assistant Custom Component, der einen eigenen Conversation Provider bereitstellt und Antworten in den Frankfurter Dialekt überträgt. Der Provider lässt sich über HACS installieren und in Assist-Pipelines auswählen.

## Installation über HACS
1. Öffne **HACS → Integrations** in Home Assistant.
2. Wähle **Custom repositories** und füge dieses Repository mit dem Typ **Integration** hinzu.
3. Suche nach **Frankfurt Assist** in HACS und installiere die Integration.
4. Starte Home Assistant neu, damit der Conversation Provider registriert wird.

## Aktivierung als Conversation Provider
1. Öffne **Einstellungen → Sprachassistent → Pipelines**.
2. Bearbeite eine Pipeline oder lege eine neue an.
3. Wähle unter **Conversation Provider** den Eintrag **Frankfurt Assist** aus.
4. Speichere die Pipeline. Alle Antworten werden nun in den Frankfurter Dialekt übertragen.

## Beispiele für Dialektantworten
- „Das Licht ist eingeschaltet, gell?“
- „Die Kaffeemaschine laaft jetzt, hoste?“
- „Temperatur is bei 22 Grad, mei Guddzje.“

## Hinweise
- Die Integration nutzt den eingebauten Conversation-Service und verändert ausschließlich die Formulierung der Antworten.
- Der Dialekt ist eine stilisierte Annäherung und experimentell. Ergebnisse können variieren.
