
import time
from models import Consent
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail


class Daemon :
    @staticmethod
    def check_consents():
        while True:
            now = timezone.now()
            print('running daemon')
            # Calculate the date 1 minute ago
            one_minute_ago = now - timedelta(minutes=1)

            # Query all consents that were signed between three days before one year ago and one year ago
            consents = Consent.objects.filter(
                date_of_signature__range=[one_minute_ago, one_minute_ago]
            )

            
            # Process each consent
            for consent in consents:
                send_email_to_admin(consent.client_name)
                print(f"Email sent to admin for client consent expiry.")

            # Delay for 1 minute before checking again (for demo purposes)
            time.sleep(60)  # 1 minute in seconds
            
    def get_consent_with_3day_to_expiry_from_database(self):
        # Calculate the date 1 year ago
        one_year_ago = timezone.now() - timedelta(days=365)

        # Calculate the date 3 days from one year ago
        three_days_before_one_year_ago = one_year_ago - timedelta(days=3)

        # Query all consents that were signed between three days before one year ago and one year ago
        return Consent.objects.filter(
            date_of_signature__range=[three_days_before_one_year_ago, one_year_ago]
        )
        
    @staticmethod
    def start_daemon():
        Daemon.check_consents()
    
    def send_email_to_admin(client_name):
        data = {
            "subject":"Consent Expiry",
            "email_body":f"{client_name} consent document expires in 3 days, please send a reminder.",
            "recepient":"davidodia4@gmail.com"
        }
        Daemon.send_email(data)
        
    
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
    
    
    
# # Get today's date
            # today = datetime.now().date()
            
            # # Calculate the date 1 year ago
            # one_year_ago = timezone.now() - timedelta(days=365)

            # # Calculate the date 3 days from one year ago
            # three_days_before_one_year_ago = one_year_ago - timedelta(days=3)


# # Process each consent
            # for consent in consents:
            #     birthday_date = consent.date_of_signature.date() + timedelta(days=365)
            #     if birthday_date.month == today.month and birthday_date.day == today.day:
            #         send_email(consent.client_name)
            #         print(f"Email sent to {consent.client_name} for their 1-year consent anniversary.")
            