import pygame


######## CORE
coreemptypic = pygame.image.load("pics\coreempty.bmp")
coreemptypic.set_colorkey((0,0,0))
core0pic = pygame.image.load("pics\core0.bmp")
core0pic.set_colorkey((0,0,0))
core1pic = pygame.image.load("pics\core1.bmp")
core1pic.set_colorkey((0,0,0))
core2pic = pygame.image.load("pics\core2.bmp")
core2pic.set_colorkey((0,0,0))
cores = {}


cores["c000"] = [coreemptypic, "   ", "...empty...", 0, 0, 0, 0, 0, 0, 0, 0, "nothing"]
cores["c100"] = [core1pic, "Basic N30", "Weapon", 8, 10, 1, 10, 1, 12, "Standard Projectile Weapon", 5]
cores["c200"] = [core0pic, "Basic N30", "Core", 0, 10, 1, 10, 0, 15, 10, 5, "Basic Module", 0]
cores["c300"] = [core2pic, "Basic N3O", "Engine", 0, 0, 1, 10, 0, 33, 30, 5, "Basic Engine", 10]

## 3: cooldown 4: max energy 5: energy reg 6: max hp 7: hp reg 8: gold value
## CORE/MOD:  9: armor  10weight 11: description 12: critical
#### weapon: 9: description 10 weight
### engine: 9: speed 10 weight 11: description 12: speed variable


cores["c201"] = [core0pic, "S.U.S.I. V2", "Core", 0, 100, 2, 0, 1, 35, 5, 35, "Amplifier Mod", 15]
cores["c301"] = [core2pic, "Silent", "Engine", 0, 100, 1, 100, 1, 63, 45, 45, "Light and fast", 16]



cores["c101"] = [core1pic, "Railgun", "Weapon", 5, 50, 1, 50, 2, 22, "Rapid Projectile Weapon", 15]
cores["c102"] = [core1pic, "Mines", "Weapon", 150, 150, 5, 150, 2, 35, "Places long lasting Mines", 35]
cores["c110"] = [core1pic, "Laser", "Weapon", 13, 50, 3, 50, 2, 25, "Short Range Laser", 45]
cores["c111"] = [core1pic, "Beamer", "Weapon", 55, 0, 2, 50, 2, 45, "Long Range Laser", 65]
cores["c120"] = [core1pic, "Rocket", "Weapon", 23, 0, 2, 50, 1, 45, "Rocket Launcher", 65]
cores["c121"] = [core1pic, "Rocket2", "Weapon", 33, 100, 2, 50, 1, 35, "Rocket Launcher 2", 45]




shot1pic = pygame.image.load("pics\shot1.bmp")
shot1pic.set_colorkey((0,0,0))
shot2pic = pygame.image.load("pics\shot2.bmp")
shot2pic.set_colorkey((0,0,0))
shot3pic = pygame.image.load("pics\shot3.bmp")
shot3pic.set_colorkey((0,0,0))
shot4pic = pygame.image.load("pics\shot4.bmp")
shot4pic.set_colorkey((0,0,0))
shot5pic = pygame.image.load("pics\shot5.bmp")
shot5pic.set_colorkey((0,0,0))


shots = {}
shots["1"] = [shot1pic, 55]
shots["2"] = [shot2pic, 35]
shots["3"] = [shot3pic, 175]
shots["4"] = [shot4pic, 45]
shots["5"] = [shot5pic, 55]
shots["100"] = [0, 60]
shots["101"] = [0, 21]

