# -*- coding: utf-8 -*-

import irc3
from irc3.plugins.command import command


@irc3.plugin
class ArachnoBot:
    def __init__(self, bot):
        self.bot = bot

    @irc3.event(irc3.rfc.JOIN)
    def say_hi(self, mask, channel, **kw):
        """Say hi when someone join a channel"""
        if mask.nick != self.bot.nick:
            self.bot.privmsg(channel, 'Hi %s!' % mask.nick)
        else:
            self.bot.privmsg(channel, 'Hi!')

    @command(permission='view')
    def echo(self, mask, target, args):
        """Echo

            %%echo <message>...
        """
        yield ' '.join(args['<message>'])


def main():
    # instanciate a bot
    bot = irc3.IrcBot.from_argv(argv=("config.ini",))
    bot.include([
        'irc3.plugins.core',
        'irc3.plugins.command',
        'irc3.plugins.human',
        'irc3.plugins.userlist',
        'ArachnoBot']
    )
    # bot = irc3.IrcBot.from_config(config)
    bot.run(forever=True)


if __name__ == '__main__':
    main()
