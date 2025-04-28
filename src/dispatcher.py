from src.logger import log

# src/dispatcher.py (for now, near top)

import os
import requests

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = "andrew@moonwire.app"  # Replace with your verified sender email

def send_email(to_email, subject, content):
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
    response = requests.post(url, headers=headers, json=data)
    print(f"Email status: {response.status_code}")
    return response
    
def dispatch_alerts(cache):
    # === TEMP: Inject fake sleeper signal for email testing ===
    cache.set_signal("TESTCOIN_signals", ["TESTCOIN surged +42% in last 1h"])
    # ===========================================================
    assets = ['BTC', 'ETH', 'SOL']  # or however many you are scanning
    email_list = ["andrew@moonwire.app"]  # <-- Replace with your real email address for now

    for asset in assets:
        signals = cache.get_signal(f"{asset}_signals")
        if signals:
            for signal in signals:
                log(f"[ALERT] {signal}")
                # Send signal to all registered emails
                for email in email_list:
                    send_email(email, f"MoonWire Alert: {asset}", signal)
            cache.delete_signal(f"{asset}_signals")

