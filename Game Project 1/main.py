#Rose Fall! (Rosemi-sama)
#game inspiration from https://www.youtube.com/watch?v=VhX1hicQo00&t=2349s
#game description: Game where player main task is to fall while dodging enemies and moving from platform to another
import pygame
import random

#all this for storing variables
pygame.init() #<--random genator 
pygame.mixer.init() #<--bgm
WIDTH = 500 #<--screen width size
HEIGHT = 800 #<--screen height size
fps = 60 #<--fps
timer = pygame.time.Clock() #<--timer tell how many times it tick
huge_font = pygame.font.Font('assets/font.ttf', 42)#<--Main title
font = pygame.font.Font('assets/font.ttf', 24) #<--font
pygame.display.set_caption('Rose Fall!')#<--caption title
screen = pygame.display.set_mode([WIDTH, HEIGHT]) #<--screen display
bg = (255, 174, 185) #<--color background
game_over = False #<--game over scenario 
clouds = [[200, 100, 1], [50, 330, 2], [350, 330, 3], [200, 670, 1]] #<--clouds x,y coordinates
cloud_images = [] #<--cloud images
for i in range(1, 4): #<--command to create cloud images
    img = pygame.image.load(f'assets/clouds/cloud{i}.png')
    cloud_images.append(img)

#player variables
player_x = 240
player_y = 40
rosemi = pygame.transform.scale(pygame.image.load('assets/rosemilovelock.png'), (50, 50))
direction = -1
y_speed = 0
gravity = 0.3
x_speed = 3
x_direction = 0
#score variables
score = 0
total_distance = 0
file = open('high_scores.txt', 'r')
read = file.readlines()
first_high = int(read[0])
high_score = first_high
#enemies variables
plane = pygame.transform.scale(pygame.image.load('assets/plane.png'), (300, 200))
enemies = [[-234, random.randint(400, HEIGHT - 100), 1]] #<--plane x y coordinates
#sounds and bgm
pygame.mixer.music.load('assets/theme.mp3')
bounce = pygame.mixer.Sound('assets/bounce.mp3')
end_sound = pygame.mixer.Sound('assets/game_over.mp3')
end_sound.set_volume(0.2)
dead_sound = pygame.mixer.Sound('assets/wee.mp3')
pygame.mixer.music.play()
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)

#function to create and draw clouds in display 
#VVVVVVVVV
def draw_clouds(cloud_list, images):
    platforms = [] #<--to return cloud platforms and make collusion
    for j in range(len(cloud_list)):
        image = images[cloud_list[j][2] - 1]
        platform = pygame.rect.Rect((cloud_list[j][0] + 5, cloud_list[j][1] + 70), (100, 10)) #<--cloud size
        screen.blit(image, (cloud_list[j][0], cloud_list[j][1]))
        pygame.draw.rect(screen, 'pink', [cloud_list[j][0] + 5, cloud_list[j][1] + 70, 100, 3]) #<--temp
        platforms.append(platform)
    
    return platforms

#function to create and draw player in display 
#VVVVVVV
def draw_player(x_pos, y_pos, player_img, direc): 
    if direc == -1:
        player_img = pygame.transform.flip(player_img, False, True)
    screen.blit(player_img, (x_pos, y_pos))
    player_rect = pygame.rect.Rect((x_pos + 7, y_pos + 32), (36, 10))
    #pygame.draw.rect(screen, 'green', player_rect, 3) #<--temp
    return player_rect

#function to create and draw enemy in display
#VVVVVVVV
def draw_enemies(enemy_list, plane_img):
    enemy_rects = []
    for j in range(len(enemy_list)):
        enemy_rect = pygame.rect.Rect((enemy_list[j][0] - 1, enemy_list[j][1] + 80), (300, 80))
        pygame.draw.rect(screen, 'orange', enemy_rect, 3) #<--temp
        enemy_rects.append(enemy_rect)
        if enemy_list[j][2] == 1:
            screen.blit(plane_img, (enemy_list[j][0], enemy_list[j][1]))
        elif enemy_list[j][2] == -1:
            screen.blit(pygame.transform.flip(plane_img, 1, 0), (enemy_list[j][0], enemy_list[j][1])) #<--flipping enemy viewpoint
    return enemy_rects

#function to create enemy movement
#VVVVVV
def move_enemies(enemy_list, current_score):
    enemy_speed = 2 + current_score//15
    for j in range(len(enemy_list)): #<--move from left and right
        if enemy_list[j][2] == 1:
            if enemy_list[j][0] < WIDTH: #<--from right to left
                enemy_list[j][0] += enemy_speed
            else:
                enemy_list[j][2] = -1
        elif enemy_list[j][2] == -1:
            if enemy_list[j][0] > -320: #<--from left to right
                enemy_list[j][0] -= enemy_speed
            else:
                enemy_list[j][2] = 1
        if enemy_list[j][1] < -100:
            enemy_list[j][1] = random.randint(HEIGHT, HEIGHT + 500)
    return enemy_list


#function to create infinite loop
#VVVVVV
def update_objects(cloud_list, play_y, enemy_list):
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
        if lowest_cloud < 750: #<--generating clouds
            num_clouds = random.randint(1,2)
            if num_clouds == 1:
                x_pos = random.randint(0, WIDTH - 70)
                y_pos = random.randint(HEIGHT + 100, HEIGHT + 300)
                cloud_type = random.randint (1, 3)
                cloud_list.append([x_pos, y_pos, cloud_type])
            else:
                x_pos = random.randint(0, WIDTH/2 - 70)
                y_pos = random.randint(HEIGHT + 100, HEIGHT + 300)
                cloud_type = random.randint (1, 3)
                x_pos2 = random.randint(WIDTH/2 + 70, WIDTH - 70)
                y_pos2 = random.randint(HEIGHT + 100, HEIGHT + 300)
                cloud_type2 = random.randint (1, 3)
                cloud_list.append([x_pos, y_pos, cloud_type])
                cloud_list.append([x_pos2, y_pos2, cloud_type2])
    return play_y, cloud_list, enemy_list

#main game loop
run = True #<--loop running
while run: #<--for stuff you want to happen when loop
    screen.fill(bg) 
    timer.tick(fps)
    cloud_platforms = draw_clouds(clouds, cloud_images) #<--clouds
    player = draw_player(player_x, player_y, rosemi, direction) #<--player
    enemy_boxes = draw_enemies(enemies, plane) #<--enemy
    enemies = move_enemies(enemies, score) #<--enemy movement
    player_y, clouds, enemies = update_objects(clouds, player_y, enemies)
    if game_over:
        end_text = huge_font.render('Rose Fall!', True, 'red')
        end_text2 = font.render('Game Over: Press Enter to Restart', True, 'black')
        screen.blit(end_text, (70,20))
        screen.blit(end_text2, (60,80))
        player_y = - 300
        y_speed = 0



    for i in range(len(cloud_platforms)): #<--bounce effect
        if direction == -1 and player.colliderect(cloud_platforms[i]):
            y_speed *= -1
            if y_speed > -2: 
                y_speed = -2
            bounce.play()



    for event in pygame.event.get():#<--to quit while loop
        if event.type == pygame.QUIT:
            run = False #<--to quit game
        if event.type == pygame.KEYDOWN: #<--up and down physics
            if event.key == pygame.K_LEFT:
                x_direction = -1
            elif event.key == pygame.K_RIGHT:
                x_direction = 1
            if event.key == pygame.K_RETURN and game_over: #<--to restart game if game over
                game_over = False
                player_x = 240
                player_y = 40
                direction = -1
                y_speed = 0
                x_direction = 0
                score = 0
                total_distance = 0
                enemies = [[-234, random.randint(400, HEIGHT - 100), 1]]
                clouds = [[200, 100, 1], [50, 330, 2], [350, 330, 3], [200, 670, 1]]
                end_sound.stop()
                pygame.mixer.music.play()
                pygame.mixer.music.play(-1)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                x_direction = 0
            elif event.key == pygame.K_RIGHT:
                x_direction = 0

    if y_speed < 10 and not game_over:
        y_speed += gravity #<-- moving collusion player
    player_y += y_speed
    if y_speed < 0:
        direction = 1
    else:
        direction = -1
    player_x += x_speed * x_direction

    if player_x > WIDTH: #<--phasing through screen
        player_x = -30
    elif player_x < -50:
        player_x = WIDTH - 20

    for i in range(len(enemy_boxes)): #<-- when die score gets record
        if player.colliderect(enemy_boxes[i]) and not game_over:
            end_sound.play()
            dead_sound.play()
            end_sound.play(-1)
            pygame.mixer.music.stop()
            game_over = True
            if score > first_high:
                file = open('high_scores.txt', 'w')
                write_score = str(score)
                file.write(write_score)
                file.close()
                first_high = score

    total_distance += y_speed #<--display scores
    score = round(total_distance / 100)
    score_text = font.render(f'Score: {score}', True, 'black')
    screen.blit(score_text, (10, HEIGHT - 70))
    if score > high_score:
        high_score = score
    score_text2 = font.render(f'High Score: {high_score}', True, 'black')
    screen.blit(score_text2, (10, HEIGHT - 40))

    pygame.display.flip() #<--to get out loop
pygame.quit() #<--quit 









