# csc148_a1

import pygame, random, time

class Actor:
    '''
    Represents an Actor in the game. Can be the Player, a Monster, boxes, wall.
    Any object in the game's grid that appears on the stage, and has an
    x- and y-coordinate.
    '''

    def __init__(self, icon_file, stage, x, y, delay=5):
        '''
        (Actor, str, Stage, int, int, int) -> None
        Given the name of an icon file (with the image for this Actor),
        the stage on which this Actor should appear, the x- and y-coordinates
        that it should appear on, and the speed with which it should
        update, construct an Actor object.
        '''

        self._icon = pygame.image.load(icon_file) # the image image to display of self
        self.icon = icon_file
        self.set_position(x, y) # self's location on the stage
        self._stage = stage # the stage that self is on

        # the following can be used to change this Actors 'speed' relative to other
        # actors speed. See the delay method.
        self._delay = delay
        self._delay_count = 0
    def change_icon(self, icon_file):
        self._icon = pygame.image.load(icon_file)
        return self._icon

    def set_position(self, x, y):
        '''
        (Actor, int, int) -> None
        Set the position of this Actor to the given x- and y-coordinates.
        '''
        
        (self._x, self._y) = (x, y)

    def get_position(self):
        '''
        (Actor) -> tuple of two ints
        Return this Actor's x and y coordinates as a tuple.
        '''
        
        return (self._x, self._y)

    def get_icon(self):
        '''
        (Actor) -> pygame.Surface
        Return the image associated with this Actor.
        '''

        return self._icon

    def is_dead(self):
        '''
        (Actor) -> bool
        Return True iff this Actor is not alive.
        '''
        
        return True

    def move(self, other, dx, dy):
        '''
        (Actor, Actor, int, int) -> bool

        Other is an Actor telling us to move in direction (dx, dy). In this case, we just move.
        (dx,dy) is in {(1,1), (1,0), (1,-1), (0,1), (0,0), (0,-1), (-1,1), (-1,0), (-1,-1)}
    
        In the more general case, in subclasses, self will determine 
        if they will listen to other, and if so, will try to move in
        the specified direction. If the target space is occupied, then we 
        may have to ask the occupier to move.
        '''

        self.set_position(self._x + dx, self._y + dy)
        return True

    def delay(self):
        '''
        (Actor) -> bool
        Manage self's speed relative to other Actors. 
        Each time we get a chance to take a step, we delay. If our count wraps around to 0
        then we actually do something. Otherwise, we simply return from the step method.
        '''

        self._delay_count = (self._delay_count+1) % self._delay
        return self._delay_count == 0

    def step(self):
        '''
        (Actor) -> None
        Make the Actor take a single step in the animation of the game.
        self can ask the stage to help as well as ask other Actors
        to help us get our job done.
        '''

        pass

class Player(Actor):
    '''
    A Player is an Actor that can handle events. These typically come
    from the user, for example, key presses etc.
    '''

    def __init__(self, icon_file, stage, x=0, y=0):
        '''
        (Player, str, Stage, int, int) -> None
        Construct a Player with given image, on the given stage, at
        x- and y- position.
        '''
        
        Actor.__init__(self, icon_file, stage, x, y)

    def handle_event(self, event):
        '''
        Used to register the occurrence of an event with self.
        '''
        pass

class KeyboardPlayer(Player):
    '''
    A KeyboardPlayer is a Player that can handle keypress events.
    '''
    
    def __init__(self, icon_file, stage, x=0, y=0):
        '''
        Construct a KeyboardPlayer. Other than the given Player information,
        a KeyboardPlayer also keeps track of the last key event that took place.
        '''
        
        Player.__init__(self, icon_file, stage, x, y)
        self._last_event = None # we are only interested in the last event
        self._teleport_times = 0 # Keep track of the number of time the player
        # been transported.

    def handle_event(self, event):
        '''
        (KeyboardPlayer, int) -> None
        Record the last event directed at this KeyboardPlayer.
        All previous events are ignored.
        '''

        self._last_event = event

    def step(self):
        '''
        (KeyboardPlayer) -> None
        Take a single step in the animation. 
        For example: if the user asked us to move right, then we do that.
        '''
        # Use keyboard keys for player movement.
        if self._last_event is not None:
            dx, dy = None, None
            if self._last_event == pygame.K_DOWN:
                dx, dy = 0,1
            if self._last_event == pygame.K_LEFT:
                self.change_icon("icons/mario-left.png")
                dx, dy = -1,0
            if self._last_event == pygame.K_RIGHT:
                self.change_icon("icons/mario-right.png")
                dx, dy = 1,0
            if self._last_event == pygame.K_UP:
                dx, dy = 0,-1
            if self._last_event == pygame.K_a:
                dx, dy = -1, -1
            if self._last_event == pygame.K_s:
                dx, dy = 1, -1     
            if self._last_event == pygame.K_x:
                dx, dy = 1, 1     
            if self._last_event == pygame.K_z:
                dx, dy = -1, 1
            # Transport the player at a random coor.
            if self._last_event == pygame.K_t and self._teleport_times < 3:
                x=random.randrange(self._stage.get_width())
                y=random.randrange(self._stage.get_height())
                actor = self._stage.get_actor(x,y)
                # Check if the random spot if avaible
                if actor == None:
                    self.set_position(x,y)
                self._teleport_times += 1
            if dx is not None and dy is not None:
                self.move(self, dx, dy) # we are asking ourself to move

            self._last_event = None

    def move(self, other, dx, dy):
        '''
        (Actor, Actor, int, int) -> bool
        Move this Actor by dx and dy, if possible. other is the Actor that asked to make this move.
        If a move is possible (a space is available) then move to it and return True.
        If another Actor is occupying that space, ask that Actor to move to make space, and then
        move to that spot, if possible.
        If a move is not possible, then return False.
        '''

        # Where we are supposed to move. 
        new_x = self._x + dx
        new_y = self._y + dy

        # Get the current stage
        current_stage = self._stage
        on_stage = current_stage.is_in_bounds(new_x, new_y)
        # Get the actor at the curr x and y value.
        check_coor = current_stage.get_actor(new_x, new_y)
 
        # FIX THIS ACCORDING TO LAB INSTRUCTIONS IN PART 1
        # TODO: Check if (new_x, new_y) is on the stage. DONE
        #       If it is, then determine if another Actor is occupying that spot. If so,
        #       self asks them to move. If they moved, then we can occupy the spot. Otherwise
        #       we can't move. We return True if we moved and False otherwise.
        # If the spot if avaible, move the actor.
        if on_stage and check_coor == None :
            res = True
            Actor.move(self, other, dx, dy)
        # Check if the moved to Monster's spot.
        elif (check_coor is not None) and on_stage and isinstance(check_coor, Monster) and not isinstance(check_coor,invisibleMonster):
            # Set self.is_dead to True since the player is dead
            self.is_dead = True
            res = False
            # Remove the actor from the stage.
            self._stage.remove_actor(self)
        # If the spot if not aviable, ask the actor to move if possible.
        elif (check_coor is not None) and on_stage and isinstance(check_coor, Box): 
            # Move the other actors
            check_coor.move(self, dx, dy)
            check_coor = current_stage.get_actor(new_x, new_y)
            if(check_coor == None):
                # Move the player after the spot is avaible.
                Actor.move(self, other, dx, dy)
                # set the res to True
                res = True
            else:
                # Set the res to False, because menaing the move didn't happen.
                res = False     
        else:
            res = False
        # Return res
        return res


class Box(Actor):
    '''
    A Box Actor.
    '''
    
    def __init__(self, icon_file, stage, x=0, y=0):
        '''
        (Actor, str, Stage, int, int) -> None
        Construct a Box on the given stage, at given position.
        '''
        
        Actor.__init__(self, icon_file, stage, x, y)  

    def move(self, other, dx, dy):
        '''
        (Actor, Actor, int, int) -> bool
        Move this Actor by dx and dy, if possible. other is the Actor that asked to make this move.
        If a move is possible (a space is available) then move to it and return True.
        If another Actor is occupying that space, ask that Actor to move to make space, and then
        move to that spot, if possible.
        If a move is not possible, then return False.
        '''
        # Get the new x and y value
        new_x = self._x + dx
        new_y = self._y + dy
        # Get the current stage.
        current_stage = self._stage
        on_stage = current_stage.is_in_bounds(new_x, new_y)
        
        check_coor = current_stage.get_actor(new_x, new_y)

        if on_stage and check_coor == None:
            # Set the res to True
            res = True
            Actor.move(self, other, dx, dy)
        # If the space is occupied, Ask the Actor to move.
        elif (check_coor is not None) and on_stage and isinstance(check_coor, Box):
            # Move the other actors
            check_coor.move(self, dx, dy)
            check_coor = current_stage.get_actor(new_x, new_y)
            if(check_coor == None):
                Actor.move(self, other, dx, dy)
                res = True
            else:
                # Set the res to False, because menaing the move didn't happen.
                res = False
        else:
            res = False
        # Return the res
        return res


class stickyBox(Box):
    '''
    A special type of Box Actor.
    '''
    def __init__(self, icon_file, stage, x=0, y=0):
        '''
        (Actor, str, Stage, int, int) -> None
        Construct a stickyBox on the given stage, at given position.
        '''
        Box.__init__(self, icon_file, stage, x, y)
        
    def move(self, other, dx, dy):
        # get the x and y values.
        new_x = self._x + dx
        new_y = self._y + dy
        # Check the actor at the new_x and new_y value
        actor = self._stage.get_actor(new_x, new_y)
        # Check if the actor is a Monster type
        if isinstance(actor, Monster):
            # Change self icon to a different icon.
            self.change_icon("icons/close_box.png")
            # Move to the spot where the Monster currently is.
            Actor.move(self, other, dx, dy)
            actor.inside_stickyBox= True
        else:
            Box.move(self, other, dx, dy)
            self.change_icon("icons/open-box.png")


# COMPLETE THIS CLASS FOR PART 2 OF LAB
class Wall(Actor): 
    '''
    Construct a Wall on the given stage, at given position.
    '''
    def __init__(self, icon_file, stage, x, y):
        '''(Actor, str, Stage, int, int) -> None
        '''
        Actor.__init__(self, icon_file, stage, x, y) 


class Stage:
    '''
    A Stage that holds all the game's Actors (Player, monsters, boxes, etc.).
    '''
    
    def __init__(self, width, height, icon_dimension):
        '''Construct a Stage with the given dimensions.'''
        
        self._actors = [] # all actors on this stage (monsters, player, boxes, ...)
        self._player = None # a special actor, the player

        # the logical width and height of the stage
        self._width, self._height = width, height

        self._icon_dimension=icon_dimension # the pixel dimension of all actors
        # the pixel dimensions of the whole stage
        self._pixel_width = self._icon_dimension * self._width
        self._pixel_height = self._icon_dimension * self._height
        self._pixel_size = self._pixel_width, self._pixel_height

        # get a screen of the appropriate dimension to draw on
        self._screen = pygame.display.set_mode(self._pixel_size)
        # Window title
        pygame.display.set_caption("Warehouse Wars")

    def is_in_bounds(self, x, y):
        '''
        (Stage, int, int) -> bool
        Return True iff the position (x, y) falls within the dimensions of this Stage.'''

        return self.is_in_bounds_x(x) and self.is_in_bounds_y(y)

    def is_in_bounds_x(self, x):
        '''
        (Stage, int) -> bool
        Return True iff the x-coordinate given falls within the width of this Stage.
        '''

        return 0 <= x and x < self._width

    def is_in_bounds_y(self, y):
        '''
        (Stage, int) -> bool
        Return True iff the y-coordinate given falls within the height of this Stage.
        '''

        return 0 <= y and y < self._height

    def get_width(self):
        '''
        (Stage) -> int
        Return width of Stage.
        '''

        return self._width

    def get_height(self):
        '''
        (Stage) -> int
        Return height of Stage.
        '''
        
        return self._height


    def get_pixel_width(self):
        '''(Stage) -> int
        Return width of stage in pixel
        '''
        return self._icon_dimension * self._width
    
    def get_picel_height(self):
        '''(stage) -> int
        Return height of stage in pixel
        '''
        return self._icon_dimension * self._height


    def set_player(self, player):
        '''
        (Stage, Player) -> None
        A Player is a special actor, store a reference to this Player in the attribute
        self._player, and add the Player to the list of Actors.
        '''
        
        self._player=player
        self.add_actor(self._player)

    def remove_player(self):
        '''
        (Stage) -> None
        Remove the Player from the Stage.
        '''
        
        self.remove_actor(self._player)
        self._player=None

    def player_event(self, event):
        '''
        (Stage, int) -> None
        Send a user event to the player (this is a special Actor).
        '''
        
        self._player.handle_event(event)

    def add_actor(self, actor):
        '''
        (Stage, Actor) -> None
        Add the given actor to the Stage.
        '''

        self._actors.append(actor)

    def remove_actor(self, actor):
        '''
        (Stage, Actor) -> None
        Remove the given actor from the Stage.
        '''

        self._actors.remove(actor)

    def step(self):
        '''
        (Stage) -> None
        Take one step in the animation of the game. 
        Do this by asking each of the actors on this Stage to take a single step.
        '''

        for a in self._actors:
            a.step()

    def get_actors(self):
        '''
        (Stage) -> None
        Return the list of Actors on this Stage.
        '''

        return self._actors

    def get_actor(self, x, y):
        '''
        (Stage, int, int) -> Actor or None
        Return the first actor at coordinates (x,y).
        Or, return None if there is no Actor in that position.
        '''
        
        for a in self._actors:
            if a.get_position() == (x,y):
                return a
        return None

    def draw(self):
        '''
        (Stage) -> None
        Draw all Actors that are part of this Stage to the screen.
        '''

        self._screen.fill((0,0,0)) # (0,0,0)=(r,g,b)=black
        for a in self._actors:
            icon = a.get_icon()
            (x,y) = a.get_position()
            d = self._icon_dimension
            rect = pygame.Rect(x*d, y*d, d, d)
            self._screen.blit(icon, rect)
        pygame.display.flip()


class Monster(Actor):
    '''A Monster class.'''
    
    def __init__(self, icon_file, stage, x=0, y=0, delay=5):
        '''Construct a Monster.'''
        
        Actor.__init__(self, icon_file, stage, x, y, delay)
        self._dx = 1
        self._dy = 1
        self.inside_stickyBox = False


    def step(self):
        '''
        Take one step in the animation (this Monster moves by one space).
        If it's being delayed, return None. Else, return True.
        '''
        # Get the current Stage.
        curr_stage = self._stage
        # Check if the monster is dead.
        if self.is_dead():
            # Remove the monster from the stage.
            curr_stage.remove_actor(self)
        if not self.delay() and not self.inside_stickyBox: return 
        self.move(self, self._dx, self._dy)
        if self.inside_stickyBox:
            # If its in the stickyBox, Don't do anything.
            pass
        return True


    def move(self, other, dx, dy):
        '''
        (Actor, Actor, int, int) -> bool
        Move this Actor by dx and dy, if possible. other is the Actor that asked to make this move.
        If a move is possible (a space is available) then move to it and return True.
        If another Actor is occupying that space, or if that space is out of bounds,
        bounce back in the opposite direction.
        If a bounce back happened, then return False.
        '''
 
        if other != self: # Noone pushes me around
            return False
        # Set bounce_off_edge to False
        bounce_off_edge = False
        # Check if the monster is dead
        is_dead = self.is_dead()
        # Get the current values of x and y
        new_x = self._x + self._dx
        new_y = self._y + self._dy
        # Check if its inside the stickyBox
        if self.inside_stickyBox:
            # Do nothing
            pass
        else:
            # Get the actor at the current position
            actor = self._stage.get_actor(new_x, new_y)
            # Check if the new position is a Player
            if isinstance(actor, KeyboardPlayer):
                # Remove the player from the stage
                self._stage.remove_actor(actor)
                # Set is_dead to True
                actor.is_dead = True
            if not self._stage.is_in_bounds_x(new_x) or actor != None:
                # Set the x value to opposite direction
                self._dx =-self._dx
                bounce_off_edge=True
            if not self._stage.is_in_bounds_y(new_y) or actor != None:
                # Set the y value to opposite direction
                self._dy =- self._dy
                bounce_off_edge = True
            else:
                # Move the actor
                return Actor.move(self, other, dx, dy)
            # Check if bounce off happend.
            if bounce_off_edge: 
                return False    


    def is_dead(self):
        '''
        Return whether this Monster has died.
        That is, if self is surrounded on all sides, by either Boxes or
        other Monsters.'''

        # TODO: This is part of the assignment and not yet required for the lab.
        # If you have extra time in lab, feel free to get working on this.
        # Set a var is_dead to False
        is_dead = False
        curr_position = self.get_position()
        x_value = curr_position[0]
        y_value = curr_position[1]

        # Check for boxes around the monster.
        actor1 = self._stage.get_actor(x_value-1, y_value)
        actor2 = self._stage.get_actor(x_value+1, y_value)
        actor3 = self._stage.get_actor(x_value, y_value-1)
        actor4 = self._stage.get_actor(x_value, y_value+1)
        actor5 = self._stage.get_actor(x_value+1, y_value+1)
        actor6 = self._stage.get_actor(x_value-1, y_value+1)
        actor7 = self._stage.get_actor(x_value+1, y_value-1)
        actor8 = self._stage.get_actor(x_value-1, y_value-1)
        # Check all the conditions.
        if(actor1 and actor2 and actor3 and actor4 and actor5 and actor6 and actor7 and actor8) != None:
            # Set is-dead to True
            is_dead = True
            # Set self is deaad
            Actor.is_dead = True
        # Return is_dead
        return is_dead


class boxEater(Monster):
    '''A special Monster class.
    Monster thats eats boxs.
    '''

    def __init__(self, icon_file, stage, x=0, y=0, delay=5):
        '''Construct a boxEater.'''

        Monster.__init__(self, icon_file, stage, x, y, delay)
        self._dx = 1
        self._dy = 1
        # Keeps the number of boxes it has eaten so far.
        self._num_boxes = 0


    def move(self, other, dx, dy):
        # Get the new x and y values
        new_x = self._x + dx
        new_y = self._y + dy
        # Get the actor at the new x and y values.
        actor = self._stage.get_actor(new_x, new_y)
        # check if self._num_boxes is less than 10
        # Check if the current spot is a box
        if isinstance(actor, Box) and self._num_boxes <= 10:
            self.change_icon("icons/ghost.png")
            Monster.move(self, other, dx, dy)
            # remove the box from the stage
            self._stage.remove_actor(actor)
            self._num_boxes += 1
        else:
            # Just move around
            Monster.move(self, other, dx, dy)
            self.change_icon("icons/ghost.png")


class camouflageMon(Monster):
    '''A special Monster class.'''
    
    def __init__(self, icon_file, stage, x=0, y=0, delay=5):
        '''Construct a CamouflageMon.'''
        Monster.__init__(self, icon_file, stage, x, y, delay)
        self._dx = 1
        self._dy = 1
        self._counter = 0
        self.camoflaged = False


    def move(self, other, dx, dy):
        timer = self._counter % 20
        # Check if timer remanider is 0
        if timer is not 0:
            # Change the icon
            self.change_icon("icons/emblem-package-2-24.png")
            # Set self.comoflaged = True
            self.camoflaged = True
            # Increase the self._counter by 1
            self._counter += 1
        else:
            # Move the monster
            Monster.move(self, other, dx, dy)
            # Change the icon
            self.change_icon("icons/Bob-omb.png")
            # Increase the self._counter by 1
            self._counter += 1


class invisibleMonster(Monster):
    '''A special Monster class.
    Invisible to the player, But its there.
    '''
    
    def __init__(self,stage, x=0, y=0, delay=5):
        '''(Actor, Stage, int, int, int) - None
        Construct a invisibleMonster.
        '''

        Monster.__init__(self,'icons/inviMon.jpg', stage, x, y, delay)
        # Monster.__init__(self,'icons/white.jpg', stage, x, y, delay)
        self._dx = 1
        self._dy = 1

    def move(self, other, dx, dy):
        '''(Actor, Actor, int, int) -> None'''
        # Get the current position fo the monster.
        new_x = self._x + dx
        new_y = self._x + dy
        actor = self._stage.get_actor(new_x, new_y)
        zeroZero_pos = self._stage.get_actor(0, 0)
        if isinstance(actor, KeyboardPlayer):
            # Check if (0,0) is empty or not.
            if zeroZero_pos != None:
                # Get random x and y values
                x=random.randrange(self._stage.get_width())
                y=random.randrange(self._stage.get_height())
                # Move the player to random (x,y) position
                actor.set_position(x,y)
            else:
                # Set the player's position to (0,0)
                actor.set_position(0,0)
        else:
            # Move around
            Monster.move(self, other, dx, dy)
            
            
            
     #####################################################################################################################
     
     import sys, pygame, random, time
from ww import *
pygame.init()


ww=Stage(20, 20, 24)
ww.set_player(KeyboardPlayer("icons/mario_front.png", ww))
ww.add_actor(Wall("icons/wall.jpg", ww, 3, 4))

# Monsters
ww.add_actor(Monster("icons/Mushroom.png", ww, 7, 4, 5))
ww.add_actor(boxEater("icons/ghost.png", ww, 7, 10, 5))
ww.add_actor(invisibleMonster(ww, 10, 10, 5))
ww.add_actor(camouflageMon("icons/Bob-omb.png", ww, 1, 6, 5))

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
intro = font.render("Warehouse Wars", True, (255,255,240))
controls = font2.render("Contols: Arrows for UP DOWN RIGT LEFT, Keys: ASZX for diagonal.", True, (255, 255, 255))
start = font2.render("Click to Start.", True, (0,0,0))
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


gameOver = font.render("Game Over", True, (0, 128, 0))
won = font.render("You Won", True, (0, 128, 0))
# Refreshes the pygame everytime a move is made by the player.
game_over = False
all_mon_dead = False
length_of_actors_lst = len(ww.get_actors())
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
    for monster in actors_lst:
        if isinstance(monster, invisibleMonster):
            num_inviMon += 1
    for wall in actors_lst:
        if isinstance(wall, Wall):
            num_wall += 1
    for box in actors_lst:
        if isinstance(box, Box):
            num_box += 1
    ww.step()
    ww.draw()
    if len(actors_lst) == num_box+num_inviMon+num_wall+1:
        ww._screen.fill((0, 0, 0))
        ww._screen.blit(won,[5, height/2])
        print('works')
        game_over = True
    if any(isinstance(actor, Player) for actor in actors_lst):
        pass 
    else:
        ww._screen.fill((0, 0, 0))
        ww._screen.blit(gameOver,[5, height/2])   
        game_over = True 
    pygame.display.flip()
