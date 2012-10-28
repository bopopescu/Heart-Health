from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import get_connection, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.timezone import utc
from survey.models import Notification
import datetime

class Command(BaseCommand):

    def handle(self, *args, **options):
        sendNotificationEmails()

def sendNotificationEmails():
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    notifications = Notification.objects.filter(send_time__lte=now)

    connection = get_connection()
    
    messages = []
    for notification in notifications:
       if notification.user.is_active:
           ctx_dict = {'user': notification.user, 'notification': notification} 
           subject = "Reminder to complete your Heart Health Assessment"

           message_text = render_to_string('reminder_email.txt', ctx_dict)
           message_html = render_to_string('reminder_email.html', ctx_dict)

           msg = EmailMultiAlternatives(subject, message_text, settings.DEFAULT_FROM_EMAIL, [notification.user.email])
           msg.attach_alternative(message_html, "text/html")
           messages.append(msg)

    notifications.delete()
    return connection.send_messages(messages)
