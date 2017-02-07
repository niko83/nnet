
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
        logger.info('--------Next turn------------')
        self.finished = False
        for pl in [self._pl1, self._pl2]:
            pl.balance -= consts.BLAIND_AMOUNT
            self.prize += consts.BLAIND_AMOUNT
            pl.current_card = random.choice(consts.CARDS)
            logger.info("%s %s got card: %s", self, pl, pl.current_card)
        return next(self.pl_step).turn(game)

    def do_bed(self, pl, amount):
        pl.balance -= amount
        self.prize += amount
        self.bed = amount
        self.step += 1
        logger.info('%s %s do bed %d', self, pl, amount)
        next(self.pl_step).turn(game)

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

    def passing(self, pl):
        logger.info('%s %s passing', self, pl)
        competitor = self._get_competitor(pl)
        self.winner = competitor
        self.finish_game()

    def check(self, pl):
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
            next(self.pl_step).turn(game)
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
        next(self.pl_step).turn(game)

    def _get_competitor(self, pl):
        if pl is self._pl1:
            return self._pl2
        return self._pl1


class Player():
    def __init__(self, name='Name'):
        self.balance = 100
        self.current_card = None
        self.name = name

    def __repr__(self):
        return "%s(%s)" % (self.name, self.balance)

    def my_desigion(self):
        [
            lambda: game.passing(self),
            lambda: game.check(self),
        ] + [lambda: game.reraise(self, c) for c in consts.COUNTS]

    def turn(self, game):

        if game.finished:
            return

        if game.can_bed:
            if self.current_card > 2:
                game.do_bed(self, 20)
            elif self.current_card > 1:
                game.do_bed(self, 10)
            else:
                game.check(self)
        elif game.can_reraise:
            if self.current_card > 2:
                game.reraise(self, 10)
            elif self.current_card > 1:
                game.check(self)
            else:
                game.passing(self)
        else:
            if self.current_card > 3:
                game.check(self)
            else:
                game.passing(self)

        if not game.finished:
            raise Exception()


    def raise_money(self, game):
        pass


if __name__ == '__main__':

    pl1 = Player('Boris')
    pl2 = Player('Ivan')

    game = Game(pl1, pl2)
    counter = 0
    while pl1.balance > 0 and pl2.balance > 0:
        counter += 1
        game.next_turn()
        if pl1.balance + pl2.balance != 200:
            assert False

    print(counter)

