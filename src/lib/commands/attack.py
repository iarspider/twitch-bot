from __future__ import print_function
import random
import sqlite3


def attack(args):
    # usage = '!attack <player>'
    # dice = []
    #
    # import types
    # if isinstance(args, types.StringTypes):
    #     args = args.split(" ")
    #
    # print(args)
    #
    # if args is None or len(args) == 0:
    #     dice = (6,)
    # else:
    #     for arg in args:
    #         if arg is None:
    #             return usage
    #
    #         # print("arg is", arg)
    #         if not 'd' in arg:
    #             continue
    #         num, sides = arg.split('d')
    #         try:
    #             if not num:
    #                 num = 1
    #             else:
    #                 num = int(num)
    #             sides = int(sides)
    #         except ValueError:
    #             continue
    #
    #         if not ((0 < num <= 10) and (4 <= sides <= 100)):
    #             continue
    #
    #         # print("Rolling {0} {1}-sided dice(s)".format(num, sides))
    #
    #         rolls = [random.randint(1, sides) for _ in xrange(num)]
    #         roll_sum = sum(rolls)
    #         # print("You rolled:", ";".join(str(x) for x in rolls), "sum is", roll_sum)
    #
    #         dice.append(roll_sum)
    #
    # return "You rolled: {}".format(", ".join(str(x) for x in dice))
    return "Not yet implemented"


def new_print(value, *args, **kwargs):
    pass


if __name__ == "__main__":
    print("Test mode")
    dice("d4")
    dice(["1d4", "2d6"])
    dice("2d6")
    # else:
    #  print=new_print