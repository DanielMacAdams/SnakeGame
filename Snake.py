#
# Tom's Pong
# A simple pong game with realistic physics and AI
# http://tomchance.org.uk/projects/pong
#
# Released under the GNU General Public License

VERSION = "0.4"

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
WIDTH = 800
HEIGHT = 800

try:
    import sys
    import random
    import math
    import os
    import getopt
    import pygame
    from socket import *
    from pygame.locals import *
except ImportError:
    print(f"couldn't load module. {ImportError}")
    sys.exit(2)

def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join("", name)
    print(fullname)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except FileNotFoundError:
        print(f"Cannot load image: {fullname}")
        raise SystemExit
    return image

def reset_game():
    pass

class Apple():
    """The apple that the snake eats, will relocate itself to a random part of
    screen that is not occupied by the snake"""

    def __init__(self):
        self.image = load_png('apple.png')
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.location = (0, 0)

    def update_location(self, x, y):
        temp_list = list(self.location)
        temp_list[0] = x
        temp_list[1] = y
        self.location = tuple(temp_list)


class Snake():
    """The body of the snake, what the player controls
    """

    def __init__(self):
        self.image = load_png('body.png')
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.head_pos = (HEIGHT/2, WIDTH/2)
        self.tail_pos = (HEIGHT/2, WIDTH/2) #will always be popped from back of array queue
        print(f"rect:{self.rect}")
        self.body_array = [self.head_pos] #will be treated like a queue
        self.direction = UP

    def update_head_tail(self):
        temp_list = list(self.head_pos)

        self.tail_pos = self.body_array[-1] #last element of list
        if self.direction == UP:
            temp_list[1] -= self.rect.height
        elif self.direction == DOWN:
            temp_list[1] += self.rect.height
        elif self.direction == LEFT:
            temp_list[0] -= self.rect.height
        elif self.direction == RIGHT:
            temp_list[0] += self.rect.height
        
        self.head_pos = tuple(temp_list)


def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((HEIGHT, WIDTH))
    pygame.display.set_caption("Snake Game")

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((100, 150, 50))

    # Initialise player
    global player
    player = Snake()

    #Initialise apple
    global appl
    appl = Apple()
    appl.update_location(player.head_pos[0] + 120, player.head_pos[1])

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    screen.blit(appl.image, appl.location)
    screen.blit(player.image, (HEIGHT/2, WIDTH/2))
    pygame.display.flip()

    # Initialise clock
    clock = pygame.time.Clock()

    #create timer for graphic updates
    timer = 0

    # Event loop
    while True:
        # Make sure game doesn't run at more than 60 frames per second
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                if event.key == K_UP and not player.direction == DOWN:
                    player.direction = UP
                if event.key == K_DOWN and not player.direction == UP:
                    player.direction = DOWN
                if event.key == K_LEFT and not player.direction == RIGHT:
                    player.direction = LEFT
                if event.key == K_RIGHT and not player.direction == LEFT:
                    player.direction = RIGHT

        
        #crude collision detection, snake eats apple


            #reset_game()

        if player.head_pos == appl.location and timer == 5:

            #remove apple from screen and spawn new apple
            old_location = appl.location
            x = random.randrange(0, WIDTH - player.rect.width, player.rect.width)
            y = random.randrange(0, HEIGHT - player.rect.width, player.rect.width)
            appl.update_location(x, y)


            #all we do differently is not blit background over the tail position
            
            #update the body_array to account for the new body segment
            player.update_head_tail() #gets new head position
            player.body_array.insert(0, player.head_pos)

            screen.blit(player.image, old_location, area=player.rect)
            screen.blit(player.image, player.head_pos)
            screen.blit(background, player.tail_pos, area=player.rect)
            screen.blit(appl.image, appl.location)
            pygame.display.flip()
            timer = 0

            #note, if the player is not eating an apple in this loop
            # we must insert new head position to front of list, and remove
            # the tail position

        #update the snake
        elif timer == 5:

            player.update_head_tail()
            player.body_array.insert(0, player.head_pos)
            player.body_array.pop() #remove last element from body array, which is the tail

            #player.tail position still tracks old tail

            screen.blit(player.image, player.head_pos)
            screen.blit(background, player.tail_pos, area=player.rect)
            pygame.display.flip()
            timer = 0
        else:
            timer += 1

        self_collide = player.body_array.count(player.head_pos)
        if self_collide > 1:
            return

if __name__ == "__main__":
    main()