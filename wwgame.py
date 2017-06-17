import sys, pygame, random
from ww import *
pygame.init()

ww=Stage(20, 20, 24)
ww.set_player(KeyboardPlayer("icons/face-cool-24.png", ww))

ww.add_actor(Wall("icons/wall.jpg", ww, 3, 4))

#ww.add_actor(Monster("icons/face-devil-grin-24.png", ww, 0, 3, 1))
#ww.add_actor(Monster("icons/face-devil-grin-24.png", ww, 7, 4, 5))
#ww.add_actor(Monster("icons/face-devil-grin-24.png", ww, 4, 10, 3))
ww.add_actor(Monster("icons/face-devil-grin-24.png", ww, 5, 20, 2))

# YOUR COMMENT GOES HERE. BRIEFLY DESCRIBE WHAT THE FOLLOWING LOOP DOES.
# Used to create boxes
# while the number of boxes is less than 100,
# Get random x and random y
# If the random x and y doesn't have a box, then add a box on the stage at
# those  coordinates.
num_boxes=0
while num_boxes<100:
    x=random.randrange(ww.get_width())
    y=random.randrange(ww.get_height())
    if ww.get_actor(x,y) is None:
        ww.add_actor(Box("icons/emblem-package-2-24.png", ww, x, y))
        num_boxes+=1
        
# HIDDEN Danger:
ran_x=random.randrange(ww.get_width())
ran_y=random.randrange(ww.get_height())



# Clock to update the screen
clock = pygame.time.Clock()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

font = pygame.font.SysFont('comicsansms', 36)
display_instructions = True
start_screen = 1
done = False
# Display start screen and the game instructions.
while not done and display_instructions:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            #instruction_page += 1
            if start_screen == 1:
                display_instructions = False
 
    #ww._screen.fill(BLACK)

    if start_screen == 1:
        text = font.render("Warehouse Wars", True, WHITE)
        ww._screen.blit(text, [10, 10])
 
        text = font.render("Page 1", True, WHITE)
        ww._screen.blit(text, [10, 40])
 
    # Limit to 60 frames per second
    clock.tick(60)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()





# YOUR COMMENT GOES HERE. BRIEFLY DESCRIBE WHAT THE FOLLOWING LOOP DOES.
# Refreshes the pygame everytime a move is made by the player.
while True:
    pygame.time.wait(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
                ww.player_event(event.key)
              
    ww.step()
    ww.draw()
