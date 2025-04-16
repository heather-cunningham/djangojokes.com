import sendgrid
from sendgrid.helpers.mail import Mail
from django.conf import settings


def send_email(to, subject, content, sender="cunningham.heatherirene@gmail.com"): 
    ## Change the sender email to the one reg'd w/ Twilio-SendGrid (i.e., your gmail)
    ## to actually send any email   
    sender_client = sendgrid.SendGridAPIClient(settings.SENDGRID_API_KEY)
    mail = Mail(
        from_email=sender,
        to_emails=to,
        subject=subject,
        html_content=content
    )
    return sender_client.send(mail)
    