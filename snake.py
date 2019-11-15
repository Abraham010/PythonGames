import pygame, random
pygame.init()

# Display
d_width = 800
d_height = 600
display = pygame.display.set_mode((d_width, d_height))

# Clock and tick rate
clock = pygame.time.Clock()
tempo = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Snake body list
s = [[d_width / 2, d_height / 2]]
s_len = 3
mov_dir = 0

# Apple starting coordinates
a0 = random.randrange(0, d_width)
a0 -= a0 % 10
a1 = random.randrange(0, d_height)
a1 -= a1 % 10
a = [a0, a1]

done = False


def snake():
    # Movement
    if mov_dir == 0:
        s.append([s[-1][0], s[-1][1] - 10])
    elif mov_dir == 1:
        s.append([s[-1][0] + 10, s[-1][1]])
    elif mov_dir == 2:
        s.append([s[-1][0], s[-1][1] + 10])
    elif mov_dir == 3:
        s.append([s[-1][0] - 10, s[-1][1]])

    if len(s) > s_len:
        del s[0]

    # Edge Handling
    if s[-1][0] < 0:
        s[-1][0] = d_width - 10
    if s[-1][0] > d_width - 10:
        s[-1][0] = 0
    if s[-1][1] < 0:
        s[-1][1] = d_height - 10
    if s[-1][1] > d_height - 10:
        s[-1][1] = 0

# Drawing Snake
    for cell in s:
        pygame.draw.rect(display, BLACK, [cell[0], cell[1], 10, 10])
# Drawing Apple
    pygame.draw.rect(display, RED, [a[0], a[1], 10, 10])


while not done:

    clock.tick(tempo)
    display.fill(WHITE)

# Player Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
        	# Space = Eat apple
            if event.key == pygame.K_SPACE:
                s_len += 1
                tempo += 0.5
            if event.key == pygame.K_LEFT and mov_dir != 1:
                mov_dir = 3
            if event.key == pygame.K_RIGHT and mov_dir != 3:
                mov_dir = 1
            if event.key == pygame.K_UP and mov_dir != 2:
                mov_dir = 0
            if event.key == pygame.K_DOWN and mov_dir != 0:
                mov_dir = 2

    # Apple
    if a0 == s[-1][0] and a1 == s[-1][1]:
        s_len += 1
        tempo += 1
        # New apple
        a0 = random.randrange(0, d_width)
        a0 -= a0 % 10
        a1 = random.randrange(0, d_height)
        a1 -= a1 % 10
        a = [a0, a1]

    snake()

    pygame.display.flip()