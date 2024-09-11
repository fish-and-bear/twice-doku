import asyncio
import json
import pygame
import generate
import solve
import variables as Var
import time
import random
import os
import sys
import ptext
import pygame_gui as pgui
from datetime import datetime
import filehandler as fileHandler
from audio import AudioHandler
import pygame.mixer
import logging

pygame.init()
pygame.mixer.init()
pygame.mixer.pre_init()
pygame.font.init()

# Initializing variables
time_file = Var.timefile
grid_file = Var.gridfile
scores_file = Var.scoresfile
settings_file = Var.settingsfile
gameIcon = pygame.image.load(Var.icon)
pygame.display.set_icon(gameIcon)
now = datetime.now()
dt_string = now.strftime("%m/%d/%Y %H:%M:%S")

x = 0
y = 0

# Picking images from theme chosen
# folder, background color, grid color, selection color, text color, button color
theme_attr = {'CHEER UP': ['assets/tiles/cheerup', Var.cuBLUEGREEN, Var.cuWHITE, Var.cuWHITE, Var.cuWHITE, Var.cuWHITE],
              'What is Love': ['assets/tiles/whatislove', Var.wilPINK, Var.wilRED, Var.wilBLACK, Var.wilRED, Var.wilRED],
              'Dance the Night Away': ['assets/tiles/dancethenightaway', Var.dtnaLIGHTBLUE, Var.dtnaWHITE, Var.dtnaYELLOW, Var.dtnaBLUE, Var.dtnaBLUE],
              'Yes or Yes': ['assets/tiles/yesoryes', Var.yoyLIGHTPURPLE, Var.yoyWHITE, Var.yoyDARKPURPLE, Var.yoyDARKPURPLE, Var.yoyDARKPURPLE],
              'FANCY': ['assets/tiles/fancy', Var.fSKYBLUE, Var.fYELLOW, Var.fPINK, Var.fWHITE, Var.fWHITE],
              'Breakthrough': ['assets/tiles/breakthrough', Var.bDARKBLUE, Var.bPINK, Var.bPURPLE, Var.bWHITE, Var.bWHITE],
              'Feel Special': ['assets/tiles/feelspecial', Var.fsPEACH, Var.fsLIGHTGOLD, Var.fsGOLD, Var.fsGOLD, Var.fsLIGHTGOLD],
              'More and More': ['assets/tiles/moreandmore', Var.mamGREEN, Var.mamGOLD, Var.mamORANGE, Var.mamWHITE, Var.mamWHITE]
              }
members = {1: 'chaeyoung.png',
           2: 'dahyun.png',
           3: 'jeongyeon.png',
           4: 'jihyo.png',
           5: 'mina.png',
           6: 'momo.png',
           7: 'nayeon.png',
           8: 'sana.png',
           9: 'tzuyu.png'}

logging.basicConfig(filename='twicedoku.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def log_error(e, context=""):
    logging.error(f"{context}: {str(e)}", exc_info=True)

# Get position of cursor and determine where to place numbers, draw grid, etc.
def get_coordinates(position, grid_offs, grid_size, dif):
    if position[0] > grid_offs[0] and position[0] < grid_offs[0] + grid_size and position[1] > grid_offs[1] and position[1] < grid_offs[1] + grid_size:
        x = position[0] - grid_offs[0]
        y = position[1] - grid_offs[1]
        return x // dif, y // dif
    else:
        return None


# Highlight the cell selected
def draw_box(x, y, theme, screen, dif, grid_offs):
    for i in range(2):
        pygame.draw.line(screen, theme_attr[theme][3], (x * dif + grid_offs[0] - 3, (y + i) *
                                                        dif + grid_offs[1]), (x * dif + dif + 3 + grid_offs[0], (y + i) * dif + grid_offs[1]), 7)
        pygame.draw.line(screen, theme_attr[theme][3], ((x + i) * dif + grid_offs[0], y *
                                                        dif + grid_offs[1]), ((x + i) * dif + grid_offs[0], y * dif + dif + grid_offs[1]), 7)


# Function to draw required lines for making Sudoku grid
def draw(grid, grid_offs, dif, theme, screen, w):
    # Fill cells with members (Sudoku grid)
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                # Fill grid with member assigned to number in grid
                path = theme_attr[theme][0] + '/given/' + members[grid[i][j]]
                img = pygame.image.load(path)
                img = pygame.transform.smoothscale(img, (int(dif), int(dif)))
                screen.blit(
                    img, (j * dif + grid_offs[0], i * dif + grid_offs[1]))
    # Fill cells with members (Guide)
    for i in range(9):
        path = theme_attr[theme][0] + '/given/' + members[i+1]
        img = pygame.image.load(path)
        img = pygame.transform.smoothscale(img, (int(dif), int(dif)))
        screen.blit(img, (grid_offs[0]*3.15, i * dif + grid_offs[1]))
        membername = ''.join(members[i+1].split())[:-4].upper()
        ptext.draw(f'{membername} - PRESS {i+1}', (grid_offs[0]*3.18 + dif, i * dif + grid_offs[1]
                                                   * 1.5), width=360, fontname=Var.text, fontsize=w/70, color=theme_attr[theme][4])


def border(screen, theme, grid_offs, grid_size, dif, grid_dims):
    # To draw the boxes of the sudoku GUI
    for i in range(0, grid_dims + 1):
        if i % 3 == 0:
            # For the main grid lines
            thick = 7
        else:
            # For the interior lines of the grid
            thick = 3
        pygame.draw.line(screen, theme_attr[theme][2], (grid_offs[0], grid_offs[1] +
                                                        i * dif), (grid_offs[0] + grid_size, grid_offs[1] + i * dif), thick)
        pygame.draw.line(screen, theme_attr[theme][2], (grid_offs[0] + i * dif,
                                                        grid_offs[1]), (grid_offs[0] + i * dif, grid_offs[1] + grid_size), thick)
    # Drawing border lines for the guide at the right
    for i in range(0, grid_dims + 1):
        if i == 0 or i == grid_dims:
            thick = 7
        else:
            thick = 3
        pygame.draw.line(screen, theme_attr[theme][2], (grid_offs[0]*3.15, grid_offs[1] +
                                                        i * dif), (grid_offs[0]*3.15 + dif, grid_offs[1] + i * dif), thick)
    for i in range(0, 2):
        thick = 7
        pygame.draw.line(screen, theme_attr[theme][2], (grid_offs[0]*3.15 + i * dif,
                                                        grid_offs[1] + 0), (grid_offs[0]*3.15 + i * dif, grid_offs[1] + grid_size), thick)


# Fill value entered in cell
def draw_val(val, x, y, screen, grid_offs, dif, theme):
    path = theme_attr[theme][0] + '/input/' + members[val]
    img = pygame.image.load(path)
    img = pygame.transform.smoothscale(img, (int(dif), int(dif)))
    screen.blit(img, (x * dif + grid_offs[0], y * dif + grid_offs[1],
                      dif + 1 + grid_offs[0], dif + 1 + grid_offs[1]))

# Convert time to a format
def time_convert(sec):
    return time.strftime("%H:%M:%S", time.gmtime(sec))

# Raise error when wrong value entered
def throw_error(a, i, j, val, screen, grid_offs, grid_dims, grid_size, dif, theme, w, h, highscore, time):
    # Highlight the wrong input
    s = pygame.Surface((int(dif), int(dif)), pygame.SRCALPHA)
    s.fill((255, 0, 0, 55))
    border(screen, theme, grid_offs, grid_size, dif, grid_dims)
    for it in range(9):
        if a[j][it] == val:
            screen.blit(s, (it * dif + grid_offs[0], j * dif + grid_offs[1],
                            dif + 1 + grid_offs[0], dif + 1 + grid_offs[1]))
            border(screen, theme, grid_offs, grid_size, dif, grid_dims)
        if a[it][i] == val:
            screen.blit(s, (i * dif + grid_offs[0], it * dif + grid_offs[1],
                            dif + 1 + grid_offs[0], dif + 1 + grid_offs[1]))
            border(screen, theme, grid_offs, grid_size, dif, grid_dims)
    it = i // 3
    jt = j // 3
    # to check in the 3x3 sub block of the sudoku
    for i in range(jt * 3, jt * 3 + 3):
        for j in range(it * 3, it * 3 + 3):
            if a[i][j] == val:
                screen.blit(
                    s, (j * dif + + grid_offs[0], i * dif + grid_offs[1], dif + 1 + grid_offs[0], dif + 1 + grid_offs[1]))
                border(screen, theme, grid_offs, grid_size, dif, grid_dims)
    # pygame.draw.rect(screen, (255,0,0), (x * dif, y * dif, dif + 1, dif + 1))
    ptext.draw('Wrong input!', (w/50, h/1.5), width=360,
               fontname=Var.text, fontsize=w/30, color=theme_attr[theme][4])
    ptext.draw('PRESS ESC FOR MAIN MENU', (w/50, h/1.35), width=360,
               fontname=Var.text, fontsize=w/45, color=theme_attr[theme][4])
    ptext.draw('PRESS R TO REFRESH', (w/50, h/1.3), width=360,
               fontname=Var.text, fontsize=w/45, color=theme_attr[theme][4])
    ptext.draw('HIGHSCORE: {}'.format(highscore), (w/50, h/1.2), width=360,
               fontname=Var.text, fontsize=w/45, color=theme_attr[theme][4])
    ptext.draw(time, (w/50, h/1.15), width=360, fontname=Var.text,
               fontsize=Var.gametextsize, color=theme_attr[theme][4])
    #text1 = Var.font2.render("Wrong input!", 1, theme_attr[theme][4])
    #screen.blit(text1, (20, 450))
    pygame.display.update()


# Check if the value entered in board is valid
def check_valid(a, i, j, val, solution):
    if val != solution[i][j]:
        return False
    return True

# Display instruction for the game
def instruction(time, highscore, theme, w, h):
    ptext.draw('PRESS ESC FOR MAIN MENU', (w/50, h/1.35), width=360,
               fontname=Var.text, fontsize=w/45, color=theme_attr[theme][4])
    ptext.draw('PRESS R TO REFRESH', (w/50, h/1.3), width=360,
               fontname=Var.text, fontsize=w/45, color=theme_attr[theme][4])
    ptext.draw('HIGHSCORE: {}'.format(highscore), (w/50, h/1.2), width=360,
               fontname=Var.text, fontsize=w/45, color=theme_attr[theme][4])
    ptext.draw(time, (w/50, h/1.15), width=360, fontname=Var.text,
               fontsize=Var.gametextsize, color=theme_attr[theme][4])
    # pygame.display.update()

# Display options when solved
def display_result(theme, w, h, time):
    ptext.draw('Finished! Press R', (w/50, h/1.35), width=360,
               fontname=Var.text, fontsize=w/50, color=theme_attr[theme][4])
    ptext.draw('to solve a new puzzle', (w/50, h/1.3), width=360,
               fontname=Var.text, fontsize=w/50, color=theme_attr[theme][4])
    ptext.draw('or ESC to go to Menu', (w/50, h/1.25), width=360,
               fontname=Var.text, fontsize=w/50, color=theme_attr[theme][4])
    ptext.draw(time, (w/50, h/1.15), width=360, fontname=Var.text,
               fontsize=Var.gametextsize, color=theme_attr[theme][4])
    pygame.display.update()

# Change music per era/theme
def load_music(theme):
    path = os.path.join("assets", "songs", theme)
    songs = []
    for filename in os.listdir(path):
        if filename.endswith(".ogg"):
            songs.append(os.path.join(path, filename))
        else:
            continue
    return songs

# If ever I decide to put background pictures...
def bg(theme):
    try:
        background_image = pygame.image.load(os.path.join("assets", "pictures", f"{theme}.png"))
        return background_image
    except FileNotFoundError:
        return None

# Settings variables
async def getsettings():
    try:
        settings = await fileHandler.json_open(Var.settingsfile)
        resolution_string = settings.get('resolution', '800x600').split('x')
        w = int(resolution_string[0])
        h = int(resolution_string[1])
        theme = settings.get('theme', 'Default')
        volume = settings.get('volume', 50)
        return w, h, theme, volume
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(f"Error getting settings: {e}")
        print("Using default settings")
        return 800, 600, 'Default', 50
    except Exception as e:
        print(f"Unexpected error in getsettings: {e}")
        raise

# Animated backgrounds
global animation_frames
animation_frames = {}

def load_animation(path, frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 1
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = os.path.join('assets', path, animation_frame_id + '.png')
        if os.path.exists(img_loc):
            try:
                animation_image = pygame.image.load(img_loc)
                animation_frames[animation_frame_id] = animation_image.copy()
                for i in range(frame):
                    animation_frame_data.append(animation_frame_id)
            except pygame.error as e:
                print(f"Error loading image {img_loc}: {e}")
        else:
            print(f"Warning: Animation frame not found: {img_loc}")
        n += 1
    return animation_frame_data if animation_frame_data else None

animation_database = {}

animation_paths = [
    ('settings', 'animations/settings', [7, 7]),
    ('menu', 'animations/menu', [7, 7, 7]),
    ('highscores', 'animations/highscores', [10, 10]),
    ('display_highscores', 'animations/displayhighscores', [7] * 35)
]

for name, path, durations in animation_paths:
    result = load_animation(path, durations)
    if result:
        animation_database[name] = result
    else:
        print(f"Warning: Failed to load animation for {name}")
        # Add a fallback animation or placeholder
        animation_database[name] = ['placeholder']

def resolution_changed(selected):
    resolution_string = selected.split('x')
    resolution_width = int(resolution_string[0])
    resolution_height = int(resolution_string[1])
    if (resolution_width != Var.WIDTH or resolution_height != Var.HEIGHT[1]):
        Var.WIDTH = resolution_width
        Var.HEIGHT = resolution_height
        resolution = (resolution_width, resolution_height)
        window_surface = pygame.display.set_mode(resolution)

# Main loop of game
async def startgame(level, highscore, menu_options):
    run = True
    flag1 = 0   # Select Flag
    rs = 0      # Result Flag
    error = 0   # Error Flag
    val = 0     # Put Value Flag
    g = 0       # Game Not Done Flag
    seconds = 0
    guesses = 0
    time = 0
    game_completed = False
    clock = pygame.time.Clock()
    runclock = pygame.USEREVENT+1
    pygame.time.set_timer(runclock, 1000)
    player_flip = False
    w, h, theme, volume = await getsettings()
    newvolume = volume/100
    try:
        if os.stat(grid_file).st_size > 0:
            if os.stat(time_file).st_size > 0:
                saved = await fileHandler.json_open(time_file)
                level = saved["level"]
                seconds = saved["currenttime"]
                guesses = saved["guesses"]
                dt = saved["dateandtime"]
            else:
                seconds = 0
            grid = await fileHandler.json_open(grid_file)
            print(f'\nLevel: {level}')
            print(f'Guesses: {guesses}')
            print(f'Saved TWICE-doku! Grid as of {dt}:')
            count = 0
            for i in grid:
                print(i[0:3], i[3:6], i[6:10])
                count += 1
                if count % 3 == 0:
                    print("")
        else:
            grid = generate.main(level)
    except OSError:
        grid = generate.main(level)
    solution = solve.sudoku(grid)
    pygame.mixer.init()
    game_music = load_music(theme)
    current_music_index = 0

    def play_next_song():
        nonlocal current_music_index
        pygame.mixer.music.load(game_music[current_music_index])
        pygame.mixer.music.play()
        current_music_index = (current_music_index + 1) % len(game_music)

    play_next_song()
    pygame.mixer.music.set_endevent(pygame.USEREVENT + 2)

    # Defining window size
    screen = pygame.display.set_mode((w, h))
    grid_size = w / 2
    grid_dims = 9
    dif = grid_size / grid_dims
    # Where to draw the top-left corner of the grid so it's centered in the screen
    grid_offs = (w // 2 - grid_size / 2,  h // 2 - grid_size / 2)
    click = False
    # The loop that keeps the window running
    while run:
        # Theme background
        backg = bg(theme)
        if backg == None:
            screen.fill(theme_attr[theme][1])
        else:
            newbg = pygame.transform.smoothscale(backg, (w, h))
            screen.blit(pygame.transform.flip(
                newbg, player_flip, False), (0, 0))
        option_button = pygame.Rect(w/40, h/60, w/10, h/16)
        draw(grid, grid_offs, dif, theme, screen, w)
        ptext.draw('OPTIONS', center=(option_button.center), width=360,
                   fontname=Var.text, fontsize=w/30, color=theme_attr[theme][5])
        # Loop through the events stored in event.get()
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT + 2:  # Music ended
                play_next_song()
            
            # Quit the game window
            if event.type == pygame.QUIT:
                await fileHandler.quit_save(
                    grid_file, time_file, level, grid, seconds, guesses, dt_string)
                pygame.quit()
                sys.exit()
            # Run timer
            if event.type == runclock:
                if rs == 0:
                    seconds += 1
            # Using mouse chose block to enter number
            if event.type == pygame.MOUSEBUTTONDOWN:
                flag1 = 1
                position = pygame.mouse.get_pos()
                if get_coordinates(position, grid_offs, grid_size, dif) != None:
                    x, y = get_coordinates(position, grid_offs, grid_size, dif)
                elif event.button == 1:
                    flag1 = 0
                    click = True
                else:
                    flag1 = 0
            # Get the number to be inserted
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x -= 1
                    if x < 0:
                        x += 1
                    else:
                        flag = 1
                if event.key == pygame.K_RIGHT:
                    x += 1
                    if x > 8:
                        x -= 1
                    else:
                        flag = 1
                if event.key == pygame.K_UP:
                    y -= 1
                    if y < 0:
                        y += 1
                    else:
                        flag = 1
                if event.key == pygame.K_DOWN:
                    y += 1
                    if y > 8:
                        y -= 1
                    else:
                        flag = 1
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, 
                                 pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                    val = int(event.unicode)
                # If R pressed regenerate the sudoku board
                if event.key == pygame.K_r:
                    rs = 0
                    error = 0
                    grid = generate.main(level)
                    solution = solve.sudoku(grid)
                    seconds = 0
                # If ESC is pressed go back to menu
                if event.key == pygame.K_ESCAPE:
                    g = 1
                    rs = 2
                    flag1 = 0
                    screen.fill(theme_attr[theme][1])
                    ptext.draw('Saving data...', center=((w/2, h/2)), width=360,
                               fontname=Var.text, fontsize=w/30, color=theme_attr[theme][5])
                    pygame.mixer.music.stop()
                    if solution != 0:
                        await fileHandler.quit_save(
                            grid_file, time_file, level, grid, seconds, guesses, dt_string)
                    run = False
                # Press spacebar to show solution (for code testing only!)
                if event.key == pygame.K_SPACE:
                    count = 0
                    print('\nSolution:')
                    for i in solution:
                        print(i[0:3], i[3:6], i[6:10])
                        count += 1
                        if count % 3 == 0:
                            print("")
        mx, my = pygame.mouse.get_pos()
        if option_button.collidepoint((mx, my)):
            if click:
                flag1 = 0
                if solution != 0:
                    await fileHandler.quit_save(
                        grid_file, time_file, level, grid, seconds, guesses, dt_string)
                pygame.display.update()
                should_return = await menu_options(return_to_game=True)  # Get the return value
                if not should_return:
                    return False  # Exit the game if options indicates we shouldn't return
                # Reload game settings after options
                w, h, theme, volume = await getsettings()
                newvolume = volume / 100
                game_music = load_music(theme)
                current_music_index = 0
                play_next_song()
                # Reset the screen and continue the game loop
                screen = pygame.display.set_mode((w, h))
                continue  # Skip the rest of the loop and start over
        if val != 0:
            try:
                if grid[int(y)][int(x)] == 0:
                    draw_val(val, x, y, screen, grid_offs, dif, theme)
                    if check_valid(grid, int(y), int(x), val, solution) == True:
                        grid[int(y)][int(x)] = val
                        count = 0
                        guesses += 1
                        print(f"\nGuesses:  {guesses}")
                        for i in grid:
                            print(i[0:3], i[3:6], i[6:10])
                            count += 1
                            if count % 3 == 0:
                                print("")
                        if grid == solution:
                            rs = 1
                    else:
                        guesses += 1
                        print(f"\nWrong Input!")
                        print(f"Guesses:  {guesses}")
                        count = 0
                        for i in grid:
                            print(i[0:3], i[3:6], i[6:10])
                            count += 1
                            if count % 3 == 0:
                                print("")
                        throw_error(grid, int(x), int(y), val, screen, grid_offs,
                                    grid_dims, grid_size, dif, theme, w, h, highscore, time)
                        grid[int(y)][int(x)] = 0
            except IndexError:
                flag1 = 0
            val = 0
        if error == 1:
            throw_error(grid, int(x), int(y), val, screen, grid_offs,
                        grid_dims, grid_size, dif, theme, w, h, highscore, time)
            
        if grid == solution and not game_completed:
            game_completed = True
            try:
                save_result = await fileHandler.score_save(Var.scoresfile, level, seconds, dt_string)
                if save_result:
                    logging.info(f"Score saved: Level {level}, Time {seconds}, Date {dt_string}")
                else:
                    logging.warning("Failed to save score.")
            except Exception as e:
                log_error(e, "Error during score saving")

            if grid_file:
                await fileHandler.remove_file(grid_file)
            if time_file:
                await fileHandler.remove_file(time_file)

        if game_completed:
            display_result(theme, w, h, time_convert(seconds))
            pygame.display.update()
            waiting_for_input = True
            while waiting_for_input:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            return True  # Start a new game
                        elif event.key == pygame.K_ESCAPE:
                            return False  # Return to menu
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                await asyncio.sleep(0)  # Allow other tasks to run

        if g == 0:
            draw(grid, grid_offs, dif, theme, screen, w)
            border(screen, theme, grid_offs, grid_size, dif, grid_dims)
        if flag1 == 1:
            draw_box(x, y, theme, screen, dif, grid_offs)
        if rs == 0:
            time = time_convert(seconds)
            instruction(time, highscore, theme, w, h)
        if rs == 1:
            result(theme, w, h, time)
        # Update window
        pygame.display.update()
        pygame.mixer.music.set_volume(newvolume)

        await asyncio.sleep(0)  # Allow other tasks to run

    return False  # Return to menu if the game loop exits
