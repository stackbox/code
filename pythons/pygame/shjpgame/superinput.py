import pygame
from pygame.locals import *
keystates = [0, 0, 0, 0, 0]
def Input():
    global keystates
    inputmsg = "no"
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_q:
            inputmsg = "q"
        if event.type == KEYDOWN and event.key == K_w:
            inputmsg = "w"
        if event.type == KEYDOWN and event.key == K_e:
            inputmsg = "e"
        if event.type == KEYDOWN and event.key == K_r:
            inputmsg = "r"
        if event.type == KEYDOWN and event.key == K_t:
            inputmsg = "t"
        if event.type == KEYDOWN and event.key == K_z:
            inputmsg = "z"
        if event.type == KEYDOWN and event.key == K_u:
            inputmsg = "u"
        if event.type == KEYDOWN and event.key == K_i:
            inputmsg = "i"
        if event.type == KEYDOWN and event.key == K_o:
            inputmsg = "o"
        if event.type == KEYDOWN and event.key == K_p:
            inputmsg = "p"
        if event.type == KEYDOWN and event.key == K_a:
            inputmsg = "a"
        if event.type == KEYDOWN and event.key == K_s:
            inputmsg = "s"
        if event.type == KEYDOWN and event.key == K_d:
            inputmsg = "d"
        if event.type == KEYDOWN and event.key == K_f:
            inputmsg = "f"
        if event.type == KEYDOWN and event.key == K_g:
            inputmsg = "g"
        if event.type == KEYDOWN and event.key == K_h:
            inputmsg = "h"
        if event.type == KEYDOWN and event.key == K_j:
            inputmsg = "j"
        if event.type == KEYDOWN and event.key == K_k:
            inputmsg = "k"
        if event.type == KEYDOWN and event.key == K_l:
            inputmsg = "l"
        if event.type == KEYDOWN and event.key == K_y:
            inputmsg = "y"
        if event.type == KEYDOWN and event.key == K_x:
            inputmsg = "x"
        if event.type == KEYDOWN and event.key == K_c:
            inputmsg = "c"
        if event.type == KEYDOWN and event.key == K_v:
            inputmsg = "v"
        if event.type == KEYDOWN and event.key == K_b:
            inputmsg = "b"
        if event.type == KEYDOWN and event.key == K_n:
            inputmsg = "n"
        if event.type == KEYDOWN and event.key == K_m:
            inputmsg = "m"
        if event.type == KEYDOWN and event.key == K_1:
            inputmsg = "1"
        if event.type == KEYDOWN and event.key == K_2:
            inputmsg = "2"
        if event.type == KEYDOWN and event.key == K_3:
            inputmsg = "3"
        if event.type == KEYDOWN and event.key == K_4:
            inputmsg = "4"
        if event.type == KEYDOWN and event.key == K_5:
            inputmsg = "5"
        if event.type == KEYDOWN and event.key == K_6:
            inputmsg = "6"
        if event.type == KEYDOWN and event.key == K_7:
            inputmsg = "7"
        if event.type == KEYDOWN and event.key == K_8:
            inputmsg = "8"
        if event.type == KEYDOWN and event.key == K_9:
            inputmsg = "9"
        if event.type == KEYDOWN and event.key == K_0:
            inputmsg = "0"
        if event.type == KEYDOWN and event.key == K_COMMA:
            inputmsg = ","
        if event.type == KEYDOWN and event.key == K_MINUS:
            inputmsg = "-"
        if event.type == KEYDOWN and event.key == K_QUESTION:
            inputmsg = "?"
        if event.type == KEYDOWN and event.key == K_EXCLAIM:
            inputmsg = "!"
        if event.type == KEYDOWN and event.key == K_SPACE:
            inputmsg = "space"
        if event.type == KEYDOWN and event.key == K_BACKSPACE:
            inputmsg = "bkspc"
        if event.type == KEYDOWN and event.key == K_RETURN:
            inputmsg = "return"
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            inputmsg = "esc"
        if event.type == KEYDOWN and event.key == K_UP:
            inputmsg = "up"
        if event.type == KEYDOWN and event.key == K_DOWN:
            inputmsg = "down"
        if event.type == KEYDOWN and event.key == K_RIGHT:
            inputmsg = "right"
        if event.type == KEYDOWN and event.key == K_LEFT:
            inputmsg = "left"

        if event.type == KEYUP and event.key == K_UP:
            inputmsg = "upup"
        if event.type == KEYUP and event.key == K_DOWN:
            inputmsg = "downup"
        if event.type == KEYUP and event.key == K_RIGHT:
            inputmsg = "rightup"
        if event.type == KEYUP and event.key == K_LEFT:
            inputmsg = "leftup"
        if event.type == KEYUP and event.key == K_SPACE:
            inputmsg = "spaceup"
        if event.type == KEYUP and event.key == K_a:
            inputmsg = "aup"
            keystates[1] = "no"
        if event.type == KEYUP and event.key == K_s:
            inputmsg = "sup"
            keystates[2] = "no"
        if event.type == KEYUP and event.key == K_d:
            inputmsg = "dup"
            keystates[3] = "no"
        if event.type == KEYUP and event.key == K_w:
            inputmsg = "wup"
            keystates[0] = "no"

        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            inputmsg = "m1"
            keystates[4] = "do"
        if event.type == MOUSEBUTTONUP and event.button == 1:
            inputmsg = "m1off"
            keystates[4] = "no"
        if event.type == MOUSEBUTTONDOWN and event.button == 3:
            inputmsg = "m2"
        if event.type == MOUSEBUTTONUP and event.button == 3:
            inputmsg = "m2off"
        if event.type == MOUSEBUTTONDOWN and event.button == 5:
            inputmsg = "m5"
        if event.type == MOUSEBUTTONDOWN and event.button == 4:
            inputmsg = "m4"

    keys=pygame.key.get_pressed()  #checking pressed keys
    if keys[119] == 1:
        keystates[0] = "do"
    if keys[119] == 0:
        keystates[0] = "no"
    if keys[97] == 1:
        keystates[1] = "do"
    if keys[97] == 0:
        keystates[1] = "no"
    if keys[115] == 1:
        keystates[2] = "do"
    if keys[115] == 0:
        keystates[2] = "no"
    if keys[100] == 1:
        keystates[3] = "do"
    if keys[100] == 0:
        keystates[3] = "no"

    return inputmsg
