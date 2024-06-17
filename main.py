import pygame
import os
import random
import time
import sys
import math
import neat

pygame.init()

# Global_Constants
SCREEN_HEIGHT = 400
SCREEN_WIDTH = 400
BLOCK_SIZE = 25
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


clock = pygame.time.Clock()


# Functions
def Grid():
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
        for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, "#3c3c3b", rect, 1)          #grey

Grid()


def show_score(choice, color, font, size, score):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Max Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    SCREEN.blit(score_surface, score_rect)

def dist(x1, x2, y1, y2):
    return abs(pow(x1 - x2, 2) - pow(y1 - y2, 2))

# Classes
class Snake:
    def __init__(self):
        self.x, self.y = BLOCK_SIZE * int(random.randint(0, SCREEN_WIDTH) / BLOCK_SIZE), BLOCK_SIZE * int(
            random.randint(0, SCREEN_HEIGHT) / BLOCK_SIZE)
        self.xdir = 1  # by default the snake moves towards the right
        self.ydir = 0
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body = [pygame.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE,
                                 BLOCK_SIZE)]  # body of the snake is represented by a list
        self.dead = False  # the snake starts off as alive
        self.len = 1 + len(self.body)

    def update(self):
        # first update the body
        self.body.append(self.head)
        for i in range(len(self.body) - 1):
            self.body[i].x = self.body[i + 1].x
            self.body[i].y = self.body[i + 1].y

        # updating the location of the head
        self.head.x += self.xdir * BLOCK_SIZE
        self.head.y += self.ydir * BLOCK_SIZE
        self.body.remove(self.head)

        # checking for snake death
        global apple
        for square in self.body:
            if self.head.x == square.x and self.head.y == square.y:
                self.dead = True
            if self.head.x not in range(0, SCREEN_WIDTH) or self.head.y not in range(0, SCREEN_HEIGHT):
                self.dead = True
            if self.dead:
                self.x, self.y = BLOCK_SIZE * int(random.randint(0, SCREEN_WIDTH) / BLOCK_SIZE), BLOCK_SIZE * int(
                    random.randint(0, SCREEN_HEIGHT) / BLOCK_SIZE)
                self.xdir = 1  # by default the snake moves towards the right
                self.ydir = 0
                self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
                self.body = [pygame.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE,
                                         BLOCK_SIZE)]  # body of the snake is represented by a list
                self.dead = False
                apple = Apple()

class SnakeAI:
    def __init__(self):
        self.x, self.y = BLOCK_SIZE * int(random.randint(0, SCREEN_WIDTH) / BLOCK_SIZE), BLOCK_SIZE * int(
            random.randint(0, SCREEN_HEIGHT) / BLOCK_SIZE)
        self.xdir = 1  # by default the snake moves towards the right
        self.ydir = 0
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body = [pygame.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]  # body of the snake is represented by a list
        self.dead = False  # the snake starts off as alive
        self.len = 1 + len(self.body)
        self.selfallowance = [0, 0, 0]     #rlf
        self.wallallowance = [0, 0, 0]     #rlf

    def update(self):
        # first update the body
        self.body.append(self.head)
        for i in range(len(self.body) - 1):
            self.body[i].x = self.body[i + 1].x
            self.body[i].y = self.body[i + 1].y

        # updating the location of the head
        self.head.x += self.xdir * BLOCK_SIZE
        self.head.y += self.ydir * BLOCK_SIZE
        self.body.remove(self.head)

        

    # checking for snake death
    def checkdeath(self):
        for square in self.body:
            if self.head.x == square.x and self.head.y == square.y:
                self.dead = True
            if self.head.x not in range(0, SCREEN_WIDTH) or self.head.y not in range(0, SCREEN_HEIGHT):
                self.dead = True
            if self.dead:
                self.xdir = 0
                self.ydir = 0
                self.head.x, self.head.y = 0, 0
                for i, square in enumerate(self.body):
                    self.body.pop(i)

        return self.dead


class Apple:
    def __init__(self):
        self.x = BLOCK_SIZE * int(random.randint(0, SCREEN_WIDTH) / BLOCK_SIZE)
        self.y = BLOCK_SIZE * int(random.randint(0, SCREEN_HEIGHT) / BLOCK_SIZE)
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)

    def update(self):
        pygame.draw.rect(SCREEN, "red", self.rect)


# RUNNING = [pygame.image.load(os.path.join)]

# Running the game
def Game():
    pygame.display.set_caption("Snake")
    global snake
    snake = Snake()
    global apple
    apple = Apple()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    snake.ydir = 1
                    snake.xdir = 0
                elif event.key == pygame.K_UP:
                    snake.ydir = -1
                    snake.xdir = 0
                elif event.key == pygame.K_RIGHT:
                    snake.ydir = 0
                    snake.xdir = 1
                elif event.key == pygame.K_LEFT:
                    snake.ydir = 0
                    snake.xdir = -1

        snake.update()
        SCREEN.fill('black')
        Grid()
        apple.update()

        # draw snake head on the screen
        pygame.draw.rect(SCREEN, "green", snake.head)

        # draw snake body on the screen
        for square in snake.body:
            pygame.draw.rect(SCREEN, "green", square)

        # check if apple is eaten
        if snake.head.x == apple.x and snake.head.y == apple.y:
            snake.body.append(pygame.Rect(snake.head.x, snake.head.y, BLOCK_SIZE, BLOCK_SIZE))
            apple = Apple()

        pygame.display.update()
        clock.tick(10)

generation_count = 0

def eval_genomes(genomes, config):
    global generation_count
    pygame.display.set_caption('Snake AI, Generation : ' + str(generation_count))

    global snake, apples, ge, nets
    snakes = []
    apples = []
    ge = []
    nets = []

    for genome_id, genome in genomes:
        snakes.append(SnakeAI())
        apples.append(Apple())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0  # initial fitness of the snakes is zero

    max_score=0
    Run = True
    while Run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            for i, snake in enumerate(snakes):
                snake_score=0
                reqxdir, reqydir = 0, 0
                if (apples[i].x > snake.head.x):
                    reqxdir = 1
                if (apples[i].x < snake.head.x):
                    reqxdir = -1
                if (apples[i].x == snake.head.x):
                    reqxdir = 0
                if (apples[i].y > snake.head.y):
                    reqydir = 1
                if (apples[i].y < snake.head.y):
                    reqydir = -1
                if (apples[i].y == snake.head.y):
                    reqydir = 0


                # give input variables to the output function
                # input is: req xdir, req ydir, direction allowance wrt body, direction allowance wrt walls
                output = nets[i].activate((reqxdir,
                                           reqydir,
                                           snake.selfallowance[0],
                                           snake.selfallowance[1],
                                           snake.selfallowance[2],
                                           snake.wallallowance[0],
                                           snake.wallallowance[1],
                                           snake.wallallowance[2]))

                if output[0] == max(output) and snake.selfallowance[0] != 1:  # right
                    ge[i].fitness -= 5
                if output[1] == max(output) and snake.selfallowance[1] != 1:  # left
                    ge[i].fitness -= 5
                if output[2] == max(output) and snake.selfallowance[2] != -1:  # front
                    ge[i].fitness -= 5

                if output[0] == max(output):   # right
                    if snake.xdir == 1:
                        snake.xdir = 0
                        snake.ydir = -1
                    if snake.xdir == -1:
                        snake.xdir = 0
                        snake.ydir = 1
                    if snake.ydir == 1:
                        snake.xdir = 1
                        snake.ydir = 0
                    if snake.ydir == -1:
                        snake.xdir = -1
                        snake.ydir = 0
                if output[1] == max(output):  # left
                    if snake.xdir == 1:
                        snake.xdir = 0
                        snake.ydir = 1
                    if snake.xdir == -1:
                        snake.xdir = 0
                        snake.ydir = -1
                    if snake.ydir == 1:
                        snake.xdir = -1
                        snake.ydir = 0
                    if snake.ydir == -1:
                        snake.xdir = 1
                        snake.ydir = 0
                if output[2] == max(output):  # front
                    continue

            for i, snake in enumerate(snakes):
                snake_score=0


                if snake.checkdeath() == True:
                    ge[i].fitness -= 10
                    snakes.pop(i)
                    apples.pop(i)
                    nets.pop(i)
                    ge.pop(i)
                    i-=1

                    if len(snakes) == 0:
                        Run=False
                        break



                # check if apple is eaten
                if snake.head.x == apples[i].x and snake.head.y == apples[i].y and snake.dead == False:
                    ge[i].fitness += 50
                    snake_score+=1
                    max_score=max(max_score, snake_score)
                    snake.body.append(pygame.Rect(snake.head.x, snake.head.y, BLOCK_SIZE, BLOCK_SIZE))
                    apples[i] = Apple()

                snake.update()
                SCREEN.fill('black')
                Grid()
                apples[i].update()

                # draw snake head on the screen
                pygame.draw.rect(SCREEN, "green", snake.head)

                # draw snake body on the screen
                for square in snake.body:
                    pygame.draw.rect(SCREEN, "green", square)



            show_score(1, pygame.Color(255, 255, 255), 'comic sans', 20, max_score)
            pygame.display.update()
            clock.tick(60)

        generation_count += 1

# Setup the NEAT

def run(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    pop = neat.Population(config)  # generate a population based on the config file
    pop.run(eval_genomes, 50)  # calls the game 50 times and pass in the generated populations


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)
