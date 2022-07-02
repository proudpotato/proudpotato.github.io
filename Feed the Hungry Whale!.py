# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 15:35:22 2022

@author: lin
"""

import pygame
import random

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 600
displayscreen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Feed the Hungry Whale!")

# set FPS
FPS = 60
clock = pygame.time.Clock()


#set game values
PLAYER_STARTING_LIVES = 5
PLAYER_VELOCITY = 10
COIN_STARTING_VELOCITY = 5
COIN_ACCELERATION = 0.1 #加速度


score = 0
lives = PLAYER_STARTING_LIVES
coin_velocity = COIN_STARTING_VELOCITY

GREEN = (0,255,0)
DARKGREEN = (10,50,10)
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (25,130,148)
LIGHTBLUE = (154,221,233)

font = pygame.font.Font("AttackGraffiti.ttf", 32)

score_text = font.render("Score: "+str(score), True, WHITE)
score_text_rect = score_text.get_rect()
score_text_rect.topleft = (10, 10)

title_text = font.render("Feed the Hungry Whale", True, WHITE)
title_text_rect = title_text.get_rect()
title_text_rect.centerx = WINDOW_WIDTH//2
title_text_rect.y = 10

lives_text = font.render("Lives: "+str(lives), True, WHITE)
lives_text_rect = lives_text.get_rect()
lives_text_rect.topright = (WINDOW_WIDTH-10, 10)

gameover_text = font.render("GAMEOVER", True, WHITE)
gameover_text_rect = gameover_text.get_rect()
gameover_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

continue_text = font.render("Press anykey to play again", True, WHITE)
continue_text_rect = continue_text.get_rect()
continue_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2+32)

coin_sound = pygame.mixer.Sound("soundwhale.wav")
miss_sound = pygame.mixer.Sound("soundman.wav")
miss_sound.set_volume(1.0)
pygame.mixer.music.load("Powerful-Trap-.mp3")

player_image = pygame.image.load("whale.png")
player_rect = player_image.get_rect()
player_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT-32)

coin_image = pygame.image.load("man.png")
coin_rect = coin_image.get_rect()
coin_rect.centerx = random.randint(32, WINDOW_WIDTH-32)
coin_rect.y = 67

pygame.mixer.music.play(-1,0.0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #Key move
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left>0:
        player_rect.x -= PLAYER_VELOCITY
        
    if keys[pygame.K_RIGHT] and player_rect.right<WINDOW_WIDTH:
        player_rect.x += PLAYER_VELOCITY
    
    #Coin move
    if coin_rect.y>WINDOW_HEIGHT:
        lives-=1
        miss_sound.play()
        coin_rect.centerx = random.randint(32, WINDOW_WIDTH-32)
        coin_rect.y = 67
        
    else:
        coin_rect.y+=coin_velocity
        
    #Check the collision
    if player_rect.colliderect(coin_rect):
        score += 1
        coin_sound.play()
        coin_velocity += COIN_ACCELERATION
        coin_rect.centerx = random.randint(32, WINDOW_WIDTH-32)
        coin_rect.y = 67
        
    #Update the text
    score_text = font.render("Score: "+str(score), True, WHITE, LIGHTBLUE)
    lives_text = font.render("Lives: "+str(lives), True, WHITE, LIGHTBLUE)
    
    #check_for_gameover
    if lives==0:
        displayscreen.blit(gameover_text, gameover_text_rect)
        displayscreen.blit(continue_text, continue_text_rect)
        pygame.display.update()
        pygame.mixer.music.stop()
        
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    is_paused = False
                    running = False
                    
                if event.type == pygame.KEYDOWN:
                    score = 0
                    lives = PLAYER_STARTING_LIVES
                    player_rect.centery = WINDOW_HEIGHT-32
                    coin_velocity = COIN_STARTING_VELOCITY
                    pygame.mixer.music.play(-1, 0.0)
                    is_paused = False
                
    
    displayscreen.fill(BLUE)
    
    
    displayscreen.blit(score_text, score_text_rect)
    displayscreen.blit(title_text, title_text_rect)
    displayscreen.blit(lives_text, lives_text_rect)
    pygame.draw.line(displayscreen, WHITE, (0,64), (WINDOW_WIDTH, 64), 3)
    
    displayscreen.blit(player_image, player_rect)
    displayscreen.blit(coin_image, coin_rect)

    pygame.display.update()
    clock.tick(FPS)
    
pygame.quit()