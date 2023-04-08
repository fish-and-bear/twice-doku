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
audioHandler = AudioHandler()
pygame.init()
pygame.mixer.init()
audioHandler.pre_init()
audioHandler.init()
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
theme_attr = {'CHEER UP': ['tiles/cheerup', Var.cuBLUEGREEN, Var.cuWHITE, Var.cuWHITE, Var.cuWHITE, Var.cuWHITE],
              'What is Love': ['tiles/whatislove', Var.wilPINK, Var.wilRED, Var.wilBLACK, Var.wilRED, Var.wilRED],
              'Dance the Night Away': ['tiles/dancethenightaway', Var.dtnaLIGHTBLUE, Var.dtnaWHITE, Var.dtnaYELLOW, Var.dtnaBLUE, Var.dtnaBLUE],
              'Yes or Yes': ['tiles/yesoryes', Var.yoyLIGHTPURPLE, Var.yoyWHITE, Var.yoyDARKPURPLE, Var.yoyDARKPURPLE, Var.yoyDARKPURPLE],
              'FANCY': ['tiles/fancy', Var.fSKYBLUE, Var.fYELLOW, Var.fPINK, Var.fWHITE, Var.fWHITE],
              'Breakthrough': ['tiles/breakthrough', Var.bDARKBLUE, Var.bPINK, Var.bPURPLE, Var.bWHITE, Var.bWHITE],
              'Feel Special': ['tiles/feelspecial', Var.fsPEACH, Var.fsLIGHTGOLD, Var.fsGOLD, Var.fsGOLD, Var.fsLIGHTGOLD],
              'More and More': ['tiles/moreandmore', Var.mamGREEN, Var.mamGOLD, Var.mamORANGE, Var.mamWHITE, Var.mamWHITE]
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
def result(theme, w, h, time):
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
    path = "./songs/" + theme + "/"
    songs = []
    for filename in os.listdir(path):
        if filename.endswith(".ogg"):
            songs.append(pygame.mixer.Sound(os.path.join(path, filename)))
        else:
            continue
    return songs

# If ever I decide to put background pictures...
def bg(theme):
    try:
        background_image = pygame.image.load('/pictures/' + theme + '.png')
        return background_image
    except FileNotFoundError:
        return None

# Settings variables
def getsettings():
    try:
        if os.stat(settings_file).st_size > 0:
            settings = fileHandler.json_open(settings_file)
            resolution_string = settings['resolution'].split('x')
            w = int(resolution_string[0])
            h = int(resolution_string[1])
            theme = settings["theme"]
            volume = settings["volume"]
        else:
            theme = Var.themedef
            w = Var.WIDTH
            h = Var.HEIGHT
            volume = Var.volumedef
    except OSError:
        theme = Var.themedef
        w = Var.WIDTH
        h = Var.HEIGHT
        volume = Var.volumedef
    return w, h, theme, volume

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
        img_loc = path + '/' + animation_frame_id + '.png'
        # player_animations/idle/idle_0.png
        animation_image = pygame.image.load(img_loc)
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

animation_database = {}

animation_database['settings'] = load_animation('animations/settings', [7, 7])

def resolution_changed(selected):
    resolution_string = selected.split('x')
    resolution_width = int(resolution_string[0])
    resolution_height = int(resolution_string[1])
    if (resolution_width != Var.WIDTH or resolution_height != Var.HEIGHT[1]):
        Var.WIDTH = resolution_width
        Var.HEIGHT = resolution_height
        resolution = (resolution_width, resolution_height)
        window_surface = pygame.display.set_mode(resolution)

# Settings page
def options(screen, theme):
    running = True
    player_action = 'settings'
    mainClock = pygame.time.Clock()
    settings_surface = pygame.display.set_mode((Var.WIDTH, Var.HEIGHT))
    player_frame = 0
    player_flip = False
    time_delta = mainClock.tick(60)/1000.0
    manager = pgui.UIManager((Var.WIDTH, Var.HEIGHT), Var.optionstheme)
    themes = pgui.elements.UIDropDownMenu(options_list=['CHEER UP', 'What is Love', 'Dance the Night Away', 'Yes or Yes', 'FANCY', 'Breakthrough', 'Feel Special', 'More and More'],
                                          starting_option=Var.themedef,
                                          relative_rect=pygame.Rect(
                                              Var.WIDTH/2.5, Var.HBTN1-Var.bottommargin*2, Var.WIDTH/5, Var.HEIGHT/16),
                                          manager=manager)
    resolution = pgui.elements.UIDropDownMenu(options_list=['1000x600', '1280x768'],
                                              starting_option=Var.resolutiondef,
                                              relative_rect=pygame.Rect(
                                                  Var.WIDTH/2.5, Var.HBTN1-Var.bottommargin*0.5, Var.WIDTH/5, Var.HEIGHT/16),
                                              manager=manager)
    volume_slider = pgui.elements.UIHorizontalSlider(relative_rect=pygame.Rect(Var.WIDTH/2.5, Var.HBTN1+Var.bottommargin, Var.WIDTH/5, Var.HEIGHT/16),
                                                     start_value=Var.volumedef,
                                                     value_range=(0, 100),
                                                     manager=manager)
    # volume_slider.enable()
    while running:
        player_frame += 1
        if player_frame >= len(animation_database[player_action]):
            player_frame = 0
        player_img_id = animation_database[player_action][player_frame]
        player_img = pygame.transform.scale(
            animation_frames[player_img_id], (Var.WIDTH, Var.HEIGHT))
        screen.blit(pygame.transform.flip(
            player_img, player_flip, False), (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if event.user_type == pgui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == volume_slider:
                        Var.volumedef = volume_slider.get_current_value()
                if event.user_type == pgui.UI_DROP_DOWN_MENU_CHANGED and event.ui_element == resolution:
                    if Var.resolutiondef != resolution.selected_option:
                        Var.resolutiondef = resolution.selected_option
                        resolution_changed(resolution.selected_option)
                        manager.clear_and_reset()
                        running = False
                        options(screen, theme)
                if event.user_type == pgui.UI_DROP_DOWN_MENU_CHANGED and event.ui_element == themes:
                    if Var.themedef != themes.selected_option:
                        Var.themedef = themes.selected_option
            elif event.type == pygame.QUIT:
                fileHandler.settings_save(
                    Var.settingsfile, Var.themedef, Var.resolutiondef, Var.volumedef)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    fileHandler.settings_save(
                        Var.settingsfile, Var.themedef, Var.resolutiondef, Var.volumedef)
                    if Var.themedef != theme:
                        audioHandler.clear_all_queues()
                        audioHandler.fadeout_all(2000)
                    running = False
            manager.process_events(event)
            volume = volume_slider.get_current_value()
            Var.volumedef = volume
        newvolume = volume/100
        audioHandler.set_all_volume(newvolume)
        ptext.draw("Options", center=(Var.WIDTH/2, Var.HEIGHT/20), width=Var.WIDTH, fontname=Var.title, fontsize=Var.headersize2,
                   color=Var.RED, gcolor=Var.DARKRED, owidth=1, ocolor=Var.ORANGE)
        ptext.draw('Theme/Era', center=(Var.WIDTH/2, Var.HBTN1-Var.bottommargin*2.2),
                   width=360, fontname=Var.text, fontsize=Var.textsize, color=Var.RED)
        ptext.draw('Resolution', center=(Var.WIDTH/2, Var.HBTN1-Var.bottommargin*0.7),
                   width=360, fontname=Var.text, fontsize=Var.textsize, color=Var.RED)
        ptext.draw('Volume: {}'.format(volume), center=(Var.WIDTH/2, Var.HBTN1+Var.bottommargin *
                                                        0.8), width=360, fontname=Var.text, fontsize=Var.textsize, color=Var.RED)
        ptext.draw('Press ESC to save settings and go to menu', center=(Var.WIDTH/2, Var.HEIGHT/1.05),
                   width=360, fontname=Var.text, fontsize=Var.guidetextsize, color=Var.DARKRED)
        manager.update(time_delta)
        manager.draw_ui(settings_surface)
        pygame.display.update()
        mainClock.tick(60)

# Main loop of game
def startgame(level, highscore):
    run = True
    flag1 = 0   # Select Flag
    rs = 0      # Result Flag
    error = 0   # Error Flag
    val = 0     # Put Value Flag
    g = 0       # Game Not Done Flag
    seconds = 0
    guesses = 0
    time = 0
    clock = pygame.time.Clock()
    runclock = pygame.USEREVENT+1
    pygame.time.set_timer(runclock, 1000)
    player_flip = False
    w, h, theme, volume = getsettings()
    newvolume = volume/100
    try:
        if os.stat(grid_file).st_size > 0:
            if os.stat(time_file).st_size > 0:
                saved = fileHandler.json_open(time_file)
                level = saved["level"]
                seconds = saved["currenttime"]
                guesses = saved["guesses"]
                dt = saved["dateandtime"]
            else:
                seconds = 0
            grid = fileHandler.json_open(grid_file)
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
    game_music = load_music(theme)
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
        audioHandler.set_all_volume(newvolume)
        if len(audioHandler.backgroundQueue) == 0:
            audioHandler.queue(random.choice(game_music),
                               AudioHandler.BACKGROUND)
        audioHandler.refresh()
        # Theme background
        backg = bg(theme)
        if backg == None:
            screen.fill(theme_attr[theme][1])
        else:
            newbg = pygame.transform.smoothscale(backg, (WIDTH, HEIGHT))
            screen.blit(pygame.transform.flip(
                newbg, player_flip, False), (0, 0))
        option_button = pygame.Rect(w/40, h/60, w/10, h/16)
        draw(grid, grid_offs, dif, theme, screen, w)
        ptext.draw('OPTIONS', center=(option_button.center), width=360,
                   fontname=Var.text, fontsize=w/30, color=theme_attr[theme][5])
        # Loop through the events stored in event.get()
        for event in pygame.event.get():
            # Quit the game window
            if event.type == pygame.QUIT:
                fileHandler.quit_save(
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
                if event.key == pygame.K_1:
                    val = 1
                if event.key == pygame.K_2:
                    val = 2
                if event.key == pygame.K_3:
                    val = 3
                if event.key == pygame.K_4:
                    val = 4
                if event.key == pygame.K_5:
                    val = 5
                if event.key == pygame.K_6:
                    val = 6
                if event.key == pygame.K_7:
                    val = 7
                if event.key == pygame.K_8:
                    val = 8
                if event.key == pygame.K_9:
                    val = 9
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
                    audioHandler.clear_all_queues()
                    audioHandler.fadeout_all(2000)
                    if solution != 0:
                        fileHandler.quit_save(
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
            theme_attr[theme][5] = theme_attr[theme][3]
            if click:
                flag1 = 0
                g = 1
                rs = 2
                if solution != 0:
                    fileHandler.quit_save(
                        grid_file, time_file, level, grid, seconds, guesses, dt_string)
                options(screen, theme)
                run = False
                pygame.display.update()
                startgame(level, highscore)
        else:
            theme_attr[theme][5] = theme_attr[theme][4]
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
        if grid == solution:
            result(theme, w, h, time)
            fileHandler.score_save(scores_file, level, seconds, dt_string)
            fileHandler.remove_file(grid_file)
            fileHandler.remove_file(time_file)
            rs = 1
            solution = 0
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
