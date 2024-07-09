# Currency Conversion System

## Installationsanleitung für das Currency Conversion System

Dieses Dokument beschreibt die Schritte zur Installation und Konfiguration des Currency Conversion Systems auf AWS-Servern unter Verwendung von Linux und Windows.

## Linux Installation

Für die Installation unter Linux sind zwei AWS-Server erforderlich. Einer fungiert als Webserver mit Nginx, und der andere als Skript-Server.

### Schritte:

1. **AWS-Server einrichten:**
   - Richten Sie zwei EC2-Instanzen ein. Eine für Nginx und die andere für das Skript.

2. **Nginx Server konfigurieren:**
   - Installieren Sie Nginx auf einer der EC2-Instanzen.
   - Öffnen Sie die Firewall für Port 80, um Zugriff vom Web zu ermöglichen.

3. **Skript-Server konfigurieren:**
   - Klonen Sie das Repository auf die zweite EC2-Instanz.
   - Importieren Sie das `.pem` Schlüsseldatei in das Verzeichnis `.ssh` des Skript-Servers.
   - Stellen Sie sicher, dass die Datei `run_currency_script.sh` ausführbar ist:
     ```bash
     chmod +x run_currency_script.sh
     ```
   - Führen Sie das Skript aus mit:
     ```bash
     bash run_currency_script.sh
     ```

## Windows Installation

Für die Installation unter Windows ist ein AWS-Server erforderlich.

### Schritte:

1. **AWS-Server einrichten:**
   - Richten Sie eine EC2-Instanz ein.

2. **Nginx installieren:**
   - Installieren Sie Nginx auf der EC2-Instanz.

3. **Firewall-Konfiguration:**
   - Öffnen Sie die Firewall für Port 80 auf AWS, um Zugriff vom Web zu ermöglichen.

4. **Konfiguration der Sicherheitseinstellungen:**
   - Importieren Sie die `.pem` Schlüsseldatei unter `C:\Users\username\.ssh`.

5. **Skript ausführen:**
   - Führen Sie das Skript `currency.py` aus:
     ```bash
     python currency.py
     ```

## Zusätzliche Hinweise

- Stellen Sie sicher, dass alle nötigen Abhängigkeiten auf beiden Servern installiert sind, bevor Sie die Skripte ausführen.
- Überprüfen Sie die Netzwerkeinstellungen und Sicherheitsgruppen in AWS, um den Zugriff auf die notwendigen Ports sicherzustellen.
- Passen Sie Pfade und Benutzernamen an Ihre spezifische Serverkonfiguration und Ihre AWS-Instanz an.
