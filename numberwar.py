import pygame
from random import randint, choice
from time import sleep
from math import sqrt, log

pygame.init()

# user information
people_num = 10
bonus = ['+0','+0']
malus = ['-0','-0']
start_motion_speed = 10
main_color = (255, 228, 181)

# technic information
clock = pygame.time.Clock()
fps = 100 # 50 or 100 works good 25 was more tiring
motion_speed = start_motion_speed
motion = int(motion_speed * 25/fps) # it's adapt the speed to the fps
ennemy_size = lambda prop, start_num: int(-log(prop)/log(0.5) if prop > 0 else 0) + 20

lost = False
other_pos = 0
people_pos = 400
now_option = 0
option_pos = 0
go_to = 0
options_list = []
possible_num = people_num

generalfont = pygame.font.SysFont('Verdana',15, True)

# loops

def find_the_common_divisor(number):# for exemple: when put 12, it shows `[2,3,4,6]`
    common_divisors = []
    for num in range(1,number):
        if number % num == 0:
            common_divisors.append(num)
    return common_divisors

def biggest_possibilities(number,options):# for exemple with 60 and ['+10', '*2'], it is 120 because 120 > 70
    possibility1 = eval(str(number) + options[0])
    possibility2 = eval(str(number) + options[1])
    if possibility1 > possibility2:
        return possibility1
    else:
        return possibility2

def create_the_options_list(max_positive_between_negative_options,max_options_num):
    global options_list
    global possible_num
    
    option_num = 0
    possible_num = people_num

    while option_num <= max_options_num:
        
        # a few positive options
        for i in range(0,max_positive_between_negative_options+1):
            
            options_list.append([])
            # add two positive options to `options_list [-1]`
            for op in range(0,2):
                option_label = ''
                option_label += choice(['*','+'])
                option_label += str(randint(0,11)) if option_label == '+' else str(randint(0,4))

                options_list[-1].append(option_label)

                # count the number of options
                option_num += 1
            
            # set `possible_num` to the biggest possible number
            possible_num = int(biggest_possibilities(possible_num, options_list[-1]))
        
        # negative option :
        options_list.append([])
        # add two negative options
        for op in range(0,2):
            common_divisors = find_the_common_divisor(possible_num)
            option_label = ''
            if len(common_divisors):# the option will be '/' or '-'
                option_label += choice(['//','-'])
                option_label += str(choice(common_divisors))
            else:# option will be '-'
                option_label += '-'
                randint(0,16)

            options_list [-1].append(option_label)

        # set `possible_num` to the biggest possible number
        possible_num = biggest_possibilities(possible_num, options_list[-1])
        
        # count the number of options
        option_num += 1

def next_option(people_position):
    global now_option
    global people_num
    global option_pos
    global motion_speed
    global motion
    global lost

    # accelerate a litle bit
    # motion_speed += 0.5 # need to be inplemented
    # motion = motion_speed * 25/fps//1

    if people_position <= 400:# receive the first option
        people_num = eval(str(people_num) + options_list[now_option][0])
    else:# receive the second option
        people_num = int(eval(str(people_num) + options_list[now_option][1]))
        
    if people_num < 0:
        people_num = 0

    if people_num == 0:# you lost
        lost = True

    if now_option < len(options_list)-1:# pass to a new option
        # pass to the next option
        now_option += 1
        option_pos = -10
    else:
        endchalenge()

def endchalenge():
    global people_num

    ennemy_num = randint(possible_num-150, possible_num)
    if ennemy_num < 0:# if the number is to small, we do it bigger
        ennemy_num = randint(1,possible_num)
    ennemy_pos = -10

    # # variable for the battle
    # if people_num < 3000:
    #     battle_fps = 25
    #     removal = 2
    # elif people_num < 20000:
    #     battle_fps = 40
    #     removal = 7
    # else:
    #     battle_fps = 55 * people_num//20000
    #     removal = 13 * people_num//20000
    # change the numbers so that it's and with 0 and not a negative num
    # ennemy_num = (ennemy_num//removal)*removal
    # new_people_num = (people_num//removal)*removal

    running = True
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:# quit the game
                running = False
        
        # seize 
        # create the ennemy
        ennemy_size_coef = ennemy_size(ennemy_num, 1.1)
        show_one_people_or_option(400,ennemy_pos,140+ennemy_size_coef//2,ennemy_size_coef,(255,0,0), str(ennemy_num))
        # create the people
        people_size_coef = ennemy_size(people_num, 1.1)
        show_one_people_or_option(400,550,140 + people_size_coef//2 ,people_size_coef,(0,0,255),str(people_num))

        # who won?
        if people_num == ennemy_num and people_num <= 0:# draw
            pass
        elif people_num <= 0:# the people lost
            game_over(False)
        elif ennemy_num <= 0:# the ennemy lost
            game_over(True)
        # ennemy is attacking
        if ennemy_pos < 550 - ennemy_size(ennemy_num, 1.1):# ennemy is coming dangerously down
            ennemy_pos += start_motion_speed * 25/fps//1

            
            clock.tick(fps)

        else:# the battle is going
            removal = sqrt(ennemy_num if ennemy_num<people_num else people_num)
            removal = int(removal)
            ennemy_num -= removal
            people_num -= removal

            ennemy_pos = 550 - ennemy_size(ennemy_num, 1.1)

            clock.tick(fps)



        pygame.display.update()

        # clear all
        window.fill((255, 228, 181))
    
    pygame.quit()

def game_over(iswin):
    bigfont = pygame.font.SysFont('Times New Roman',50)
    if iswin:
        win_surface = bigfont.render('You won !!!',True,(0, 210, 0))
        win_rect = win_surface.get_rect()
        win_rect.midtop = (400,300)

        window.blit(win_surface,win_rect)

        pygame.display.update()
        sleep(3)
        pygame.quit()
        exit(0)
    else:
        lose_surface = bigfont.render('You\'re a loser !!',True,(255,0,0))
        lose_rect = lose_surface.get_rect()
        lose_rect.midtop = 400,250

        window.blit(lose_surface,lose_rect)

        no_people_surface = bigfont.render('0 people in your army',True,(255,0,0))
        no_people_rect = no_people_surface.get_rect()
        no_people_rect.midtop = 400,350

        window.blit(no_people_surface,no_people_rect)

        pygame.display.update()
        sleep(3)
        pygame.quit()
        exit(0)

def show_one_people_or_option(position_x,position_y,width,height,color,text):

    # the colored rectangle
    pygame.draw.rect(window,color,pygame.Rect(position_x - (width//2),position_y,width,height), border_radius = 4)
    # the text of the entity
    new_text = text.replace("*", "x").replace("//","/")
    entity_text_label = generalfont.render(new_text,True,main_color)
    entity_text_label_rect = entity_text_label.get_rect()
    entity_text_label_rect.midtop = (position_x ,position_y)

    window.blit(entity_text_label,entity_text_label_rect)


# main loop
create_the_options_list(3,20)

window = pygame.display.set_mode((800,600))

running = True
while running:
    # handle events
    for ev in pygame.event.get():
        event = ev.type
        if event == pygame.QUIT:
            running = False
        if event == pygame.KEYDOWN:# a key is pressed
            if ev.key == pygame.K_LEFT:# people must go left
                if go_to != "LEFT":
                    go_to = "LEFT"
            if ev.key == pygame.K_RIGHT:# people must go right
                if go_to != "RIGHT":
                    go_to = "RIGHT"
            if ev.key == pygame.K_UP or ev.key == pygame.K_DOWN or ev.key == pygame.K_SPACE:# people stops moving
                people_direction = 'NOTHING'
    
    if go_to == "LEFT" and people_pos > 200:# people goes left
        people_pos -= motion
    if go_to == "RIGHT" and people_pos < 600:# people goes right
        people_pos += motion

    # create the people
    people_size_coef = ennemy_size(people_num, 1.1)
    show_one_people_or_option(people_pos,550,140 + people_size_coef//2,people_size_coef,(0,0,255),str(people_num))

    # lose
    if lost:
        game_over(False)

    # verify where the option is
    if option_pos >= 550:# an option touched the people
        next_option(people_pos)

    # create the options
    show_one_people_or_option(200,option_pos,60,20,
        ((255,0,0)if '-'in options_list[now_option][0] or '/'in options_list[now_option][0] else (0,0,255)), options_list[now_option][0]) # option 1
    show_one_people_or_option(600,option_pos,60,20,
        ((255,0,0)if '-'in options_list[now_option][1] or '/'in options_list[now_option][1] else (0,0,255)) ,options_list[now_option][1]) # option 2
    
    # options go down from 10
    option_pos += motion

    pygame.display.update()
    clock.tick(fps)
    window.fill(main_color)# clear all


pygame.quit()
