import pygame
import os
import random
import time
import neat

random.seed(434)

pygame.init()

# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Global_Constants
SCREEN_HEIGHT = 300
SCREEN_WIDTH = 300
BLOCK_SIZE = 10
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# Functions
def Grid():
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
        for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, "#3c3c3b", rect, 1)  # grey


Grid()

score = 0


def show_score(choice, color, font, size, score):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Max Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    SCREEN.blit(score_surface, score_rect)


def game_over():
    my_font = pygame.font.SysFont('comic sans', 50)

    game_over_surface = my_font.render('Your Score is : ' + str(score), True, red)

    game_over_rect = game_over_surface.get_rect()

    game_over_rect.midtop = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)

    SCREEN.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

    # after 2 seconds we will quit the program
    time.sleep(2)

    # deactivating pygame library
    pygame.quit()

    # quit the program
    quit()


# classes


class Snake():
    def __init__(self):
        self.x, self.y = BLOCK_SIZE * int(random.randint(0, SCREEN_WIDTH) / BLOCK_SIZE), BLOCK_SIZE * int(
            random.randint(0, SCREEN_HEIGHT) / BLOCK_SIZE)
        self.dir = 'r'  # default direction is right
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body = [(pygame.Rect(self.x, self.y, BLOCK_SIZE,
                                  BLOCK_SIZE))]  # body of the snake is represented by a list
        self.dead = False  # the snake starts off as alive
        self.len = 1 + len(self.body)
        self.steps = 0
        self.self_allowance = [0, 0, 0]  # rlf
        self.wall_allowance = [0, 0, 0]  # rlf
        self.score = 0
        self.life = life

    def update(self):

        if self.dir == 'r':
            self.head.x += BLOCK_SIZE
        elif self.dir == 'l':
            self.head.x -= BLOCK_SIZE
        elif self.dir == 'u':
            self.head.y -= BLOCK_SIZE
        elif self.dir == 'd':
            self.head.y += BLOCK_SIZE

        self.body.insert(0, pygame.Rect(self.head.x, self.head.y, BLOCK_SIZE, BLOCK_SIZE))
        if len(self.body) > self.len:
            self.body.pop()

    def change_dir(self, direction: str) -> None:
        if direction == 'u' and self.dir != 'd':
            self.dir = 'u'
        elif direction == 'd' and self.dir != 'u':
            self.dir = 'd'
        elif direction == 'l' and self.dir != 'r':
            self.dir = 'l'
        elif direction == 'r' and self.dir != 'l':
            self.dir = 'r'

    def draw(self, screen) -> None:
        # draw snake head on the screen
        pygame.draw.rect(SCREEN, "green", self.head)
        # draw snake body on the screen
        for square in self.body:
            pygame.draw.rect(SCREEN, "green", square)

    def check_death(self):
        # Check collision with itself
        for square in self.body[1:]:  # Exclude the head itself
            if self.head.colliderect(square):
                self.dead = True
                return self.dead

        # Check collision with screen boundaries
        if self.head.x >= SCREEN_WIDTH or self.head.x < 0 or self.head.y >= SCREEN_HEIGHT or self.head.y < 0:
            self.dead = True

        return self.dead

    def eat(self, apple) -> None:
        if self.head.x == apple.x and self.head.y == apple.y:
            self.body.append(pygame.Rect(self.head.x, self.head.y, BLOCK_SIZE, BLOCK_SIZE))
            return True

    def neat_feed(self, apple, width, height) -> list:
        out = [
            0, 0, 0,  # if food is r/l/f
            0, 0, 0,  # if the snake can move r/l/f wrt wall
            0, 0, 0  # if the snake can move r/l/f wrt self
        ]

        # check if food is to the right
        if self.dir == 'u' and self.head.x < apple.x and self.head.y == apple.y:
            out[0] = 1
        elif self.dir == 'd' and self.head.x > apple.x and self.head.y == apple.y:
            out[0] = 1
        elif self.dir == 'l' and self.head.y > apple.y and self.head.x == apple.x:
            out[0] = 1
        elif self.dir == 'r' and self.head.y < apple.y and self.head.x == apple.x:
            out[0] = 1
        # check if food is to the left
        if self.dir == 'u' and self.head.x > apple.x and self.head.y == apple.y:
            out[1] = 1
        elif self.dir == 'd' and self.head.x < apple.x and self.head.y == apple.y:
            out[1] = 1
        elif self.dir == 'l' and self.head.y < apple.y and self.head.x == apple.x:
            out[1] = 1
        elif self.dir == 'r' and self.head.y > apple.y and self.head.x == apple.x:
            out[1] = 1
        # check if food is in the front
        if self.dir == 'u' and self.head.y > apple.y and self.head.x == apple.x:
            out[2] = 1
        elif self.dir == 'd' and self.head.y < apple.y and self.head.x == apple.x:
            out[2] = 1
        elif self.dir == 'l' and self.head.x > apple.x and self.head.y == apple.y:
            out[2] = 1
        elif self.dir == 'r' and self.head.x < apple.x and self.head.y == apple.y:
            out[2] = 1

        '''if self.dir == 'r':
            xdir = 1
            ydir = 0
        if self.dir == 'l':
            xdir = -1
            ydir = 0
        if self.dir == 'u':
            xdir = 0
            ydir = 1
        if self.dir == 'd':
            xdir = 0
            ydir = -1

        if xdir == 0:
            if ydir == 1:
                if self.head.x + 1 not in self.body:
                    self.self_allowance[0] = 1
                else:
                    self.self_allowance[0] = 0
                if self.head.x - 1 not in self.body:
                    self.self_allowance[1] = 1
                else:
                    self.self_allowance[1] = 0
                if self.head.y + ydir not in self.body:
                    self.self_allowance[2] = 1
                else:
                    self.self_allowance[2] = 0

                if self.head.x * BLOCK_SIZE < SCREEN_WIDTH:
                    self.wall_allowance[0] = 1
                else:
                    self.wall_allowance[0] = 0
                if self.head.x * BLOCK_SIZE > 0:
                    self.wall_allowance[1] = 1
                else:
                    self.wall_allowance[1] = 0
                if self.head.y * BLOCK_SIZE < SCREEN_HEIGHT:
                    self.wall_allowance[2] = 1
                else:
                    self.wall_allowance[2] = 0
            else:
                if self.head.x - 1 not in self.body:
                    self.self_allowance[0] = 1
                else:
                    self.self_allowance[0] = 0
                if self.head.x + 1 not in self.body:
                    self.self_allowance[1] = 1
                else:
                    self.self_allowance[1] = 0
                if self.head.y + ydir not in self.body:
                    self.self_allowance[2] = 1
                else:
                    self.self_allowance[2] = 0

                if (self.head.x * BLOCK_SIZE > 0):
                    self.wall_allowance[0] = 1
                else:
                    self.wall_allowance[0] = 0
                if (self.head.x * BLOCK_SIZE < SCREEN_WIDTH):
                    self.wall_allowance[1] = 1
                else:
                    self.wall_allowance[1] = 0
                if (self.head.y * BLOCK_SIZE > 0):
                    self.wall_allowance[2] = 1
                else:
                    self.wall_allowance[2] = 0
        if ydir == 0:
            if xdir == 1:
                if self.head.y - 1 not in self.body:
                    self.self_allowance[0] = 1
                else:
                    self.self_allowance[0] = 0
                if self.head.y + 1 not in self.body:
                    self.self_allowance[1] = 1
                else:
                    self.self_allowance[1] = 0
                if self.head.x + xdir not in self.body:
                    self.self_allowance[2] = 1
                else:
                    self.self_allowance[2] = 0

                if self.head.y * BLOCK_SIZE > 0:
                    self.wall_allowance[0] = 1
                else:
                    self.wall_allowance[0] = 0
                if (self.head.y * BLOCK_SIZE < SCREEN_HEIGHT):
                    self.wall_allowance[1] = 1
                else:
                    self.wall_allowance[1] = 0
                if (self.head.x * BLOCK_SIZE < SCREEN_WIDTH):
                    self.wall_allowance[2] = 1
                else:
                    self.wall_allowance[2] = 0
            else:
                if self.head.y + 1 not in self.body:
                    self.self_allowance[0] = 1
                else:
                    self.self_allowance[0] = 0
                if self.head.y - 1 not in self.body:
                    self.self_allowance[1] = 1
                else:
                    self.self_allowance[1] = 0
                if self.head.x + xdir not in self.body:
                    self.self_allowance[2] = 1
                else:
                    self.self_allowance[2] = 0

                if (self.head.y * BLOCK_SIZE < SCREEN_HEIGHT):
                    self.wall_allowance[0] = 1
                else:
                    self.wall_allowance[0] = 0
                if (self.head.y * BLOCK_SIZE > 0):
                    self.wall_allowance[1] = 1
                else:
                    self.wall_allowance[1] = 0
                if (self.head.x * BLOCK_SIZE > 0):
                    self.wall_allowance[2] = 1
                else:
                    self.wall_allowance[2] = 0'''

        # check if the snake can move to the right (no wall to the right)
        if self.dir == 'u' and self.head.x + BLOCK_SIZE < SCREEN_WIDTH:
            out[3] = 1
        elif self.dir == 'd' and self.head.x - BLOCK_SIZE >= 0:
            out[3] = 1
        elif self.dir == 'l' and self.head.y - BLOCK_SIZE >= 0:
            out[3] = 1
        elif self.dir == 'r' and self.head.y + BLOCK_SIZE < SCREEN_HEIGHT:
            out[3] = 1

        # check if the snake can move to the right (no body part to the right)
        if self.dir == 'u' and (self.head.x + BLOCK_SIZE, self.head.y) not in self.body:
            out[6] = 1
        elif self.dir == 'd' and (self.head.x - BLOCK_SIZE, self.head.y) not in self.body:
            out[6] = 1
        elif self.dir == 'l' and (self.head.x, self.head.y - BLOCK_SIZE) not in self.body:
            out[6] = 1
        elif self.dir == 'd' and (self.head.x, self.head.y + BLOCK_SIZE) not in self.body:
            out[6] = 1

        # check if the snake can move to the left (no wall to the left)
        if self.dir == 'u' and self.head.x - BLOCK_SIZE >= 0:
            out[4] = 1
        elif self.dir == 'd' and self.head.x + BLOCK_SIZE < SCREEN_WIDTH:
            out[4] = 1
        elif self.dir == 'l' and self.head.y + BLOCK_SIZE < SCREEN_HEIGHT:
            out[4] = 1
        elif self.dir == 'r' and self.head.y - BLOCK_SIZE >= 0:
            out[4] = 1

        # check if the snake can move to the left (no body part to the left)
        if self.dir == 'u' and (self.head.x - BLOCK_SIZE, self.head.y) not in self.body:
            out[7] = 1
        elif self.dir == 'd' and (self.head.x + BLOCK_SIZE, self.head.y) not in self.body:
            out[7] = 1
        elif self.dir == 'l' and (self.head.x, self.head.y + BLOCK_SIZE) not in self.body:
            out[7] = 1
        elif self.dir == 'r' and (self.head.x, self.head.y - BLOCK_SIZE) not in self.body:
            out[7] = 1

        # check if the snake can move forward (no wall in front)
        if self.dir == 'u' and self.head.y - BLOCK_SIZE >= 0:
            out[5] = 1
        elif self.dir == 'd' and self.head.y + BLOCK_SIZE < SCREEN_HEIGHT:
            out[5] = 1
        elif self.dir == 'l' and self.head.x - BLOCK_SIZE >= 0:
            out[5] = 1
        elif self.dir == 'r' and self.head.x + BLOCK_SIZE < SCREEN_WIDTH:
            out[5] = 1

        # check if the snake can move forward (no body part in front)
        if self.dir == 'u' and (self.head.x, self.head.y - BLOCK_SIZE) not in self.body:
            out[8] = 1
        elif self.dir == 'd' and (self.head.x, self.head.y + BLOCK_SIZE) not in self.body:
            out[8] = 1
        elif self.dir == 'l' and (self.head.x - BLOCK_SIZE, self.head.y) not in self.body:
            out[8] = 1
        elif self.dir == 'r' and (self.head.x + BLOCK_SIZE, self.head.y) not in self.body:
            out[8] = 1

        '''out[3] = self.wall_allowance[0]
        out[4] = self.wall_allowance[1]
        out[5] = self.wall_allowance[2]
        out[6] = self.self_allowance[0]
        out[7] = self.self_allowance[1]
        out[8] = self.self_allowance[2]'''
        # print(out)
        return out


class Apple():
    def __init__(self):
        self.x = BLOCK_SIZE * int(random.randint(0, SCREEN_WIDTH) / BLOCK_SIZE)
        self.y = BLOCK_SIZE * int(random.randint(0, SCREEN_HEIGHT) / BLOCK_SIZE)
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)

    def draw(self, screen):
        pygame.draw.rect(SCREEN, "red", self.rect)


pygame.display.set_caption('Snake')
fps = pygame.time.Clock()
snake_speed = 25

life = 200

generation_count = 0


def eval_genomes(genomes, config):
    global generation_count
    pygame.display.set_caption('Generation : ' + str(generation_count))

    apples = []
    snakes = []
    nets = []
    ge = []

    for genome_id, genome in genomes:
        snakes.append(Snake())
        apples.append(Apple())
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0  # initial fitness of the snakes is zero
        ge.append(genome)

    high_score = 0
    Run = True
    while Run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        for i, snake in enumerate(snakes):
            snake.steps += 1
            ge[i].fitness += 0.5
            snake.update()

            # give input variables to the output function
            input_data = snake.neat_feed(apples[i], SCREEN_WIDTH, SCREEN_HEIGHT)
            output = nets[i].activate(input_data)

            # we follow rlf

            if (output[0] == max(output)) and input_data[3] != 1:
                ge[i].fitness -= 10
            elif (input_data[4] != 1):
                ge[i].fitness += 5
            if (output[1] == max(output)) and input_data[4] != 1:
                ge[i].fitness -= 10
            elif (input_data[3] != 1):
                ge[i].fitness += 5
            if (output[2] == max(output)) and input_data[5] != 1:
                ge[i].fitness -= 10
            elif (input_data[5] != 1):
                ge[i].fitness += 5

            elif output[0] == max(output):  # take right
                if snake.dir == 'u':
                    snake.dir = 'r'
                elif snake.dir == 'r':
                    snake.dir = 'd'
                elif snake.dir == 'd':
                    snake.dir = 'l'
                elif snake.dir == 'l':
                    snake.dir = 'u'

            if output[1] == max(output):  # take left
                if snake.dir == 'u':
                    snake.dir = 'l'
                elif snake.dir == 'l':
                    snake.dir = 'd'
                elif snake.dir == 'd':
                    snake.dir = 'r'
                elif snake.dir == 'r':
                    snake.dir = 'u'

        for i, snake in enumerate(snakes):
            dead = False
            if snake.check_death():
                dead = True
                ge[i].fitness -= 25
                # print(ge[i].fitness)
                apples.pop(i)
                snakes.pop(i)
                nets.pop(i)
                ge.pop(i)
                # i -= 1

                # check if no snakes left
                if (len(snakes) == 0):
                    Run = False
                    break

            # giving the snake incentive to not roam around meaninglessly
            if (not dead) and snake.steps > snake.life:
                dead = True
                ge[i].fitness -= 30
                apples.pop(i)
                snakes.pop(i)
                nets.pop(i)
                ge.pop(i)
                # i -= 1

                if len(snakes) == 0:
                    Run = False
                    break

            if (not dead) and snake.eat(apples[i]):
                snake.score += 1
                # snake.update()
                apples[i] = Apple()
                ge[i].fitness += 70
                high_score = max(high_score, snake.score)
                snake.life += 100
                snake.update()

        SCREEN.fill('black')
        Grid()
        for apple in apples:
            apple.draw(SCREEN)
        for snake in snakes:
            snake.draw(SCREEN)

        show_score(1, pygame.Color(255, 255, 255), 'comic sans', 20, high_score)
        pygame.display.update()
        fps.tick(snake_speed)

    # now will go to the next generation
    generation_count += 1


def run(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    pop = neat.Population(config)  # generate a population based on the config file

    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    pop.run(eval_genomes, 50)  # calls the game 50 times and pass in the generated populations


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
