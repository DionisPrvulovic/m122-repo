import requests
import json
import matplotlib.pyplot as plt
import pandas as pd
import paramiko
from scp import SCPClient
import numpy as np
from matplotlib.colors import hsv_to_rgb, hex2color
import os
import configparser
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formataddr

# Load configuration
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'currency.cfg'))

# API configuration
API_KEY = config['API']['API_KEY']
API_URL = config['API']['API_URL'].format(API_KEY=API_KEY)

# SSH configuration
SSH_HOST = config['SSH']['SSH_HOST']
SSH_USER = config['SSH']['SSH_USER']
SSH_KEY_PATH = config['SSH']['SSH_KEY_PATH']

# Options configuration
DUMPING_TABLE_IMAGE = config.getboolean('OPTIONS', 'DUMPING_TABLE_IMAGE')
DUMPING_JSON_FILE = config.getboolean('OPTIONS', 'DUMPING_JSON_FILE')
CHF_COMMAS = config.getboolean('OPTIONS', 'CHF_COMMAS')
DECIMAL_PLACE = config.getint('OPTIONS', 'DECIMAL_PLACE')
VALUES = list(map(int, config['OPTIONS']['VALUES'].split(',')))
COLOR = config['OPTIONS']['COLOR']
TRANSPARENCY = config.getfloat('OPTIONS', 'TRANSPARENCY')
CURRENCY_LOG = config.getboolean('OPTIONS', 'CURRENCY_LOG')
SEND_EMAIL = config.getboolean('OPTIONS', 'SEND_EMAIL')

# Email configuration
SMTP_SERVER = config['EMAIL']['SMTP_SERVER']
SMTP_PORT = config['EMAIL']['SMTP_PORT']
SMTP_USER = config['EMAIL']['SMTP_USER']
SMTP_PASSWORD = config['EMAIL']['SMTP_PASSWORD']
TO_EMAIL = config['EMAIL']['TO_EMAIL']

# Paths
DUMP_PATH = os.path.join(os.path.dirname(__file__), 'dump')
LOCAL_PATH = os.path.join(DUMP_PATH, 'table.png')
JSON_PATH = os.path.join(DUMP_PATH, 'currency_data.json')
LOG_PATH = os.path.join(DUMP_PATH, 'currency.log')
REMOTE_PATH = config['PATHS']['REMOTE_PATH']  # Nginx Standardpfad

# Ensure dump directory exists
os.makedirs(DUMP_PATH, exist_ok=True)

# Set up logging
if CURRENCY_LOG:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s',
        handlers=[
            logging.FileHandler(LOG_PATH)
        ]
    )
    logger = logging.getLogger()
else:
    logger = None
    if os.path.exists(LOG_PATH):
        os.remove(LOG_PATH)

def log_message(level, message):
    if logger:
        getattr(logger, level)(message)

def fetch_currency_data():
    log_message('info', 'Fetching currency data from API')
    response = requests.get(API_URL)
    response.raise_for_status()
    log_message('info', 'Currency data fetched successfully')
    return response.json()

def format_large_numbers(value, decimal_places):
    formatted_value = f"{value:,.{decimal_places}f}"
    return formatted_value.replace(',', "'")

def get_color():
    if COLOR.lower() == "random":
        h = np.random.rand()
        s = 0.5 + 0.5 * np.random.rand()  # Saturation between 0.5 and 1
        v = 0.7 + 0.3 * np.random.rand()  # Brightness between 0.7 und 1
        return hsv_to_rgb((h, s, v))
    else:
        return hex2color(COLOR)

def generate_table(data):
    log_message('info', 'Generating table from currency data')
    rates = data['data']
    last_updated = data['meta']['last_updated_at']
    currency_pairs = VALUES
    table_data = {currency: [rates[currency]['value'] * int(pair) for pair in currency_pairs] for currency in rates}
    df = pd.DataFrame(table_data, index=[f"{pair} CHF" for pair in currency_pairs])

    # Apply number formatting to the values
    df = df.apply(lambda x: x.map(lambda x: round(x, DECIMAL_PLACE)).map(lambda x: format_large_numbers(x, DECIMAL_PLACE)))

    # Format the index without decimal places if CHF_COMMAS is False
    df.index = df.index.map(lambda x: format_large_numbers(float(x.split(' ')[0]), 2 if CHF_COMMAS else 0) + ' CHF')

    # Format the table
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.axis('tight')
    ax.axis('off')

    # Create a list of cells to be displayed, including the last updated timestamp
    cell_text = [[last_updated] + [f"{df.columns[col]}" for col in range(len(df.columns))]]
    cell_text += [[f"{df.index[row]}"] + [df.iloc[row, col] for col in range(len(df.columns))] for row in range(len(df.index))]

    table = ax.table(cellText=cell_text, cellLoc='center', loc='center')

    # Generate a random color or use specified color
    table_color = get_color()
    table_color_hex = "#{:02x}{:02x}{:02x}".format(int(table_color[0]*255), int(table_color[1]*255), int(table_color[2]*255))

    # Improve the appearance
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)

    for (i, j), cell in table.get_celld().items():
        cell.set_alpha(TRANSPARENCY)
        if i == 0 or j == 0:
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor(table_color_hex)
        else:
            cell.set_facecolor('#E6F2FF')

    plt.savefig(LOCAL_PATH, bbox_inches='tight', dpi=300)
    plt.close()
    log_message('info', 'Table image generated and saved')

def upload_to_server(local_file, remote_path):
    log_message('info', 'Uploading table image to server')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SSH_HOST, username=SSH_USER, key_filename=SSH_KEY_PATH)
    
    with SCPClient(ssh.get_transport()) as scp:
        scp.put(local_file, remote_path)
    ssh.close()
    log_message('info', 'Table image uploaded to server')

def send_email(subject, body, attachment_path):
    log_message('info', 'Sending email with table attachment')

    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with open(attachment_path, "rb") as attachment:
        part = MIMEApplication(attachment.read(), Name=os.path.basename(attachment_path))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
        msg.attach(part)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, TO_EMAIL, msg.as_string())
    
    log_message('info', 'Email sent successfully')

def main():
    try:
        log_message('info', 'Script started')
        data = fetch_currency_data()

        if DUMPING_JSON_FILE:
            with open(JSON_PATH, 'w') as f:
                json.dump(data, f, indent=4)
            log_message('info', 'JSON data dumped to file')
        elif os.path.exists(JSON_PATH):
            os.remove(JSON_PATH)
            log_message('info', 'Existing JSON file deleted')

        generate_table(data)
        print("Daten erfolgreich abgerufen, verarbeitet und Tabelle erstellt.")

        if DUMPING_TABLE_IMAGE:
            upload_to_server(LOCAL_PATH, REMOTE_PATH)
            print("Tabelle erfolgreich auf den Server hochgeladen.")

            if SEND_EMAIL:
                send_email("Aktuelle Wechselkurstabelle", "Anbei die aktuelle Wechselkurstabelle.", LOCAL_PATH)
                print("Email erfolgreich verschickt.")
        elif os.path.exists(LOCAL_PATH):
            os.remove(LOCAL_PATH)
            log_message('info', 'Existing table image deleted')
        log_message('info', 'Script completed successfully')
    except Exception as e:
        log_message('error', f"Error occurred: {e}")
        print(f"Fehler: {e}")

if __name__ == "__main__":
    main()
