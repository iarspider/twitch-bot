"""
Simple IRC Bot for Twitch.tv

Developed by Aidan Thomson <aidraj0@gmail.com>
"""

from collections import defaultdict

import lib.functions_commands as commands
import lib.irc as irc_
from lib.functions_general import *


class Roboraj:
    def __init__(self, config):
        self.config = config
        self.irc = irc_.irc(config)
        self.socket = self.irc.get_irc_socket_object()
        self.users = defaultdict(set)

    def run(self):
        irc = self.irc
        sock = self.socket
        config = self.config

        while True:
            data_raw = sock.recv(config['socket_buffer_size']).rstrip()

            for data in data_raw.split('\r'):
                data = data.strip()
                if len(data) == 0:
                    pp('Connection was lost, reconnecting.')
                    sock = self.irc.get_irc_socket_object()

                if config['debug']:
                    print data

                # check for ping, reply with pong
                if irc.check_for_ping(data):
                    continue

                if irc.check_for_join(data):
                    user, channel = irc.get_join(data)
                    self.users[channel].add(user.lower())
                    pp("User {0} joined {1}".format(user, channel))
                    continue

                if irc.check_for_part(data):
                    user, channel = irc.get_part(data)
                    try:
                        self.users[channel].remove(user.lower())
                    except KeyError:
                        pass
                    pp("User {0} left {1}".format(user, channel))
                    continue

                if irc.check_for_message(data):
                    message_dict = irc.get_message(data)

                    channel = message_dict['channel']
                    message = message_dict['message']
                    username = message_dict['username']

                    ppi(channel, message, username)

                    # check if message is a command with no arguments
                    if commands.is_valid_command(message) or commands.is_valid_command(message.split(' ')[0]):
                        command = message

                        if commands.check_returns_function(command.split(' ')[0]):
                            if commands.check_has_correct_args(command, command.split(' ')[0]):
                                command_name = command.split(' ')[0]
                                args = command.split(' ')[1:]

                                if commands.is_on_cooldown(command_name, channel):
                                    pbot('Command is on cooldown. (%s) (%s) (%ss remaining)' % (
                                        command, username, commands.get_cooldown_remaining(command_name, channel)),
                                         channel
                                         )
                                else:
                                    pbot('Command is valid an not on cooldown. (%s) (%s)' % (
                                        command, username),
                                         channel
                                         )

                                    result = commands.pass_to_function(command_name[1:], args, username,
                                                                       self.users[channel])
                                    commands.update_last_used(command_name, channel)

                                    if result:
                                        for r in result:
                                            resp = '(%s) > %s' % (username, r)
                                            pbot(resp, channel)
                                            irc.send_message(channel, resp)

                        else:
                            if commands.is_on_cooldown(command, channel):
                                pbot('Command is on cooldown. (%s) (%s) (%ss remaining)' % (
                                    command, username, commands.get_cooldown_remaining(command, channel)),
                                     channel
                                     )
                            elif commands.check_has_return(command):
                                pbot('Command is valid and not on cooldown. (%s) (%s)' % (
                                    command, username),
                                     channel
                                     )
                                commands.update_last_used(command, channel)

                                resp = '(%s) > %s' % (username, commands.get_return(command))
                                commands.update_last_used(command, channel)

                                pbot(resp, channel)
                                irc.send_message(channel, resp)
