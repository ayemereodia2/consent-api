
import time
import threading
import schedule
from .models import Consent
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.db.models import F
from schedule import Scheduler

from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import Consent
import time

class Daemon:
    @staticmethod
    def send_email(data):
        print('sending that email...')
        subject = data['subject']
        body = data['email_body']
        recipient = data['recipient']
        send_mail(
            subject,
            body,
            'odiadavid2@gmail.com',
            [recipient],
            fail_silently=False,
        )

    def send_email_to_admin(self, client_name):
        print(f"Email sent to admin for client consent expiry.")
        data = {
            "subject": "Consent Expiry",
            "email_body": f"{client_name} consent document expires in 3 days, please send a reminder.",
            "recipient": "davidodia4@gmail.com"
        }
        self.send_email(data)

    @staticmethod
    def check_consents():
        while True:
            now = timezone.now()
            print('running daemon')
            # Calculate the date 1 minute ago
            one_minute_ago = now - timedelta(minutes=1)

            # Query all consents
            consents = Consent.objects.all()

            print(len(consents))
            # Process each consent
            for consent in consents:
                Daemon().send_email_to_admin(consent.client_name)

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



def background_job():
    print('Hello from the background thread')
    Daemon.check_consents()
    



def run_continuously(interval=1):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


schedule.every().second.do(background_job)

# Start the background thread
stop_run_continuously = run_continuously()

# Do some other things...
#time.sleep(10)

# Stop the background thread
stop_run_continuously.set()


def start_scheduler():
    pass
    #scheduler = Scheduler()
    #scheduler.every().second.do(background_job)
    #scheduler.run_continuously()