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

    def server_ready(self):
        """triggered after the server sent the MOTD (require core plugin)"""
        self.bot.loop.call_later(1, self.bot.get_messages)

    def connection_lost(self):
        """triggered when connection is lost"""
        pass

    def connection_made(self):
        """triggered when connection is up"""
        pass

    @irc3.event(irc3.rfc.PRIVMSG)
    def on_privmsg(self, mask=None, data=None, **kw):
        print("received privmsg from %s -> %s" % (mask.nick, data))
        # get django session using session_key from commandline
        try:
            session = Session.objects.get(session_key=self.bot.config.django_session_key)
        except Session.DoesNotExist:
            print("Session with session_key %s not found" % self.bot.config.django_session_key)
            return

        payload = {
            "sender": mask.nick,
            "message": data
        }
        Channel(self.bot.config.reply_channel).send({'text': json.dumps(payload)})
 
    @irc3.extend
    def get_messages(self):
        queuename = 'to-ircbot-%s' % self.bot.config.django_session_key
        channel, message = channel_layer.receive_many([queuename])
        if message and channel:
            self.bot.privmsg(message['text']['target'], message['text']['message'])
            self.bot.loop.call_later(1, self.bot.get_messages)
        else:
            self.bot.loop.call_later(5, self.bot.get_messages)

