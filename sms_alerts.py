from twilio.rest import Client
import json

CONFIG = json.load(open("config.json"))

client = Client(CONFIG["twilio_account_sid"], CONFIG["twilio_auth_token"])

def send_sms(message):
    client.messages.create(
        body=message,
        from_=CONFIG["twilio_phone_number"],
        to=CONFIG["your_phone_number"]
    )
