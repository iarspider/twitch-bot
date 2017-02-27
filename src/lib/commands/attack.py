from __future__ import print_function

import random


def attack(args, sender, online_users):
    print("{0}: !attack {1}".format(sender, repr(args)))
    usage = '!attack <player>'
    if len(args) != 1:
        return usage

    if args[0].lower() not in online_users:
        return "Sorry, user {0} is not online at the moment!".format(args[0])

    if args[0].lower() == sender.lower():
        return "RKN forbids me to do that!"

    if args[0].lower() == "arachnobot":
        return "Don't ya dare hurt ma bot!"

    # print ("{0} vs {1}".format(sender, args[0]))
    result = ["Battle: @{0} vs @{1}!".format(sender, args[0])]

    attack_d = random.randint(1, 6)
    defence_d = random.randint(1, 6)

    if attack_d > defence_d:
        result.append("@{0} wins!")
    elif attack_d < defence_d:
        result.append("@{1} wins!")
    else:
        result.append("It's a draw!")

    return result
