import pygame
from classes.Dashboard import Dashboard
from classes.Level import Level
from classes.Menu import Menu
from classes.Sound import Sound
from entities.Mario import Mario
from window_state import set_screen, screen, windowSize, fullscreen

VIRTUAL_RES = (640, 480)

def main():
    global screen, windowSize, fullscreen
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()
    screen = set_screen(windowSize, False)
    max_frame_rate = 100
    game_surface = pygame.Surface(VIRTUAL_RES)
    dashboard = Dashboard("./img/font.png", 8, game_surface)
    sound = Sound()
    level = Level(game_surface, sound, dashboard)
    menu = Menu(game_surface, dashboard, level, sound)

    while not menu.start:
        menu.update()
        # Update game_surface reference in menu in case of resize/toggle
        menu.screen = game_surface
        menu.dashboard.screen = game_surface
        menu.level.screen = game_surface
        # Scale and blit to window
        _blit_scaled(game_surface, screen)
        pygame.display.update()

    mario = Mario(0, 0, level, game_surface, dashboard, sound)
    clock = pygame.time.Clock()

    while not mario.restart:
        pygame.display.set_caption("Super Mario running with {:d} FPS".format(int(clock.get_fps())))
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE and not fullscreen:
                screen = set_screen((event.w, event.h), False)
                # No need to update game_surface, just scale output
                dashboard.screen = game_surface
                level.screen = game_surface
                menu.screen = game_surface
                mario.screen = game_surface
                mario.pauseObj.screen = game_surface
        if mario.pause:
            mario.pauseObj.update()
        else:
            level.drawLevel(mario.camera)
            dashboard.update()
            mario.update()
        # Scale and blit to window
        _blit_scaled(game_surface, screen)
        pygame.display.update()
        clock.tick(max_frame_rate)
    return 'restart'

def _blit_scaled(source, dest):
    win_w, win_h = dest.get_size()
    if (win_w, win_h) == source.get_size():
        dest.blit(source, (0, 0))
    else:
        scaled = pygame.transform.smoothscale(source, (win_w, win_h))
        dest.blit(scaled, (0, 0))

if __name__ == "__main__":
    exitmessage = 'restart'
    while exitmessage == 'restart':
        exitmessage = main()
