from django.core.management.base import BaseCommand, CommandError
from time import sleep
import irc3, sys, asyncio
from alveos.asgi import channel_layer
from django.contrib.sessions.models import Session

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('session_key', nargs=1, type=str)


    def handle(self, *args, **options):
        self.session_key = options['session_key'][0]

        # get django session using session_key from commandline
        try:
            session = Session.objects.get(session_key=self.session_key)
        except Session.DoesNotExist:
            print("Session with session_key %s not found" % self.session_key)
            sys.exit(1)

        # connect to IRC
        config = {
            'nick': session.get_decoded()['nickname'],
            'autojoins': ['#alveos'],
            'host': 'ircd.tyknet.dk',
            'port': 6697,
            'ssl': True,
            'timeout': 30,
            'includes': [
                'irc3.plugins.core',
                'irc3.plugins.human',
                'alveos.irc',
            ],
            'django_session_key': self.session_key,
            'reply_channel': session.get_decoded()['reply_channel'],
        }
        irc3.IrcBot(**config).run(forever=True)

