import pygame

windowSize = [640, 480]
fullscreen = False
screen = None

def set_screen(size, fullscreen_mode):
    global screen, fullscreen, windowSize
    flags = pygame.RESIZABLE
    if fullscreen_mode:
        flags |= pygame.FULLSCREEN
    screen = pygame.display.set_mode(size, flags)
    windowSize[0], windowSize[1] = size[0], size[1]
    fullscreen = fullscreen_mode
    return screen 