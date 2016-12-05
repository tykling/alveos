import irc3, json
from alveos.asgi import channel_layer
from django.contrib.sessions.models import Session
from channels import Channel

@irc3.plugin
class Plugin(object):
    """Alveos IRC3 class"""

    requires = [
        'irc3.plugins.core',
        'irc3.plugins.userlist',
        'irc3.plugins.command',
        'irc3.plugins.human',
    ]

    def __init__(self, bot):
        self.bot = bot
        self.log = self.bot.log


    def server_ready(self, **kwargs):
        """triggered after the server sent the MOTD (require core plugin)"""
        print("inside server_ready")
        print(kwargs)
        self.bot.sysmsg_to_browser('Done connecting to IRC server!')
        self.bot.loop.call_later(1, self.bot.get_messages)


    def connection_lost(self, **kwargs):
        """triggered when connection is lost"""
        print("inside connection_lost")
        print(kwargs)
        self.bot.sysmsg_to_browser('Lost connection to IRC server!')


    def connection_made(self, **kwargs):
        """triggered when connection is up"""
        print("inside connection_made")
        print(kwargs)
        self.bot.sysmsg_to_browser('Connection to IRC server established...')


    @irc3.event(irc3.rfc.JOIN_PART_QUIT)
    def on_join_part_quit(self, **kwargs):
        print("inside on_join_part_quit()")
        print(kwargs)
        self.bot.ircmsg_to_browser(kwargs)


    @irc3.event(irc3.rfc.PRIVMSG)
    def on_privmsg(self, **kwargs):
        print("inside on_privmsg")
        print(kwargs)
        self.bot.ircmsg_to_browser(kwargs)


    @irc3.extend
    def get_messages(self):
        channel, message = channel_layer.receive_many(['to-ircbot-%s' % self.bot.config.django_session_key])
        if message and channel:
            print("got message from channel: %s" % message['text'])
            if message['text']['type'] == 'irc-message':
                self.bot.privmsg(message['text']['target'], message['text']['message'])
            elif message['text']['type'] == 'command':
                if message['text']['command'] == 'die':
                    self.bot.quit(reason=message['text']['reason'])
                else:
                    print("unsupported command received: %s" % message['text']['command'])
            else:
                print("message with unsupported type '%s' received, not processing" % message['text']['type'])

        # call this function again in 1 second
        self.bot.loop.call_later(1, self.bot.get_messages)


    @irc3.extend
    def sysmsg_to_browser(self, message):
        self.bot.send_to_browser({"alveos_version": "alveos-v1", "type": 'system_message', 'payload': {'message': message}})


    @irc3.extend
    def ircmsg_to_browser(self, message):
        self.bot.send_to_browser({"alveos_version": "alveos-v1", 'type': 'irc_message', 'payload': message})


    @irc3.extend
    def send_to_browser(self, payload):
        print("send to channel %s: %s" % (self.bot.config.reply_channel, payload))
        Channel(self.bot.config.reply_channel).send({'text': json.dumps(payload)})


    @irc3.extend
    def get_django_session(self):
        # get django session using session_key from commandline
        try:
            return Session.objects.get(session_key=self.bot.config.django_session_key)
        except Session.DoesNotExist:
            print("Session with session_key %s not found" % self.bot.config.django_session_key)
            return False


