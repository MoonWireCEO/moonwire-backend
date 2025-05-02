
import os
import requests
from datetime import datetime
from src.logger import log
from src.cache_instance import cache

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = "andrew@moonwire.app"

def send_email(to_email, subject, content):
    print(f"Preparing to send email to {to_email} with subject '{subject}'")

    url = "https://api.sendgrid.com/v3/mail/send"
    headers = {
        "Authorization": f"Bearer " + SENDGRID_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "personalizations": [{
            "to": [{"email": to_email}],
            "subject": subject
        }],
        "from": {"email": FROM_EMAIL},
        "content": [{
            "type": "text/plain",
            "value": content
        }]
    }

    response = requests.post(url, headers=headers, json=data)
    print(f"SendGrid response status: {response.status_code}")
    print(f"SendGrid response body: {response.text}")
    return response

def label_confidence(score):
    if score >= 0.75:
        return "High Confidence"
    elif score >= 0.4:
        return "Medium Confidence"
    else:
        return "Low Confidence"

def dispatch_alerts():
    assets = ['BTC', 'ETH', 'SOL', 'TEST']
    email_list = ["andrew@moonwire.app"]

    for asset in assets:
        signals = cache.get_signal(f"{asset}_signals")
        if not signals:
            print(f"[Dispatch] No signals found for {asset}")
            continue

        for signal in signals:
            if isinstance(signal, dict):
                sentiment = cache.get_signal(f"{asset}_sentiment") or 0.0
                price_score = signal['movement'] / 10
                confidence = round((price_score + sentiment) / 2, 2)
                rank = label_confidence(confidence)

                msg = (
                    f"{signal['asset']} ALERT:\n"
                    f"Price moved {signal['movement']:.2f}%\n"
                    f"Volume: ${signal['volume']:,.0f}\n"
                    f"Sentiment Score: {sentiment:+.2f}\n"
                    f"Confidence Score: {confidence:.2f} ({rank})\n"
                    f"Time: {signal['time'].strftime('%Y-%m-%d %H:%M:%S')} UTC"
                )

                subject = f"MoonWire Alert: {asset} ({rank})"
            else:
                msg = str(signal)
                subject = f"MoonWire Alert: {asset}"

            log(f"[ALERT] {msg}")
            for email in email_list:
                send_email(email, subject, msg)

        cache.delete_signal(f"{asset}_signals")
