import sys, pygame, random, time
from ww import *
pygame.init()


ww=Stage(20, 20, 24)
ww.set_player(KeyboardPlayer("icons/mario_front.png", ww))
ww.add_actor(Wall("icons/wall.jpg", ww, 3, 4))

# Instances of all the type of monsters.
ww.add_actor(Monster("icons/Mushroom.png", ww, 7, 4, 5))
ww.add_actor(boxEater("icons/ghost.png", ww, 7, 10, 5))
ww.add_actor(invisibleMonster(ww, 10, 10, 5))
ww.add_actor(camouflageMon("icons/Bob-omb.png", ww, 1, 6, 5))
# Instance of stickyBox
ww.add_actor(stickyBox("icons/open-box.png", ww, 1, 1))

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

# Clock to update the screen
clock = pygame.time.Clock()
# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)    
font = pygame.font.SysFont("comicsansms", 72)
font2 = pygame.font.SysFont("comicsansms", 20)
intro = font.render("Warehouse Wars", True, (WHITE))
controls = font2.render("Contols: Arrows for UP DOWN RIGT LEFT, Keys: ASZX for diagonal.", True, (255, 255, 255))
start = font2.render("Click to Start.", True, (BLACK))
display_instructions = True
start_screen = 'start'
done = False

# Display start screen and the game instructions.
while not done and display_instructions:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_screen == 'start':
                display_instructions = False
    if start_screen == 'start':
        height = ww.get_picel_height()
        width = ww.get_pixel_width()
        ww._screen.fill((53, 102, 149))
        ww._screen.blit(intro,[0, 0])
        ww._screen.blit(controls,[0, height/3])
        ww._screen.blit(start,[0, height/2])

    # Limit to 60 frames per second
    clock.tick(60)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Pygame text/font
gameOver = font.render("Game Over", True, (0, 128, 0))
won = font.render("You Won", True, (0, 128, 0))
# init game_over, all_mon_dead vars.
game_over = False
all_mon_dead = False
# Get the number of Actors on the stage.
length_of_actors_lst = len(ww.get_actors())
# Refreshes the pygame everytime a move is made by the Actors
while not game_over:
    pygame.time.wait(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
                ww.player_event(event.key)
    actors_lst = ww.get_actors()
    num_inviMon = 0
    num_wall = 0
    num_box = 0
    # Loop to count the total monsters.
    for monster in actors_lst:
        if isinstance(monster, invisibleMonster):
            num_inviMon += 1
    # Loop to count the total walls.
    for wall in actors_lst:
        if isinstance(wall, Wall):
            num_wall += 1
    # Loop tp count the total Boxs
    for box in actors_lst:
        if isinstance(box, Box):
            num_box += 1
    ww.step()
    ww.draw()
    # Check if the player won
    if len(actors_lst) == num_box+num_inviMon+num_wall+1:
        ww._screen.fill((0, 0, 0))
        # Display the You Won screen.
        ww._screen.blit(won,[5, height/2])
        game_over = True
    if any(isinstance(actor, Player) for actor in actors_lst):
        pass 
    else:
        # Display the gameOver screen
        ww._screen.fill((0, 0, 0))
        ww._screen.blit(gameOver,[5, height/2])   
        game_over = True 
    pygame.display.flip()
