# TWICE-Doku!

_TWICE-doku!_ is a picture-based reintroduction of the classic 9x9 grid Sudoku puzzle game.

The player is given a 9x9 grid that is partially-filled according to the player’s chosen difficulty level (Easy, Mild, or Difficult), and, under the least possible amount of time, the player has to fill the empty cells of this 9x9 grid using the picture choices so that each row, each column, and each of the nine 3x3 minigrids that make up the 9x9 grid contain all nine members of the South Korean girl group TWICE. The player is challenged to continually beat the best time recorded in the game’s leaderboards. _TWICE-doku!_ also features various themes and instrumental soundtracks based on the style and music of different TWICE ‘eras’. This game utilizes the Pygame library.

## Requirements

- Python 3.9+
- Pygame 2.0.1
- Pygame GUI 0.5.7

## How to install

1. Run this command in a command prompt:
```
cd /directory/to/TWICE-Doku!
```

2. Then run:
```
pip install -r requirements.txt
```

3. Finally, run:
```
py main.py
```

Then you're all set!

## Compiling to .exe

To compile the game to a `.exe` file, follow these steps:

1. Ensure you have PyInstaller installed. If not, install it using:
```
pip install pyinstaller
```

2. Run the following command to generate the executable:
```
pyinstaller TWICE-Doku!.spec
```

3. The executable will be created in the `dist/TWICE-Doku!` directory.

## Web Deployment

To deploy the game for web browsers:

1. Install Pygbag: `pip install pygbag`
2. Run the build command:
   ```
   pygbag --app twice-doku --title "TWICE-Doku!" --html itch.html --cdn https://pygame-web.github.io/archives/0.9/ web_main.py
   ```
3. The built files will be in the `build/web` directory
4. Upload the contents of `build/web` to your web server
5. To run the game locally after building:
   - Navigate to the `build/web` directory
   - Start a local server:
     ```
     python -m http.server 8000
     ```
   - Open a web browser and go to `http://localhost:8000`