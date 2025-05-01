import os
import requests
from datetime import datetime
from src.logger import log
from src.cache_instance import cache  # Shared cache instance

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = "andrew@moonwire.app"

def send_email(to_email, subject, content):
    print(f"Preparing to send email to {to_email} with subject '{subject}'")

    url = "https://api.sendgrid.com/v3/mail/send"
    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
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

    print("Sending POST request to SendGrid...")
    response = requests.post(url, headers=headers, json=data)

    print(f"SendGrid response status: {response.status_code}")
    print(f"SendGrid response body: {response.text}")

    return response

def dispatch_alerts():
    assets = ['BTC', 'ETH', 'SOL', 'TEST']
    email_list = ["andrew@moonwire.app"]

    for asset in assets:
        signals = cache.get_signal(f"{asset}_signals")
        if not signals:
            print(f"[Dispatch] No signals found for {asset}")
            continue

        print(f"[Dispatch] Found {len(signals)} signal(s) for {asset}")

        for signal in signals:
            if isinstance(signal, dict):
                msg = (
                    f"{signal['asset']} ALERT:\n"
                    f"Price moved {signal['movement']:.2f}%\n"
                    f"Volume: ${signal['volume']:,.0f}\n"
                    f"Time: {signal['time'].strftime('%Y-%m-%d %H:%M:%S')} UTC"
                )
            else:
                msg = str(signal)

            print(f"[ALERT] {msg}")
            for email in email_list:
                print(f"Preparing to send email to {email}")
                response = send_email(email, f"MoonWire Alert: {asset}", msg)
                print(f"SendGrid response status: {response.status_code}")
                print(f"SendGrid response body: {response.text}")

        cache.delete_signal(f"{asset}_signals")
