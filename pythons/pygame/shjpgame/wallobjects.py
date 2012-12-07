import pygame

objectlist = {}

wallpic1 = pygame.image.load("pics\objects\wall1.bmp")
wallpic1.set_colorkey((0,0,0))
wallpic2 = pygame.image.load("pics\objects\wall2.bmp")
wallpic2.set_colorkey((0,0,0))





objectlist["1"] = [980, 300, 40, 700, wallpic1]

objectlist["2"] = [100, 100, 50, 50, wallpic2]
objectlist["3"] = [1850, 100, 50, 50, wallpic2]

objectlist["4"] = [975, 1250, 50, 50, wallpic2]
objectlist["5"] = [975, 1100, 50, 50, wallpic2]
objectlist["6"] = [975, 150, 50, 50, wallpic2]
