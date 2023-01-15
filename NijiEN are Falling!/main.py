#Rose Fall! (Rosemi-sama)
#game inspiration from https://www.youtube.com/watch?v=VhX1hicQo00&t=2349s

import pygame
import random

pygame.init()
pygame.mixer.init()
WIDTH = 500
HEIGHT = 800
fps = 60
timer = pygame.time.Clock()
huge_font = pygame.font.Font('assets/font.ttf', 42)
font = pygame.font.Font('assets/font.ttf', 24)
pygame.display.set_caption('Rosemi is Falling!')
screen = pygame.display.set_mode([WIDTH, HEIGHT])
bg = (135, 206, 235)
game_over = False
clouds = [[200, 100, 1], [50, 330, 2], [350, 330, 3], [200, 670, 1]]
clouds_images = []
for i in range(1, 4):
    img = pygame.image.load(f'assets/clouds/cloud{i}.png')
    clouds_images.append(img)
# player variables
Player_X = 240
Player_Y = 40
rosemi = pygame.transform.scale(pygame.image.load('assets/rosemilovelock.png'), (50, 50))
direction = -1
Y_Speed = 0
Gravity = 0.2
X_Speed = 3
X_direction = 0
# score variables
Score = 0
Total_Distance = 0
file = open('High_Scores.txt', 'r')
read = file.readlines()
First_High = int(read[0])
High_Score = First_High
# enemies
plane = pygame.transform.scale(pygame.image.load('assets/plane.png'), (300, 200))
enemies = [[-234, random.randint(400, HEIGHT - 100), 1]]
# sounds and music
pygame.mixer.music.load('assets/theme.mp3')
bounce = pygame.mixer.Sound('assets/bounce.mp3')
end_sound = pygame.mixer.Sound('assets/game_over.mp3')
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.2)

#making the clouds visual
def draw_clouds(cloud_list, images):
    platforms = []
    for j in range(len(cloud_list)):
        image = images[cloud_list[j][2] - 1]
        platform = pygame.rect.Rect((cloud_list[j][0] + 5, cloud_list[j][1] + 40), (120, 10))
        screen.blit(image, (cloud_list[j][0], cloud_list[j][1]))
        #pygame.draw.rect(screen, 'gray', [cloud_list[j][0] + 5, cloud_list[j][1] + 40, 120, 3])
        platforms.append(platform)
    return platforms

#making the player visual
def draw_player(x_pos, y_pos, player_img, direc):
    if direc == -1:
        player_img = pygame.transform.flip(player_img, False, True)
    screen.blit(player_img, (x_pos, y_pos))
    player_rect = pygame.rect.Rect((x_pos + 7, y_pos + 40), (36, 10))
    # pygame.draw.rect(screen, 'green', player_rect, 3)
    return player_rect

#making the enemies visual
def draw_enemies(enemy_list, plane_img):
    enemy_rects = []
    for j in range(len(enemy_list)):
        enemy_rect = pygame.rect.Rect((enemy_list[j][0] + 40, enemy_list[j][1] + 50), (215, 70))
        # pygame.draw.rect(screen, 'orange', enemy_rect, 3)
        enemy_rects.append(enemy_rect)
        if enemy_list[j][2] == 1:
            screen.blit(plane_img, (enemy_list[j][0], enemy_list[j][1]))
        elif enemy_list[j][2] == -1:
            screen.blit(pygame.transform.flip(plane_img, 1, 0), (enemy_list[j][0], enemy_list[j][1]))
    return enemy_rects

#movement for enemies
def move_enemies(enemy_list, current_Score):
    enemY_Speed = 2 + current_Score//15
    for j in range(len(enemy_list)):
        if enemy_list[j][2] == 1:
            if enemy_list[j][0] < WIDTH:
                enemy_list[j][0] += enemY_Speed
            else:
                enemy_list[j][2] = -1
        elif enemy_list[j][2] == -1:
            if enemy_list[j][0] > -235:
                enemy_list[j][0] -= enemY_Speed
            else:
                enemy_list[j][2] = 1
        if enemy_list[j][1] < -100:
            enemy_list[j][1] = random.randint(HEIGHT, HEIGHT + 500)
    return enemy_list

#for generating infinite object platform for gameplay
def update_objects(cloud_list, play_y, enemy_list): #<-- clouds position
    lowest_cloud = 0
    update_speed = 10
    if play_y > 200:
        play_y -= update_speed
        for q in range(len(enemy_list)):
            enemy_list[q][1] -= update_speed
        for j in range(len(cloud_list)):
            cloud_list[j][1] -= update_speed
            if cloud_list[j][1] > lowest_cloud:
                lowest_cloud = cloud_list[j][1]
        if lowest_cloud < 750: #<-- for clouds randomizer
            num_clouds = random.randint(1, 2)
            if num_clouds == 1:
                x_pos = random.randint(0, WIDTH - 70)
                y_pos = random.randint(HEIGHT + 100, HEIGHT + 300)
                cloud_type = random.randint(1, 3)
                cloud_list.append([x_pos, y_pos, cloud_type])
            else:
                x_pos = random.randint(0, WIDTH / 2 - 70)
                y_pos = random.randint(HEIGHT + 100, HEIGHT + 300)
                cloud_type = random.randint(1, 3)
                x_pos2 = random.randint(WIDTH / 2 + 70, WIDTH - 70)
                y_pos2 = random.randint(HEIGHT + 100, HEIGHT + 300)
                cloud_type2 = random.randint(1, 3)
                cloud_list.append([x_pos, y_pos, cloud_type])
                cloud_list.append([x_pos2, y_pos2, cloud_type2])
    return play_y, cloud_list, enemy_list


run = True
while run:
    screen.fill(bg)
    timer.tick(fps)
    cloud_platforms = draw_clouds(clouds, clouds_images)
    player = draw_player(Player_X, Player_Y, rosemi, direction)
    enemy_boxes = draw_enemies(enemies, plane)
    enemies = move_enemies(enemies, Score)
    Player_Y, clouds, enemies = update_objects(clouds, Player_Y, enemies) #<-- generate continously platform for the game
    if game_over:
        end_text = huge_font.render('Rosemi is Falling!', True, 'black')
        end_text2 = font.render('Game Over: Press Enter to Restart', True, 'black')
        screen.blit(end_text, (70, 20))
        screen.blit(end_text2, (60, 80))
        Player_Y = - 300
        Y_Speed = 0

    #Bouncing Mechanics on cloud platform
    for i in range(len(cloud_platforms)):
        if direction == -1 and player.colliderect(cloud_platforms[i]):
            Y_Speed *= -1
            if Y_Speed > -2:
                Y_Speed = -2
            bounce.play()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        #Player Movement Event Down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                X_direction = -1
            elif event.key == pygame.K_RIGHT:
                X_direction = 1
            if event.key == pygame.K_RETURN and game_over:
                game_over = False
                Player_X = 240
                Player_Y = 40
                direction = -1
                Y_Speed = 0
                X_direction = 0
                Score = 0
                Total_Distance = 0
                enemies = [[-234, random.randint(400, HEIGHT - 100), 1]]
                clouds = [[200, 100, 1], [50, 330, 2], [350, 330, 3], [200, 670, 1]]
                pygame.mixer.music.play()

        #Player Movement Event Up
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                X_direction = 0
            elif event.key == pygame.K_RIGHT:
                X_direction = 0

    #Player Movement Physics
    if Y_Speed < 10 and not game_over:
        Y_Speed += Gravity
    Player_Y += Y_Speed
    if Y_Speed < 0:
        direction = 1
    else:
        direction = -1
    Player_X += X_Speed * X_direction
    #Player Transicion
    if Player_X > WIDTH:
        Player_X = -30
    elif Player_X < -50:
        Player_X = WIDTH - 20

    for i in range(len(enemy_boxes)):
        if player.colliderect(enemy_boxes[i]) and not game_over:
            end_sound.play()
            game_over = True
            if Score > First_High:
                file = open('High_Scores.txt', 'w')
                write_Score = str(Score)
                file.write(write_Score)
                file.close()
                First_High = Score

    Total_Distance += Y_Speed
    Score = round(Total_Distance / 100)
    Score_text = font.render(f'Score: {Score}', True, 'black')
    screen.blit(Score_text, (10, HEIGHT - 70))
    if Score > High_Score:
        High_Score = Score
    Score_text2 = font.render(f'High Score: {High_Score}', True, 'black')
    screen.blit(Score_text2, (10, HEIGHT - 40))

    pygame.display.flip()
pygame.quit()
