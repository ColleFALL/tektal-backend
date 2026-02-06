import os
import requests


def send_brevo_email(to_email, subject, html_content):
    api_key = os.getenv("BREVO_API_KEY")
    sender = os.getenv("DEFAULT_FROM_EMAIL", "TEKTAL <no-reply@tektal.com>")

    if not api_key:
        raise RuntimeError("BREVO_API_KEY is not defined")

    # Parse "Name <email@domain>"
    sender_name = "TEKTAL"
    sender_email = "no-reply@tektal.com"
    if "<" in sender and ">" in sender:
        sender_name = sender.split("<")[0].strip()
        sender_email = sender.split("<")[1].split(">")[0].strip()

    payload = {
        "sender": {
            "name": sender_name,
            "email": sender_email,
        },
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
        timeout=20,
    )

    response.raise_for_status()
