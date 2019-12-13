#!/usr/bin/python
# -*- coding: utf-8 -*-

# Andrew Gosselin
# CST-186/Fall 2018
# Chapter 12 Project
# I chose #3, I was getting random crashes for awhile but I seemed to have fixed it.
# The biggest problem I was having was python caching my files so I ended up making the
# folder structure less organized than I wanted to.
# instead of having seperate class files I just have 1 called Entities.
# Just run the "main.py" and it should start.

import pygame
from random import *
from time import *

from entities import *

# - Starting the main game class
def window():
    pygame.init()

    # - Using the cl_vars for the window
    screen = pygame.display.set_mode([MAP_SIZE[0], MAP_SIZE[1] + 70])
    # - Title
    pygame.display.set_caption(GAME_TITLE)
    # - Creating the player class
    player = Player(WALL_SIZE + 8 * PLAYER_SIZE, WALL_SIZE + 14 * PLAYER_SIZE, PLAYER_SIZE)
    entities = pygame.sprite.Group()
    entities.add(player)
    clock = pygame.time.Clock()
    score_count = Text(210, 410, 35)
    score_label = Text(70, 410, 35)
    level_map = Map()
    score_value = 0
    enemy_value = 200
    for i in range(3):
        # - Pretty much the main game loop
        # This is a lot simpler than the other game cause its pacman
        done = False
        edible = False
        count = 0
        # - Calculating FPS
        while not done:
            count += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.change_direction(-4, 0)
                    elif event.key == pygame.K_RIGHT:
                        player.change_direction(4, 0)
                    elif event.key == pygame.K_DOWN:
                        player.change_direction(0, 4)
                    elif event.key == pygame.K_UP:
                        player.change_direction(0, -4)
                    elif event.key == pygame.K_SPACE:
                        unpause = False
                        while not unpause:
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_SPACE:
                                        unpause = True
            for i in level_map.enemy_list:
                i.move(level_map)
            # - Drawing, THIS SHOULD BE MOVED TO SEPERATE FUNCTION
            player.move(level_map)
            screen.fill([0, 0, 30])
            score_label.update(screen, 'Score: ')
            score_count.update(screen, str(score_value))
            level_map.button_list.draw(screen)
            level_map.wall_list.draw(screen)
            level_map.food_list.draw(screen)
            level_map.enemy_list.draw(screen)
            entities.draw(screen)
            foodlist = pygame.sprite.spritecollide(player,
                    level_map.food_list, False)
            if edible:
                if count == 30 * 6:
                    enemy_value = 200
                    edible = False
                    for i in level_map.enemy_list:
                        i.change_color(i.color)
                        i.edible = False
                elif count > 30 * 3:
                    for i in level_map.enemy_list:
                        if i.edible:
                            if count % 15 == 0 or count % 15 == 1:
                                i.change_color([150, 255, 150])
                            elif count % 15 == 2:
                                i.change_color([60, 60, 225])
            for i in foodlist:
                score_value += 10
                level_map.food_list.remove(i)
            buttonlist = pygame.sprite.spritecollide(player,
                    level_map.button_list, False)
            if buttonlist:
                edible = True
                count = 0
                for i in buttonlist:
                    level_map.button_list.remove(i)
                for i in level_map.enemy_list:
                    i.change_color([60, 60, 255])
                    i.edible = True
            enemylist = pygame.sprite.spritecollide(player,
                    level_map.enemy_list, False)
            if enemylist:
                if enemylist[0].edible:
                    score_value += enemy_value
                    enemy_value *= 2
                    enemylist[0].waitcount = 0
                    enemylist[0].wait = True
                    enemylist[0].rect.y = WALL_SIZE + 8 * PLAYER_SIZE
                    enemylist[0].rect.x = WALL_SIZE + 8 * PLAYER_SIZE
                    enemylist[0].change_color(enemylist[0].color)
                    enemylist[0].edible = False
                else:
                    done = True
            pygame.display.flip()
            clock.tick(30)
        player.rect.x = WALL_SIZE + 8 * PLAYER_SIZE
        player.rect.y = WALL_SIZE + 14 * PLAYER_SIZE
        for i in level_map.enemy_list:
            i.change_color(i.color)
            i.rect.x = WALL_SIZE + 8 * PLAYER_SIZE
            i.rect.y = WALL_SIZE + 6 * PLAYER_SIZE
        enemy_value = 200
        clock.tick(1 / 3)
    pygame.quit()


window()
