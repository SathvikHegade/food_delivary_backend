import os
import smtplib
from email.message import EmailMessage


def send_security_alert(user_email: str):
    msg=EmailMessage()

    msg["Subject"] ="Security Alert - Multiple Failed Login Attempts"
    msg["From"] =os.getenv("EMAIL_USERNAME")
    msg["To"] =user_email

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

    with smtplib.SMTP(
        os.getenv("EMAIL_HOST"),
        int(os.getenv("EMAIL_PORT"))
    ) as smtp:

        smtp.starttls()

        smtp.login(
            os.getenv("EMAIL_USERNAME"),
            os.getenv("EMAIL_PASSWORD")
        )

        smtp.send_message(msg)