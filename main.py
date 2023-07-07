import pygame
from background import Background
from player import Player
from boss import Boss1, Boss2, Boss3
import asyncio
from pygame import event

pygame.init()

clock = pygame.time.Clock()
fps = 60

# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# width, height = pyautogui.size()

width, height = 1300, 900
screen = pygame.display.set_mode(((width, height)))

pygame.display.set_caption('Merry Christmas!')

pygame.mixer.music.load('sounds/bg_music.mp3')
pygame.mixer.music.play(-1, 0.0)

bg = Background(0, 0)

global state
state = ["begin"]


async def play(which_boss, bg2):
    while True:
        # print(state)
        if state[0] == "begin":
            player = Player(width / 5, height / 3)

            player.basic_keys(bg, play, True, state)
            pygame.display.update()

        elif state[0] == "selection":
            # player = Player(width / 5, height / 3)
            bg2 = Background(0, 0)

            # while True:

            clock.tick(fps)

            player.basic_keys(bg2, play, False, state)

            bg2.selection_screen(player, play, bg2, state)

            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                bg2.again = True

            pygame.display.update()
            # pygame.display.update()
        elif state[0] == "death1":
            t = "player_death"
            bg2.again = False
            bg.ending_bg(t)
            player.basic_keys(bg, play, False, state)
            pygame.display.update()
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                state[0] = "boss1"
        elif state[0] == "win1":
            t = "player_win"
            bg2.again = False
            bg.ending_bg(t)
            player.basic_keys(bg, play, False, state)
            pygame.display.update()
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                state[0] = "boss1"
        elif state[0] == "death2":
            t = "player_death"
            bg2.again = False
            bg.ending_bg(t)
            player.basic_keys(bg, play, False, state)
            pygame.display.update()
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                state[0] = "boss2"
        elif state[0] == "win2":
            t = "player_win"
            bg2.again = False
            bg.ending_bg(t)
            player.basic_keys(bg, play, False, state)
            pygame.display.update()
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                state[0] = "boss2"
        else:
            if state[0] == "boss1":
                boss = Boss1(width - 90, height / 1.5)
                bg.surface = pygame.image.load('images/background.png')
                bg.surface = pygame.transform.scale(bg.surface, (width, height)).convert_alpha()
                bg.mg_surface = pygame.image.load('images/midground.png')
                bg.mg_surface = pygame.transform.scale(bg.mg_surface, (width, height / 2)).convert_alpha()
            elif state[0] == "boss2":
                boss = Boss2(width - 90, height / 1.5, player)
                bg.surface = pygame.image.load('images/cranes_bg.png')
                bg.surface = pygame.transform.scale(bg.surface, (width, height)).convert_alpha()
                bg.mg_surface = pygame.image.load('images/boxes_bg.png')
                bg.mg_surface = pygame.transform.scale(bg.mg_surface, (width, height / 2)).convert_alpha()
            elif which_boss == 3:
                bg.surface = pygame.image.load('images/background.png')
                bg.surface = pygame.transform.scale(bg.surface, (width, height)).convert_alpha()
                bg.mg_surface = pygame.image.load('images/midground.png')
                bg.mg_surface = pygame.transform.scale(bg.mg_surface, (width, height / 2)).convert_alpha()
            start_time = pygame.time.get_ticks()
            player = Player(width / 5, height / 3)
            # if which_boss == 1:
            #     boss = Boss1(width - 90, height / 1.5)
            # elif which_boss == 2:
            #     boss = Boss2(width - 90, height / 1.5, player)
            # elif which_boss == 3:
            #     boss = Boss3(width - 90, height / 1.5, player)

            pausing = False

            while boss.rect.top < height + 100 and player.health_remaining > 0:
            # while boss.rect.top < height + 100:

                if state[0] == "selection":
                    break

                key = pygame.key.get_pressed()

                if not player.pausing:

                    clock.tick(fps)

                    bg.draw()
                    boss.boss_name()

                    player.basic_keys(bg, play, False, state)

                    player.bullet_group.draw(screen)

                    boss.health_and_attacks()

                    boss.sounds()

                    player.move_and_draw()
                    player.display_health()

                    player.get_attacked(boss)

                    if boss.health_remaining <= 0:
                        boss.death()

                    pygame.display.update()
                else:
                    player.basic_keys(bg, play, False, state)
                    clock.tick(fps)

                    pause_bg = pygame.image.load('./images/paused.png')
                    pause_bg = pygame.transform.scale(pause_bg, (width, height)).convert_alpha()
                    screen.blit(pause_bg, (0, 0))

                    pygame.display.update()
                await asyncio.sleep(0)

            if state[0] == "boss1":
                if boss.health_remaining <= 0:
                    soundObj = pygame.mixer.Sound('sounds/thank_you.mp3')
                    soundObj.play()
                    state[0] = "win1"
                elif player.health_remaining <= 0:
                    soundObj = pygame.mixer.Sound('sounds/sad_trombone.mp3')
                    soundObj.play()
                    state[0] = "death1"
            else:
                if boss.health_remaining <= 0:
                    soundObj = pygame.mixer.Sound('sounds/thank_you.mp3')
                    soundObj.play()
                    state[0] = "win2"
                elif player.health_remaining <= 0:
                    soundObj = pygame.mixer.Sound('sounds/sad_trombone.mp3')
                    soundObj.play()
                    state[0] = "death2"

            if which_boss == 1:
                bg2.again1 = True
            if which_boss == 2:
                bg2.again2 = True
            if which_boss == 3:
                bg2.again3 = True

            pygame.display.update()
            await asyncio.sleep(0)
        await asyncio.sleep(0)


bg.starting_bg()
player = Player(width / 5, height / 3)

asyncio.run(play(1, bg))
