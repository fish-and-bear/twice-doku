import asyncio
import pygame
import sys

async def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    try:
        from mainmenu import intro
    except ImportError as e:
        print(f"Error importing mainmenu: {e}")
        return

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        try:
            await intro(screen)  # Pass the screen to intro
        except Exception as e:
            print(f"Error in intro: {e}")
            running = False

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())