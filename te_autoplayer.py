''' Implement an AI to play tetris '''
from random import Random
from te_settings import Direction
from te_settings import MAXROW, MAXCOL

class AutoPlayer():
    ''' A very simple dumb AutoPlayer controller '''
    def __init__(self, controller):
        self.controller = controller
        self.rand = Random()

    def next_move(self, gamestate):
        ''' next_move() is called by the game, once per move.
            gamestate supplies access to all the state needed to autoplay the game.'''
        self.shrewd_next_move(gamestate)

    def random_next_move(self, gamestate):
        ''' make a random move and a random rotation.  Not the best strategy! '''
        rnd = self.rand.randint(-1, 1)
        if rnd == -1:
            direction = Direction.LEFT
        elif rnd == 1:
            direction = Direction.RIGHT
        if rnd != 0:
            gamestate.move(direction)
        rnd = self.rand.randint(-1, 1)
        if rnd == -1:
            direction = Direction.LEFT
        elif rnd == 1:
            direction = Direction.RIGHT
        if rnd != 0:
            gamestate.rotate(direction)
        gamestate.print_block_tiles()

    def shrewd_next_move(self, gamestate):
        """ violently search the best strategy """
        shrewd_move = 0
        judge_result = 0
        for virtual_rotate in range(4):
            for virtual_move_direction in [0,1,-1]:
                for virtual_move in range(MAXCOL // 2):
                    landed = False
                    virtual_game = gamestate.clone(True)
                    for i in range(virtual_rotate):
                        if landed:
                            break
                        virtual_game.rotate(Direction.RIGHT)
                        landed = virtual_game.update()
                    if virtual_move_direction == 1:
                        for j in range(virtual_move):
                            if landed:
                                break
                            virtual_game.move(Direction.RIGHT)
                            landed = virtual_game.update()
                    elif virtual_move_direction == -1:
                        for j in range(virtual_move):
                            if landed:
                                break
                            virtual_game.move(Direction.LEFT)
                            landed = virtual_game.update()
                    while not landed:
                        landed = virtual_game.update()
                    new_judge_result = judge(virtual_game)
                    if new_judge_result > judge_result:
                        if virtual_rotate != 0:
                            shrewd_move = Direction.RIGHT
                        else:
                            shrewd_move = virtual_move_direction + 100
                        judge_result = new_judge_result
        if shrewd_move == Direction.RIGHT:
            gamestate.rotate(Direction.RIGHT)
        elif shrewd_move - 100 == 1:
            gamestate.move(Direction.RIGHT)
        elif shrewd_move - 100 == -1:
            gamestate.move(Direction.LEFT)

def judge(gamestate):
    """ make judgement on the landed tiles """
    tiles = gamestate.get_tiles()
    judge = 10 * gamestate.get_score()
    for y in range(1,MAXROW):
        for x in range(MAXCOL):
            if not tiles[y][x] and tiles[y - 1][x]:
                judge -= 75
    for y in range(MAXROW):
        for x in range(MAXCOL):
            if tiles[y][x]:
                judge += 5 * y
                if x != MAXCOL - 1 and tiles[y][x + 1]:
                    judge += 1
                if y != MAXROW - 1 and tiles[y + 1][x]:
                    judge += 1
    for y in range(MAXROW):
        if tiles[y][0]:
            judge += 1
        if tiles[y][MAXCOL - 1]:
            judge += 1
    for x in range(MAXCOL):
        if tiles[MAXROW - 1][x]:
            judge += 1
    return judge
