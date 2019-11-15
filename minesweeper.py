import pygame, random, math, os
pygame.init()

# SIZE SETTINGS =
BLOCK_SIZE = 25
TOP_SIZE = 2 * BLOCK_SIZE
DISPLAY_SIZE = 3 * BLOCK_SIZE

# GAME SETTINGS: MIN WIDTH = 2, MIN HEIGHT = 0
WIDTH = 40
HEIGHT = 30
BOMBS = 100

# MOUSE BUTTON SIDES
LEFT = 1
RIGHT = 3

# GAME INITIALIZATION
screen = pygame.display.set_mode((WIDTH * BLOCK_SIZE, HEIGHT * BLOCK_SIZE + TOP_SIZE))
clock = pygame.time.Clock()
FPS = 30

# 1: IN-GAME, 2: WIN, 0: LOSS
WIN = 1
# Number of flagged and checked blocks
FLAGS = 0
CHECKED = 0

# IMAGES
dir_path = os.path.dirname(os.path.realpath(__file__))

n_display = pygame.image.load("{}/Images/Number_Display.png".format(dir_path))
n_0 = pygame.image.load("{}/Images/Num0.png".format(dir_path))
n_1 = pygame.image.load("{}/Images/Num1.png".format(dir_path))
n_2 = pygame.image.load("{}/Images/Num2.png".format(dir_path))
n_3 = pygame.image.load("{}/Images/Num3.png".format(dir_path))
n_4 = pygame.image.load("{}/Images/Num4.png".format(dir_path))
n_5 = pygame.image.load("{}/Images/Num5.png".format(dir_path))
n_6 = pygame.image.load("{}/Images/Num6.png".format(dir_path))
n_7 = pygame.image.load("{}/Images/Num7.png".format(dir_path))
n_8 = pygame.image.load("{}/Images/Num8.png".format(dir_path))
n_9 = pygame.image.load("{}/Images/Num9.png".format(dir_path))
fb_unclicked = pygame.image.load("{}/Images/Face_Button.png".format(dir_path))
fb_clicked = pygame.image.load("{}/Images/Face_Button_Clicked.png".format(dir_path))
b_unchecked = pygame.image.load("{}/Images/Unchecked.png".format(dir_path))
b_empty = pygame.image.load("{}/Images/Empty.png".format(dir_path))
b_flag = pygame.image.load("{}/Images/Flag.png".format(dir_path))
b_question = pygame.image.load("{}/Images/Question.png".format(dir_path))
b_bomb = pygame.image.load("{}/Images/Bomb.png".format(dir_path))
b_bomb_unchecked = pygame.image.load("{}/Images/Bomb_Unchecked.png".format(dir_path))
b_1 = pygame.image.load("{}/Images/1.png".format(dir_path))
b_2 = pygame.image.load("{}/Images/2.png".format(dir_path))
b_3 = pygame.image.load("{}/Images/3.png".format(dir_path))
b_4 = pygame.image.load("{}/Images/4.png".format(dir_path))
b_5 = pygame.image.load("{}/Images/5.png".format(dir_path))
b_6 = pygame.image.load("{}/Images/6.png".format(dir_path))
b_7 = pygame.image.load("{}/Images/7.png".format(dir_path))
b_8 = pygame.image.load("{}/Images/8.png".format(dir_path))
f_midgame = pygame.image.load("{}/Images/Face_MidGame.png".format(dir_path))
f_check = pygame.image.load("{}/Images/Face_Check.png".format(dir_path))
f_bomb = pygame.image.load("{}/Images/Face_Bomb.png".format(dir_path))
f_win = pygame.image.load("{}/Images/Face_Win.png".format(dir_path))

# FACE SETTINGS
CUR_FACE = f_midgame
CUR_FBUTTON = fb_unclicked
FBUTTON_TIMER = 0.0
FACE_TIMER = 0.0
BUTTON_CLICK_DELAY = 0.05
FACE_CHECK_DELAY = 0.5

# BLOCK CLASS
class Block(object):
    def __init__(self, type=0, loc=[0, 0], display=screen):
        self.type = type
        self.checked = False
        self.mark = 0
        self.checkable = True
        self.display = display
        self.loc = loc

    def reveal_around(self, block):
        global board
        if block[0] > 0:
            if not board[block[0] - 1][block[1]].checked: board[block[0] - 1][block[1]].check()
            if block[1] > 0:
                if not board[block[0] - 1][block[1] - 1].checked: board[block[0] - 1][block[1] - 1].check()
            if block[1] < WIDTH - 1:
                if not board[block[0] - 1][block[1] + 1].checked: board[block[0] - 1][block[1] + 1].check()

        if block[1] > 0:
            if not board[block[0]][block[1] - 1].checked: board[block[0]][block[1] - 1].check()
        if block[1] < WIDTH - 1:
            if not board[block[0]][block[1] + 1].checked: board[block[0]][block[1] + 1].check()

        if block[0] < HEIGHT - 1:
            if not board[block[0] + 1][block[1]].checked: board[block[0] + 1][block[1]].check()
            if block[1] > 0:
                if not board[block[0] + 1][block[1] - 1].checked: board[block[0] + 1][block[1] - 1].check()
            if block[1] < WIDTH - 1:
                if not board[block[0] + 1][block[1] + 1].checked: board[block[0] + 1][block[1] + 1].check()

    def check_flags(self, block):
        global board
        flags = 0
        if block[0] > 0:
            if board[block[0] - 1][block[1]].mark == 1: flags += 1
            if block[1] > 0:
                if board[block[0] - 1][block[1] - 1].mark == 1: flags += 1
            if block[1] < WIDTH - 1:
                if board[block[0] - 1][block[1] + 1].mark == 1: flags += 1

        if block[1] > 0:
            if board[block[0]][block[1] - 1].mark == 1: flags += 1
        if block[1] < WIDTH - 1:
            if board[block[0]][block[1] + 1].mark == 1: flags += 1

        if block[0] < HEIGHT - 1:
            if board[block[0] + 1][block[1]].mark == 1: flags += 1
            if block[1] > 0:
                if board[block[0] + 1][block[1] - 1].mark == 1: flags += 1
            if block[1] < WIDTH - 1:
                if board[block[0] + 1][block[1] + 1].mark == 1: flags += 1

        if flags >= board[block[0]][block[1]].type:
            return True
        else:
            return False

    def check(self):
        global WIN, CUR_FACE, FACE_TIMER, FACE_CHECK_DELAY, CHECKED
        if self.checked and not self.checkable and self.mark == 0:
            if self.check_flags(self.loc):
                self.reveal_around(self.loc)

        if self.checkable and not self.checked and self.mark == 0:
            self.checked = True
            self.checkable =False
            if self.type == 9:
                WIN = 0
                CUR_FACE = f_bomb
            else:
                CUR_FACE = f_check
                FACE_TIMER = FACE_CHECK_DELAY
                CHECKED += 1
                check_win()
            if self.type == 0:
                self.reveal_around(self.loc)

    def flag(self):
        global FLAGS
        if not self.checked:
            self.checkable = False
            self.mark += 1
            if self.mark == 1:
                FLAGS += 1
                check_win()
            elif self.mark == 2:
                FLAGS -= 1
        if self.mark > 2:
            self.mark = 0
        if self.mark == 0 and not self.checked:
            self.checkable = True

    def draw(self, loc):
        if not self.checked:
            if self.mark == 0:
                self.display.blit(b_unchecked, loc)
            if self.mark == 1:
                self.display.blit(b_flag, loc)
            if self.mark == 2:
                self.display.blit(b_question, loc)

        else:
            if self.type == 9:
                self.display.blit(b_bomb, loc)
            elif self.type == 1:
                self.display.blit(b_1, loc)
            elif self.type == 2:
                self.display.blit(b_2, loc)
            elif self.type == 3:
                self.display.blit(b_3, loc)
            elif self.type == 4:
                self.display.blit(b_4, loc)
            elif self.type == 5:
                self.display.blit(b_5, loc)
            elif self.type == 6:
                self.display.blit(b_6, loc)
            elif self.type == 7:
                self.display.blit(b_7, loc)
            elif self.type == 8:
                self.display.blit(b_8, loc)
            else:
                self.display.blit(b_empty, loc)


def check_win():
    global WIN
    # Checks if all cells are flagged or checked
    if FLAGS == BOMBS:
        if CHECKED == WIDTH*HEIGHT - FLAGS:
            WIN = 2

board = []

# BOARD CREATION
def make_board():
    global FLAGS, CHECKED
    board = []
    FLAGS = 0
    CHECKED = 0
    for row in range(0, HEIGHT):
        board.append([])
        for block in range(0, WIDTH):
            board[row].append(0)

    for row in range(0, HEIGHT):
        for block in range(0, WIDTH):
            board[row][block] = Block(0, [row, block])

    # BOMBS
    bombs = []
    for bomb in range(0, BOMBS):
        bomb_row = random.randrange(0, HEIGHT, 1)
        bomb_block = random.randrange(0, WIDTH, 1)
        while (bomb_row, bomb_block) in bombs:
            bomb_row = random.randrange(0, HEIGHT, 1)
            bomb_block = random.randrange(0, WIDTH, 1)
        board[bomb_row][bomb_block].type = 9
        bombs.append((bomb_row, bomb_block))

    # FILL NUMBERS
    for b in bombs:
        if b[0] > 0:
            if board[b[0] - 1][b[1]].type != 9: board[b[0] - 1][b[1]].type += 1
            if b[1] > 0:
                if board[b[0] - 1][b[1] - 1].type != 9: board[b[0] - 1][b[1] - 1].type += 1
            if b[1] < WIDTH - 1:
                if board[b[0] - 1][b[1] + 1].type != 9: board[b[0] - 1][b[1] + 1].type += 1

        if b[1] > 0:
            if board[b[0]][b[1] - 1].type != 9: board[b[0]][b[1] - 1].type += 1
        if b[1] < WIDTH - 1:
            if board[b[0]][b[1] + 1].type != 9: board[b[0]][b[1] + 1].type += 1

        if b[0] < HEIGHT - 1:
            if board[b[0] + 1][b[1]].type != 9: board[b[0] + 1][b[1]].type += 1
            if b[1] > 0:
                if board[b[0] + 1][b[1] - 1].type != 9: board[b[0] + 1][b[1] - 1].type += 1
            if b[1] < WIDTH - 1:
                if board[b[0] + 1][b[1] + 1].type != 9: board[b[0] + 1][b[1] + 1].type += 1

    return board

# MAIN GAME LOOP FUNCTION
def main_loop():
    global FACE_TIMER, CUR_FACE, CUR_FBUTTON, FBUTTON_TIMER, WIN, board
    board = make_board()
    # IN GAME
    while WIN == 1:
        clock.tick(FPS)
        mouse_pos = [math.floor(pygame.mouse.get_pos()[0] / BLOCK_SIZE),
                     math.floor((pygame.mouse.get_pos()[1] - TOP_SIZE) / BLOCK_SIZE)]

        if FACE_TIMER == 0.0:
            CUR_FACE = f_midgame
        if FACE_TIMER > 0.0:
            FACE_TIMER -= 1 / FPS
        if FACE_TIMER < 0.0:
            FACE_TIMER = 0.0

        if FBUTTON_TIMER == 0.0:
            CUR_FBUTTON = fb_unclicked
        if FBUTTON_TIMER > 0.0:
            FBUTTON_TIMER -= 1 / FPS
        if FBUTTON_TIMER < 0.0:
            FBUTTON_TIMER = 0.0

        # INPUT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                # LEFT CLICK ON GAME BOARD
                if mouse_pos[1] >= 0:
                    board[mouse_pos[1]][mouse_pos[0]].check()
                # LEFT CLICK ON TOP BAR
                else:
                    if mouse_pos[0] >= WIDTH / 2 - TOP_SIZE / BLOCK_SIZE \
                            and mouse_pos[0] < WIDTH / 2 + TOP_SIZE / BLOCK_SIZE:
                        FBUTTON_TIMER = BUTTON_CLICK_DELAY
                        CUR_FBUTTON = fb_clicked
                        main_loop()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
                if mouse_pos[1] >= 0:
                    board[mouse_pos[1]][mouse_pos[0]].flag()

        # DRAW TOP BAR ON SCREEN
        screen.blit(CUR_FBUTTON, (WIDTH * BLOCK_SIZE / 2 - TOP_SIZE / 2, 0))
        screen.blit(CUR_FACE, (WIDTH * BLOCK_SIZE / 2 - TOP_SIZE / 2, 0))
        screen.blit(n_display, (WIDTH * BLOCK_SIZE / 2 - TOP_SIZE / 2 - DISPLAY_SIZE, 0))
        # UPPER NUMBERS
        screen.blit(n_0, (WIDTH * BLOCK_SIZE / 2 - TOP_SIZE / 2 - DISPLAY_SIZE, 0))
        screen.blit(n_0, (WIDTH * BLOCK_SIZE / 2 - TOP_SIZE / 2 - DISPLAY_SIZE * 2 / 3, 0))
        screen.blit(n_0, (WIDTH * BLOCK_SIZE / 2 - TOP_SIZE / 2 - DISPLAY_SIZE / 3, 0))
        # LOWER NUMBERS
        screen.blit(n_0, (WIDTH * BLOCK_SIZE / 2 - TOP_SIZE / 2 - DISPLAY_SIZE, TOP_SIZE / 2))
        screen.blit(n_0, (WIDTH * BLOCK_SIZE / 2 - TOP_SIZE / 2 - DISPLAY_SIZE * 2 / 3, TOP_SIZE / 2))
        screen.blit(n_0, (WIDTH * BLOCK_SIZE / 2 - TOP_SIZE / 2 - DISPLAY_SIZE / 3, TOP_SIZE / 2))

        # DRAW BLOCKS ON SCREEN
        r_loc = 0
        b_loc = 0
        for row in board:
            b_loc = 0
            for block in row:
                block.draw((b_loc, r_loc + TOP_SIZE))
                b_loc += BLOCK_SIZE
            r_loc += BLOCK_SIZE

        pygame.display.update()

    # LOSS / WIN
    while WIN == 0 or WIN == 2:
        clock.tick(FPS)
        mouse_pos = [math.floor(pygame.mouse.get_pos()[0] / BLOCK_SIZE),
                     math.floor((pygame.mouse.get_pos()[1] - TOP_SIZE) / BLOCK_SIZE)]
        if WIN == 0:
            CUR_FACE = f_bomb
        else:
            CUR_FACE = f_win

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == LEFT:
                    if mouse_pos[1] < 0:
                        if mouse_pos[0] >= WIDTH / 2 - TOP_SIZE / BLOCK_SIZE \
                                and mouse_pos[0] < WIDTH / 2 + TOP_SIZE / BLOCK_SIZE:
                            FBUTTON_TIMER = BUTTON_CLICK_DELAY
                            CUR_FBUTTON = fb_clicked
                            WIN = 1
                            main_loop()

        # DRAW TOP BAR ON SCREEN
        screen.blit(CUR_FBUTTON, (WIDTH * BLOCK_SIZE / 2 - TOP_SIZE / 2, 0))
        screen.blit(CUR_FACE, (WIDTH * BLOCK_SIZE / 2 - TOP_SIZE / 2, 0))
        screen.blit(n_display, (WIDTH * BLOCK_SIZE / 2 - TOP_SIZE / 2 - DISPLAY_SIZE, 0))

        pygame.display.update()




main_loop()