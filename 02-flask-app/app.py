import boto3
import csv
from flask import Flask, render_template, request
from comprehend import *

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
SESSION = boto3.Session(profile_name='saml')
COMP_CLIENT = SESSION.client('comprehend')
COMP_DETECT = ComprehendDetect(COMP_CLIENT)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = "" 

    if request.method == 'POST':
        message = request.form['message']

        # Detect PII using AWS Comprehend
        response = {"Entities":  
                COMP_DETECT.detect_pii(text=message, language_code='en')
                }
        # Dummy response 
        # response = {"Entities": [{"BeginOffset": 0, "EndOffset": 3}] }

        pii_entities = response['Entities']
        pii_detected = len(pii_entities) > 0

        if pii_detected:
            # Redact PII if detected
            redacted_message = redact_pii(message, pii_entities)
            return render_template('index.html', message=message, redacted_message=redacted_message)
        else:
            # No PII detected
            return render_template('index.html', message=message, redacted_message=None)

    return render_template('index.html', message=message, redacted_message=None)

def save_to_csv(message):
    with open('messages.csv', 'a', newline='') as _f:
        writer = csv.writer(_f)
        writer.writerow([message])

@app.route('/submit', methods=['POST'])
def submit():
    confirmed_message = request.form['message']

    # Perform further processing or submission logic here
    save_to_csv(confirmed_message)

    success_message = "Message submitted successfully!"
    return render_template('index.html', success_message=success_message)

def redact_pii(message, pii_entities):
    for entity in pii_entities:
        start = entity['BeginOffset']
        end = entity['EndOffset']
        message = message[:start] + '*' * (end - start) + message[end:]
    return message

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)

