
import random
import consts


class Game():

    def __init__(self, pl1, pl2):
        self._pl1 = pl1
        self._pl2 = pl2
        self.pl_step = itertools.cycle([pl1, pl2])
        self.priz = 0
        self.can_reraise = False
        self.bed = 0

    def next_turn(self):
        for pl in [self.pl1, self.pl2]:
            pl.balance -= consts.BLAIND_AMOUNT
            self.priz += consts.BLAIND_AMOUNT
            pl.current_card = random.choice(consts.CARDS)
        next(self.pl_step).turn(game)

    def do_bed(self, pl, amount):
        pl.balance -= amount
        self.priz += amount
        self.bed = amount
        next(self.pl_step).turn(game)

    def finish_game(self):
        if winner:
            winner.balance += self.priz
        self.prize = 0
        self.bed = None
        self.can_reraise = False

    def passing(self, pl):
        competitor = self._get_competitor(pl)
        competitor.balance += self.priz
        self.winner = competitor
        self.finish_game()

    def check(self, pl):
        self.prize += self.bed
        pl.balance -= self.bed
        self.bed = None
        competitor = self._get_competitor(pl)
        if pl.current_card < competitor.current_card:
            self.winner = competitor
        elif pl.current_card > competitor.current_card:
            self.winner = pl
        else:
            self.winner = None

        self.finish_game()

    def reraise(self, pl, reraise):
        self.prize += self.bed
        pl.balance -= self.bed
        self.prize += reraise
        pl.balance -= reraise
        self.can_reraise = False

    def _get_competitor(self, pl):
        if pl is self.pl1:
            return self.pl2
        return self.pl1


class Player():
    def __init__(self, name='Name'):
        self.balance = 100
        self.current_card = None

    def my_desigion(self):
        [
            lambda: game.passing(self),
            lambda: game.check(self),
        ] + [lambda : game.reraise(self, c) for c in consts.COUNTS]


    def turn(self, game):
        if game.bed is None:
            if self.current_card > 2:
                game.do_bed(self, 20)
            elif self.current_card > 1:
                game.do_bed(self, 10)
            else:
                game.check(self)
        else:
            if self.current_card > 2:
                game.reraise(self, 10)
            elif self.current_card > 1:
                game.check(self)
            else:
                game.passing(self)


    def raise_money(self, game):
        pass


pl1 = Player('Boris')
pl2 = Player('Ivan')

game = Game(pl1, pl2)

game.next_turn()
