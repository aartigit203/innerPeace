import requests, os

TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_ID = os.getenv("PHONE_NUMBER_ID")

def send_message(to, msg):
    requests.post(
        f"https://graph.facebook.com/v18.0/{PHONE_ID}/messages",
        headers={"Authorization": f"Bearer {TOKEN}"},
        json={"messaging_product":"whatsapp","to":to,"type":"text","text":{"body":msg}}
    )

def send_buttons(to, body, buttons):
    requests.post(
        f"https://graph.facebook.com/v18.0/{PHONE_ID}/messages",
        headers={"Authorization": f"Bearer {TOKEN}"},
        json={
            "messaging_product":"whatsapp",
            "to":to,
            "type":"interactive",
            "interactive":{
                "type":"button",
                "body":{"text":body},
                "action":{"buttons":buttons}
            }
        }
    )
