#!python3
# -*- coding: utf-8 -*-
import random
import datetime
import requests
# import simplejson
# from requests_oauthlib import OAuth2Session
import streamlabs_api as api
from obswebsocket import requests as obsws_requests
from obswebsocket import obsws  # , requests, events

import irc3
from irc3.plugins.command import command
from irc3.testing import ini2config
from irc3.rfc import raw

from config import *
import codecs

USERSTATE = raw.new('USERSTATE',
               r'^(@(?P<tags>\S+) )?:(?P<mask>\S+) USERSTATE :?(?P<channel>\S+)')

@irc3.plugin
class ArachnoBot:
    def __init__(self, bot):
        self.bot = bot
        self.channel = '#iarspider'
        self.oauth = api.get_streamlabs_session(client_id, client_secret, redirect_uri)
        self.ws = obsws('192.168.1.199', 4444, 'spider')
        self.ws.connect()
        self.aud_sources = self.ws.call(obsws_requests.GetSpecialSources())
        self.plusches = 0
        self.write_plusch()
        self.mods = []
        self.subs = []
        self.viewers = []

    # @irc3.event(irc3.rfc.JOIN)
    # def say_hi(self, mask, channel, **kw):
    #     self.viewers.add(mask.nick)
    #     """Say hi when someone join a channel"""
    # if mask.nick == self.bot.nick:
    #    self.bot.privmsg(channel, 'Hi %s!' % mask.nick)
    # else:
    #    self.bot.privmsg(channel, u'Арахнобот прибыл и готов к работе!')

    @irc3.event(USERSTATE)
    def userstate(self, tags, mask, channel):
        tags_list = tags.split(';')
        tags_dict = {}
        for tag in tags_list:
            key, val = tag.split('=')
            tags_dict[key] = val
            
        if int(tags_dict['mod']) == 1:
            self.mods.append(tags_dict


    # @command(permission='view')
    # def echo(self, mask, target, args):
    # """Echo

    # %%echo <message>...
    # """
    # yield ' '.join(args['<message>'])

    # noinspection PyUnusedLocal
    @command(permission='view')
    def dice(self, mask, target, args):
        """Roll some dice

            %% dice <foo> ...
        """
        dices = []

        if args is None or len(args) == 0:
            dices = (6,)
        else:
            for arg in args['<foo>']:
                print("arg is", arg)
                if 'd' not in arg:
                    continue
                num, sides = arg.split('d')
                try:
                    if not num:
                        num = 1
                    else:
                        num = int(num)
                    sides = int(sides)
                except ValueError:
                    continue

                if not ((0 < num <= 10) and (4 <= sides <= 100)):
                    continue

                print("Rolling {0} {1}-sided dice(s)".format(num, sides))

                rolls = [random.randint(1, sides) for _ in range(num)]
                roll_sum = sum(rolls)
                print("You rolled:", ";".join(str(x) for x in rolls), "sum is", roll_sum)

                dices.append(roll_sum)

        yield "You rolled: {}".format(", ".join(str(x) for x in dices))

    # noinspection PyUnusedLocal
    @command(permission='view')
    def attack(self, mask, target, args):
        """Attack another (online) viewer

            %% attack <player>
        """

        attacker = mask.nick
        defender = args["<player>"]
        # if defender not in list(self.bot.channels[self.channel]):
        #     self.bot.privmsg(self.channel, u"> {1}, {0} сейчас не в сети!".format(attacker, defender))
        #     return

        if defender == attacker:
            self.bot.privmsg(self.channel, "РКН на вас нет, негодяи!")
            return

        if defender.lower() == "arachnobot" or defender.lower() == "nightbot":
            self.bot.privmsg(self.channel, "Ботика не трожь!")
            return

        self.bot.privmsg(self.channel, "Пусть начнётся битва: {0} против {1}!".format(attacker, defender))

        attack_d = random.randint(1, 6)
        defence_d = random.randint(1, 6)

        # result.append("@{0} ds {1}, @{2} rolls {3}".format(sender, attack_d, args["<player>"], defence_d))

        if attack_d > defence_d:
            self.bot.privmsg(self.channel,
                             "@{0} побеждает с результатом {1}:{2}!".format(attacker, attack_d, defence_d))
        elif attack_d < defence_d:
            self.bot.privmsg(self.channel,
                             "@{0} побеждает с результатом {2}:{1}!".format(defender, attack_d, defence_d))
        else:
            self.bot.privmsg(self.channel, "Бой закончился вничью!")

    # noinspection PyUnusedLocal
    @command(permission='view', aliases=("кусь",))
    # @command(permission='special')
    def bite(self, mask, target, args):
        """
            выясни сам
            %% bite <player>
        """
        if not 'bite' in self.bot.db:
            self.bot.db['bite'] = {}

        now = datetime.datetime.now()

        attacker = mask.nick
        defender = args["<player>"].lstrip('@')
        try:
            last_bite = self.bot.db['bite'][attacker]
        except KeyError:
            last_bite = 31525200.0  # some arbitrary time

        last_bite = datetime.datetime.fromtimestamp(last_bite)
        if (now - last_bite).seconds < 90 and attacker != 'iarspider':
            self.bot.privmsg(self.channel, "Не кусай так часто, @{0}! Дай моим челюстям отдохнуть!".format(attacker))
            return
        
        self.bot.db['bite'][attacker] = now.timestamp()

        if defender.lower() in ['arachnobot', 'nightbot']:
            self.bot.privmsg(self.channel, '/w ' + attacker + ' Не сметь!')
            self.bot.privmsg(self.channel, '/timeout ' + attacker + ' 300')
            self.bot.privmsg(self.channel, '@' + attacker + ' попытался укусить ботика. @'+attacker+' SMOrc')
            return

        if defender.lower() == 'кусь':
            self.bot.privmsg(self.channel, '/timeout ' + attacker + ' 1')
            self.bot.privmsg(self.channel, '@' + attacker + ' попытался сломать систему, но не смог BabyRage')

        if attacker.lower() == defender.lower():
            self.bot.privmsg(self.channel, '@{0} укусил сам себя за жопь. Как, а главное - зачем он это сделал? Загадка...'.format(attacker))
            return

        prefix = u"нежно " if random.randint(1, 2) == 1 else "ласково "
        if defender.lower() == "prayda_alpha":
            target = u" за хвостик" if random.randint(1, 2) == 1 else " за ушко"
        else:
            if defender.lower() == "looputaps":
                target = u" за лапку в тапке"
            else:
                target = u""

        self.bot.privmsg(self.channel, "По поручению {0} {1} кусаю @{2}{3}".format(attacker, prefix, defender, target))

    # noinspection PyUnusedLocal
    @command(permissions='view', aliases=("баги",))
    def bugs(self, mask, target, args):
        """
            Показывает текущее число "багов" (очков лояльности)

            %%bugs
        """
        user = mask.nick
        try:
            res = api.get_points(self.oauth, user)['points']
        except requests.HTTPError:
            res = 0

        self.bot.privmsg(self.channel, '/w ' + user + ' Набрано багов: {0}'.format(res))

    # noinspection PyUnusedLocal
    @command(permissions='streamer', aliases=("break","икуфл"), show_in_help_list=False)
    def pause(self, mask, target, args):
        """
            Запускает перерыв

            %%pause
        """
        res = self.ws.call(obsws_requests.SetCurrentScene("Paused"))
        self.ws.call(obsws_requests.SetMute(self.aud_sources.getMic1(), True))

    @command(permissions='streamer', aliases=("continue","куыгьу"), show_in_help_list=False)
    def resume(self, mask, target, args):
        """
            Отменяет перерыв

            %%resume
        """
        res = self.ws.call(obsws_requests.SetCurrentScene("Game"))
        self.ws.call(obsws_requests.SetMute(self.aud_sources.getMic1(), False))

    @command(permissions='streamer', aliases=("плющ",))
    def plusch(self, mask, target, args):
        """
            Раздаёт плющи

            %% plusch <who>
        """
        who = args["<who>"]
        self.bot.privmsg(self.channel, "Эк {0} поплющило...".format(who))
        self.plusches += 1
        self.write_plusch()

    def write_plusch(self):
        with codecs.open("e:\\plusch.txt", "w", "utf8") as f:
            f.write("Кого-то поплющило {0} раз...".format(self.plusches))

def main():
    # instanciate a bot
    # bot = irc3.IrcBot.from_argv(argv=("config.ini", "-r", "-v"))
    config = {
        'nick': 'arachnobot',
        'username': 'arachnobot',
        'password': password,
        'host': 'irc.twitch.tv',
        'port': '6667',
        'autojoins': ['#iarspider'],
        'autocommands': ['CAP REQ :twitch.tv/membership', 'CAP REQ :twitch.tv/commands'],
        'storage': 'json://bot.json',
        'debug': 'False'
    }

    newconfig = ini2config("""[irc3.plugins.command]
# command plugin configuration

# set command char
cmd = !

# set guard policy
guard = irc3.plugins.command.mask_based_policy

[irc3.plugins.command.masks]
# this section is used by the guard to secure the bot's command
# change your nickname and uncomment the line below
iarspider!*@* = all_permissions
* = view
iarspider!*@* = streamer
CweLTH!*@* = special
KLMendor!*@* = special
Prayda_Alpha!*@* = special
LoopuTaps!*@* = special
BabyTigerOnTheSunflower!*@* = special""")

    config.update(newconfig)
    # from pprint import pprint
    # pprint (config)
    # return

    bot = irc3.IrcBot.from_config(config)
    bot.include(
        'irc3.plugins.core',
        'irc3.plugins.command',
        'irc3.plugins.autocommand',
        'irc3.plugins.autojoins',
        'irc3.plugins.userlist',
        'irc3.plugins.storage',
        __name__)

    # bot.oauth =
    bot.run(forever=True)
    # bot.test(":iarspider!iarspider@iarspider.tmi.twitch.tv PRIVMSG #iarspider :!bite @iarspider")


if __name__ == '__main__':
    main()
