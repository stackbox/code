#!/usr/bin/env/python
# -*- coding:utf-8 -*-

"""
    This file is part of pySnake.

    PySnake is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    pySnake is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with pySnake.  If not, see <http://www.gnu.org/licenses/>.
"""


import sys,pygame
import math,geom
from os import path
pygame.init()

class vars:
#### Objects ####
    size=0
    objects=[]
    mov=[]
    collide=[]
    dirt_lst=[]
    screen=0
    trace_lst=[]
#### FPS-TIMER ####
    count=0
    all=0
    tim=[]
    rate=0
    fps_show=""
    font=pygame.font.Font("DejaVuSans.ttf", 40)
    empty=font.render("FPS: ",0,[200,50,50])
###################
def init(size=(800,600)):
    vars.size=size
    vars.screen = pygame.display.set_mode(size)
    vars.dirt_lst=[]
    vars.collide=[]
    vars.objects=[[],[],[],[]]
    vars.mov=[]
    vars.update=20
def clear():
    vars.objects=[[],[],[],[]]
def dirt_u():
    for i in range(len(vars.dirt_lst)-1):
        if i+1 <= len(vars.dirt_lst)-1:
            n=0
            vars.collide=[]
            coll=[]
            coll=vars.dirt_lst[i].collidelistall(vars.dirt_lst[i+1:])
            if len(coll)>0:
                for c in coll:
                    vars.collide.append(vars.dirt_lst[i+c+1-n])
                    del vars.dirt_lst[i+c+1-n]
                    n+=1
                vars.dirt_lst[i]=vars.dirt_lst[i].unionall(vars.collide)
def dirt(rect):
    vars.dirt_lst.append(rect.copy())
def show():
    for m in vars.mov:
        m.move(m.spx,m.spy)
    for i in vars.objects:
        for o in i:
            vars.screen.blit(o.image,o.pos)
    dirt_u()
    if len(vars.dirt_lst)>0:
        for d in vars.dirt_lst:
            pygame.display.update(d)
        vars.dirt_lst=[]
def objadd(obj,layer):
    vars.objects[layer].append(obj)
class font_wid:
    evade=[]
    spacex= 10
    spacey= 0
    sel_rgb=(50,50,200)
    rgb=(100,50,50)
    def __init__(self,text=[""],meta="",do=[None],stackv=True,off=(0,0),targeth=None,targetv=None,rgb=rgb,sel_rgb=sel_rgb):
        font_wid.evade.append(self)
        self.text=text
        self.targeth=targeth
        self.targetv=targetv
        self.meta=meta
        self.index=0
        self.farbe=rgb
        self.sel_rgb=sel_rgb
        self.pos=(0,0)
        self.object=object(vars.font.render(self.text[self.index],0,self.rgb),self.pos[0],self.pos[1],layer=3)
        if type(targeth)==str:
            if targeth=='last':targeth=font_wid.evade[len(font_wid.evade)-2]
        elif type(targeth)==int:targeth=font_wid.evade[len(font_wid.evade)-targeth]
        if type(targetv)==str:
            if targetv=='last':targetv=font_wid.evade[len(font_wid.evade)-2]
        elif type(targetv)==int:targetv=font_wid.evade[len(font_wid.evade)-targetv]
        for i in do:
            if i!=None:
                if i=="center":self.center(stackv,off)
                elif i=='centerh':self.centerh(off)
                elif i=='centerv':self.centerv(off)
                elif i=='alignv':self.alignv(targetv,off)
                elif i=='alignh':self.alignh(targeth,off)
        self.render()
    def select(self):
        self.farbe=self.sel_rgb
        self.render()
    def deselect(self):
        self.farbe=self.rgb
        self.render()
    def render(self):
        self.object.img_set(vars.font.render(self.text[self.index],0,self.farbe))
    def cycle(self):
        self.index+=1
        if self.index>len(self.text)-1:self.index=0
        self.render()
    def center(self,stackv=True,addpos=(0,0)):
        self.centerh(addpos)
        self.centerv(addpos)
        if stackv==True:
            if stackv==True:self.checkv()
            else:self.checkh()
    def centerh(self,addx=(0,0)):
        self.object.pos.x=vars.size[0]/2-self.object.pos.width/2+addx[0]
    def checkh(self):
        for p in font_wid.evade:
            for i in font_wid.evade:
                if not(p is i) and p.object.pos.colliderect(i.object.pos)>0:
                    p.object.pos.y-=(i.object.pos.height/2 + font_wid.spacey/2)
                    i.object.pos.y+=(p.object.pos.height/2 + font_wid.spacey/2)
                    self.checkh()
                    return 1
    def centerv(self,addy=(0,0)):
        self.object.pos.y=vars.size[1]/2-self.object.pos.height/2+addy[1]
    def checkv(self):
        for p in font_wid.evade:
            for i in font_wid.evade:
                if not (p is i) and p.object.pos.colliderect(i.object.pos)>0:
                    p.object.pos.y-=(i.object.pos.height/2 + font_wid.spacey/2)
                    i.object.pos.y+=(p.object.pos.height/2 + font_wid.spacey/2)
                    self.checkv()
                    return 1
    def alignv(self,target,off=(0,0)):
        self.object.pos.y=target.object.pos.y+off[1]
    def alignh(self,target,off=(0,0)):
        self.object.x=target.object.x+off[0]        
class object:
    def __init__(self,image,x=0,y=0,sphyp=0,angle=0,layer=0,trace=0):
        self.track=0
        self.layer=layer
        self.image=image.convert_alpha()
        if type(x)==type(self):
            self.pos=x.pos.copy()
        else:
            self.pos=self.image.get_rect().move(x,y)
        self.hyp=sphyp
        self.alpha=angle
        objadd(self,layer)
        if self.hyp!=0:
            vars.mov.append(self)
        self.speed_calc()
        dirt(self.pos)
    def img_set(self,image):
        dirt(self.pos)
        self.image=image
        self.pos.width=image.get_rect().width
        self.pos.height=image.get_rect().height
        dirt(self.pos)
    def speed_set(self,hyp):
        self.hyp=hyp
        if self.hyp != 0 and vars.mov.count(self)==0:
            vars.mov.append(self)
        elif self.hyp == 0 and vars.mov.count(self)>0:
            pass
        self.speed_calc()
        if type(self.tracedby) == type(self):
            self.tracedby.speed_set(hyp)
    def speed_add(self,addhyp):
        self.hyp+=addhyp
        if self.hyp !=0 and vars.mov.count(self)==0:
            vars.mov.append(self)
        self.speed_calc()
    def speed_calc(self):
        self.spy=math.sin(math.radians(self.alpha))*self.hyp
        self.spx=math.cos(math.radians(self.alpha))*self.hyp
        if self.hyp !=0 and vars.mov.count(self)==0:
            vars.mov.append(self)
    def speed_rot(self,angle=0,setangle=None):
        if setangle!=None:
            self.alpha=setangle
        else:
            self.alpha+=angle
        if self.alpha > 360:
            self.alpha-=360
        elif self.alpha < -360:
            self.alpha+=360
        self.speed_calc()
    def move(self,addx,addy):
        dirt(self.pos)
        self.pos.x+=addx
        self.pos.y+=addy
        dirt(self.pos)
    def update_track(self,length):
            self.track.add_point(self.pos.x,self.pos.y)
            self.track.resize(length,1)            
            self.track.defrag()
    def remove(self):
        self.dirt()
        vars.objects[self.layer].remove(self)
        if vars.mov.count(self)>0:vars.mov.remove(self)
    def dirt(self):
        dirt(self.pos)

class trace:
    def __init__(self):
        self.track_lst=[]
        self.trace_lst=[]
    def add_trace(self,track,length,trace):
        self.track_lst.append((track,length))
        track.track=geom.curve()
        track.track.add_point(track.pos.x,track.pos.y,track.pos.x,track.pos.y)
        self.trace_lst.append(trace)
    def update_track(self):
        for o in self.track_lst:
            o[0].update_track(o[1])
    def update_trace(self):
        for o in enumerate(self.trace_lst):
            xy=self.track_lst[o[0]][0].track.get_startpoint()
            o[1].dirt()
            o[1].pos.x=xy[0]
            o[1].pos.y=xy[1]
            o[1].dirt()
    def reset(self):
        self.track_lst=[]
        self.trace_lst=[]

        
def fps_init(update=10):
    vars.fps_show = object(vars.empty,0,0,layer=3)
    vars.timer=pygame.time.Clock()
    vars.update=update
def tick(rate=0,show=0):
    vars.timer.tick(vars.update)
    fps()
def fps():
    vars.fps_show.img_set(vars.font.render("FPS: "+str(round(vars.timer.get_fps(),1)),0,[200,50,50]))