import os
import requests

def send_brevo_email(to_email, subject, html_content):
    api_key = os.getenv("BREVO_API_KEY")

    payload = {
        "sender": {"name": "TEKTAL", "email": "no-reply@tektal.com"},
        "to": [{"email": to_email}],
        "subject": subject,
        "htmlContent": html_content,
    }

    response = requests.post(
        "https://api.brevo.com/v3/smtp/email",
        headers={
            "api-key": api_key,
            "content-type": "application/json",
        },
        json=payload,
    )

    response.raise_for_status()
