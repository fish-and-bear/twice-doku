import asyncio
import pygame
import pygame_gui
import os
import warnings
from mainmenu import intro

# Add this near the top of your main script, before initializing Pygame
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
warnings.filterwarnings("ignore", category=UserWarning, module="pygame")

async def main():
    print("Initializing Pygame...")
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        await intro()
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()
    print("Pygame quit successfully.")

if __name__ == "__main__":
    print("Starting main function...")
    asyncio.run(main())
    print("Main function ended.")
