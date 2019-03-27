''' Implement an AI to play tetris '''
from random import Random
from te_settings import Direction
from te_settings import MAXROW, MAXCOL
from copy import deepcopy

class AutoPlayer():
    ''' A very simple dumb AutoPlayer controller '''
    def __init__(self, controller):
        self.controller = controller
        self.shrewd_move_plan = []
        self.tiles = []
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
        if self.shrewd_move_plan == []:
            self.shrewd_move_plan = self.find_shrew_move_plan(gamestate)
        shrewd_move = self.shrewd_move_plan.pop(0)
        if shrewd_move == "LET_IT_BE":
            self.shrewd_move_plan.append(shrewd_move)
            #print("LET_IT_BE")
        elif shrewd_move == "ROTATE":
            gamestate.rotate(Direction.RIGHT)
            #print("ROTATE")
        elif shrewd_move == "MOVE_RIGHT":
            gamestate.move(Direction.RIGHT)
            #print("MOVE_RIGHT")
        elif shrewd_move == "MOVE_LEFT":
            gamestate.move(Direction.LEFT)
            #print("MOVE_LEFT")
        new_tiles = gamestate.get_tiles()
        if self.tiles != new_tiles:
            self.tiles = deepcopy(new_tiles)
            self.shrewd_move_plan = []
            #print("RESET MOVE PLAN")

    def find_shrew_move_plan(self, gamestate):
        judge_result = 0
        shrewd_move_plan = []
        for virtual_rotate1 in range(4):
            for virtual_move_direction1 in [0,1,-1]:
                for virtual_move1 in range(MAXCOL):
                    new_shrewd_move_plan = []
                    landed = False
                    virtual_game1 = gamestate.clone(True)
                    for i in range(virtual_rotate1):
                        if landed:
                            break
                        new_shrewd_move_plan.append("ROTATE")
                        virtual_game1.rotate(Direction.RIGHT)
                        landed = virtual_game1.update()
                    if virtual_move_direction1 == 1:
                        for j in range(virtual_move1):
                            if landed:
                                break
                            new_shrewd_move_plan.append("MOVE_RIGHT")
                            virtual_game1.move(Direction.RIGHT)
                            landed = virtual_game1.update()
                    elif virtual_move_direction1 == -1:
                        for j in range(virtual_move1):
                            if landed:
                                break
                            new_shrewd_move_plan.append("MOVE_LEFT")
                            virtual_game1.move(Direction.LEFT)
                            landed = virtual_game1.update()
                    while not landed:
                        landed = virtual_game1.update()
                    for virtual_rotate2 in range(4):
                        for virtual_move_direction2 in [0,1,-1]:
                            for virtual_move2 in range(MAXCOL):
                                virtual_game2 = virtual_game1.clone(True)
                                landed = False
                                judge_result2 = 0
                                for i in range(virtual_rotate2):
                                    if landed:
                                        break
                                    virtual_game2.rotate(Direction.RIGHT)
                                    landed = virtual_game2.update()
                                if virtual_move_direction2 == 1:
                                    for j in range(virtual_move2):
                                        if landed:
                                            break
                                        virtual_game2.move(Direction.RIGHT)
                                        landed = virtual_game2.update()
                                elif virtual_move_direction2 == -1:
                                    for j in range(virtual_move2):
                                        if landed:
                                            break
                                        virtual_game2.move(Direction.LEFT)
                                        landed = virtual_game2.update()
                                while not landed:
                                    landed = virtual_game2.update()
                                new_judge_result2 = judge(virtual_game2)
                                if new_judge_result2 > judge_result2:
                                    judge_result2 = new_judge_result2
                    new_judge_result = judge_result2
                    if new_judge_result > judge_result:
                        judge_result = new_judge_result
                        shrewd_move_plan = deepcopy(new_shrewd_move_plan)
        shrewd_move_plan.append("LET_IT_BE")
        '''print("move plan for:" + gamestate.get_falling_block_type())
        for i in shrewd_move_plan:
            print("move:", i)'''
        return shrewd_move_plan

def judge(gamestate):
    tiles = gamestate.get_tiles()
    judge = 11 * gamestate.get_score()
    for y in range(1,MAXROW):
        for x in range(MAXCOL):
            if not tiles[y][x] and tiles[y - 1][x]:
                judge -= 500
    for y in range(MAXROW):
        for x in range(MAXCOL):
            if tiles[y][x]:
                judge += y * 5
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
