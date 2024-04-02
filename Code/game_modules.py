import sys
from settings import *

pygame.mixer.init()
end_music = pygame.mixer.Sound('../Music/death music.mp3')


def game(level):
    bg_img = pygame.image.load('../Graphics/Decorations/background.jpg').convert_alpha()
    bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
    while True:
        screen.blit(bg_img, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        # music
        level.run()

        pygame.display.update()
        clock.tick(60)


def respawn(level):
    bg_img = pygame.image.load('../Graphics/Decorations/background.jpg').convert_alpha()
    click = False
    bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
    respawn_text = pygame.image.load('../Graphics/Background/respawntext.png').convert_alpha()
    respawn_button = pygame.image.load('../Graphics/Background/respawnbutton.png').convert_alpha()
    while True:
        screen.blit(bg_img, (0, 0))
        mx, my = pygame.mouse.get_pos()
        button = pygame.Rect(360, 430, 475, 120)
        if button.collidepoint((mx, my)):
            if click:
                game(level)
        screen.blit(respawn_button, (210, 400))
        screen.blit(respawn_text, (335, 100))
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
        clock.tick(60)


def end():
    bg_img = pygame.image.load('../Graphics/Decorations/background.jpg').convert_alpha()
    click = False
    bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
    end_maintext = pygame.image.load('../Graphics/Background/endmaintext.png').convert_alpha()
    end_smalltext = pygame.image.load('../Graphics/Background/endsmalltext.png').convert_alpha()
    end_button = pygame.image.load('../Graphics/Background/endbutton.png').convert_alpha()
    end_music.play(loops=-1)
    while True:
        screen.blit(bg_img, (0, 0))
        mx, my = pygame.mouse.get_pos()
        button = pygame.Rect(360, 430, 475, 120)
        if button.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()
        click = False
        screen.blit(end_button, (210, 400))
        screen.blit(end_maintext, (280, 100))
        screen.blit(end_smalltext, (375, 250))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
        clock.tick(60)


def completed():
    bg_img = pygame.image.load('../Graphics/Decorations/background.jpg').convert_alpha()
    click = False
    bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
    completed_maintext = pygame.image.load('../Graphics/Background/completedcongrats.png').convert_alpha()
    completed_smalltext = pygame.image.load('../Graphics/Background/completedsmalltext.png').convert_alpha()
    end_button = pygame.image.load('../Graphics/Background/endbutton.png').convert_alpha()
    while True:
        screen.blit(bg_img, (0, 0))
        mx, my = pygame.mouse.get_pos()
        button = pygame.Rect(360, 430, 475, 120)
        if button.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()
        click = False
        screen.blit(end_button, (210, 400))
        screen.blit(completed_maintext, (125, 100))
        screen.blit(completed_smalltext, (200, 250))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
        clock.tick(60)
