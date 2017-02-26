from __future__ import print_function

import random


# noinspection PyUnusedLocal
def dice(args, sender, online_users):
    usage = '!dice <num>d<sides> [<num>d<sides>] ...'
    dices = []

    import types
    if isinstance(args, types.StringTypes):
        args = args.split(" ")

    print(args)

    if args is None or len(args) == 0:
        dices = (6,)
    else:
        for arg in args:
            if arg is None:
                return usage

            # print("arg is", arg)
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

            # print("Rolling {0} {1}-sided dice(s)".format(num, sides))

            rolls = [random.randint(1, sides) for _ in xrange(num)]
            roll_sum = sum(rolls)
            # print("You rolled:", ";".join(str(x) for x in rolls), "sum is", roll_sum)

            dices.append(roll_sum)

    return "You rolled: {}".format(", ".join(str(x) for x in dices))


if __name__ == "__main__":
    print("Test mode")
    dice("d4")
    dice(["1d4", "2d6"])
    dice("2d6")
