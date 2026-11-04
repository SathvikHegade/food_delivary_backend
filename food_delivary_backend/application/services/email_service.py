import os
import smtplib
from email.message import EmailMessage


def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def send_security_alert(user_email: str) -> None:
    username = required_env("EMAIL_USERNAME")
    password = required_env("EMAIL_PASSWORD")
    host = required_env("EMAIL_HOST")
    port = int(required_env("EMAIL_PORT"))

    msg = EmailMessage()
    msg["Subject"] = "Security Alert - Multiple Failed Login Attempts"
    msg["From"] = username
    msg["To"] = user_email

    msg.set_content(
        """
        We detected multiple failed login attempts on your account.

        If this was you, you can ignore this email.

        If this was not you, we recommend changing your password
        and securing your account.

        Regards,
        Food Delivery Team
        """
    )

    with smtplib.SMTP(host, port) as smtp:
        smtp.starttls()
        smtp.login(username, password)
        smtp.send_message(msg)