# Currency Conversion System

## Konfigurationsdatei

Die Konfigurationsdatei (`currency.cfg`) wird verwendet, um das Verhalten des Währungsskripts einzurichten und anzupassen. Jede Sektion in dieser Datei enthält spezifische Einstellungen, die den API-Zugriff, SSH-Verbindungen, Optionen für das Speichern von Dateien, Logging, Datenformatierung und Pfade für die Dateispeicherung und -übertragung steuern.

### Konfigurationsoptionen

#### [API]

- `API_KEY`: Dein API-Schlüssel für den Zugriff auf die Währungsdaten-API.
- `API_URL`: Die URL für die Währungsdaten-API, inklusive API-Schlüssel und den abzurufenden Währungen.

#### [SSH]

- `SSH_HOST`: Die SSH-Hostadresse für den Remote-Server.
- `SSH_USER`: Der SSH-Benutzername für den Remote-Server.
- `SSH_KEY_PATH`: Der vollständige Pfad zur SSH-Schlüsseldatei für die Authentifizierung.

#### [OPTIONS]

- `DUMPING_TABLE_IMAGE`: 
  - `true`: Behalte die Tabellenbilddatei.
  - `false`: Löscht die Tabellenbilddatei beim nächsten Ausführen.

- `DUMPING_JSON_FILE`: 
  - `true`: Behalte die JSON-Datei.
  - `false`: Löscht die JSON-Datei beim nächsten Ausführen.

- `CURRENCY_LOG`: 
  - `true`: Schreibt detaillierte Logs in die Logdatei.
  - `false`: Löscht die Logdatei beim nächsten Ausführen.

- `CHF_COMMAS`: 
  - `true`: Formatiert CHF-Werte mit 2 Dezimalstellen (z.B. `100.00`).
  - `false`: Formatiert CHF-Werte ohne Dezimalstellen (z.B. `100`).

- `DECIMAL_PLACE`: Die Anzahl der Dezimalstellen für berechnete Werte in der Tabelle (z.B. `2` für `0.00`).

- `VALUES`: Eine durch Kommas getrennte Liste von Werten, die in der Tabelle berechnet und angezeigt werden (z.B. `1,5,10,25,50,100,500,1000,5000,10000`).

- `COLOR`: 
  - `random`: Verwendet zufällige Farben für die Tabelle.
  - Hexadezimaler Farbcode (z.B. `#FF0000`): Verwendet die angegebene Farbe für die Tabelle.

- `TRANSPARENCY`: Der Transparenzgrad der Tabellenzellen, von `0` (unsichtbar) bis `1` (vollständig sichtbar).

#### [PATHS]

- `REMOTE_PATH`: Der Pfad auf dem Remote-Server, wo die Tabellenbilddatei hochgeladen wird.

### Zweck der Konfigurationsdatei

Diese Konfigurationsdatei (`currency.cfg`) ermöglicht es dir, das Verhalten des Währungsskripts anzupassen. Sie enthält Einstellungen für:

- Den Zugriff auf die Währungsdaten-API.
- Die Verbindung zu einem Remote-Server via SSH.
- Die Konfiguration von Optionen für das Speichern von Tabellenbildern und JSON-Dateien.
- Das Aktivieren oder Deaktivieren von detaillierten Logs.
- Die Formatierung von Währungswerten und die Einstellung der Dezimalstellenanzahl.
- Die Spezifizierung der Farbe und Transparenz der Tabelle.
- Die Definition des Pfads zum Speichern und Hochladen der Tabellenbilddatei.

Durch das Anpassen dieser Einstellungen kannst du steuern, wie das Skript Währungsdaten abruft, verarbeitet und speichert, sowie wie es die resultierenden Informationen loggt und formatiert.
