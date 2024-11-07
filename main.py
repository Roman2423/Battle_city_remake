import pygame as pg
from classes import *
from mapmanager import load_map
from tkinter import messagebox
pg.mixer.init()
pg.init()
pg.font.init()
# Звуки #
background_music = pg.mixer.music.load("files/background_music.mp3")
pg.mixer.music.set_volume(0.5)
pg.mixer.music.play(-1)

shoot_sound = pg.mixer.Sound("files/bullet_sound.mp3")
# Экран #
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Battle City Remake")
clock = pg.time.Clock()


                            # Сам Цикл #
def game_loop():  
                                           
    walls, player, enemy = load_map("map.txt") # Загрузка карты #

    bullets = pg.sprite.Group()
    explosions = pg.sprite.Group()

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    bullet = player.shoot()
                    if bullet:
                        bullets.add(bullet)
                        shoot_sound.play()

                if event.key == pg.K_ESCAPE:
                    pause_menu(screen)
                    
        player.update(walls)
        enemy.update(player, walls)
        bullets.update()
        explosions.update()

        if enemy.alive:
            for bullet in bullets:
                if bullet.rect.colliderect(enemy.rect):
                    explosion = Explosion(enemy.rect.centerx,
                                          enemy.rect.centery)
                    explosions.add(explosion)
                    bullet.kill()
                    enemy.kill()

        screen.fill(BACKGROUND_COLOR)
        screen.blit(player.image, player.rect)
        if enemy.alive:
            screen.blit(enemy.image, enemy.rect)
        walls.draw(screen)
        bullets.draw(screen)
        explosions.draw(screen)
        pg.display.flip()
        clock.tick(60)


main_menu(screen)
game_loop()
