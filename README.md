# Hessisch Assist

Hessisch Assist ist ein Home Assistant Custom Component, das einen eigenen Conversation Provider bereitstellt und Antworten in hessischen Dialekt übersetzt. Die Integration ist über HACS installierbar und erscheint direkt als auswählbarer Provider in Assist-Pipelines.

## Installation über HACS
1. Öffne **HACS → Integrations** in Home Assistant.
2. Wähle **Custom repositories** und füge `https://github.com/binbashmedium/hessisch-assist` als Repository vom Typ **Integration** hinzu.
3. Suche nach **Hessisch Assist** in HACS und installiere die Integration.
4. Starte Home Assistant neu, damit der Conversation Provider registriert wird.

## Aktivierung im Assist-System
1. Öffne **Einstellungen → Sprachassistent → Pipelines**.
2. Bearbeite eine bestehende Pipeline oder lege eine neue an.
3. Wähle unter **Conversation Provider** den Eintrag **Hessisch Assist** aus.
4. Speichere die Pipeline. Alle Antworten des Assistants werden nun automatisch ins Hessische übertragen.

> Hinweis: Es ist **keine** Konfiguration in `configuration.yaml` nötig. Die Integration arbeitet ausschließlich über die Conversation-Provider-Schnittstelle und lädt keine weiteren Plattformmodule.

## Beispiele hessischer Antworten
- „Das Licht is ferdisch an, gell, mei guddzje.“
- „Die Heizung laaft, ei jo, hoschd, odder.“
- „Temperatur is bei 22 Grad, aaldä, gell.“

## Hinweise
- Die Integration nutzt den eingebauten `conversation.process`-Service und ändert ausschließlich die Formulierung der Antworten.
- Der Dialekt ist eine stilisierte Annäherung und experimentell; Ergebnisse können variieren.
- Mindestversion Home Assistant: 2024.6.0.
