# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('assets/pictures/twice-logo.ico', '.'),  # Path to your icon file
        ('assets', 'assets'),  # Path to your assets directory
        ('assets/files/settings.json', 'assets/files'),  # Path to your settings.json file
        ('assets/files/grid.json', 'assets/files'),  # Path to your grid.json file
        ('assets/files/time.json', 'assets/files'),  # Path to your time.json file
        ('assets/files/scores.json', 'assets/files'),  # Path to your scores.json file
        ('themes/options.json', 'assets/themes'),  # Path to your options.json file
        ('themes/button.json', 'assets/themes'),  # Path to your button.json file
        ('themes/default_theme.json', 'themes'),  # Path to your default_theme.json file
        ('themes/button2.json', 'themes'),  # Path to your button2.json file
        ('themes/label.json', 'themes'),  # Path to your label.json file
        ('themes/menu.json', 'themes'),  # Path to your menu.json file
        ('pygame_gui/data/default_theme.json', 'pygame_gui/data'),  # Path to pygame_gui default theme
        ('assets/pictures/intrologo.png', 'assets/pictures'),  # Path to your intro logo
        ('assets/songs/sfx/intro.ogg', 'assets/songs/sfx'),  # Path to your intro sound
        ('themes', 'themes'),  # Include the themes directory
        ('pygame_gui', 'pygame_gui'),  # Include the pygame_gui directory
    ],
    hiddenimports=['pygame', 'pygame_gui', 'ptext', 'generate', 'solve', 'filehandler', 'audio'],
    hookspath=['hooks'],  # Add the hooks directory
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='twice_doku',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    icon='assets/pictures/twice-logo.ico'  # Path to your icon file
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TWICE-Doku!',
)