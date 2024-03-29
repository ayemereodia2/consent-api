from django.core.mail import send_mail

class Utils:
    @staticmethod
    def send_email(data):
        subject = data['subject']
        body = data['email_body']
        recepient = data['recepient']
        send_mail(
                subject,
                body,
                'odiadavid2@gmail.com',
                [recepient],
                fail_silently=False,
            )