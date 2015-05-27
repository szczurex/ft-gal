from smtplib import SMTPException
from traceback import print_exc
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from ft.local_settings import DEFAULT_FROM_EMAIL
from msg.models import TaskedMail

class Command(BaseCommand):
    help = 'Sends out all tasked emails'

    # TODO: PIECE OF SHIT MANDRILL DOES NOT WORK,
    # FIND OUT WHY.

    def handle(self, *args, **options):

        tasked_mails = TaskedMail.objects.all()#.filter(success=False)
        for t in tasked_mails:
            try:
                # print(t.subject)
                # print(t.message)
                # print(t.destination)
                send_mail(
                    subject=t.subject,
                    message=t.message,
                    recipient_list=[t.destination],
                    from_email=DEFAULT_FROM_EMAIL
                )
                t.success = True
                t.save()
                self.stdout.write("Successfully sent email to '{0}' ".format(t.destination))
            except SMTPException:
                print_exc()
                # TODO: log the exception.
                self.stdout.write("Failed to deliver to '{0}' ".format(t.destination))