from __future__ import print_function
import random
import sqlite3
from config.config import *


def attack(args, sender, online_users):
    usage = '!attack <player>'
    if len(args) != 1:
        return usage

    if args[1] not in online_users:
        return "Sorry, user {0} is not online at the moment!".format(args[1])

    if args[1].lower() == sender.lower():
        return "RKN forbids me to do that!"

    if args[1].lower() == config['username']:
        return "Can't do that!"

    result = ["Battle: {0} vs {1}!".format(sender, args[1])]

    attack_d = random.randint(1, 6)
    defence_d = random.randint(1, 6)

    if attack_d > defence_d:
        result.append("{0} wins!")
    elif attack_d < defence_d:
        result.append("{1} wins!")
    else:
        result.append("It's a draw!")

    return result
