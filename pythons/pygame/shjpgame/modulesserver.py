cores = {}
cores["c000"] = [0, "empty", "m", 0, 0, 0, 0, 0]
cores["c100"] = [12, "weapon", "m", 10, 1, 10, 1, 35, 55, 6, "shot", 45, 1, 8, 5]
cores["c200"] = [15, "modification", "m", 10, 1, 10, 1, 10, 5, 0]
cores["c300"] = [33, "engine", "m", 10, 1, 10, 1, 30, 5, 10]

###### 0: gold value 1: coretype 2: unused 3: +max energy 4: +energy restoration 5: health 6: health reg

#### weapon type: 7: energy cost 8: shot duration 9: speed/damage(laser) 10: type 11: explosion range 12: shot type 13: cooldown 14: weight

#### mod type: 7: armor 8: weight 9: critical

#### engine: 7: speed 8: weight 9: speed variable


cores["c201"] = [35, "modification", "m", 100, 2, 0, 1, 5, 35, 15]
cores["c301"] = [63, "engine", "m", 100, 1, 100, 1, 45, 45, 16]

cores["c101"] = [22, "weapon", "m", 50, 1, 50, 2, 15, 50, 7, "shot", 45, 2, 5, 15]
cores["c102"] = [35, "weapon", "m", 100, 2, 150, 2, 65, 555, 0, "shot", 95, 3, 150, 35]   ### mine
cores["c110"] = [25, "weapon", "m", 50, 3, 50, 2, 5, 8, 21, "laser", 300, 101, 13, 45]
cores["c111"] = [45, "weapon", "m", 0, 2, 50, 2, 25, 14, 60, "laser", 425, 100, 55, 65]
cores["c120"] = [45, "weapon", "m", 0, 2, 50, 1, 45, 325, 8, "rocket", 5, 4, 23, 65]
cores["c121"] = [35, "weapon", "m", 100, 2, 50, 1, 45, 360, 9, "rocket", 5, 5, 33, 45]


### defined weapon types: shot, laser
### defined shot types: 1, 2, 3, 4, 5, 100=cyan, 101=blue


shots = {}
shots["1"] = [55]
shots["2"] = [35]
shots["3"] = [175]
shots["4"] = [45]
shots["5"] = [55]

### raw dmg
