from itertools import repeat
import random

def dice(args):
  dice = []
  if args is None or len(args) == 0:
    dice = (6,)
  else:
      for arg in args:
        if not 'd' in arg:
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

        if not ((0 < num < 10) and (4 < sides < 100)):
            continue

        dice.extend(sum(random.randint(1, sides) for _ in xrange(num)))

  usage = '!dice <num>d<sides> [<num>d<sides>] ...'

  # carry out validation
  try:
    return "You rolled: {}".format(", ".join(dice))
  except:
    return usage