import socket, thread, time, modulesserver, pygame, superlib, math, sys, random, wallobjects
HostIP, Port, players, maintube, onlineplayers, authplayers = "", 50005, {}, [], {}, {}
clock = pygame.time.Clock()
clock3 = pygame.time.Clock()
listensoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listensoc.bind((HostIP, Port))
listensoc.listen(100)
cooldowns = {}
onlineplayers["1"] = ["Generic1", "pvp", 1, 100,  "c101", "c000", "c000", "c000", "c000", "c000", "c000", "c000", "c000", 200, 750, 0, 0, 0, 1000, 1000, 4, 1000, 1000, 1, "Red", 70, 0, "1y2y3y4y5y6y7y8y9y"]
onlineplayers["2"] = ["Generic2", "pvp", 1, 100,  "c101", "c000", "c000", "c000", "c000", "c000", "c000", "c000", "c000", 1800, 750, 0, 0, 0, 1000, 1000, 4, 1000, 1000, 1, "Blue", 70, 0, "1y2y3y4y5y6y7y8y9y"]
for player2 in onlineplayers.keys():
    playership2 = onlineplayers[player2][4:13]
    for module2 in playership2:
        if modulesserver.cores[module2][1] == "weapon":
            namecorestring = "%s%s" %(player2, module2)
            cooldowns[namecorestring] = [module2, 0]

def writedatabase():
    try:
        f = open("database", "r+")
    except:
        f = open("database", "w")
        f.close()
        print "database created"
        f = open("database", "r+")
    for element in players:
        savestring = ""
        for item in players[element]:
            savestring = "%s%s " % (savestring, item)
        savestring = "%s\n" % savestring
        f.write(savestring)
    f.close()
    print "database saved"

def readdatabase():
    try:
        f = open("database", "r+")
        for line in f:
            g = line.split()
            name = g[0]
            players[name] = [name]
            g.pop(0)
            for element in g:
                players[name].append(element)
        print "finished reading database"
    except:
        print "couldnt read database"
        writedatabase()

readdatabase()
def sender(uid):
    while 1:
        if len(authplayers[uid][1]) == 0:
            time.sleep(0.03)
        try:
            if len(authplayers[uid][1]) > 0:
                supersendstring = "%s" %authplayers[uid][1][0]
                if len(supersendstring) > 1000:
                    print len(supersendstring), "> 1000 critical error: string might be longer then buffer (1024)"
                while len(supersendstring) < 1024:
                    supersendstring += "#"
                authplayers[uid][0][0].send(supersendstring)
                authplayers[uid][1].pop(0)
        except:
            try:
                del onlineplayers[uid]
                del authplayers[uid]
            except:
                pass
            break

def receiver(uid):
    while 1:
        try:
            data = authplayers[uid][0][0].recv(1024)
            datatype = data[:3]
            data = data[3:]
            truther = data.find("#")
            data = data[:truther]
            if datatype != "999":
                maintube.append([uid, datatype, data])
            if datatype == "999":
                newdata = data.split()
                onlineplayers[uid][17] = int(newdata[0])    ##
                newdata.pop(0)
                authplayers[uid][2]["w"] = newdata[0]
                authplayers[uid][2]["a"] = newdata[1]
                authplayers[uid][2]["s"] = newdata[2]
                authplayers[uid][2]["d"] = newdata[3]
                authplayers[uid][2]["m1"] = newdata[4]

        except:
            try:
                del onlineplayers[uid]
                del authplayers[uid]
            except:
                pass
            break

def acceptconnections(Port):
    uid = 100  
    while 1:
        uid += 1
        conn, addr = listensoc.accept()
        authplayers[uid] = [[conn, addr], [], {}]
        authplayers[uid][2]["w"] = "no"
        authplayers[uid][2]["a"] = "no"
        authplayers[uid][2]["s"] = "no"
        authplayers[uid][2]["d"] = "no"
        authplayers[uid][2]["m1"] = "no"
        ####authplayer### 0: connection info   1: SENDTUBE 2: keystates             <- connection info
        thread.start_new_thread(receiver, (uid, ))
        thread.start_new_thread(sender, (uid, ))





def serverop(Port):       ########## work the maintube
    while 1:
        if len(maintube) > 0:
            name, jobtype, jobdata = maintube[0][0], maintube[0][1], maintube[0][2]
            newdata = jobdata.split()
            
            if jobtype == "001":                                                    ########## 001: AUTHENTICATION
                truther = newdata[0] in players
                if truther == True:
                    print "existing player"
                    if newdata[1] == players[newdata[0]][1]:
                        truther2 = newdata[0] in onlineplayers
                        if truther2 == True:
                            print "logged in already!"
                            authplayers[name][1].append("001log")
                        else:
                            onlineplayers[name] = [newdata[0], "nowhere", int(players[newdata[0]][2]), int(players[newdata[0]][3]), players[newdata[0]][4], players[newdata[0]][5], players[newdata[0]][6], players[newdata[0]][7], players[newdata[0]][8], players[newdata[0]][9], players[newdata[0]][10], players[newdata[0]][11], players[newdata[0]][12], 400, 300, 0, 0, 0, 100, 100, 0, 100, 100, 0, "none", 0, 0, "1y2y3y4y5y6y7y8y9y"]
                            #########onlineplayers 0: nickname 1: chatroom 2: level 3: gold 4-12: ship values 13: xpos 14: ypos 15: xspeed 16: yspeed 17: rotate 18: energy 19: maxenergy 20: energyreg 21: healrh 22: max healrh 23: health reg 24: team affiliation 25: critical  26: weight 27: weapon states   <- session values, copy to new player -> there
                            print "authenticated"
                            authplayers[name][1].append("001auth %s" %newdata[0])
                    else:
                        print "wrong password!"
                        authplayers[name][1].append("001wpw")
                else:
                    onlineplayers[name] = [newdata[0], "nowhere", 1, 100,  "c000", "c100", "c000", "c000", "c200", "c000", "c000", "c300", "c000", 400, 300, 0, 0, 0, 100, 100, 0, 100, 100, 0, "none", 0, 0, "1y2y3y4y5y6y7y8y9y"]                  ####   <- here
                    players[newdata[0]] = [newdata[0], newdata[1], "1", "100", "c000", "c100", "c000", "c000", "c200", "c000", "c000", "c300", "c000"]
                    ########### players: 0: name 1: password 2: level 3: gold 4-12: ship values                      <- database values
                    writedatabase()
                    print "new player"
                    authplayers[name][1].append("001new %s" %newdata[0])



            if jobtype == "002":                                                      ################ CHATTING
                if newdata[0] == "steering":
                    if newdata[1] == "lobby":
                        onlineplayers[name][1] = "lobby"
                        sendstring = ""
                        for player in onlineplayers.keys():
                            if onlineplayers[player][1] == "lobby":
                                sendstring = sendstring + "%s " %onlineplayers[player][0]
                        authplayers[name][1].append("002updch %s" %sendstring) 
                if newdata[0] == "says:":
                    if newdata[1] == "lobby":
                        for player in onlineplayers.keys():
                            if onlineplayers[player][1] == "lobby":
                                sendstring = ' '.join(newdata)
                                authplayers[player][1].append("002%s %s" % (onlineplayers[name][0], sendstring))



            if jobtype == "003":                                                   ############## PVP
                if newdata[0] == "init":
                    maintube.append([name, "004", "init"])
                    onlineplayers[name][1] = "pvp"
                    amountred = 0
                    amountblue = 0
                    if onlineplayers[name][24] == "none":
                        for player in onlineplayers.keys():
                            if onlineplayers[player][24] == "Red" and onlineplayers[player][1] == "pvp":
                                amountred += 1
                            if onlineplayers[player][24] == "Blue" and onlineplayers[player][1] == "pvp":
                                amountblue += 1
                        if amountred > amountblue:
                            onlineplayers[name][24] = "Blue"
                        else:
                            onlineplayers[name][24] = "Red"
                    if onlineplayers[name][24] == "Blue":
                        onlineplayers[name][13] = 1600
                        onlineplayers[name][14] = 300
                    if onlineplayers[name][24] == "Red":
                        onlineplayers[name][13] = 400
                        onlineplayers[name][14] = 300
                        
                if newdata[0] == "exit":
                    onlineplayers[name][1] = "lobby"
                    for player in onlineplayers.keys():
                        if onlineplayers[player][1] == "pvp" and int(player) > 99:
                            authplayers[player][1].append("003exitpvp %s" %onlineplayers[name][0])

                if newdata[0] == "switchstate":
                    weaponslist = []
                    playercores = onlineplayers[name][4:13]
                    for core in playercores:
                        if modulesserver.cores[core][1] == "weapon":
                            weaponslist.append(core)
                    index = 0
                    finder = 0
                    for core2 in weaponslist:
                        if core2 == newdata[1]:
                            finder = index
                        index += 1
                    firststring = onlineplayers[player][27][:finder*2+1]
                    laststring = onlineplayers[player][27][finder*2+2:]
                    if onlineplayers[player][27][finder*2+1] == "n":
                        onlineplayers[player][27] = "%sy%s" %(firststring, laststring)
                    else:
                        onlineplayers[player][27] = "%sn%s" %(firststring, laststring)



            if jobtype == "004":                                                      ################## CUSTOM
                if newdata[0] == "init":
                    sendstring = ""
                    playership = onlineplayers[name][4:13]
                    for entry in playership:
                        sendstring += "%s " %entry
                    authplayers[name][1].append("004updship %s %i" %(sendstring, onlineplayers[name][3]))  #### send player his modules
                    onlineplayers[name][18] = 1000                          ### update player stats from modules
                    onlineplayers[name][19] = 1000
                    onlineplayers[name][20] = 0
                    onlineplayers[name][21] = 1000
                    onlineplayers[name][22] = 1000
                    onlineplayers[name][23] = 0
                    onlineplayers[name][25] = 0
                    armorvalue = 0
                    for module in playership:
                        onlineplayers[name][19] += modulesserver.cores[module][3]
                        onlineplayers[name][20] += modulesserver.cores[module][4]
                        onlineplayers[name][22] += modulesserver.cores[module][5]
                        onlineplayers[name][23] += modulesserver.cores[module][6]
                        if modulesserver.cores[module][1] == "weapon":
                            namecorestring = "%s%s" %(name, module)
                            cooldowns[namecorestring] = [module, 0]
                        if modulesserver.cores[module][1] == "modification":
                            armorvalue += modulesserver.cores[module][7]
                            onlineplayers[name][25] += modulesserver.cores[module][9]

                    onlineplayers[name][22] += armorvalue * onlineplayers[name][22] / 100    ### 100 armor = double hp 
                            
                if newdata[0] == "upd":   ####### player sends his new cores
                    newdata.pop(0)
                    t = 0
                    previousstate = onlineplayers[name][4:13]
                    for core in newdata:
                        t += 1
                        onlineplayers[name][3+t] = core
                        players[onlineplayers[name][0]][3+t] = core
                    nowstate = onlineplayers[name][4:13]
                    maintube.append([name, "004", "init"])
                    nowstatesum = 0
                    prevstatesum = 0
                    for core in nowstate:
                        nowstatesum += modulesserver.cores[core][0]
                    for core in previousstate:
                        prevstatesum += modulesserver.cores[core][0]
                    endsum = prevstatesum - nowstatesum
                    players[onlineplayers[name][0]][3] = str(int(players[onlineplayers[name][0]][3])+endsum)
                    onlineplayers[name][3] += endsum
                    #### O_ O_ _ O_O O do gold from previous core and nowcore   (in players!)
                    writedatabase()
            
            maintube.pop(0)


def dopvp(Port):
    weaponeffects = {}
    #### weapon effects:   0: position x 1: position y 2: duration 3: counter 4: vectorx 5: vectory 6: speed 7: type 8: explode range 9: origin 10: target 11: shot type 12: team affiliaton
    wpfxuid = 0
    while 1:
        clock.tick(30)
        for entry in cooldowns.keys():
            cooldowns[entry][1] += 1
        for player in onlineplayers.keys():
            try:
                if onlineplayers[player][13] > -900 and onlineplayers[player][14] > -900:
                    for objecti in wallobjects.objectlist.keys():
                        if wallobjects.objectlist[objecti][0]-20 < onlineplayers[player][13] < wallobjects.objectlist[objecti][0]+20 + wallobjects.objectlist[objecti][2] and wallobjects.objectlist[objecti][1]-20 < onlineplayers[player][14] < wallobjects.objectlist[objecti][1]+20 + wallobjects.objectlist[objecti][3]:
                            onlineplayers[player][15] = -onlineplayers[player][15]
                            onlineplayers[player][16] = -onlineplayers[player][16]
     
                    
                    onlineplayers[player][13] += onlineplayers[player][15]   ### move             ############# AYAYAY   MUUUUUUSICA! 
                    onlineplayers[player][14] += onlineplayers[player][16]
                    if onlineplayers[player][14] < 0:
                        onlineplayers[player][16] = -onlineplayers[player][16]
                    if onlineplayers[player][13] < 0:
                        onlineplayers[player][15] = -onlineplayers[player][15]
                    if onlineplayers[player][13] > 2000:
                        onlineplayers[player][15] = -onlineplayers[player][15]
                    if onlineplayers[player][14] > 1500:
                        onlineplayers[player][16] = -onlineplayers[player][16]
                
                if onlineplayers[player][21] < 0:   ## player deads
                    onlineplayers[player][13] = -1000
                    onlineplayers[player][14] = -1000
                    onlineplayers[player][15] = 0
                    onlineplayers[player][16] = 0
                    onlineplayers[player][21] = onlineplayers[player][22]
                    onlineplayers[player][18] = onlineplayers[player][19]
                    if player == "1":
                        print "game over: blue team has won"
                        onlineplayers[player][13] = 200
                        onlineplayers[player][14] = 750
                        creditamount = 0
                        for playboy in onlineplayers.keys():
                            if onlineplayers[playboy][24] == "Red" and int(playboy) > 99:
                                creditamount += 1
                        for playeri in onlineplayers.keys():
                            if onlineplayers[playeri][1] == "pvp" and int(playeri) > 99:
                                if onlineplayers[playeri][24] == "Blue":
                                    onlineplayers[playeri][3] += creditamount
                                    players[onlineplayers[playeri][0]][3] = str(int(players[onlineplayers[playeri][0]][3]) + creditamount)
                                authplayers[playeri][1].append("005gg Blue %i" %creditamount)
                                
                    if player == "2":
                        print "game over: red team has won"
                        onlineplayers[player][13] = 1800
                        onlineplayers[player][14] = 750
                        creditamount = 0
                        for playboy in onlineplayers.keys():
                            if onlineplayers[playboy][24] == "Blue" and int(playboy) > 99:
                                creditamount += 1
                        for playeri in onlineplayers.keys():
                            if onlineplayers[playeri][1] == "pvp" and int(playeri) > 99:
                                if onlineplayers[playeri][24] == "Red":
                                    onlineplayers[playeri][3] += creditamount
                                    players[onlineplayers[playeri][0]][3] = str(int(players[onlineplayers[playeri][0]][3]) + creditamount)
                                authplayers[playeri][1].append("005gg Red %i" %creditamount)

                    if player == "1" or player == "2":
                        for playero in onlineplayers.keys():
                            if onlineplayers[playero][1] == "pvp" and int(playero) > 99:
                                if onlineplayers[playero][24] == "Blue":
                                    onlineplayers[playero][13] = 1900
                                if onlineplayers[playero][24] == "Red":
                                    onlineplayers[playero][13] = 100
                                onlineplayers[playero][14] = random.randint(500, 1000)
                                onlineplayers[playero][15] = 0
                                onlineplayers[playero][16] = 0
                                onlineplayers[playero][18] = onlineplayers[playero][19]
                                onlineplayers[playero][21] = onlineplayers[playero][22]
                shoot = "no"
                if 99 < int(player):
                    if authplayers[player][2]["m1"] == "do":     ##### fire weapons
                        shoot = "yes"
                if 100 > int(player):
                    shoot = "yes"
                if shoot == "yes":
                    playercores = onlineplayers[player][4:13]
                    weaponslist = []
                    for core3 in playercores:
                        if modulesserver.cores[core3][1] == "weapon":
                            weaponslist.append(core3)
                    for core in playercores:
                        if modulesserver.cores[core][1] == "weapon" and onlineplayers[player][18] > modulesserver.cores[core][7]:
                            index = 0
                            finder = 0
                            for core2 in weaponslist:
                                if core2 == core:
                                    finder = index
                                index += 1
                            if onlineplayers[player][27][finder*2+1] == "y":     #### if weapon active
                                namecorestring = "%s%s" % (player, core)
                                if cooldowns[namecorestring][1] > modulesserver.cores[core][13]:   #### cooldown per core TYPE (:<)
                                    cooldowns[namecorestring][1] = 0
                                    onlineplayers[player][18] -= modulesserver.cores[core][7]   ### energy cost

                                    gogo, gugu = superlib.Move(1, 1, onlineplayers[player][17], modulesserver.cores[core][9])
                                    if 100 > int(player):
                                        disteranzu = 350
                                        disteranzuplayer = "none"
                                        for playboy in onlineplayers.keys():   ### generic shot: if target < 350: pick
                                            if player != playboy and onlineplayers[player][24] != onlineplayers[playboy][24] and onlineplayers[playboy][1] == "pvp":
                                                distanzi = superlib.Distance(onlineplayers[playboy][13], onlineplayers[playboy][14], onlineplayers[player][13], onlineplayers[player][14])
                                                if distanzi < disteranzu:
                                                    disteranzu = distanzi
                                                    disteranzuplayer = playboy
                                        if disteranzuplayer != "none":
                                            smartmengspeed = disteranzu / modulesserver.cores[core][9]
                                            if smartmengspeed < 1:
                                                smartmengspeed = 1
                                            rotation = superlib.Angle(onlineplayers[player][13], onlineplayers[player][14], onlineplayers[disteranzuplayer][13]+(onlineplayers[disteranzuplayer][15]*smartmengspeed), onlineplayers[disteranzuplayer][14]+(onlineplayers[disteranzuplayer][16]*smartmengspeed))
                                            try:
                                                rotation = -rotation
                                            except:
                                                rotation = 1
                                            rotation += 180
                                            if rotation < 0:
                                                rotaton = rotation + 360
                                            gogo, gugu = superlib.Move(1, 1, rotation, modulesserver.cores[core][9])
                                        
                                    xvector = -int(gogo*modulesserver.cores[core][9])    #### shot vector
                                    yvector = -int(gugu*modulesserver.cores[core][9])

                                    target = "none"
                                    if modulesserver.cores[core][10] == "laser" or modulesserver.cores[core][10] == "rocket":
                                        distanzo = 1000
                                        for playboy in onlineplayers.keys():   #### pick a target in range of core weapon
                                            if player != playboy and onlineplayers[player][24] != onlineplayers[playboy][24] and onlineplayers[playboy][1] == "pvp":
                                                distanzi = superlib.Distance(onlineplayers[playboy][13], onlineplayers[playboy][14], onlineplayers[player][13], onlineplayers[player][14])
                                                if modulesserver.cores[core][10] == "laser":
                                                    if distanzi < modulesserver.cores[core][11] and distanzi < distanzo:
                                                        target = onlineplayers[playboy][0]
                                                        distanzo = distanzi
                                                if modulesserver.cores[core][10] == "rocket":
                                                    if distanzi < modulesserver.cores[core][8] and distanzi < distanzo:
                                                        target = onlineplayers[playboy][0]
                                                        distanzo = distanzi
                                        if target == "none":
                                            onlineplayers[player][18] += modulesserver.cores[core][7]  ### refund energy if laser with no target
                                            
                                    if modulesserver.cores[core][10] == "laser" and target != "none" or modulesserver.cores[core][10] == "rocket" and target != "none" or modulesserver.cores[core][10] == "shot" :
                                        if int(player) < 100 and disteranzuplayer == "none":
                                            onlineplayers[player][18] += modulesserver.cores[core][7]   #### refund generic shooting no target
                                        else:
                                            weaponeffects[wpfxuid] = [onlineplayers[player][13], onlineplayers[player][14], modulesserver.cores[core][8], 0, xvector, yvector, modulesserver.cores[core][9], modulesserver.cores[core][10], modulesserver.cores[core][11], onlineplayers[player][0], target, str(modulesserver.cores[core][12]), onlineplayers[player][24]]
                                            if target != "none" and modulesserver.cores[core][10] == "laser":
                                                try:
                                                    for onlineplayer in onlineplayers.keys():
                                                        if onlineplayers[onlineplayer][0] == target:
                                                            otarget = onlineplayer
                                                            onlineplayers[otarget][21] -= weaponeffects[wpfxuid][6] #hp loss from laser
                                                except: print "error no hp loss", otarget, target, sys.exc_info()[0]
                                            wpfxstring = "005wpfx %i %i %i %i %i %s %s %i %i %s %i %s" %(wpfxuid, onlineplayers[player][13], onlineplayers[player][14], xvector, yvector,  modulesserver.cores[core][10], target, modulesserver.cores[core][12], modulesserver.cores[core][8], onlineplayers[player][0], modulesserver.cores[core][9], core)
                                            ##### sendstring: uid, xpos, ypos, vectorx, vectory, type, target, shot type, duration, origin, core

                                            for player2 in onlineplayers.keys():
                                                if onlineplayers[player2][1] == "pvp" and int(player2) > 99:
                                                    authplayers[player2][1].append(wpfxstring)
                                            wpfxuid += 1
            except:
                print "error O_O"
                                            

        for effect in weaponeffects.keys():        ########## weapon effects
            if weaponeffects[effect][7] == "shot":                        #### move shots
                for objecti in wallobjects.objectlist.keys():
                    if wallobjects.objectlist[objecti][0] < weaponeffects[effect][0] < wallobjects.objectlist[objecti][0] + wallobjects.objectlist[objecti][2] and wallobjects.objectlist[objecti][1] < weaponeffects[effect][1] < wallobjects.objectlist[objecti][1] + wallobjects.objectlist[objecti][3]:
                        weaponeffects[effect][4] = -weaponeffects[effect][4]
                        weaponeffects[effect][5] = -weaponeffects[effect][5]
                if weaponeffects[effect][0] < 0:
                    weaponeffects[effect][4] = -weaponeffects[effect][4]
                if weaponeffects[effect][0] > 2000:
                    weaponeffects[effect][4] = -weaponeffects[effect][4]
                if weaponeffects[effect][1] < 0:
                    weaponeffects[effect][5] = -weaponeffects[effect][5]
                if weaponeffects[effect][1] > 1500:
                    weaponeffects[effect][5] = -weaponeffects[effect][5]
                weaponeffects[effect][0] += weaponeffects[effect][4]
                weaponeffects[effect][1] += weaponeffects[effect][5]

            if weaponeffects[effect][7] == "rocket" and weaponeffects[effect][10] != "none":
                for playero in onlineplayers.keys():
                    if onlineplayers[playero][0] == weaponeffects[effect][10]:
                        try:
                        
                            xd = weaponeffects[effect][0]-onlineplayers[playero][13]
                            yd = weaponeffects[effect][1]-onlineplayers[playero][14]
                            xres =  (1000000*xd) / int(1000*math.sqrt((xd*xd + yd*yd)))
                            yres =  (1000000*yd) / int(1000*math.sqrt((xd*xd + yd*yd)))
                            weaponeffects[effect][0] -= int((weaponeffects[effect][6]*xres)/1000)   #### move rocket
                            weaponeffects[effect][1] -= int((weaponeffects[effect][6]*yres)/1000)

                        except:
                            print sys.exc_info()[0]
                
            weaponeffects[effect][3] += 1                                 #### delete expired shots
            if weaponeffects[effect][7] == "rocket":
                weaponeffects[effect][3] += 4
            if weaponeffects[effect][3] > weaponeffects[effect][2]:
                del weaponeffects[effect]
            try:
                for objecti in wallobjects.objectlist.keys():
                    if wallobjects.objectlist[objecti][0] < weaponeffects[effect][0] < wallobjects.objectlist[objecti][0] + wallobjects.objectlist[objecti][2] and wallobjects.objectlist[objecti][1] < weaponeffects[effect][1] < wallobjects.objectlist[objecti][1] + wallobjects.objectlist[objecti][3]:
                        if weaponeffects[effect][7] == "rocket":
                            del weaponeffects[effect]
            except:
                pass
        playershit = {}
        for effect in weaponeffects.keys():          #### shot collision
            if weaponeffects[effect][7] == "shot" or weaponeffects[effect][7] == "rocket":
                for player in onlineplayers.keys():
                    if weaponeffects[effect][9] != onlineplayers[player][0] and onlineplayers[player][24] != weaponeffects[effect][12]:
                        distance = superlib.Distance(weaponeffects[effect][0], weaponeffects[effect][1], onlineplayers[player][13], onlineplayers[player][14])
                        if distance < weaponeffects[effect][8]:
                            crityes = 0
                            for playboy in onlineplayers.keys():
                                if onlineplayers[playboy][0] == weaponeffects[effect][9]:
                                    critical = onlineplayers[playboy][25]    ######### cRIT
                                    if critical > random.randint(1, 100+critical):
                                        onlineplayers[player][21] -= int((modulesserver.shots[weaponeffects[effect][11]][0] * critical)/100)
                                        crityes = critical
                            onlineplayers[player][21] -= modulesserver.shots[weaponeffects[effect][11]][0]
                            if effect in playershit.keys() == True:
                                playershit[effect].append([player, crityes])
                            else: playershit[effect] = [[player, crityes]]
        for effect in playershit.keys():
            for player in onlineplayers.keys():
                if onlineplayers[player][1] == "pvp" and int(player) > 99:
                    authplayers[player][1].append("005shotcol %i %i" %(effect, playershit[effect][0][1]))   #### send shot to delete
            del weaponeffects[effect]






def sendmove(Port):
    while 1:
        posistring = "003posupd "
        posistring2 = "003posupd "
        for player in onlineplayers.keys():
            playercores2 = onlineplayers[player][4:13]
            weight = 0
            speed = 0
            speedvar = 0
            for core in playercores2:
                if modulesserver.cores[core][1] == "weapon":
                    weight = weight + modulesserver.cores[core][14]
                if modulesserver.cores[core][1] == "modification":
                    weight = weight + modulesserver.cores[core][8]
                if modulesserver.cores[core][1] == "engine":
                    weight = weight + modulesserver.cores[core][8]
                    speed = speed + modulesserver.cores[core][7]
                    speedvar = modulesserver.cores[core][9]
            try:
                maxspeed = speed-(weight/speedvar)
            except:
                maxspeed = 0
            onlineplayers[player][26] = weight
            if maxspeed < 0:
                maxspeed = 0
            if maxspeed > 50:
                maxspeed = 50
            if onlineplayers[player][1] == "pvp" and int(player) > 99:
                if authplayers[player][2]["w"] == "do" and onlineplayers[player][16]  > -(maxspeed/10):
                    onlineplayers[player][16] -= 1
                if authplayers[player][2]["a"] == "do" and onlineplayers[player][15]  > -(maxspeed/10):
                    onlineplayers[player][15] -= 1
                if authplayers[player][2]["s"] == "do" and onlineplayers[player][16]  <  (maxspeed/10):
                    onlineplayers[player][16] += 1
                if authplayers[player][2]["d"] == "do" and onlineplayers[player][15]  <  (maxspeed/10):
                    onlineplayers[player][15] += 1
        
        for player in onlineplayers.keys():
            if onlineplayers[player][1] == "pvp" and int(player) > 99:
                healthamount = int(onlineplayers[player][21]*100/onlineplayers[player][22])
                energyamount = int(onlineplayers[player][18]*100/onlineplayers[player][19])
                posistring = posistring + "%s %i %i %i %i %i %i %i %s %i " %(onlineplayers[player][0], onlineplayers[player][13], onlineplayers[player][14], onlineplayers[player][15], onlineplayers[player][16], onlineplayers[player][17], healthamount, energyamount, onlineplayers[player][24], onlineplayers[player][26])
            if onlineplayers[player][1] == "pvp" and int(player) < 100:
                healthamount = int(onlineplayers[player][21]*100/onlineplayers[player][22])
                energyamount = int(onlineplayers[player][18]*100/onlineplayers[player][19])
                posistring2 = posistring2 + "%s %i %i %i %i %i %i %i %s %i " %(onlineplayers[player][0], onlineplayers[player][13], onlineplayers[player][14], onlineplayers[player][15], onlineplayers[player][16], onlineplayers[player][17], healthamount, energyamount, onlineplayers[player][24], onlineplayers[player][26])

        for player in onlineplayers.keys():
            if onlineplayers[player][1] == "pvp" and int(player) > 99:
                authplayers[player][1].append(posistring)
                authplayers[player][1].append(posistring2)
        for player in onlineplayers.keys():
            if onlineplayers[player][1] == "pvp" and onlineplayers[player][21] > 0:
                onlineplayers[player][18] += onlineplayers[player][20]   ## energy reg
                if onlineplayers[player][24] == "Blue":
                    distanzi = superlib.Distance(onlineplayers[player][13], onlineplayers[player][14], 1800, 750)
                if onlineplayers[player][24] == "Red":
                    distanzi = superlib.Distance(onlineplayers[player][13], onlineplayers[player][14], 200, 750)
                if distanzi < 350:
                    onlineplayers[player][18] += 3
                    onlineplayers[player][21] += 3   ### extra reg if in base distance
                if onlineplayers[player][18] > onlineplayers[player][19]:
                    onlineplayers[player][18] = onlineplayers[player][19]
                onlineplayers[player][21] += onlineplayers[player][23]   ### health reg
                if onlineplayers[player][21] > onlineplayers[player][22]:
                    onlineplayers[player][21] = onlineplayers[player][22]
        clock3.tick(5)

thread.start_new_thread(acceptconnections, (Port, ))
thread.start_new_thread(serverop, (Port, ))
thread.start_new_thread(dopvp, (Port, ))
thread.start_new_thread(sendmove, (Port, ))

while 1:
    time.sleep(5)
    for player in onlineplayers.keys():          #### update players lobby participant list
        if onlineplayers[player][1] == "lobby":
            maintube.append([player, "002", "steering lobby"])
            

        
