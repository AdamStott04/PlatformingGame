import sys
from settings import *
from level import Level
from game_data import Level_0
from game_modules import game

# game setup
pygame.init()
lives = 3
coins = 0
sound = True
music = pygame.mixer.Sound('../Music/title screen.mp3')
music.set_volume(0.5)


def main_menu(sound):
    text = pygame.image.load('../Graphics/Background/mainmenutext.png').convert_alpha()
    click = False
    bg_img = pygame.image.load('../Graphics/Background/mainmenubackground.jpg').convert_alpha()
    bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
    start_button = pygame.image.load('../Graphics/Background/mainmenuplaybutton.png').convert_alpha()
    options_button = pygame.image.load('../Graphics/Background/mainmenuoptionsbutton.png').convert_alpha()
    if sound == True:
        music.play(loops=-1)
    else:
        music.stop()
    while True:

        screen.blit(bg_img, (0, 0))
        screen.blit(text, (250, 100))
        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(360, 290, 450, 100)
        button_2 = pygame.Rect(360, 490, 450, 100)

        if button_1.collidepoint((mx, my)):
            if click:
                music.stop()
                game(level)
        if button_2.collidepoint((mx, my)):
            if click:
                options(sound)
        screen.blit(start_button, (200, 250))
        screen.blit(options_button, (200, 450))

        click = False
        level = Level(Level_0, screen, lives, coins, sound)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()
        clock.tick(60)


def options(sound):
    bg_img = pygame.image.load('../Graphics/Background/mainmenubackground.jpg').convert_alpha()
    bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
    text = pygame.image.load('../Graphics/Background/optionstext.png').convert_alpha()
    sound_enabled = pygame.image.load('../Graphics/Background/sound-fixed.png')
    sound_disabled = pygame.image.load('../Graphics/Background/nosound-fixed.png')
    mute_button = pygame.image.load('../Graphics/Background/optionsmute.png')
    unmute_button = pygame.image.load('../Graphics/Background/optionsunmute.png')
    back_button = pygame.image.load('../Graphics/Background/optionsback.png')
    click = False
    while True:
        screen.blit(bg_img, (0, 0))
        screen.blit(text, (350, 100))
        screen.blit(back_button, (200, 500))
        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(360, 340, 450, 100)
        button_2 = pygame.Rect(360, 540, 450, 100)
        if sound == True:
            screen.blit(sound_enabled, (510, 210))
            screen.blit(mute_button, (200, 300))
        else:
            screen.blit(sound_disabled, (510, 210))
            screen.blit(unmute_button, (200, 300))

        if button_1.collidepoint((mx, my)):
            if click:
                if sound == True:
                    music.stop()
                    sound = False
                else:
                    music.play(loops=-1)
                    sound = True
        if button_2.collidepoint((mx, my)):
            if click:
                music.stop()
                main_menu(sound)
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()
        clock.tick(60)


main_menu(sound)
