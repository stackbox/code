import socket, thread, time, pygame, superinput, modulesclient, superlib, random, math, wallobjects
HostIP, Port = "localhost", 50005
connectsoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connectsoc.connect((HostIP, Port))
pygame.init()
pygame.font.init()
font1 = pygame.font.SysFont("Arial", 15, False, False)
font2 = pygame.font.SysFont("Arial", 20, False, False)
font3 = pygame.font.SysFont("Arial", 12, False, False)
playershipoid = pygame.image.load("pics\spaceshipred.bmp")
playershipoid.set_colorkey((0,0,0))
playershipoid2 = pygame.image.load("pics\spaceshipblue.bmp")
playershipoid2.set_colorkey((0,0,0))
teambase = pygame.image.load("pics/ateambase.bmp")
teambase.set_colorkey((0,0,0))
playerbomboroid = pygame.image.load("pics\spacebomberred.bmp")
playerbomboroid.set_colorkey((0,0,0))
settingspic = pygame.image.load("pics\settings.bmp")
star1 = pygame.image.load("pics\star1.bmp")
star1.set_colorkey((0,0,0))
planet1 = pygame.image.load("pics\planet1.bmp")
planet1.set_colorkey((0,0,0))
checkbox = pygame.image.load("pics\checkbox.bmp")
checkbox.set_colorkey((0,0,0))
currentship = ["c000", "c000", "c000", "c000", "c000", "c000", "c000", "c000", "c000"]
clock, clock2 = pygame.time.Clock(), pygame.time.Clock()
maintube, lobbychatlist, onlineplayers = [], [], {}
keyinput, myname = "no", "noname"
authorized = 0
rotation = 0
scale = 1.0
playergold = 0
camera = [0, 0]
damagefonts = []
weaponeffects = {}
playersmooth = {}
sendlist = []
currentweapons = []
winvar = [playershipoid, "no"]
resolution = [800, 600]
weaponstates = ["yes", "yes", "yes", "yes", "yes", "yes", "yes", "yes", "yes"]
allowedpvp = 600

def takeinput():
    global keyinput
    keyinput = superinput.Input()

def receiver(Port):
    global authorized
    while 1:
        data = connectsoc.recv(1024)
        datatype = data[:3]
        data = data[3:]
        truther = data.find("#")
        data = data[:truther]
        maintube.append([datatype, data])

def sender(Port):
    while 1:
        if len(sendlist) == 0:
            time.sleep(0.03)
        try:
            if len(sendlist) > 0:
                supersendstring = "%s" %sendlist[0]
                while len(supersendstring) < 1024:
                    supersendstring += "#"
                connectsoc.send(supersendstring)
                sendlist.pop(0)
        except:
            print "uh oh..!"
            break

def authorize():
    global authorized
    screen=pygame.display.set_mode([300,300])
    loginpic = pygame.image.load("pics\login.bmp")
    usernamelist = []
    passwordlist = []
    switchnamepw = 0
    while authorized != 1:
        takeinput()
        if keyinput not in ("m4", "m5", "no", "return", "space", "spaceup", "wup", "dup", "aup", "sup", "bkspc", "esc", "up", "down", "left", "right", "upup", "downup", "leftup", "rightup", "m1", "m2", "m1off", "m2off"):
            if switchnamepw == 0:
                usernamelist.append(keyinput)
            if switchnamepw == 1:
                passwordlist.append(keyinput)
        if keyinput == "bkspc":
            if switchnamepw == 0 and len(usernamelist) > 0:
                usernamelist.pop(-1)
            if switchnamepw == 1 and len(passwordlist) > 0:
                passwordlist.pop(-1)            
        if keyinput == "space":
            if switchnamepw == 0:
                switchnamepw = 1
            else: switchnamepw = 0
        usernamestring = "-"
        passwordstring = "-"
        if len(usernamelist) > 0:
            for entry in usernamelist:
                usernamestring = usernamestring + "%s" %entry
        if len(passwordlist) > 0:
            for entry in passwordlist:
                passwordstring = passwordstring + "%s" %entry
        if keyinput == "return" and len(passwordstring) > 4 and len(usernamestring) > 4:
            usernamestring = usernamestring[1:]
            usernamestring = usernamestring.capitalize()
            usernamestring = "-%s"%usernamestring
            sendlist.append("001 %s %s" %(usernamestring, passwordstring))
            time.sleep(2)
            if authorized == 2:
                print "wrong password!"
                usernamelist = []
                passwordlist = []
                switchnamepw = 0
                authorized = 0
            if authorized == 3:
                print "already logged in!"
        if keyinput == "return" and len(passwordstring) < 5 or keyinput == "return" and len(usernamestring) < 5:
            print "name or password too short (< 5)"
        screen.blit(loginpic, [0,0])
        usernamepic = font1.render(usernamestring, True, (250, 150, 150), (0, 0, 0))
        screen.blit(usernamepic, [100, 100])
        passwordpic = font1.render(passwordstring, True, (250, 150, 150), (0, 0, 0))
        screen.blit(passwordpic, [100, 200])
        pygame.display.flip()



def dopvp():
    global rotation, scale, myname, currentweapons, allowedpvp
    screen=pygame.display.set_mode([resolution[0],resolution[1]])
    currentweapons = []
    for core in currentship:
        if modulesclient.cores[core][2] == "Weapon":
            currentweapons.append([core, 9, modulesclient.cores[core][3]])
    lockedkey = "no"
    localcounter = 0
    Stars = []
    Stars2 = []
    for i in range(1, 40):
        Stars.append([random.randint(-200, 1000), random.randint(-200, 800), random.randint(20, 215), random.randint(5, 18)])
    for i in range(1, 10):
        Stars2.append([random.randint(-200, 1000), random.randint(-200, 800), random.randint(20, 215), random.randint(3, 12)])
    planetcoords = [random.randint(-200, 1000), random.randint(-200, 800), random.randint(2, 4)]

    while 1:
        if onlineplayers[myname][1] < -900:
            allowedpvp = 600
            lobbychatlist.append(["-You have died! You may reenter PVP in 10 seconds."])
            break
        screen.fill((0, 0, 0))        ### background
        for star in Stars:
            pygame.draw.rect(screen, (star[2], star[2], star[2]), (star[0]-(onlineplayers[myname][1]/star[3]), star[1]-(onlineplayers[myname][2]/star[3]), 2, 2))
        for star in Stars2:
            screen.blit(star1, [star[0]-(onlineplayers[myname][1]/star[3]), star[1]-(onlineplayers[myname][2]/star[3])])
        screen.blit(planet1, [planetcoords[0]-(onlineplayers[myname][1]/planetcoords[2]), planetcoords[1]-(onlineplayers[myname][2]/planetcoords[2])])
        takeinput()
        if keyinput != "no":                #### do keyinput
            try:
                if keyinput == "1":
                    sendlist.append("003switchstate %s" %currentweapons[0][0])
                    if weaponstates[0] == "no":
                        weaponstates[0] = "yes"
                    else:
                        weaponstates[0] = "no"
                if keyinput == "2":
                    sendlist.append("003switchstate %s" %currentweapons[1][0])
                    if weaponstates[1] == "no":
                        weaponstates[1] = "yes"
                    else:
                        weaponstates[1] = "no"
                if keyinput == "3":
                    sendlist.append("003switchstate %s" %currentweapons[2][0])
                    if weaponstates[2] == "no":
                        weaponstates[2] = "yes"
                    else:
                        weaponstates[2] = "no"
                if keyinput == "4":
                    sendlist.append("003switchstate %s" %currentweapons[3][0])
                    if weaponstates[3] == "no":
                        weaponstates[3] = "yes"
                    else:
                        weaponstates[3] = "no"
                if keyinput == "5":
                    sendlist.append("003switchstate %s" %currentweapons[4][0])
                    if weaponstates[4] == "no":
                        weaponstates[4] = "yes"
                    else:
                        weaponstates[4] = "no"
                if keyinput == "6":
                    sendlist.append("003switchstate %s" %currentweapons[5][0])
                    if weaponstates[5] == "no":
                        weaponstates[5] = "yes"
                    else:
                        weaponstates[5] = "no"
                if keyinput == "7":
                    sendlist.append("003switchstate %s" %currentweapons[6][0])
                    if weaponstates[6] == "no":
                        weaponstates[6] = "yes"
                    else:
                        weaponstates[6] = "no"
                if keyinput == "8":
                    sendlist.append("003switchstate %s" %currentweapons[7][0])
                    if weaponstates[7] == "no":
                        weaponstates[7] = "yes"
                    else:
                        weaponstates[7] = "no"
                if keyinput == "9":
                    sendlist.append("003switchstate %s" %currentweapons[8][0])
                    if weaponstates[8] == "no":
                        weaponstates[8] = "yes"
                    else:
                        weaponstates[8] = "no"
            except:
                pass
            if keyinput == "esc":
                if onlineplayers[myname][6] > 90:
                    allowedpvp = 600
                    break
            if keyinput == "m5":
                scale = 0.5
                camera[0] = resolution[0]/2-onlineplayers[myname][1]*scale
                camera[1] = resolution[1]/2-onlineplayers[myname][2]*scale 
            if keyinput == "m4":
                scale = 1
                camera[0] = resolution[0]/2-onlineplayers[myname][1]*scale
                camera[1] = resolution[1]/2-onlineplayers[myname][2]*scale

        sendlist.append("999%i %s %s %s %s %s "%(rotation, superinput.keystates[0], superinput.keystates[1], superinput.keystates[2], superinput.keystates[3], superinput.keystates[4]))

        mousepos = pygame.mouse.get_pos()   ## get rotation from ship - mousepos
        rotation = superlib.Angle(int(onlineplayers[myname][1]*scale+camera[0]), int(onlineplayers[myname][2]*scale+camera[1]), mousepos[0], mousepos[1])
        try:
            rotation = -rotation
        except:
            rotation = 1
        rotation += 180
        if rotation < 0:
            rotaton = rotation + 360

        camera[0] = resolution[0]/2-onlineplayers[myname][1]*scale     ### set camera to player
        camera[1] = resolution[1]/2-onlineplayers[myname][2]*scale

        for playert in onlineplayers.keys():        ##### base circles
            if onlineplayers[playert][0] == "Generic1" or onlineplayers[playert][0] == "Generic2":
                if onlineplayers[playert][8] == "Red":
                    pygame.draw.circle(screen, (50, 0, 0), [int(onlineplayers[playert][1]*scale+camera[0]), int(onlineplayers[playert][2]*scale+camera[1])], int(350*scale), 2)
                if onlineplayers[playert][8] == "Blue":
                    pygame.draw.circle(screen, (0, 0, 50), [int(onlineplayers[playert][1]*scale+camera[0]), int(onlineplayers[playert][2]*scale+camera[1])], int(350*scale), 2)

        for effect in weaponeffects.keys():           ############## do weaaponeffects
            try:
                weaponeffects[effect][0] += 1
                if weaponeffects[effect][5] == "rocket":
                    weaponeffects[effect][0] += 4
                if weaponeffects[effect][5] == "shot":
                    for objecti in wallobjects.objectlist.keys():
                        if wallobjects.objectlist[objecti][0] < weaponeffects[effect][1] < wallobjects.objectlist[objecti][0] + wallobjects.objectlist[objecti][2] and wallobjects.objectlist[objecti][1] < weaponeffects[effect][2] < wallobjects.objectlist[objecti][1] + wallobjects.objectlist[objecti][3]:
                            weaponeffects[effect][3] = -weaponeffects[effect][3]
                            weaponeffects[effect][4] = -weaponeffects[effect][4]
                    if weaponeffects[effect][1] < 0:
                        weaponeffects[effect][3] = -weaponeffects[effect][3]
                    if weaponeffects[effect][1] > 2000:
                        weaponeffects[effect][3] = -weaponeffects[effect][3]
                    if weaponeffects[effect][2] < 0:
                        weaponeffects[effect][4] = -weaponeffects[effect][4]
                    if weaponeffects[effect][2] > 1500:
                        weaponeffects[effect][4] = -weaponeffects[effect][4]
                    weaponeffects[effect][1] += weaponeffects[effect][3]
                    weaponeffects[effect][2] += weaponeffects[effect][4]

                    blitshippiewidth = modulesclient.shots[weaponeffects[effect][7]][0].get_width()
                    blitshippieheight = modulesclient.shots[weaponeffects[effect][7]][0].get_height()
                    blitshippie = pygame.transform.scale(modulesclient.shots[weaponeffects[effect][7]][0], (int(blitshippiewidth*scale), int(blitshippieheight*scale)))
                    blitshippiewidth = blitshippie.get_width()
                    blitshippieheight = blitshippie.get_height()
                    
                    screen.blit(blitshippie, [int(weaponeffects[effect][1]*scale)-blitshippiewidth/2+camera[0], int(weaponeffects[effect][2]*scale)-blitshippieheight/2+camera[1]])


                if weaponeffects[effect][5] == "rocket":
                    for playero in onlineplayers.keys():
                        if playero == weaponeffects[effect][6]:
                            
                            xd = weaponeffects[effect][1]-onlineplayers[playero][1]
                            yd = weaponeffects[effect][2]-onlineplayers[playero][2]
                            xres =  (1000000*xd) / int(1000*math.sqrt((xd*xd + yd*yd)))
                            yres =  (1000000*yd) / int(1000*math.sqrt((xd*xd + yd*yd)))
                            weaponeffects[effect][1] -= int((weaponeffects[effect][10]*xres)/1000)   #### move rocket
                            weaponeffects[effect][2] -= int((weaponeffects[effect][10]*yres)/1000)

                    blitshippiewidth = modulesclient.shots[weaponeffects[effect][7]][0].get_width()
                    blitshippieheight = modulesclient.shots[weaponeffects[effect][7]][0].get_height()
                    blitshippie = pygame.transform.scale(modulesclient.shots[weaponeffects[effect][7]][0], (int(blitshippiewidth*scale), int(blitshippieheight*scale)))
                    blitshippiewidth = blitshippie.get_width()
                    blitshippieheight = blitshippie.get_height()
                    arotation = superlib.Angle(weaponeffects[effect][1], weaponeffects[effect][2], onlineplayers[weaponeffects[effect][6]][1], onlineplayers[weaponeffects[effect][6]][2])
                    try:
                        arotation = -arotation
                    except:
                        arotation = 1
                    arotation += 180
                    if arotation < 0:
                        arotaton = arotation + 360
                    blitshippie = pygame.transform.rotate(blitshippie, arotation)
                    screen.blit(blitshippie, [int(weaponeffects[effect][1]*scale)-blitshippiewidth/2+camera[0], int(weaponeffects[effect][2]*scale)-blitshippieheight/2+camera[1]])


                if weaponeffects[effect][5] == "laser":
                    if weaponeffects[effect][6] != "none":
                        try:
                            color = (150, 150, 150)
                            if weaponeffects[effect][7] == "100":
                                color = (0, 250, 250)
                            if weaponeffects[effect][7] == "101":
                                color = (0, 0, 250)
                            xrandy = random.randint(-5, 5)
                            yrandy = random.randint(-5, 5)
                            pygame.draw.line(screen, color, [(onlineplayers[weaponeffects[effect][6]][1]+xrandy)*scale+camera[0], (onlineplayers[weaponeffects[effect][6]][2]+yrandy)*scale+camera[1]], [onlineplayers[weaponeffects[effect][9]][1]*scale+camera[0], onlineplayers[weaponeffects[effect][9]][2]*scale+camera[1]], 5)
                        except:
                            print "laser error", effect, weaponeffects
                        
                if weaponeffects[effect][0] > weaponeffects[effect][8]:
                    del weaponeffects[effect]
                try:
                    if weaponeffects[effect][5] == "rocket":
                        for objecti in wallobjects.objectlist.keys():
                            if wallobjects.objectlist[objecti][0] < weaponeffects[effect][1] < wallobjects.objectlist[objecti][0] + wallobjects.objectlist[objecti][2] and wallobjects.objectlist[objecti][1] < weaponeffects[effect][2] < wallobjects.objectlist[objecti][1] + wallobjects.objectlist[objecti][3]:
                                del weaponeffects[effect]
                except:
                    pass  ## only no error if shottype hits object
                
            except:
                print "."
                try:
                    del weaponeffects[effect]
                except:
                    pass
            
        for player in onlineplayers.keys():           ######################### do players
            if onlineplayers[player][1] > -900 and onlineplayers[player][2] > -900:
                onlineplayers[player][1] += onlineplayers[player][3]
                onlineplayers[player][2] += onlineplayers[player][4]
                try:
                    playersmooth[player][0] += playersmooth[player][2]
                    playersmooth[player][1] += playersmooth[player][3]
                    if onlineplayers[player][1] < 0:
                        onlineplayers[player][3] = -onlineplayers[player][3]
                    if onlineplayers[player][2] < 0:
                        onlineplayers[player][4] = -onlineplayers[player][4]
                    if onlineplayers[player][1] > 2000:
                        onlineplayers[player][3] = -onlineplayers[player][3]
                    if onlineplayers[player][2] > 1500:
                        onlineplayers[player][4] = -onlineplayers[player][4]
                    if onlineplayers[player][1] < playersmooth[player][0] -5:
                        onlineplayers[player][1] += 1
                    if onlineplayers[player][1] > playersmooth[player][0] +5:
                        onlineplayers[player][1] -= 1
                    if onlineplayers[player][2] < playersmooth[player][1] -5:
                        onlineplayers[player][2] += 1
                    if onlineplayers[player][2] > playersmooth[player][1] +5:
                        onlineplayers[player][2] -= 1
                    if onlineplayers[player][1] < playersmooth[player][0] -50:
                        onlineplayers[player][1] = playersmooth[player][0]
                        onlineplayers[player][2] = playersmooth[player][1]
                    if onlineplayers[player][1] > playersmooth[player][0] +50:
                        onlineplayers[player][1] = playersmooth[player][0]
                        onlineplayers[player][2] = playersmooth[player][1]
                    if onlineplayers[player][2] < playersmooth[player][1] -50:
                        onlineplayers[player][1] = playersmooth[player][0]
                        onlineplayers[player][2] = playersmooth[player][1]
                    if onlineplayers[player][2] > playersmooth[player][1] +50:
                        onlineplayers[player][1] = playersmooth[player][0]
                        onlineplayers[player][2] = playersmooth[player][1]
                except:
                    pass
                if onlineplayers[player][0] != "Generic1" and onlineplayers[player][0] != "Generic2":
                    if onlineplayers[player][8] == "Red":
                        blitshippie = pygame.transform.rotate(playershipoid, onlineplayers[player][5])
                        if onlineplayers[player][9] > 70:
                            blitshippie = pygame.transform.rotate(playerbomboroid, onlineplayers[player][5])
                    else:
                        blitshippie = pygame.transform.rotate(playershipoid2, onlineplayers[player][5])
                        if onlineplayers[player][9] > 70:
                            blitshippie = pygame.transform.rotate(playerbomboroid, onlineplayers[player][5])
                else:
                    blitshippie = pygame.transform.rotate(teambase, onlineplayers[player][5])
                blitshippiewidth = blitshippie.get_width()
                blitshippieheight = blitshippie.get_height()
                blitshippie = pygame.transform.scale(blitshippie, (int(blitshippiewidth*scale), int(blitshippieheight*scale)))
                blitshippiewidth = blitshippie.get_width()
                blitshippieheight = blitshippie.get_height()
                if onlineplayers[player][1] != -1000 and onlineplayers[player][2] != -1000:
                    screen.blit(blitshippie, [int(onlineplayers[player][1]*scale)-blitshippiewidth/2+camera[0], int(onlineplayers[player][2]*scale)-blitshippieheight/2+camera[1]])

                pygame.draw.line(screen, (50, 230, 50), [(onlineplayers[player][1]-15)*scale+camera[0], (onlineplayers[player][2]-35)*scale+camera[1]], [(onlineplayers[player][1]+(onlineplayers[player][6]/3)-15)*scale+camera[0], (onlineplayers[player][2]-35)*scale+camera[1]], 3)
                pygame.draw.line(screen, (150, 150, 220), [(onlineplayers[player][1]-15)*scale+camera[0], (onlineplayers[player][2]-35)*scale+camera[1]+4], [(onlineplayers[player][1]+(onlineplayers[player][7]/3)-15)*scale+camera[0], (onlineplayers[player][2]-35)*scale+camera[1]+4], 3)
                if onlineplayers[player][8] == "Red":
                    pygame.draw.line(screen, (250, 50, 50), [(onlineplayers[player][1]-15)*scale+camera[0]-6, (onlineplayers[player][2]-35)*scale+camera[1]-2], [(onlineplayers[player][1]-15)*scale+camera[0]-6, (onlineplayers[player][2]-35)*scale+camera[1]+6], 5)
                if onlineplayers[player][8] == "Blue":
                    pygame.draw.line(screen, (50, 50, 250), [(onlineplayers[player][1]-15)*scale+camera[0]-6, (onlineplayers[player][2]-35)*scale+camera[1]-2], [(onlineplayers[player][1]-15)*scale+camera[0]-6, (onlineplayers[player][2]-35)*scale+camera[1]+6], 5)

            if player[0] != "G":
                playernamestring = "%s" %onlineplayers[player][0][1:]
                playernamepic = font3.render(playernamestring, True, (250, 250, 250), (0, 0, 0))
                playernamepic.set_colorkey((0, 0, 0))
                screen.blit(playernamepic, [(onlineplayers[player][1]-15)*scale+camera[0]-8, (onlineplayers[player][2]-35)*scale+camera[1]-18]) 


            if player[0] == "G":
                playernamestring = "%s Team Base" %onlineplayers[player][8]
                playernamepic = font3.render(playernamestring, True, (250, 250, 250), (0, 0, 0))
                playernamepic.set_colorkey((0, 0, 0))
                screen.blit(playernamepic, [(onlineplayers[player][1]-15)*scale+camera[0]+(15*scale)-40, (onlineplayers[player][2]-35)*scale+camera[1]-18]) 
                
                
##        try:   #### server position
##            pygame.draw.line(screen, (240, 0, 0), [playersmooth[myname][0]*scale-2+camera[0], playersmooth[myname][1]*scale+camera[1]], [playersmooth[myname][0]*scale+2+camera[0], playersmooth[myname][1]*scale+camera[1]], 5)
##        except:
##            pass

        
        pygame.draw.line(screen, (150, 150, 50), [-5*scale+camera[0], -5*scale+camera[1]], [2005*scale+camera[0], -5*scale+camera[1]], 5)  #####playfiields
        pygame.draw.line(screen, (150, 150, 50), [-5*scale+camera[0], -5*scale+camera[1]], [-5*scale+camera[0], 1505*scale+camera[1]], 5)
        pygame.draw.line(screen, (150, 150, 50), [-5*scale+camera[0], 1505*scale+camera[1]], [2005*scale+camera[0], 1505*scale+camera[1]], 5)
        pygame.draw.line(screen, (150, 150, 50), [2005*scale+camera[0], -5*scale+camera[1]], [2005*scale+camera[0], 1505*scale+camera[1]], 5)

        for objecti in wallobjects.objectlist.keys():          #### OBJECTS
##            pygame.draw.rect(screen, (150, 150, 150), ((wallobjects.objectlist[objecti][0])*scale+camera[0], (wallobjects.objectlist[objecti][1])*scale+camera[1], (wallobjects.objectlist[objecti][2])*scale, (wallobjects.objectlist[objecti][3])*scale), 4)

            blitshippiewidth = wallobjects.objectlist[objecti][4].get_width()
            blitshippieheight = wallobjects.objectlist[objecti][4].get_height()
            blitshippie = pygame.transform.scale(wallobjects.objectlist[objecti][4], (int(blitshippiewidth*scale), int(blitshippieheight*scale)))
            blitshippiewidth = blitshippie.get_width()
            blitshippieheight = blitshippie.get_height()
            
            screen.blit(blitshippie, [(wallobjects.objectlist[objecti][0])*scale+camera[0], (wallobjects.objectlist[objecti][1])*scale+camera[1]])


        o = 0
        for font in damagefonts:
            damagefonts[o][3] += 3
            if font[4] == 0: 
                fonttext = "%i" % modulesclient.shots[font[2]][1]
                damagepic = font1.render(fonttext, True, (160-font[3], 60-(font[3]/3), 60-(font[3]/3)), (0, 0, 0))
            else:
                critnumba = int(modulesclient.shots[font[2]][1] + (modulesclient.shots[font[2]][1]*font[4])/100)
                fonttext = "%i" % critnumba
                damagepic = font2.render(fonttext, True, (220-font[3], 120-(font[3]/3), 120-(font[3]/3)), (0, 0, 0))

            damagepic.set_colorkey((0,0,0))
            screen.blit(damagepic, [font[0]*scale+camera[0], font[1]*scale-font[3]+camera[1]])
            if font[3] > 150:
                damagefonts.pop(o)
                o -= 1
            o = o + 1


        if winvar[1] == "yes":
            localcounter += 1
            screen.blit(winvar[0], [300, resolution[1]-100])
            if localcounter > 150:
                winvar[1] = "no"
                localcounter = 0



################ PVP UI STARTS HERE
                
        index = 0
        for weapon in currentweapons:
            currentweapons[index][1] -= 1
            if currentweapons[index][1] < 0:
                currentweapons[index][1] = 0
            if weaponstates[index] == "no" or currentweapons[index][1] > 0 or onlineplayers[myname][7] < 3:
                pygame.draw.rect(screen, (150, 50, 50), (1+index*51, resolution[1]-52, 50, 50), 3)
            if weaponstates[index] == "yes" and currentweapons[index][1] == 0 and onlineplayers[myname][7] > 2:
                pygame.draw.rect(screen, (50, 150, 50), (1+index*51, resolution[1]-52, 50, 50), 3)
            blitshippiewidth = modulesclient.cores[weapon[0]][0].get_width()
            blitshippieheight = modulesclient.cores[weapon[0]][0].get_height()
            blitshippie = pygame.transform.scale(modulesclient.cores[weapon[0]][0], (int(blitshippiewidth/2), int(blitshippieheight/2)))
            blitshippiewidth = blitshippie.get_width()
            blitshippieheight = blitshippie.get_height()
            screen.blit(blitshippie, [index*51, resolution[1]-50])
            index += 1

        pygame.draw.line(screen, (10, 50, 10), [1, resolution[1]-65], [201, resolution[1]-65], 3)
        pygame.draw.line(screen, (10, 10, 50), [1, resolution[1]-58], [201, resolution[1]-58], 3)
        pygame.draw.line(screen, (50, 160, 50), [1, resolution[1]-65], [1+onlineplayers[myname][6]*2, resolution[1]-65], 5)
        pygame.draw.line(screen, (50, 50, 150), [1, resolution[1]-58], [1+onlineplayers[myname][7]*2, resolution[1]-58], 5)

                             
        pygame.display.flip()
        clock.tick(30)
                

def lobby():
    global allowedpvp, resolution
    sendlist.append("002steering lobby")
    screen=pygame.display.set_mode([640,480])
    loginpic = pygame.image.load("pics\lobby.bmp")
    chatoutlist = []
    chooser = 1
    Lobbystars = []
    while 1:
        allowedpvp -= 1
        takeinput()
        if keyinput == "esc":
            chooser = 10
            break
        if keyinput == "m1":
            mousepos = pygame.mouse.get_pos()
            if 20 < mousepos[0] < 125 and 20 < mousepos[1] < 60:
                if allowedpvp < 1:
                    chooser = 1
                    break
            if 256 < mousepos[0] < 362 and 20 < mousepos[1] < 60:
                chooser = 2
                break
            if 372 < mousepos[0] < 478 and 20 < mousepos[1] < 60:
                time.sleep(0.2)
                while 1:     ######################################### SETTINGS
                    allowedpvp -= 1
                    screen.fill((0,0,0))
                    takeinput()
                    mousepos = pygame.mouse.get_pos()
                    if keyinput == "m1":
                        if 480 < mousepos[0] < 600 and 392 < mousepos[1] < 438:
                            time.sleep(0.2)
                            break
                        if 155 < mousepos[0] < 175 and 65 < mousepos[1] < 85:
                            resolution = [800, 600]
                        if 155 < mousepos[0] < 175 and 85 < mousepos[1] < 105:
                            resolution = [1024, 768]
                    screen.blit(settingspic, [0, 0])
                    if resolution[0] == 800:
                        screen.blit(checkbox, [155, 65])
                    if resolution[0] == 1024:
                        screen.blit(checkbox, [155, 85])
                    pygame.display.flip()
                    clock.tick(60)
                    
        if keyinput not in ("no", "return", "spaceup", "wup", "dup", "aup", "sup", "esc", "up", "down", "left", "right", "upup", "downup", "leftup", "rightup", "m1", "m2", "m1off", "m2off", "m4", "m5"):
            chatoutlist.append(keyinput)
            i = 0
            if chatoutlist[0] == "bkspc":
                chatoutlist.pop(0)
            for entry in chatoutlist:
                if entry == "space":
                    chatoutlist[i] = " "
                if entry == "bkspc" and len(chatoutlist) > 1:
                    chatoutlist.pop(-1)
                    chatoutlist.pop(-1)
                    i -= 1
                i += 1
        if keyinput == "return" and len(chatoutlist) > 0:
            sendstring = "".join(chatoutlist)
            sendlist.append("002says: lobby %s" %sendstring)
            chatoutlist = []
        screen.blit(loginpic, [0,0])
        i = 0
        while len(lobbychatlist) > 10:
            lobbychatlist.pop(0)
        for entry in lobbychatlist:
            i = i + 1
            linesay = " ".join(entry)
            linesay = linesay[1:]
            linesaypic = font1.render(linesay, True, (250, 150, 150), (0, 0, 0))
            linesaypic.set_colorkey((0,0,0))
            screen.blit(linesaypic, [15, 95+i*20])
        i = 0
        for entry in onlineplayers.keys():
            if entry[0] == "-":
                i = i + 1
                linesaypic = font1.render(entry[1:], True, (250, 150, 150), (0, 0, 0))
                linesaypic.set_colorkey((0,0,0))
                screen.blit(linesaypic, [480, 95+i*20])
        inputstring = "".join(chatoutlist)
        linesaypic = font1.render(inputstring, True, (222, 222, 222), (0, 0, 0))
        linesaypic.set_colorkey((0,0,0))
        screen.blit(linesaypic, [15, 440])

        while len(Lobbystars) < 10:
            Lobbystars.append([random.randint(489, 625), random.randint(65, 106), random.randint(20, 180)])

        index = 0
        for star in Lobbystars:
            if star[1] < 65:
                pygame.draw.rect(screen, (star[2], star[2], star[2]), (star[0], star[1], 2, 2))
            Lobbystars[index][1] -= 1
            if Lobbystars[index][1] < 19:
                Lobbystars.pop(index)
                index -= 1
            index += 1

        if allowedpvp > 0:
            allowpvpmsg = "Locked out from PvP:  %i Seconds" %(int(allowedpvp/60)+1)
            allowpvppic = font1.render(allowpvpmsg, True, (222, 122, 52), (0, 0, 0))
            screen.blit(allowpvppic, [18, 80])
            
        pygame.display.flip()
        clock.tick(60)
    return chooser
        


def tubeoperations(Port):
    global onlineplayers, authorized, myname, playergold, currentweapons
    while 1:
        if len(maintube) > 0:
            jobtype, jobdata = maintube[0][0], maintube[0][1]
            newdata = jobdata.split()

            if jobtype == "001":                                ##### 001: AUTHENTICATION
                if newdata[0] == "auth":
                    authorized = 1
                    myname  = newdata[1]
                if newdata[0] == "new":
                    authorized = 1
                    myname  = newdata[1]
                if newdata[0] == "log":
                    authorized = 3
                if newdata[0] == "wpw":
                    authorized = 2

            if jobtype == "002":                                ###### 002: CHATTING
                if newdata[1] == "says:" and newdata[2] == "lobby":
                    newdata.pop(2)
                    lobbychatlist.append(newdata)
                if newdata[0] == "updch":
                    newdata.pop(0)
                    for entry in newdata:
                        onlineplayers[entry] = [entry, -800, -800, 0, 0, 0, 0, 0, "none", 0]

            if jobtype == "003":                                ####### 003: PVP
                if newdata[0] == "exitpvp":
                    del onlineplayers[newdata[1]]
                if newdata[0] == "posupd":
                    newdata.pop(0)
                    while len(newdata) > 3:               #################################################### ANTI SMOOTH!!!!
                        if newdata[1] == "400" and newdata[2] == "300":
                            playersmooth[newdata[0]] = [int(newdata[1]), int(newdata[2]), int(newdata[3]), int(newdata[4])]
                            onlineplayers[newdata[0]] = [newdata[0], int(newdata[1]), int(newdata[2]), int(newdata[3]), int(newdata[4]), int(newdata[5]), int(newdata[6]), int(newdata[7]), newdata[8], int(newdata[9])]
                        ##### onlineplayers       0: name 1: xpos 2: ypos 3: xvector 4: yvector 5: rotate  6: health %    7: energy %   8: team affiliation 9: weight
                        else:
                            playersmooth[newdata[0]] = [int(newdata[1]), int(newdata[2]), int(newdata[3]), int(newdata[4])]
                            try:
                                schnab = onlineplayers[newdata[0]][1]
                                schnub = onlineplayers[newdata[0]][2]
                            except:
                                schnab = 1
                                schnub = 1
                            onlineplayers[newdata[0]] = [newdata[0], schnab, schnub, int(newdata[3]), int(newdata[4]), int(newdata[5]), int(newdata[6]), int(newdata[7]), newdata[8], int(newdata[9])]
                            
                        newdata.pop(0)
                        newdata.pop(0)
                        newdata.pop(0)
                        newdata.pop(0)
                        newdata.pop(0)
                        newdata.pop(0)
                        newdata.pop(0)
                        newdata.pop(0)
                        newdata.pop(0)
                        newdata.pop(0)


            if jobtype == "004":                               ####### 004: CUSTOM
                if newdata[0] == "updship":
                    newdata.pop(0)
                    i = 0
                    playergold = int(newdata[-1])
                    newdata.pop(-1)
                    for entry in newdata:
                        currentship[i] = entry
                        i = i + 1

            if jobtype == "005":                                 ###### 005: Weapon Effects
                if newdata[0] == "wpfx":
                    newdata.pop(0)
                    if newdata[9] == myname:
                        index = 0
                        for weapon in currentweapons:
                            if weapon[0] == newdata[11]:
                                currentweapons[index][1] = currentweapons[index][2]
                            index += 1
                    weaponeffects[newdata[0]] = [0, int(newdata[1]), int(newdata[2]), int(newdata[3]), int(newdata[4]), newdata[5], newdata[6], newdata[7], int(newdata[8]), newdata[9], int(newdata[10]), newdata[11]]
                    ### 0counter, xpos, ypos, 3 vectorx, vectory, 5 type, target, shot type,  8duration 9origin 10 speed 11 core
                    if newdata[5] == "laser":
                        damagefonts.append([onlineplayers[weaponeffects[newdata[0]][6]][1], onlineplayers[weaponeffects[newdata[0]][6]][2], weaponeffects[newdata[0]][7], 0, 0])
                if newdata[0] == "shotcol":
                    try:
                        if weaponeffects[newdata[1]][5] == "shot" or weaponeffects[newdata[1]][5] == "rocket":

                            damagefonts.append([weaponeffects[newdata[1]][1], weaponeffects[newdata[1]][2], weaponeffects[newdata[1]][7], 0, int(newdata[2])])

                            del weaponeffects[newdata[1]]
                    except:
                        pass
                if newdata[0] == "gg":
                    winstring = "%s team has won! Winners receive %i Credits." %(newdata[1], int(newdata[2]))
                    linesaypico = font1.render(winstring, True, (250, 150, 250), (0, 0, 0))
                    linesaypico.set_colorkey((0, 0, 0))
                    winvar[0] = linesaypico
                    winvar[1] = "yes"
                    
            maintube.pop(0)
            

def docustom():
    global playergold, allowedpvp
    screen=pygame.display.set_mode([800,600])
    custompic = pygame.image.load("pics\custom.bmp")
    chooser = [0, 0, 1, 10]
    chooser2 = [0, 0, 1, 10]
    ### x, y, length, corenumber
    coreslist = []
    weaponcoreslist = []
    enginecoreslist = []
    modifycoreslist = []
    
    for core in modulesclient.cores.keys():
        if core != "c000" and modulesclient.cores[core][2] == "Weapon":
            weaponcoreslist.append([core, modulesclient.cores[core][2], modulesclient.cores[core][1]])
        if core != "c000" and modulesclient.cores[core][2] == "Core":
            modifycoreslist.append([core, modulesclient.cores[core][2], modulesclient.cores[core][1]])
        if core != "c000" and modulesclient.cores[core][2] == "Engine":
            enginecoreslist.append([core, modulesclient.cores[core][2], modulesclient.cores[core][1]])
    tuleb = len(coreslist)
    errormsg = ""
    while 1:
        allowedpvp -= 1
        takeinput()
        screen.blit(custompic, [0, 0])
        if keyinput == "m1":           ########## key input custom
            errormsg = ""
            mousepos = pygame.mouse.get_pos()

            if 456 < mousepos[0] < 550 and 38 < mousepos[1] < 72:
                coreslist = weaponcoreslist
                chooser2 = [0, 1, 1, 10]
            if 456 < mousepos[0] < 550 and 121 < mousepos[1] < 156:
                coreslist = enginecoreslist
                chooser2 = [0, 1, 1, 10]
            if 456 < mousepos[0] < 550 and 79 < mousepos[1] < 114:
                coreslist = modifycoreslist
                chooser2 = [0, 1, 1, 10]
            tuleb = len(coreslist)
            if 50 < mousepos[0] < 150 and 50 < mousepos[1] < 150:
                chooser = [50, 50, 100, 0]
            if 150 < mousepos[0] < 250 and 50 < mousepos[1] < 150:
                chooser = [150, 50, 100, 1]
            if 250 < mousepos[0] < 350 and 50 < mousepos[1] < 150:
                chooser = [250, 50, 100, 2]
            if 50 < mousepos[0] < 150 and 150 < mousepos[1] < 250:
                chooser = [50, 150, 100, 3]
            if 150 < mousepos[0] < 250 and 150 < mousepos[1] < 250:
                chooser = [150, 150, 100, 4]
            if 250 < mousepos[0] < 350 and 150 < mousepos[1] < 250:
                chooser = [250, 150, 100, 5]
            if 50 < mousepos[0] < 150 and 250 < mousepos[1] < 350:
                chooser = [50, 250, 100, 6]
            if 150 < mousepos[0] < 250 and 250 < mousepos[1] < 350:
                chooser = [150, 250, 100, 7]
            if 250 < mousepos[0] < 350 and 250 < mousepos[1] < 350:
                chooser = [250, 250, 100, 8]
            if 415 < mousepos[0] < 507 and 239 < mousepos[1] < 275:
                if chooser[0] != 0:
                    if currentship[chooser[3]] != "c000":
                        playergold += modulesclient.cores[currentship[chooser[3]]][8]
                        currentship[chooser[3]] = "c000"             ### remove
                    else: errormsg = "Cannot remove from empty Slot!"
                else: errormsg = "No slot selected!"

            for a in range(0, tuleb):
                if 590 < mousepos[0] < 790 and 50+a*30 < mousepos[1] < 80+a*30:
                    chooser2 = [553, 48+a*30, 30, a]
            if 415 < mousepos[0] < 507 and 197 < mousepos[1] < 232:
                if chooser2[0] != 0 and chooser[0] != 0:
                    getpass = 1
                    for corz in currentship:
                        if corz == coreslist[chooser2[3]][0]:
                            errormsg = "Cannot install 2 of the same Parts!"
                            getpass = 0
                    if currentship[chooser[3]] == "c000" and getpass == 1:
                        enginesamount = 0
                        if coreslist[chooser2[3]][1] == "Engine":
                            for coru in currentship:
                                if modulesclient.cores[coru][2] == "Engine":
                                    enginesamount += 1
                        if enginesamount < 1:
                            if playergold >= modulesclient.cores[coreslist[chooser2[3]][0]][8]:    #### add ship and remove credits
                                currentship[chooser[3]] = coreslist[chooser2[3]][0]
                                playergold -= modulesclient.cores[coreslist[chooser2[3]][0]][8]
                            else:
                                errormsg = "Not enough Credits!"
                        else:
                            errormsg = "Cannot install more then 1 Engine!"
                    else:
                        if getpass == 1:
                            errormsg = "This Slot is not empty!"
                else:
                    errormsg = "You need to Select both a Slot and a Part!"

            if 415 < mousepos[0] < 507 and 282 < mousepos[1] < 318:
                sendstring = ""
                for core in currentship:
                    sendstring += "%s " %core
                sendlist.append("004upd %s" %sendstring)
                break

        i = 0
        o = 0
        for core in currentship:    ##### print ship
            screen.blit(modulesclient.cores[core][0], [50+i, 50+o])
            i = i + 100
            if i == 300:
                o = o + 100
                i = 0
        i = 0
        for core in coreslist: ### print list
            corestring = "%i   %s" %(modulesclient.cores[core[0]][8], core[2])
            linesaypic = font1.render(corestring, True, (250, 150, 150), (0, 0, 0))
            screen.blit(linesaypic, [600, 55+i*30])
            newpic = pygame.transform.scale(modulesclient.cores[core[0]][0], (25, 25))
            screen.blit(newpic, [556, 52+i*30])
            i = i + 1

        playermaxhealth = 1000
        playermaxenergy = 1000
        playerenergyreg = 0
        playerhealthreg = 0
        playerarmor = 0
        playerspeed = 0
        playerweight = 0
        playercrit = 0
        speedvar = 0
        for core in currentship:
            playermaxenergy += modulesclient.cores[core][4]
            playerenergyreg += modulesclient.cores[core][5]
            playermaxhealth += modulesclient.cores[core][6]
            playerhealthreg += modulesclient.cores[core][7]
            playerweight += modulesclient.cores[core][10]
            if modulesclient.cores[core][2] == "Core":
                playerarmor += modulesclient.cores[core][9]
                playercrit += modulesclient.cores[core][12]
            if modulesclient.cores[core][2] == "Engine":
                playerspeed += modulesclient.cores[core][9]
                speedvar = modulesclient.cores[core][12]
        try:
            playerspeed = int(playerspeed-(playerweight/speedvar))
        except:
            playerspeed = 0
        if playerspeed < 0:
            playerspeed = 0
        if playerspeed > 50:
            playerspeed = 50

        if chooser[0] == 0:
            corestring = "^ Select a Part ^"
            linesaypic = font2.render(corestring, True, (150, 150, 150), (0, 0, 0))
            linesaypic.set_colorkey((0, 0, 0))
            screen.blit(linesaypic, [100,370])
        if chooser2[1] == 0:
            corestring = "<-Pick a Category"
            linesaypic = font2.render(corestring, True, (150, 150, 150), (0, 0, 0))
            screen.blit(linesaypic, [600,80])


        totalintegrity = playermaxhealth + ((playermaxhealth*playerarmor)/100)
        corestring = "Total Integrity: %i    repair: %i" %(totalintegrity, playerhealthreg)
        linesaypic = font1.render(corestring, True, (150, 250, 150), (0, 0, 0))
        screen.blit(linesaypic, [50, 408])
        corestring = "Energy: %i     regeneration: %i" %(playermaxenergy, playerenergyreg)
        linesaypic = font1.render(corestring, True, (150, 150, 250), (0, 0, 0))
        screen.blit(linesaypic, [50, 428])
        reduction = 100-(10000 / (100+playerarmor))
        corestring = "Integrity Extension: %i%%" %playerarmor
        linesaypic = font1.render(corestring, True, (150, 250, 150), (0, 0, 0))
        screen.blit(linesaypic, [50, 448])
        corestring = "Weight: %i   Speed: %i" %(playerweight, playerspeed)
        linesaypic = font1.render(corestring, True, (200, 100, 50), (0, 0, 0))
        screen.blit(linesaypic, [50, 468])
        corestring = "%i Credits" %playergold
        linesaypic = font2.render(corestring, True, (250, 150, 150), (0, 0, 0))
        screen.blit(linesaypic, [395, 352])
        try:
            critperc = 100-(10000 / (100+playercrit))
        except:
            critperc = 0
        corestring = "Critical Hit: +%i (%i%%)" %(playercrit, critperc)
        linesaypic = font1.render(corestring, True, (200, 100, 250), (0, 0, 0))
        screen.blit(linesaypic, [50, 488])
        if chooser[0] != 0:
            corestring = "%s %s" %(modulesclient.cores[currentship[chooser[3]]][1], modulesclient.cores[currentship[chooser[3]]][2])
            linesaypic = font1.render(corestring, True, (250, 50, 50), (0, 0, 0))
            screen.blit(linesaypic, [50, 508])
            corestring = "+integrity: %i   +repair: %i" %(modulesclient.cores[currentship[chooser[3]]][6], modulesclient.cores[currentship[chooser[3]]][7])
            linesaypic = font1.render(corestring, True, (150, 250, 150), (0, 0, 0))
            screen.blit(linesaypic, [50, 528])
            corestring = "+energy:    %i      +reg: %i" %(modulesclient.cores[currentship[chooser[3]]][4], modulesclient.cores[currentship[chooser[3]]][5])
            linesaypic = font1.render(corestring, True, (150, 150, 250), (0, 0, 0))
            screen.blit(linesaypic, [50, 548])
        if chooser2[0] != 0:
            corestring = "+integrity: %i   +repair: %i" %(modulesclient.cores[coreslist[chooser2[3]][0]][6], modulesclient.cores[coreslist[chooser2[3]][0]][7])
            linesaypic = font1.render(corestring, True, (150, 250, 150), (0, 0, 0))
            screen.blit(linesaypic, [300, 528])
            corestring = "+energy:    %i      +reg: %i" %(modulesclient.cores[coreslist[chooser2[3]][0]][4], modulesclient.cores[coreslist[chooser2[3]][0]][5])
            linesaypic = font1.render(corestring, True, (150, 150, 250), (0, 0, 0))
            screen.blit(linesaypic, [300, 548])
            if modulesclient.cores[coreslist[chooser2[3]][0]][2] == "Weapon":
                corestring = "%s %s" %(modulesclient.cores[coreslist[chooser2[3]][0]][1], modulesclient.cores[coreslist[chooser2[3]][0]][2])
                linesaypic = font1.render(corestring, True, (250, 50, 50), (0, 0, 0))
                screen.blit(linesaypic, [300, 408])
                corestring = "%s" %modulesclient.cores[coreslist[chooser2[3]][0]][9]
                linesaypic = font1.render(corestring, True, (250, 150, 250), (0, 0, 0))
                screen.blit(linesaypic, [300, 428])
                corestring = "Weight: %i" %modulesclient.cores[coreslist[chooser2[3]][0]][10]
                linesaypic = font1.render(corestring, True, (200, 100, 50), (0, 0, 0))
                screen.blit(linesaypic, [300, 468])
                corestring = "Cooldown: %i" %modulesclient.cores[coreslist[chooser2[3]][0]][3]
                linesaypic = font1.render(corestring, True, (200, 100, 150), (0, 0, 0))
                screen.blit(linesaypic, [300, 448])
            if modulesclient.cores[coreslist[chooser2[3]][0]][2] == "Core":
                corestring = "%s %s" %(modulesclient.cores[coreslist[chooser2[3]][0]][1], modulesclient.cores[coreslist[chooser2[3]][0]][2])
                linesaypic = font1.render(corestring, True, (250, 50, 50), (0, 0, 0))
                screen.blit(linesaypic, [300, 408])
                corestring = "%s" %modulesclient.cores[coreslist[chooser2[3]][0]][11]
                linesaypic = font1.render(corestring, True, (250, 150, 250), (0, 0, 0))
                screen.blit(linesaypic, [300, 428])
                corestring = "Integrity Extension: +%i%%" %modulesclient.cores[coreslist[chooser2[3]][0]][9]
                linesaypic = font1.render(corestring, True, (150, 250, 150), (0, 0, 0))
                screen.blit(linesaypic, [300, 448])
                corestring = "Critical Hit: +%i" %modulesclient.cores[coreslist[chooser2[3]][0]][12]
                linesaypic = font1.render(corestring, True, (200, 100, 250), (0, 0, 0))
                screen.blit(linesaypic, [300, 488])
                corestring = "Weight: %i" %modulesclient.cores[coreslist[chooser2[3]][0]][10]
                linesaypic = font1.render(corestring, True, (200, 100, 50), (0, 0, 0))
                screen.blit(linesaypic, [300, 468])
            if modulesclient.cores[coreslist[chooser2[3]][0]][2] == "Engine":
                corestring = "%s %s" %(modulesclient.cores[coreslist[chooser2[3]][0]][1], modulesclient.cores[coreslist[chooser2[3]][0]][2])
                linesaypic = font1.render(corestring, True, (250, 50, 50), (0, 0, 0))
                screen.blit(linesaypic, [300, 408])
                corestring = "%s" %modulesclient.cores[coreslist[chooser2[3]][0]][11]
                linesaypic = font1.render(corestring, True, (250, 150, 250), (0, 0, 0))
                screen.blit(linesaypic, [300, 428])
                corestring = "Weight: %i   Speed: %i" %(modulesclient.cores[coreslist[chooser2[3]][0]][10], modulesclient.cores[coreslist[chooser2[3]][0]][9])
                linesaypic = font1.render(corestring, True, (200, 100, 50), (0, 0, 0))
                screen.blit(linesaypic, [300, 468])
                corestring = "Weight Compensation: %i" %modulesclient.cores[coreslist[chooser2[3]][0]][12]
                linesaypic = font1.render(corestring, True, (200, 100, 50), (0, 0, 0))
                screen.blit(linesaypic, [300, 448])

        linesaypic = font1.render(errormsg, True, (250, 50, 50), (0, 0, 0))
        screen.blit(linesaypic, [8, 13])        

        pygame.draw.line(screen, (240, 0, 0), [chooser[0], chooser[1]], [chooser[0]+chooser[2], chooser[1]], 5)
        pygame.draw.line(screen, (240, 0, 0), [chooser[0], chooser[1]], [chooser[0], chooser[1]+chooser[2]], 5)
        pygame.draw.line(screen, (240, 0, 0), [chooser[0]+chooser[2], chooser[1]], [chooser[0]+chooser[2], chooser[1]+chooser[2]], 5)
        pygame.draw.line(screen, (240, 0, 0), [chooser[0], chooser[1]+chooser[2]], [chooser[0]+chooser[2], chooser[1]+chooser[2]], 5)
        pygame.draw.line(screen, (0, 240, 0), [chooser2[0], chooser2[1]], [chooser2[0]+chooser2[2], chooser2[1]], 5)
        pygame.draw.line(screen, (0, 240, 0), [chooser2[0], chooser2[1]], [chooser2[0], chooser2[1]+chooser2[2]], 5)
        pygame.draw.line(screen, (0, 240, 0), [chooser2[0]+chooser2[2], chooser2[1]], [chooser2[0]+chooser2[2], chooser2[1]+chooser2[2]], 5)
        pygame.draw.line(screen, (0, 240, 0), [chooser2[0], chooser2[1]+chooser2[2]], [chooser2[0]+chooser2[2], chooser2[1]+chooser2[2]], 5)
        
        pygame.display.flip()
        clock.tick(60)
            
    
thread.start_new_thread(receiver, (Port, ))
thread.start_new_thread(sender, (Port, ))
thread.start_new_thread(tubeoperations, (Port, ))
authorize()
while 1:
    sendlist.append("002steering lobby")
    chooser = lobby()
    pygame.display.quit()
    if chooser == 1:
        sendlist.append("003init")
        dopvp()
        sendlist.append("003exit")
        pygame.display.quit()
    if chooser == 2:
        sendlist.append("004init")
        docustom()
        pygame.display.quit()
    if chooser == 10:
        pygame.quit()
        break
