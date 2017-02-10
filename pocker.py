
import random
import consts
import itertools
import logging
logging.basicConfig()

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Game():

    def __init__(self, pl1, pl2):
        self._pl1 = pl1
        self._pl2 = pl2
        self.pl_step = itertools.cycle([pl1, pl2])
        self.prize = 0
        self.bed = 0
        self.step = 0
        self.finished = False

    def __repr__(self):
        return "[step:%s prize:%s]" % (self.step, self.prize)

    @property
    def can_reraise(self):
        return self.step == 1

    @property
    def can_bed(self):
        return self.step == 0

    def next_turn(self):
        logger.info('')
        logger.info('--------Next turn------------')
        self.finished = False
        for pl in [self._pl1, self._pl2]:
            pl.balance -= consts.BLAIND_AMOUNT
            self.prize += consts.BLAIND_AMOUNT
            pl.current_card = random.choice(consts.CARDS)
            pl.add_step(pl.current_card)
            logger.info("%s %s got card: %s", self, pl, pl.current_card)
        return next(self.pl_step).turn(self)

    def finish_game(self):
        if self.winner:
            self.winner.balance += self.prize
        else:
            self._pl1.balance += int(self.prize/2)
            self._pl2.balance += int(self.prize/2)

        logger.info('Winner: %s. %s %s', self.winner, self._pl1, self._pl2)

        self.step = 0
        self.winner = None
        self.prize = 0
        self.bed = 0
        self.finished = True
        self._pl1.steps = []
        self._pl2.steps = []

    def do_bed(self, pl, amount):
        pl.balance -= amount
        self.prize += amount
        self.bed = amount
        self.step += 1
        pl.add_step("bed_%s" % amount)
        self._get_competitor(pl).add_step("c_bed_%s" % amount)
        logger.info('%s %s do bed %d', self, pl, amount)
        next(self.pl_step).turn(self)

    def do_pass(self, pl):
        logger.info('%s %s pass', self, pl)
        competitor = self._get_competitor(pl)
        self.winner = competitor
        self.finish_game()

    def do_check(self, pl):
        pl.balance -= self.bed
        self.prize += self.bed

        competitor = self._get_competitor(pl)
        if pl.current_card < competitor.current_card:
            self.winner = competitor
        elif pl.current_card > competitor.current_card:
            self.winner = pl
        else:
            self.winner = None

        logger.info('%s %s check', self, pl)
        if self.step == 0:
            self.step += 1
            pl.add_step("check")
            competitor.add_step("c_check")
            next(self.pl_step).turn(self)
        else:
            self.finish_game()

    def reraise(self, pl, amount):
        self.prize += self.bed
        self.prize += amount
        pl.balance -= self.bed
        pl.balance -= amount
        self.bed = amount
        self.step += 1
        logger.info('%s %s reraise %s', self, pl, amount)
        pl.add_step("reraise_%d" % amount)
        self._get_competitor(pl).add_step("c_reraise_%s" % amount)
        next(self.pl_step).turn(self)

    def _get_competitor(self, pl):
        if pl is self._pl1:
            return self._pl2
        return self._pl1


class Player():
    def __init__(self, name, nnet):
        self.balance = 100
        self.current_card = None
        self.name = name
        self.nnet = nnet
        self.steps = []

    def add_step(self, step):
        self.steps.append(step)

    def __repr__(self):
        return "%s(%s)" % (self.name, self.balance)

    def turn(self, game):

        if game.finished:
            return

        for action, _ in self.nnet.get_decigion(self.steps):
            if action[0] == "pass":
                game.do_pass(self)
                break
            elif action[0] == "check":
                game.do_check(self)
                break
            elif game.can_bed and action[0] == "bed":
                game.do_bed(self, action[1])
                break
            elif game.can_reraise and action[0] == "reraise":
                game.reraise(self, action[1])
                break

        if not game.finished:
            raise Exception()
