### Importing and initialising libraries

import pygame
import random
import time
pygame.font.init()
pygame.mixer.init()
from pygame.locals import *


### Constants

SCREEN_WIDTH = 416
SCREEN_HEIGHT = 608

BUTTON_WIDTH = 180
BUTTON_HEIGHT = 80

SMALL_BUTTON_WIDTH = 120
SMALL_BUTTON_HEIGHT = 53.3

SWITCH_SIZE = (60,60)

WHITE = (255,255,255)
GREY = (200,200,200)
BLACK = (0,0,0)

STONE_COLOUR = (169, 169, 169)
STONE_ACCENTS = (128, 128, 128)

SCOREBOARD_HEIGHT = 50

EXTRA_PADDING = 10
PADDING_X = 156
PADDING_Y = 156

BORDER_PADDING = 10
BORDER_THICKNESS = 4

GEM_WIDTH = 43
GEM_HEIGHT = 43

TEXT_SPEED = 30

### Secondary variables

screen_size = (SCREEN_WIDTH , SCREEN_HEIGHT + SCOREBOARD_HEIGHT)
screen_center = (SCREEN_WIDTH / 2 , (SCREEN_HEIGHT + SCOREBOARD_HEIGHT) / 2)

board_width = SCREEN_WIDTH - PADDING_X
board_height = SCREEN_HEIGHT - PADDING_Y

offset_x = (SCREEN_WIDTH - board_width) // 2
offset_y = (SCREEN_HEIGHT - board_height) // 2 - 10

score = 0
moves = 3
total_moves = 0

player_input_name = ""

current_question = ""
correct_answer = ""
user_answer = ""
input_box = pygame.Rect(300, 500, 200, 40)
input_color = (255, 255, 255)
question_start_time = None


gem_colours = ["blue", "green", "orange", "pink", "purple", "red", "teal"]
gem_size = (GEM_WIDTH,GEM_HEIGHT)

clicked_gem = None
swapped_gem = None

click_x = None
click_y = None

last_update = pygame.time.get_ticks()

text_index = 0
letter_index = 0
tutorial_dialogue = [
    "Adventurer?",
    "Good I needed someone for manual labour...",
    "I mean help of course!",
    "You wouldn't leave someone in need of help right?",
    "It's simple really, answer the questions correctly to get moves",
    "Then match three or more of those gems so they fall down",
    "We'll split the profits of course, let's say....",
    "90 to 10?",
    "What do you mean that's unfair??"

]

### Initialising the screen

screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Math Blast")

### Function For Loading Assets

def load_and_scale_image(path, dimensions):

    image = pygame.transform.smoothscale(pygame.image.load(path), dimensions)

    return image

############################# Loading Assets ################################

## Menu Screen Assets

menu_background = load_and_scale_image("Fantasy Background 2.png", screen_size)
menu_title = load_and_scale_image("Math Blast Title.png",(480,screen_center[1]))

## Options Screen Assets

options_button = load_and_scale_image("Options Button 2.png",(30,30))
options_button_hover = load_and_scale_image("Options Button 3.png",(30,30))

open_switch = load_and_scale_image("Switch(1)(1).png",(SWITCH_SIZE))
closed_switch = load_and_scale_image("Switch(1)(2).png", (SWITCH_SIZE))

## Gameplay Assets

game_background = load_and_scale_image("Game_Background(2).jpg", (screen_size))
text_box = load_and_scale_image("Text_box.png",(350,130))



### Creating and positioning Rects

## Menu Screen Rects

menu_background_rect = menu_background.get_rect(topleft =(0,0))
menu_title_rect = menu_title.get_rect(center = (screen_center[0], 150))

play_button_rect = pygame.Rect(0,0, BUTTON_WIDTH, BUTTON_HEIGHT)
play_rect = pygame.Rect(0,0, BUTTON_WIDTH, BUTTON_HEIGHT)

play_button_rect.center = (screen_center[0],(0.725 * (SCREEN_HEIGHT + SCOREBOARD_HEIGHT)))
play_rect.center = play_button_rect.center # Binding the play text to the button so they move together.

options_button_rect = options_button.get_rect(bottomright=(406,598))

## Option Screen Rects

#Positioned the options screen offscreen initially. 

done_button_rect = pygame.Rect(0,0, SMALL_BUTTON_WIDTH, SMALL_BUTTON_HEIGHT)
done_button_rect.midright = (0,430)
done_text_rect = pygame.Rect(0,0, SMALL_BUTTON_WIDTH, SMALL_BUTTON_HEIGHT)
done_text_rect.center = done_button_rect.center

tutorial_text_rect = pygame.Rect(0,0, BUTTON_WIDTH, BUTTON_HEIGHT)
music_text_rect = pygame.Rect(0,0, BUTTON_WIDTH, BUTTON_HEIGHT)
sound_fx_text_rect = pygame.Rect(0,0, BUTTON_WIDTH, BUTTON_HEIGHT)

tutorial_text_rect.center = (0, 180)
music_text_rect.center = (0, 270)
sound_fx_text_rect.center = (0, 360)

tutorial_switch_rect = open_switch.get_rect(midright=(0,180)) 
music_switch_rect = open_switch.get_rect(midright=(0,270))
sound_fx_switch_rect = open_switch.get_rect(midright=(0,360))

option_board_rect = pygame.Rect(0,0, 250, 350)
option_board_rect.midright = (0, SCREEN_HEIGHT / 2)

## Game Screen Rects

game_backgound_rect = game_background.get_rect(topleft=(0,0))
board_rect = pygame.Rect(offset_x - (BORDER_THICKNESS // 2) - EXTRA_PADDING, offset_y - (BORDER_THICKNESS // 2) - EXTRA_PADDING, board_width + BORDER_THICKNESS + 2 * EXTRA_PADDING, board_height + BORDER_THICKNESS + 2 * EXTRA_PADDING -20)
text_box_rect = text_box.get_rect(midbottom=(SCREEN_WIDTH // 2, (SCREEN_HEIGHT +SCOREBOARD_HEIGHT) - 5))

max_text_width = text_box_rect.width - 40

input_box = pygame.Rect(200, 530, 180, 50)

## Leaderboard Rects

replay_button_rect = pygame.Rect(screen.get_width()//2 - 150, 430, 120, 50)
menu_button_rect = pygame.Rect(screen.get_width()//2 + 30, 430, 120, 50)

## Loading Music and Sounds

click_sound = pygame.mixer.Sound("Button Click Sound.mp3")
wind_sound = pygame.mixer.Sound("Wind Sound.mp3")
swap_sound = pygame.mixer.Sound("Swap_sound_2.mp3")
text_blip_sound = pygame.mixer.Sound("text_blip_medium.ogg")

game_background_music = "Gameplay_Music.mp3"
menu_background_music = "Background Music.mp3"



## Loading Fonts

font_1 = pygame.font.Font("superMario256.ttf",40)
small_font_1 = pygame.font.Font("superMario256.ttf",23)
font_2 = pygame.font.Font("BebasNeue-Regular.ttf", 30)
font_3 = pygame.font.SysFont("arialblack", 18)
font_4 = pygame.font.Font("Pokemon Classic.ttf", 14)

play_text = font_1.render("Play", True, WHITE)
done_text = small_font_1.render("Done", True, WHITE)
tutorial_text = font_2.render("Tutorial", True, WHITE)
music_text = font_2.render("Music", True, WHITE)
sound_fx_text = font_2.render("Sound Fx", True, WHITE)

#GAME_STATES/FLAGS

menu_state = True

options_hovered = False
animate_menu = False
animate_options = False
particles_created = False
particle_default = False
reverse_animate_options = False
reverse_animate_menu = False
particles_moving_left = False
tutorial_state = True
music_state = True
sound_fx_state = True
music_playing = False


game_state = False

board_created = False
text_finished = False
dialogue_finished = False

question_active = False
question_result = None

leaderboard_state = False

############################################### Classes   #######################################################################################

# Class For the Particles on the main menu

class Particle:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT + SCOREBOARD_HEIGHT)
        self.size = random.randint(2, 4)
        self.vertical_speed = random.uniform(0.1, 0.3)
        self.color = (255, 255, 255, random.randint(50, 150))  # Semi-transparent
        self.horizontal_speed = 0

    def move(self):
        self.y -= self.vertical_speed
        self.x += self.horizontal_speed
        if self.y < 0:
            self.y = SCREEN_HEIGHT + SCOREBOARD_HEIGHT
            self.x = random.randint(0, SCREEN_WIDTH)
        if self.x > SCREEN_WIDTH:
            self.x = 0
            self.y = random.randint(0,SCREEN_HEIGHT + SCOREBOARD_HEIGHT)
        if self.x < 0:
            self.x = SCREEN_WIDTH
            self.y = random.randint(0,SCREEN_HEIGHT + SCOREBOARD_HEIGHT)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)



# Class for each gem in the board

class Gem:

    def __init__(self, row_num, col_num):
        
        #set the gem's position on the board

        self.row_num = row_num
        self.col_num = col_num
        self.colour = random.choice(gem_colours)
        image_name = f'lollipop_{self.colour}.png'  #Loading the Gem's Image
        self.image = pygame.image.load(image_name)
        self.image = pygame.transform.smoothscale(self.image, gem_size)  # Changing the image size to the size in the variable gem_size
        self.rect = self.image.get_rect()
        self.rect.left = col_num * GEM_WIDTH + offset_x  # Horizontal positioning
        self.rect.top = row_num * GEM_HEIGHT + offset_y   # Vertical positioning 
        
    
        
    # Drawing the gems

    def draw(self):
        screen.blit(self.image,self.rect)

    # Snapping the gems into the correct position

    def snap(self):
        self.snap_row()
        self.snap_col()

    def snap_row(self):
        self.rect.top = self.row_num * GEM_HEIGHT + offset_y

    def snap_col(self):
        self.rect.left = self.col_num * GEM_WIDTH + offset_x

    def fall(self):
        self.row_num += 1
        self.snap()






############################################### Functions For All Game States ########################################################################################

# Creates a rectangle with curves instead of corners

def draw_rounded_rect(surface, rect, color, border_radius=20, width=0):
    pygame.draw.rect(surface, color, rect, border_radius=border_radius, width=width)

def handle_quit(event):
    if event.type == pygame.QUIT:
        return False
    return True

# Function to play background music based on the current state
def play_background_music():
    if menu_state and music_state: # When in the menu and music is enabled
        pygame.mixer.music.load(menu_background_music)  # Load the menu music
        pygame.mixer.music.play(-1)  # Play it indefinitely
    elif game_state and music_state:  # When in the game and music is enabled
        pygame.mixer.music.stop()
        pygame.mixer.music.load(game_background_music)  # Load the game music
        pygame.mixer.music.play(-1)  # Play it indefinitely
    else:
        pygame.mixer.music.stop()  # Stop the music if neither state is active

    pygame.display.update()
    


######################################################### Menu Functions ############################################################################


def move_particles(particles, animate_menu, particle_default):
    for particle in particles:
        if particles_moving_left and particle.horizontal_speed < 0.00015:
            particle.horizontal_speed -= random.uniform(0.00015, 0.0002)  # Set a constant leftward speed
            # Gradually decrease upward speed
            if particle.vertical_speed > 0:
                particle.vertical_speed -= random.uniform(0.0001, 0.0015)  # Adjust this value to control how fast they level out
        else:
            # Original movement logic
            if animate_menu:
                particle.horizontal_speed += random.uniform(0.0001, 0.0015)
                if particle.vertical_speed > 0:
                    particle.vertical_speed -= random.uniform(0.0001, 0.0015)
                particle.vertical_speed = 0
            elif particle_default:
                particle.vertical_speed += random.uniform(0.00001, 0.00005)
                if particle.horizontal_speed > 0:
                    particle.horizontal_speed -= random.uniform(0.0001, 0.0003)
                elif particle.horizontal_speed < 0:
                    particle.horizontal_speed += random.uniform(0.0001, 0.0003)
            elif reverse_animate_options:
                particle.horizontal_speed -= random.uniform(0.0005, 0.0015)
                if particle.vertical_speed >= 0:
                    particle.vertical_speed -= random.uniform(0.0001, 0.0015)
                particle.vertical_speed = 0

        particle.move()
        particle.draw(screen)


# Draws the Menu

def draw_menu():
    global particle_default

    # Rendering Title and background

    screen.blit(menu_background, menu_background_rect) 
    screen.blit(menu_title, menu_title_rect)

    # Option button Hover effect

    screen.blit(options_button_hover if options_hovered else options_button, options_button_rect)

    draw_rounded_rect(screen, option_board_rect, STONE_COLOUR, border_radius=20)  # Base color of the tablet
    pygame.draw.rect(screen, STONE_ACCENTS, option_board_rect, width=10, border_radius=20)  # Accents with border

  


    mouse_pos = pygame.mouse.get_pos()

    # Play and done Button Hover Effect
    play_button_color = GREY if not play_rect.collidepoint(mouse_pos) else WHITE
    draw_rounded_rect(screen, play_rect, play_button_color, border_radius=15, width=5)

    done_button_color = GREY if not done_text_rect.collidepoint(mouse_pos) else WHITE
    draw_rounded_rect(screen, done_text_rect, done_button_color, border_radius=10, width=5)

    # Rendering texts and switches

    screen.blit(play_text, play_text.get_rect(center=play_button_rect.center))
    screen.blit(done_text, done_text.get_rect(center=done_button_rect.center))
    screen.blit(tutorial_text, tutorial_text.get_rect(midright=tutorial_text_rect.center))
    screen.blit(music_text, music_text.get_rect(midright=music_text_rect.center))
    screen.blit(sound_fx_text, sound_fx_text.get_rect(midright=sound_fx_text_rect.center))
    screen.blit(closed_switch if tutorial_state else open_switch, tutorial_switch_rect)
    screen.blit(closed_switch if music_state else open_switch, music_switch_rect)
    screen.blit(closed_switch if sound_fx_state else open_switch, sound_fx_switch_rect)


# Moving the main menu


def move_menu(speed):

    menu_title_rect.left += speed
    play_rect.left += speed
    options_button_rect.left += speed
    play_button_rect.left += speed


# Moving the options menu


def move_options(speed):
    
    option_board_rect.left += speed
    
    # Align the text labels consistently
    
    base_x_offset = 20  
    y_spacing = 51  #Vertical spacing between each option
    
    tutorial_text_rect.midleft = (option_board_rect.left + base_x_offset, option_board_rect.top + y_spacing)
    music_text_rect.midleft = (option_board_rect.left + base_x_offset - 20, tutorial_text_rect.bottom + y_spacing)
    sound_fx_text_rect.midleft = (option_board_rect.left + base_x_offset, music_text_rect.bottom + y_spacing)

    # Calculate a consistent x-coordinate for all switches

    switch_x = option_board_rect.left + 160  
    
    tutorial_switch_rect.left = switch_x 
    music_switch_rect.left = switch_x
    sound_fx_switch_rect.left = switch_x

    done_text_rect.left = option_board_rect.left + 65
    done_button_rect.left = done_text_rect.left


def create_particles():

    particles = [Particle() for _ in range(50)]

    return particles

### Menu Event Handling

# Handling menu Mouse Clicks

def handle_mouse_click_menu(event):

    global animate_menu, tutorial_state, music_state, sound_fx_state, reverse_animate_options, game_state, menu_state, music_playing

    if play_rect.collidepoint(event.pos):
        if sound_fx_state:   # Checking sound fx are enables
            click_sound.play()  
        music_playing = False
        menu_state = False
        game_state = True
        music_playing = False

    elif options_button_rect.collidepoint(event.pos):
        if sound_fx_state:
            click_sound.play()
        animate_menu = True  # Start menu animation
    elif tutorial_switch_rect.collidepoint(event.pos):
        tutorial_state = not tutorial_state
    elif music_switch_rect.collidepoint(event.pos):
        music_state = not music_state
        pygame.mixer.music.set_volume(10 if music_state else 0)
    elif sound_fx_switch_rect.collidepoint(event.pos):
        sound_fx_state = not sound_fx_state
    elif done_button_rect.collidepoint(event.pos):
        if sound_fx_state:
            click_sound.play()
        reverse_animate_options = True


def handle_events_menu():
    for event in pygame.event.get():
        if not handle_quit(event):
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_click_menu(event)
    return True

        

######################################################### Gameplay Functions ######################################################################


# Draws the board for the main game

def draw_board():

    board = []

    for row_num in range(((SCREEN_HEIGHT - PADDING_Y) // GEM_HEIGHT)):

        #add a new row to the board
        board.append([])

        for col_num in range(((SCREEN_WIDTH - PADDING_X) // GEM_WIDTH)):

            gem = Gem(row_num,col_num)
            board[row_num].append(gem)

            #making sure there are no matches when the board is made

            while (col_num > 1 and gem.colour == board[row_num][col_num - 1].colour == board[row_num][col_num - 2].colour) or (row_num > 1 and gem.colour == board[row_num - 1][col_num].colour == board[row_num - 2][col_num].colour):
                gem.colour = random.choice(gem_colours)
                gem.image = pygame.image.load(f'lollipop_{gem.colour}.png')
                gem.image = pygame.transform.smoothscale(gem.image, gem_size)
    
    return board


def draw_game():

    screen.blit(game_background,game_backgound_rect)
    #draw the gems

    draw_rounded_rect(screen, board_rect, WHITE, border_radius=20, width=BORDER_THICKNESS)
   

    for row in board:
        for gem in row:
            if gem is not None:
                gem.draw()
    
    #display the score and moves

    font = pygame.font.SysFont("arialblack", 18)
    score_text = font.render(f'Score: {score}', 1 , (255,255,255))
    score_text_rect = score_text.get_rect(center=(SCREEN_WIDTH / 4, SCREEN_HEIGHT + SCOREBOARD_HEIGHT / 2)) 
    screen.blit(score_text, score_text_rect)

    moves_text = font.render(f'Moves: {moves}', 1 , (255,255,255))
    moves_text_rect = moves_text.get_rect(center=(SCREEN_WIDTH * 3/4, SCREEN_HEIGHT + SCOREBOARD_HEIGHT / 2))
    screen.blit(moves_text,moves_text_rect)

    if question_active:

        # Timer logic
        elapsed_time = time.time() - question_start_time
        time_left = max(0, round(question_time_limit - elapsed_time))
        
        timer_text = font_4.render(f"Time: {time_left}s", True, (255, 255, 255))
        screen.blit(timer_text, (input_box.x-50, input_box.y+60))

        pygame.draw.rect(screen, input_color, input_box, border_radius=5)
        question_text = font_4.render(current_question + " = ?", True, (255, 255, 255))
        answer_text = font_4.render(user_answer, True, (0, 0, 0))
        screen.blit(question_text, (input_box.x - 150, input_box.y + 5))
        screen.blit(answer_text, (input_box.x + 5, input_box.y + 5))

    elif question_result:

        result_text = font_4.render(question_result, True, (0, 255, 0) if question_result == "Correct!" else (255, 0, 0))
        screen.blit(result_text, (input_box.x - 50, input_box.y + 60))


# Function to wrap text
def wrap_text(text, font, max_width):
    """Splits the text into lines that fit within the max_width."""
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "

    lines.append(current_line)  # Add the last line
    return lines

# Function to draw text
def draw_text(text, position):
    text_surface = font_4.render(text, True, BLACK)
    screen.blit(text_surface, position)

# Function to handle text animation
def animate_text(lines):
    global letter_index, last_update, text_finished

    # If the text is fully displayed, don't animate further
    if text_finished:
        if sound_fx_state:
            text_blip_sound.stop()
            return lines

    # Calculate time since the last letter was displayed
    now = pygame.time.get_ticks()
    if now - last_update > TEXT_SPEED:
        if sound_fx_state:
            text_blip_sound.play()
            letter_index += 1
            last_update = now

    # Join all lines together with a newline and slice the animated portion
    full_text = "\n".join(lines)
    current_text = full_text[:letter_index]
    current_lines = current_text.split('\n')

    # Check if we've finished displaying the full text
    if letter_index >= len(full_text):
        text_finished = True

    return current_lines

def text_box_function():

    if text_index < len(tutorial_dialogue):
        current_text = tutorial_dialogue[text_index]
        wrapped_lines = wrap_text(current_text, font_4, max_text_width)
        animated_lines = animate_text(wrapped_lines)

        # Draw each line with some vertical spacing
        for i, line in enumerate(animated_lines):
            draw_text(line, (text_box_rect.x + 20, text_box_rect.y + 20 + i * font_4.get_height()))

    return wrapped_lines

#swap the position of two gems

def swap(gem1 , gem2):

        
    temp_row = gem1.row_num
    temp_col = gem1.col_num

    gem1.row_num = gem2.row_num
    gem1.col_num = gem2.col_num

    gem2.row_num = temp_row
    gem2.col_num = temp_col

    #updating the gems on the board

    board[gem1.row_num][gem1.col_num] = gem1
    board[gem2.row_num][gem2.col_num] = gem2

    gem1.snap()
    gem2.snap()
    if sound_fx_state:
        swap_sound.play()

#finding neighbouring colour matches

def find_matches(gem, matches):
    # Use a stack for DFS
    stack = [gem]
    
    while stack:
        current_gem = stack.pop()
        
        # Add the current gem to matches if it's of the same color
        if current_gem.colour == gem.colour and current_gem not in matches:
            matches.add(current_gem)

            # Check neighboring gems: up, down, left, right
            # Check up
            if current_gem.row_num > 0:
                neighbor = board[current_gem.row_num - 1][current_gem.col_num]
                if neighbor and neighbor not in matches:
                    stack.append(neighbor)
           
            # Check down
            if current_gem.row_num < len(board) - 1:
                neighbor = board[current_gem.row_num + 1][current_gem.col_num]
                if neighbor and neighbor not in matches:
                    stack.append(neighbor)

            # Check left
            if current_gem.col_num > 0:
                neighbor = board[current_gem.row_num][current_gem.col_num - 1]
                if neighbor and neighbor not in matches:
                    stack.append(neighbor)

            # Check right
            if current_gem.col_num < len(board[current_gem.row_num]) - 1:
                neighbor = board[current_gem.row_num][current_gem.col_num + 1]
                if neighbor and neighbor not in matches:
                    stack.append(neighbor)
    
    return matches


#return a set of at least 3 matching gems

def match_three(gem): 
    
    matches = find_matches(gem,set())
    if len(matches) >= 3:
        return matches
    else:
        return set()

#filling the gaps formed after a match is made

def fill_gaps():
    gaps = True
    while gaps:
        gaps = False
        for row_num in range(len(board)-1, -1, -1):
            for col_num in range(len(board[row_num])):
                if board[row_num][col_num] is None and row_num > 0:
                    gaps = True
                    falling_gem = board[row_num - 1][col_num]
                    if falling_gem:
                        falling_gem.fall()
                        board[row_num][col_num] = falling_gem
                        board[row_num - 1][col_num] = None
                        

                    #making new gems if there are gaps at the top row

                elif board[row_num][col_num] is None:
                    gaps = True
                    board[row_num][col_num] = Gem(row_num, col_num)
                    

def generate_question():
    operators = ['+', '-', '*', '/']
    op = random.choice(operators)
    
    if op == '+':
        a, b = random.randint(1, 20), random.randint(1, 20)
        question = f"{a} + {b}"
        answer = a + b
    elif op == '-':
        a, b = random.randint(10, 30), random.randint(1, 10)
        question = f"{a} - {b}"
        answer = a - b
    elif op == '*':
        a, b = random.randint(2, 10), random.randint(2, 10)
        question = f"{a} × {b}"
        answer = a * b
    elif op == '/':
        b = random.randint(1, 10)
        answer = random.randint(2, 10)
        a = b * answer
        question = f"{a} ÷ {b}"
    return question, str(answer)

def find_all_matches():
    visited = set()
    all_matches = set()
    for row in board:
        for gem in row:
            if gem not in visited:
                group = find_matches(gem, set())
                visited.update(group)
                if len(group) >= 3:
                    all_matches.update(group)
    return list(all_matches)

def handle_cascading_matches(score):
    score  # Ensure score is accessible

    while True:
        matches = find_all_matches()
        if len(matches) < 3:
            break  # No more matches, end the cascade loop

        score += len(matches)

        # Shrinking animation loop
        while len(matches) > 0:
            clock.tick(100)

            for gem in matches:
                new_width = gem.image.get_width() - 1
                new_height = gem.image.get_height() - 1
                new_size = (max(0, new_width), max(0, new_height))  # Prevent negative size
                gem.image = pygame.transform.smoothscale(gem.image, new_size)
                gem.rect.left = gem.col_num * GEM_WIDTH + offset_x + (GEM_WIDTH - new_width) / 2
                gem.rect.top = gem.row_num * GEM_HEIGHT + offset_y + (GEM_HEIGHT - new_height) / 2

            # Remove gems that have shrunk to 0
            for row_num in range(len(board)):
                for col_num in range(len(board[row_num])):
                    gem = board[row_num][col_num]
                    if gem and (gem.image.get_width() <= 0 or gem.image.get_height() <= 0):
                        if gem in matches:
                            matches.remove(gem)
                        board[row_num][col_num] = None

            fill_gaps()
            draw_game()
            pygame.display.update() 
    
    return score

#################################################################### Leaderboard Functions #################################################################################
def save_score(name, score, filename="leaderboard.txt"):
    with open(filename, "a") as f:
        f.write(f"{name}:{score}\n")

def load_top_scores(n=5, filename="leaderboard.txt"):
    scores = []
    try:
        with open(filename, "r") as f:
            for line in f:
                if ':' in line:
                    name, score = line.strip().split(":")
                    scores.append((name, int(score)))
    except FileNotFoundError:
        return []

    # Bubble Sort by score descending
    for i in range(len(scores)):
        for j in range(0, len(scores) - i - 1):
            if scores[j][1] < scores[j + 1][1]:
                scores[j], scores[j + 1] = scores[j + 1], scores[j]

    return scores[:n]


def draw_leaderboard_screen(screen, font, player_input_name, top_scores,
                            replay_button_rect, menu_button_rect):
    screen.fill((20, 20, 20))

    # "Game Over" title in red
    title = font.render("Game Over", True, (200, 0, 0))
    screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 40))

    # Top scores
    score_title = font.render("Top Scores:", True, (255, 255, 255))
    screen.blit(score_title, (screen.get_width()//2 - score_title.get_width()//2, 100))

    for i, (name, score) in enumerate(top_scores):
        score_text = font.render(f"{i+1}. {name} - {score}", True, (255, 255, 255))
        screen.blit(score_text, (screen.get_width()//2 - score_text.get_width()//2, 140 + i*30))

    # Name prompt
    name_prompt = font.render("Enter your name:", True, (255, 255, 255))
    screen.blit(name_prompt, (screen.get_width()//2 - name_prompt.get_width()//2, 320))

    # Input box
    input_box = pygame.Rect(screen.get_width()//2 - 100, 360, 200, 40)
    pygame.draw.rect(screen, (255, 255, 255), input_box, 2)
    name_surface = font.render(player_input_name, True, (255, 255, 255))
    screen.blit(name_surface, (input_box.x + 5, input_box.y + 5))

    # Replay button
    pygame.draw.rect(screen, (70, 130, 180), replay_button_rect)
    replay_text = font.render("Replay", True, (255, 255, 255))
    screen.blit(replay_text, (replay_button_rect.centerx - replay_text.get_width()//2,
                              replay_button_rect.centery - replay_text.get_height()//2))

    # Main Menu button
    pygame.draw.rect(screen, (70, 130, 180), menu_button_rect)
    menu_text = font.render("Main Menu", True, (255, 255, 255))
    screen.blit(menu_text, (menu_button_rect.centerx - menu_text.get_width()//2,
                            menu_button_rect.centery - menu_text.get_height()//2))

###################################################### Game Loop ##############################################################################################################
fps = 60
clock = pygame.time.Clock()
clock.tick(fps)

run = True

while run:

    

    if menu_state:
        run = handle_events_menu()

        if not particles_created:
            particles = create_particles()
            particles_created = True

        if animate_menu:
            if menu_title_rect.left < SCREEN_WIDTH:
                move_menu(1)
                if sound_fx_state:
                    wind_sound.play()
            else:
                animate_menu = False
                finished = time.time()
                animate_options = True
        
        if animate_options:
            if time.time() - finished >= 2:
                if option_board_rect.centerx < SCREEN_WIDTH / 2:
                    move_options(1)
                else:
                    animate_options = False
                    option_board_rect.centerx = SCREEN_WIDTH/2
                    particle_default = True
        
        # Then in your game loop, you keep most of the transitions the same
        if reverse_animate_options:
            if option_board_rect.right > 1:
                move_options(-1)
                if sound_fx_state:
                    wind_sound.play()
            else:
                reverse_animate_options = False
                # Start moving particles to the left when reverse animation starts
                particles_moving_left = True  # Set the flag to move particles left
                finished1 = time.time()
                reverse_animate_menu = True

        if reverse_animate_menu:
            if time.time() - finished1 >= 3:
                if menu_title_rect.centerx > screen_center[0]:
                    move_menu(-1)
                else:
                    reverse_animate_menu = False
                    particles_moving_left = False  # Reset the particle motion when the menu is back in place
                    particle_default = False  # Reset this to false after going back to the main menu

                    # Reset particles to move upward again
                    for particle in particles:
                        particle.vertical_speed = random.uniform(0.05, 0.1)  # Set to original upward speeds
                        particle.horizontal_speed = 0
            
                    
            
        mouse_pos = pygame.mouse.get_pos()
        options_hovered = options_button_rect.collidepoint(mouse_pos)
            
        draw_menu()
        if not music_playing:
            play_background_music()
            music_playing = True
        move_particles(particles,animate_menu,particle_default)
  
        pygame.display.update()


    elif game_state:
        
        

        clock = pygame.time.Clock()

        question_time_limit = max(3, (10 - (total_moves)))

        if not board_created:
            board = draw_board()
            board_created = True

        matches = set()

        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            
            elif event.type == MOUSEBUTTONDOWN and text_box_rect.collidepoint(event.pos):
                if text_finished:
                    text_index += 1
                    letter_index = 0
                    text_finished = False
                    if text_index >= len(tutorial_dialogue):
                        text_index = len(tutorial_dialogue) - 1
                        dialogue_finished = True
                else:
                    # Skip animation and show full text
                    text_finished = True
                    letter_index = len("\n".join(wrapped_lines))
            #detect mouse click

            if clicked_gem is None and event.type == MOUSEBUTTONDOWN:

                #retrieve the gem that was clicked on 

                for row in board:
                    for gem in row:
                        if gem.rect.collidepoint(event.pos):
                            clicked_gem = gem

                            #save the coordinates of the clicked point

                            click_x = event.pos[0]
                            click_y = event.pos[1]

            #detect mouse motion

            if clicked_gem != None and event.type == MOUSEMOTION:

                #Calculate the distance between the points and the current location of the mouse

                distance_x = abs(click_x - event.pos[0])
                distance_y = abs(click_y - event.pos[1])

                #reset the position of swapped gem if direction of mouse changed

                if swapped_gem is not None:
                    swapped_gem.snap()

                #determine the direction of the neighbouring gem to swap with

                if distance_x > distance_y and click_x > event.pos[0]:
                    direction = "left"
                elif distance_x > distance_y and click_x < event.pos[0]:
                    direction = "right"
                elif distance_x < distance_y and click_y > event.pos[1]:
                    direction = "down"
                elif distance_x < distance_y and click_y < event.pos[1]:
                    direction = "up"

                #determining where to snap the clicked gem

                if direction in ["left", "right"]:
                    clicked_gem.snap_row()
                else:
                    clicked_gem.snap_col()
                
                #moving the gem to the left, making sure it can't move off the board

                if direction == "left" and clicked_gem.col_num > 0:

                    #setting swapped_gem 
                    
                    swapped_gem = board[clicked_gem.row_num][clicked_gem.col_num - 1]
                    
                    #swapping the two gems

                    clicked_gem.rect.left = clicked_gem.col_num * GEM_WIDTH + offset_x - distance_x 
                    swapped_gem.rect.left = swapped_gem.col_num * GEM_WIDTH + offset_x + distance_x

                    #snap them into their new positions on the board

                    if clicked_gem.rect.left <= swapped_gem.col_num * GEM_WIDTH + offset_x + GEM_WIDTH / 4:
                        swap(clicked_gem,swapped_gem)
                        matches.update(match_three(clicked_gem))
                        matches.update(match_three(swapped_gem))
                        moves -= 1
                        total_moves += 1
                        #logic to trigger question
                        if moves >= 0 and not question_active:
                            current_question, correct_answer = generate_question()
                            user_answer = ""
                            question_result = None
                            question_active = True
                            question_start_time = time.time()

                        clicked_gem = None
                        swapped_gem = None 

                #moving the gem to the right, making sure it can't move off the board

                if direction == "right" and clicked_gem.col_num < SCREEN_WIDTH / GEM_WIDTH - 1:

                    #setting swapped gem

                    swapped_gem = board[clicked_gem.row_num][clicked_gem.col_num + 1]

                    #swapping the two gems 

                    clicked_gem.rect.left = clicked_gem.col_num * GEM_WIDTH + offset_x + distance_x
                    swapped_gem.rect.left = swapped_gem.col_num * GEM_WIDTH + offset_x - distance_x

                    #snap them into their new positions on the board

                    if clicked_gem.rect.left >= swapped_gem.col_num * GEM_WIDTH + offset_x + GEM_WIDTH / 4:
                        swap(clicked_gem,swapped_gem)
                        matches.update(match_three(clicked_gem))
                        matches.update(match_three(swapped_gem))
                        moves -= 1
                        total_moves += 1
                        # Example logic to trigger question
                        if moves >= 0 and not question_active:
                            current_question, correct_answer = generate_question()
                            user_answer = ""
                            question_result = None
                            question_active = True
                            question_start_time = time.time()

                        clicked_gem = None
                        swapped_gem = None

                #moving the gem down, making sure it can't move off the board 

                if direction == "down" and clicked_gem.row_num > 0:

                    #setting swapped gem

                    swapped_gem = board[clicked_gem.row_num-1][clicked_gem.col_num]

                    #swapping the two gems

                    clicked_gem.rect.top = clicked_gem.row_num * GEM_HEIGHT + offset_y - distance_y
                    swapped_gem.rect.top = swapped_gem.row_num * GEM_HEIGHT + offset_y + distance_y 

                    #snap them into their new positions on the board

                    if clicked_gem.rect.top <= swapped_gem.row_num * GEM_HEIGHT + offset_y + GEM_HEIGHT / 4:
                        swap(clicked_gem,swapped_gem)
                        matches.update(match_three(clicked_gem))
                        matches.update(match_three(swapped_gem))
                        moves -= 1
                        total_moves += 1
                        # Example logic to trigger question
                        if moves >= 0 and not question_active:
                            current_question, correct_answer = generate_question()
                            user_answer = ""
                            question_result = None
                            question_active = True
                            question_start_time = time.time()

                        clicked_gem = None
                        swapped_gem = None
                
                #moving the gem up, making sure it can't move off the board

                if direction == "up" and clicked_gem.row_num < SCREEN_HEIGHT / GEM_HEIGHT - 1:

                    #setting swapped gem

                    swapped_gem = board[clicked_gem.row_num+1][clicked_gem.col_num]

                    #swapping the two gems

                    clicked_gem.rect.top = clicked_gem.row_num * GEM_HEIGHT + offset_y + distance_y
                    swapped_gem.rect.top = swapped_gem.row_num * GEM_HEIGHT + offset_y - distance_y 

                    #snap them into their new positions on the board

                    if clicked_gem.rect.top >= swapped_gem.row_num * GEM_HEIGHT + offset_y - GEM_HEIGHT / 4:
                        swap(clicked_gem,swapped_gem)
                        matches.update(match_three(clicked_gem))
                        matches.update(match_three(swapped_gem))
                        moves -= 1
                        total_moves += 1
                        # Example logic to trigger question
                        if moves >= 0 and not question_active:
                            current_question, correct_answer = generate_question()
                            user_answer = ""
                            question_result = None
                            question_active = True
                            question_start_time = time.time()

                        clicked_gem = None
                        swapped_gem = None
            
            #detect if the mouse is released 

            if clicked_gem is not None and event.type == MOUSEBUTTONUP:

                #snap them back to their original positions

                clicked_gem.snap()
                clicked_gem = None
                if swapped_gem != None:
                    swapped_gem.snap()
                    swapped_gem = None

            if question_active:
                if question_active and time.time() - question_start_time > question_time_limit:
                    question_result = "Out Of Time!"
                    question_active = False
                    moves -= 1  # Penalize for timeout
                    draw_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if user_answer == correct_answer:
                            moves += 1  # Restore a move on correct answer
                            question_result = "Correct!"
                        else:
                            question_result = "Incorrect!"
                        question_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        user_answer = user_answer[:-1]
                    elif event.unicode.isdigit():
                        user_answer += event.unicode





        draw_game()

        if tutorial_state:
            if not dialogue_finished:
                screen.blit(text_box, text_box_rect)
                wrapped_lines = text_box_function()
        pygame.display.update()

    #checking if there is a match of at least 3

        if len(matches) >= 3:
            
            score = handle_cascading_matches(score)

 
            pygame.display.update()

        if not music_playing:
            play_background_music()
            music_playing = True
            pygame.display.update()
    
        if moves < 0:
            game_state = False
            leaderboard_state = True

        pygame.display.update()

    elif leaderboard_state:

        top_scores = load_top_scores()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    player_input_name = player_input_name[:-1]
                elif event.key == pygame.K_RETURN:
                    if player_input_name:
                        save_score(player_input_name, score)
                elif len(player_input_name) < 10 and event.unicode.isprintable():
                    player_input_name += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if sound_fx_state:
                    click_sound.play()
                if replay_button_rect.collidepoint(event.pos):
                    # Reset game variables
                    moves = 3
                    score = 0
                    total_moves = 0 
                    game_state = True
                    leaderboard_state = False
                    player_input_name = ""
                    

                elif menu_button_rect.collidepoint(event.pos):
                    if sound_fx_state:
                        click_sound.play()
                    moves = 3
                    score = 0
                    total_moves = 0 
                    player_input_name = ""
                    menu_state = True
                    leaderboard_state = False
                    play_background_music()


        draw_leaderboard_screen(screen, font_4, player_input_name, top_scores,
                                replay_button_rect, menu_button_rect)
        pygame.display.flip()

        
pygame.quit()