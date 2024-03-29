# start_daemon.py
import os
import django
from deamon import Daemon

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "consent.settings")
    django.setup()
    Daemon.start_daemon()

if __name__ == "__main__":
    main()
