import asyncio
import os
import pygame as pg
import random
import sys
import variables as Var
import twicedoku
import time
import json
import ptext
import pygame_gui as pgui
import filehandler as fileHandler
from audio import AudioHandler

audioHandler = AudioHandler()

# Opening intro
async def intro():
    global screen  # Declare screen as global
    screen = pg.display.set_mode((Var.WIDTH, Var.HEIGHT))  # Initialize screen here
    screen.fill(Var.BLACK)
    logo = pg.image.load('assets/pictures/intrologo.png')
    rect = logo.get_rect()
    rect.center = (Var.WIDTH/2, Var.HEIGHT/2)
    screen.blit(logo, rect)
    pg.display.flip()
    intro_sound = await audioHandler.load_sound('assets/songs/sfx/intro.ogg')
    if intro_sound:
        audioHandler.play(intro_sound)
    newvolume = Var.volumedef/100
    audioHandler.set_volume(newvolume)
    pg.time.wait(4160)
    await menu()  # Change this to await

# Top of the window
pg.display.set_caption('Twice-Doku! (Version - 1.0.0)')
screen = pg.display.set_mode((Var.WIDTH, Var.HEIGHT), 0, 32)
mainClock = pg.time.Clock()
gameIcon = pg.image.load(Var.icon)
pg.display.set_icon(gameIcon)

levels = ["Easy", "Mild", "Difficult"]

# Animated Backgrounds
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
                animation_image = pg.image.load(img_loc)
                animation_frames[animation_frame_id] = animation_image.copy()
                for i in range(frame):
                    animation_frame_data.append(animation_frame_id)
            except pg.error as e:
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
        window_surface = pg.display.set_mode(resolution)

# Settings Page
async def options(return_to_game=False):
    running = True
    player_action = 'settings'
    settings_surface = pg.display.set_mode((Var.WIDTH, Var.HEIGHT))
    player_frame = 0
    player_flip = False
    time_delta = mainClock.tick(60)/1000.0
    theme_path = os.path.join('themes', 'options.json')
    manager = pgui.UIManager((Var.WIDTH, Var.HEIGHT), theme_path)

    element_width = Var.WIDTH * 0.2
    element_height = Var.HEIGHT * 0.06
    start_x_label = Var.WIDTH * 0.3
    start_x_element = Var.WIDTH * 0.5
    start_y = Var.HEIGHT * 0.25
    spacing = element_height * 1.15

    themes = pgui.elements.UIDropDownMenu(
        options_list=['CHEER UP', 'What is Love', 'Dance the Night Away', 'Yes or Yes', 'FANCY', 'Breakthrough', 'Feel Special', 'More and More'],
        starting_option=Var.themedef,
        relative_rect=pg.Rect(start_x_element, start_y, element_width, element_height),
        manager=manager
    )
    resolution = pgui.elements.UIDropDownMenu(
        options_list=['1000x600', '1280x768'],
        starting_option=Var.resolutiondef,
        relative_rect=pg.Rect(start_x_element, start_y + spacing, element_width, element_height),
        manager=manager
    )
    volume_slider = pgui.elements.UIHorizontalSlider(
        relative_rect=pg.Rect(start_x_element, start_y + spacing * 2, element_width, element_height),
        start_value=Var.volumedef,
        value_range=(0, 100),
        manager=manager
    )

    while running:
        player_frame += 1
        if player_frame >= len(animation_database[player_action]):
            player_frame = 0
        player_img_id = animation_database[player_action][player_frame]
        player_img = pg.transform.scale(animation_frames[player_img_id], (Var.WIDTH, Var.HEIGHT))
        screen.blit(pg.transform.flip(player_img, player_flip, False), (0, 0))

        for event in pg.event.get():
            if event.type == pg.USEREVENT:
                if event.user_type == pgui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == volume_slider:
                        Var.volumedef = int(volume_slider.get_current_value())
                        newvolume = Var.volumedef / 100
                        audioHandler.set_volume(newvolume)
                        audioHandler.set_background_volume(newvolume)
                if event.user_type == pgui.UI_DROP_DOWN_MENU_CHANGED:
                    if event.ui_element == resolution:
                        if Var.resolutiondef != resolution.selected_option:
                            Var.resolutiondef = resolution.selected_option
                            resolution_changed(resolution.selected_option)
                            manager.clear_and_reset()
                            running = False
                            await options()
                    elif event.ui_element == themes:
                        if Var.themedef != themes.selected_option:
                            Var.themedef = themes.selected_option
            elif event.type == pg.QUIT:
                await fileHandler.settings_save(Var.settingsfile, Var.themedef, Var.resolutiondef, Var.volumedef)
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    await fileHandler.settings_save(Var.settingsfile, Var.themedef, Var.resolutiondef, Var.volumedef)
                    if return_to_game:
                        return True  # Return True to indicate we should go back to the game
                    else:
                        running = False
                        return False  # Return False to indicate we're not returning to a game
            manager.process_events(event)
        
        manager.update(time_delta)
        manager.draw_ui(settings_surface)
        
        ptext.draw("OPTIONS", center=(Var.WIDTH/2, Var.HEIGHT/8), width=Var.WIDTH, fontname=Var.title, fontsize=Var.headersize2,
                   color=Var.RED, gcolor=Var.DARKRED, owidth=1, ocolor=Var.ORANGE)
        ptext.draw('THEME/ERA', (start_x_label, start_y + element_height/4), fontname=Var.text, fontsize=Var.textsize, color=Var.RED, gcolor=Var.DARKRED)
        ptext.draw('RESOLUTION', (start_x_label, start_y + spacing + element_height/4), fontname=Var.text, fontsize=Var.textsize, color=Var.RED, gcolor=Var.DARKRED)
        ptext.draw('VOLUME', (start_x_label, start_y + spacing * 2 + element_height/4), fontname=Var.text, fontsize=Var.textsize, color=Var.RED, gcolor=Var.DARKRED)
        ptext.draw('PRESS ESC TO SAVE SETTINGS AND GO TO MENU', center=(Var.WIDTH/2, Var.HEIGHT/1.05),
                   width=360, fontname=Var.text, fontsize=Var.guidetextsize, color=Var.DARKRED)
        
        pg.display.update()
        mainClock.tick(60)
        await asyncio.sleep(0)

    return False

# Display Highscore functions
async def topScore(difficulty):
    running = True
    player_action = 'display_highscores'
    player_frame = 0
    player_flip = False
    while running:
        player_frame += 1
        if player_frame >= len(animation_database[player_action]):
            player_frame = 0
        player_img_id = animation_database[player_action][player_frame]
        player_img = pg.transform.scale(
            animation_frames[player_img_id], (Var.WIDTH, Var.HEIGHT))
        screen.blit(pg.transform.flip(player_img, player_flip, False), (0, 0))
        ptext.draw(difficulty, center=(Var.WIDTH/2, Var.HEIGHT/8), width=Var.WIDTH, fontname=Var.title, fontsize=Var.WIDTH/15,
                   color=Var.YELLOW3)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
        try:
            scores = await fileHandler.json_open(Var.scoresfile)
            try:
                if len(scores[difficulty]) == 0:
                    ptext.draw("No scores yet! Play to unlock leaderboard.", center=(
                        Var.WIDTH/2, Var.HEIGHT/2), width=360, fontname=Var.text, fontsize=Var.headersize2, color=Var.YELLOW3)
                    ptext.draw('Press ESC to escape', center=(Var.WIDTH/2, Var.HEIGHT/1.05),
                               width=360, fontname=Var.text, fontsize=Var.guidetextsize, color=Var.YELLOW3)
                elif len(scores[difficulty]) < 10:
                    scorelist = []
                    timelist = {}
                    for i in range(len(scores[difficulty])):
                        score = scores[difficulty][i].split('-')
                        scorelist.append(int(score[0]))
                        timelist[int(score[0])] = score[1]
                    scorelist.sort()
                    for j in range(0, len(scorelist)):
                        text = time.strftime(
                            "%H:%M:%S", time.gmtime(scorelist[j]))
                        ypos = Var.HEIGHT/4.5 + j*Var.HEIGHT/12.5
                        ptext.draw("{}. ".format(j+1) + "{}".format(text) + " {}".format(timelist[scorelist[j]]), center=(
                            Var.WIDTH/2, ypos), width=Var.WIDTH, fontname=Var.text, fontsize=Var.WIDTH/28, color=Var.YELLOW3)
                    ptext.draw('Press ESC to escape', center=(Var.WIDTH/2, Var.HEIGHT/1.05),
                               width=360, fontname=Var.text, fontsize=Var.guidetextsize, color=Var.YELLOW3)
                else:
                    scorelist = []
                    timelist = {}
                    for i in range(0, len(scores[difficulty])):
                        score = scores[difficulty][i].split('-')
                        scorelist.append(int(score[0]))
                        timelist[int(score[0])] = score[1]
                    scorelist.sort()
                    for j in range(0, 10):
                        text = time.strftime(
                            "%H:%M:%S", time.gmtime(scorelist[j]))
                        ypos = Var.HEIGHT/4.5 + j*Var.HEIGHT/14
                        ptext.draw("{}. ".format(j+1) + "{}".format(text) + " {}".format(timelist[scorelist[j]]), center=(
                            Var.WIDTH/2, ypos), width=Var.WIDTH, fontname=Var.text, fontsize=Var.WIDTH/30, color=Var.YELLOW3)
                    ptext.draw('Press ESC to escape', center=(Var.WIDTH/2, Var.HEIGHT/1.05),
                               width=360, fontname=Var.text, fontsize=Var.guidetextsize, color=Var.YELLOW3)
            except KeyError:
                ptext.draw("No scores yet! Play to unlock leaderboard.", center=(
                    Var.WIDTH/2, Var.HEIGHT/2), width=360, fontname=Var.text, fontsize=Var.headersize2, color=Var.YELLOW3)
                ptext.draw('Press ESC to escape', center=(Var.WIDTH/2, Var.HEIGHT/1.05),
                           width=360, fontname=Var.text, fontsize=Var.guidetextsize, color=Var.YELLOW3)
        except FileNotFoundError:
            ptext.draw("No scores yet! Play to unlock leaderboard.", center=(
                Var.WIDTH/2, Var.HEIGHT/2), width=360, fontname=Var.text, fontsize=Var.headersize2, color=Var.YELLOW3)
            ptext.draw('Press ESC to escape', center=(Var.WIDTH/2, Var.HEIGHT/1.05),
                       width=360, fontname=Var.text, fontsize=Var.guidetextsize, color=Var.YELLOW3)
        pg.display.update()
        mainClock.tick(60)
        await asyncio.sleep(0)


async def displayHighscore(difficulty):
    try:
        try:
            with open(Var.scoresfile) as savedscores:
                scores = json.load(savedscores)
                if len(scores[difficulty]) == 0:
                    return 0
                else:
                    scorelist = []
                    for i in range(0, len(scores[difficulty])):
                        score = scores[difficulty][i].split('-')
                        scorelist.append(int(score[0]))
                    scorelist.sort()
                    return time.strftime("%H:%M:%S", time.gmtime(int(scorelist[0])))
        except KeyError:
            return 0
    except FileNotFoundError:
        return 0


async def highscore():
    running = True
    click = False
    player_action = 'highscores'
    player_frame = 0
    player_flip = False
    while running:
        button_1 = pg.Rect(Var.WIDTH/2.5, Var.HEIGHT/4,
                           Var.WIDTH/5, Var.HEIGHT/16)
        button_2 = pg.Rect(Var.WIDTH/2.5, (Var.HEIGHT/4) +
                           (Var.HEIGHT/12), Var.WIDTH/5, Var.HEIGHT/16)
        button_3 = pg.Rect(Var.WIDTH/2.5, (Var.HEIGHT/4) +
                           (Var.HEIGHT/12)*2, Var.WIDTH/5, Var.HEIGHT/16)
        player_frame += 1
        if player_frame >= len(animation_database[player_action]):
            player_frame = 0
        player_img_id = animation_database[player_action][player_frame]
        player_img = pg.transform.scale(
            animation_frames[player_img_id], (Var.WIDTH, Var.HEIGHT))
        screen.blit(pg.transform.flip(player_img, player_flip, False), (0, 0))
        ptext.draw("Highscores", center=(Var.WIDTH/2, Var.HEIGHT/8), width=Var.WIDTH, fontname=Var.title, fontsize=Var.WIDTH/15,
                   color=Var.YELLOW2, gcolor=Var.DARKYELLOW, owidth=1, ocolor=Var.WHITE)
        mx, my = pg.mouse.get_pos()
        if button_1.collidepoint((mx, my)):
            Var.button1 = Var.PEACH
            if click:
                await topScore("Easy")
        elif button_2.collidepoint((mx, my)):
            Var.button2 = Var.PEACH
            if click:
                await topScore("Mild")
        elif button_3.collidepoint((mx, my)):
            Var.button3 = Var.PEACH
            if click:
                await topScore("Difficult")
        else:
            Var.button1 = Var.button1def
            Var.button2 = Var.button2def
            Var.button3 = Var.button3def
        click = False

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        ptext.draw('EASY', center=(button_1.center), width=360,
                   fontname=Var.text, fontsize=Var.headersize2, color=Var.button1)
        ptext.draw('MILD', center=(button_2.center), width=360,
                   fontname=Var.text, fontsize=Var.headersize2, color=Var.button2)
        ptext.draw('DIFFICULT', center=(button_3.center), width=360,
                   fontname=Var.text, fontsize=Var.headersize2, color=Var.button3)
        ptext.draw('Press ESC to escape', center=(Var.WIDTH/2, Var.HEIGHT/1.05),
                   width=360, fontname=Var.text, fontsize=Var.guidetextsize, color=Var.PEACH)
        pg.display.update()
        mainClock.tick(60)
        await asyncio.sleep(0)  # Allow other coroutines to run

    return False  # Return False to indicate we should return to the main menu

async def reset_menu_music():
    menu_music = load_music()
    if menu_music:
        audioHandler.play_music(menu_music[0])  # Play the first song in the menu music list
        audioHandler.set_music_end_event()
        
# Go to game
async def play(level, highscore, menu_options):
    audioHandler.stop_music()  # Stop menu music
    while True:
        try:
            start_new_game = await twicedoku.startgame(level, highscore, menu_options)
            if not start_new_game:
                break
        except Exception as e:
            print(f"An error occurred in play function: {e}")
            break
    
    # Reset music when returning to the main menu
    await reset_menu_music()
    await menu()

# Background Music
def load_music():
    path = os.path.join("assets", "songs", "menu")
    songs = []
    for filename in os.listdir(path):
        if filename.endswith(".ogg"):
            songs.append(os.path.join(path, filename))
    return songs

# Don't allow changing of levels if there is a game in progress
async def get_level():
    try:
        if os.stat(Var.gridfile).st_size > 0:
            if os.stat(Var.timefile).st_size > 0:
                stats = await fileHandler.json_open(Var.timefile)
                level = stats["level"]
            else:
                level = levels[0]
        else:
            level = levels[0]
    except OSError:
        level = levels[0]
    return level

# Main Menu
async def menu():
    click = False
    player_action = 'menu'
    player_frame = 0
    player_flip = False
    level = await get_level()
    menu_music = load_music()
    displayscore = await displayHighscore(level)
    is_running = True
    i = 0
    while is_running:
        # Play a list of songs in the background
        if not hasattr(audioHandler, 'current_background_music') or audioHandler.current_background_music is None:
            menu_music_file = random.choice(menu_music)
            sound = await audioHandler.load_sound(menu_music_file)
            if sound:
                audioHandler.play(sound, loop=True, volume=audioHandler.background_volume)
                audioHandler.current_background_music = sound
        
        newvolume = Var.volumedef/100
        audioHandler.set_volume(newvolume)
        
        # Background animation
        player_frame += 1
        if player_frame >= len(animation_database[player_action]):
            player_frame = 0
        player_img_id = animation_database[player_action][player_frame]
        player_img = pg.transform.scale(
            animation_frames[player_img_id], (Var.WIDTH, Var.HEIGHT))
        screen.blit(pg.transform.flip(player_img, player_flip, False), (0, 0))

        # Header
        ptext.draw("Twice-Doku!", center=(Var.WIDTH/2, Var.HEIGHT/5), width=Var.WIDTH, fontname=Var.title, fontsize=Var.WIDTH/10,
                   color=Var.PINK, gcolor=Var.DARKPINK, owidth=1, ocolor=Var.DIRTYWHITE)

        mx, my = pg.mouse.get_pos()

        button_1 = pg.Rect(Var.WIDTH/2.5, Var.HEIGHT/2.5,
                           Var.WIDTH/5, Var.HEIGHT/16)
        button_2 = pg.Rect(Var.WIDTH/2.5, Var.HEIGHT/2.5 +
                           Var.HEIGHT/12, Var.WIDTH/5, Var.HEIGHT/16)
        button_3 = pg.Rect(Var.WIDTH/2.5, Var.HEIGHT/2.5 +
                           (Var.HEIGHT/12)*2, Var.WIDTH/5, Var.HEIGHT/16)
        button_4 = pg.Rect(Var.WIDTH/2.5, Var.HEIGHT/2.5 +
                           (Var.HEIGHT/12)*3, Var.WIDTH/5, Var.HEIGHT/16)
        button_5 = pg.Rect(Var.WIDTH/1.6, Var.HEIGHT/1.2,
                           Var.WIDTH/3, Var.HEIGHT/16)
        if button_1.collidepoint((mx, my)):
            Var.button1 = Var.hoverbutton
            if click:
                audioHandler.stop_all()
                await play(level, displayscore, options)
                is_running = False
        elif button_2.collidepoint((mx, my)):
            Var.button2 = Var.hoverbutton
            if click:
                options_result = await options()
                if options_result is False:
                    # Returned from options, refresh the menu
                    continue
        elif button_3.collidepoint((mx, my)):
            Var.button3 = Var.hoverbutton
            if click:
                highscore_result = await highscore()
                if highscore_result is False:
                    # Returned from highscore, refresh the menu
                    continue
        elif button_4.collidepoint((mx, my)):
            Var.button4 = Var.hoverbutton
            if click:
                is_running = False
                pg.quit()
                sys.exit()
        elif button_5.collidepoint((mx, my)):
            Var.difficulty = Var.hoverdifficulty
            try:
                if os.stat(Var.gridfile).st_size > 0:
                    if os.stat(Var.timefile).st_size > 0:
                        if click:
                            pass
                    else:
                        if click:
                            if i == 2:
                                i = 0
                            else:
                                i += 1
                            level = levels[i]
                else:
                    if click:
                        if i == 2:
                            i = 0
                        else:
                            i += 1
                        level = levels[i]
            except OSError:
                if click:
                    if i == 2:
                        i = 0
                    else:
                        i += 1
                    level = levels[i]
        else:
            Var.button1 = Var.button1def
            Var.button2 = Var.button2def
            Var.button3 = Var.button3def
            Var.button4 = Var.button4def
            Var.difficulty = Var.difficultydef
        click = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                is_running = False
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            ptext.draw('PLAY', center=(button_1.center), width=360,
                       fontname=Var.text, fontsize=Var.WIDTH/20, color=Var.button1)
            ptext.draw('OPTIONS', center=(button_2.center), width=360,
                       fontname=Var.text, fontsize=Var.WIDTH/20, color=Var.button2)
            ptext.draw('RANKINGS', center=(button_3.center), width=360,
                       fontname=Var.text, fontsize=Var.WIDTH/20, color=Var.button3)
            ptext.draw('EXIT', center=(button_4.center), width=360,
                       fontname=Var.text, fontsize=Var.WIDTH/20, color=Var. button4)
            ptext.draw('DIFFICULTY: {}'.format(level), center=(button_5.center),
                       width=360, fontname=Var.text, fontsize=Var.WIDTH/28, color=Var.difficulty)
            pg.display.update()
            mainClock.tick(60)
            await asyncio.sleep(0)  # Allow other coroutines to run

    return False  # Return False to indicate we should exit the game

# In your main game loop or wherever you call menu()
async def main():
    # ... other initialization code ...
    while True:
        result = await menu()
        if result is False:
            break
    # ... cleanup code ...

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
