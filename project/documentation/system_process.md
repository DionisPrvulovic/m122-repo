# Systemprozess-Dokumentation

## Überblick
Diese Dokumentation beschreibt den Ablauf des Währungsumrechnungssystems, das darauf ausgelegt ist, Währungsdaten automatisch zu erfassen, diese Daten in einer Tabelle zu visualisieren und optional per E-Mail zu versenden.

## Ablauf des Systems

### 1. Konfigurationsdatei (`currency.cfg`)
Die Konfigurationsdatei enthält wichtige Einstellungen wie API-Schlüssel, SSH-Zugangsdaten, und E-Mail-Konfigurationen. Diese Einstellungen steuern, wie das System mit externen Diensten interagiert und wie Daten verarbeitet und gespeichert werden.

### 2. Datenabruf
Das System verwendet die API-Einstellungen aus der Konfigurationsdatei, um aktuelle Währungsdaten über HTTP-Anfragen abzurufen.

### 3. Datenverarbeitung
Nach dem Abruf werden die Währungsdaten verarbeitet und in eine für die Visualisierung geeignete Form umgewandelt. Dazu gehört das Generieren einer Tabelle, die die Währungskurse darstellt.

### 4. Tabellenerstellung
Die verarbeiteten Daten werden in einer Tabelle visualisiert, welche die Wechselkurse in einer übersichtlichen Form zeigt. Diese Tabelle wird dann als Bild gespeichert, wenn dies in den Einstellungen festgelegt wurde.

### 5. Optionale E-Mail-Versendung
Wenn in der Konfiguration aktiviert, wird die erstellte Tabelle als Anhang einer E-Mail verschickt. Dies geschieht mittels Integration eines E-Mail-Dienstes, der in der `currency.cfg` konfiguriert ist.

### 6. Logging
Während des gesamten Prozesses werden wichtige Ereignisse und mögliche Fehler in einer Log-Datei festgehalten, um die Nachverfolgbarkeit zu gewährleisten und Support bei Problemen zu erleichtern.

### 7. Aufräumprozesse
Nach der Ausführung der Hauptaufgaben führt das System Aufräumarbeiten durch, wie das Löschen temporärer Dateien, sofern dies in den Einstellungen spezifiziert ist.

## Abschluss
Das System ist darauf ausgelegt, den Umgang mit Währungsdaten zu automatisieren und die Datenverbreitung zu vereinfachen. Es reduziert manuelle Aufgaben und stellt sicher, dass die Daten aktuell und leicht zugänglich sind.
