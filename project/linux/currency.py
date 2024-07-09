# =================================================
# Script Name: Currency Conversion System
# Description: Fetches currency data, generates a visual representation, and optionally sends it via email.
# Author: Dionis Prvulovic
# Date: 09.07.2024
# =================================================

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
from mailjet_rest import Client
import base64

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

# Mailjet configuration
MAILJET_API_KEY = config['MAILJET']['API_KEY']
MAILJET_API_SECRET = config['MAILJET']['API_SECRET']
SENDER_EMAIL = config['MAILJET']['SENDER_EMAIL']
RECIPIENT_EMAIL = config['MAILJET']['RECIPIENT_EMAIL']

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

# Paths
DUMP_PATH = os.path.join(os.path.dirname(__file__), 'dump')
LOCAL_PATH = os.path.join(DUMP_PATH, 'table.png')
JSON_PATH = os.path.join(DUMP_PATH, 'currency_data.json')
LOG_PATH = os.path.join(DUMP_PATH, 'currency.log')
REMOTE_PATH = config['PATHS']['REMOTE_PATH']

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
    response = requests.get(API_URL)
    data = response.json()
    log_message('info', 'Fetched currency data')
    return data

def format_large_numbers(number, decimal_places):
    return f"{number:,.{decimal_places}f}"

def get_color():
    if COLOR == 'random':
        return np.random.rand(3,)
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

def send_email(subject, text, attachment_path=None):
    mailjet = Client(auth=(MAILJET_API_KEY, MAILJET_API_SECRET), version='v3.1')
    data = {
        'Messages': [
            {
                "From": {
                    "Email": SENDER_EMAIL,
                    "Name": "Currency Converter"
                },
                "To": [
                    {
                        "Email": RECIPIENT_EMAIL,
                        "Name": "Recipient"
                    }
                ],
                "Subject": subject,
                "TextPart": text,
            }
        ]
    }
    if attachment_path:
        with open(attachment_path, "rb") as f:
            encoded_file = base64.b64encode(f.read()).decode('utf-8')
            data['Messages'][0]['Attachments'] = [
                {
                    "ContentType": "image/png",
                    "Filename": os.path.basename(attachment_path),
                    "Base64Content": encoded_file
                }
            ]
    
    result = mailjet.send.create(data=data)
    log_message('info', f"Email sent: {result.status_code} {result.json()}")

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
        elif os.path.exists(LOCAL_PATH):
            os.remove(LOCAL_PATH)
            log_message('info', 'Existing table image deleted')
        
        # Send email with table image if SEND_EMAIL is True
        if SEND_EMAIL:
            send_email("Currency Conversion Table", "Please find the attached currency conversion table.", LOCAL_PATH)

        log_message('info', 'Script completed successfully')
    except Exception as e:
        log_message('error', f"Error occurred: {e}")
        print(f"Fehler: {e}")

if __name__ == "__main__":
    main()
