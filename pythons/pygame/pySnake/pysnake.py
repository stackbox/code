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
import math,display,random,copy
import sqlite3
from os import path

class snake_new:
    def __init__(self,parent,diff=0,speed=5):
        self.parent=parent
        self.diff=diff
        self.gameover=0
        self.count=0
        self.speed_o=[]
        self.part_lst=[]
        self.plcontrol=[]
        self.collrect_lst=[]
        self.grow_i=[]
        for i in range(1,2):
            self.grow_i.append(pygame.image.load(path.join(gfx,"food"+str(i)+".png")))
        self.speed_i=[]
        for i in range(1,10):
            self.speed_i.append(pygame.image.load(path.join(gfx,"etab"+str(i)+".png")))
        self.part_i = pygame.image.load(path.join(gfx,"snake_part1.png"))
        self.head_i = pygame.image.load(path.join(gfx,"snake_head.png"))
        self.score_i=pygame.image.load(path.join(gfx,"score.png"))
        self.head_o = display.object(self.head_i,300,100,speed,layer=2,angle=0)
        self.plcontrol.append(self.head_o)
        self.grow_place()
        self.speed_place()
        self.empty=self.parent.font.render("Score: ",0,[200,50,50])
        self.score_o = display.object(self.empty,0,30,layer=3)
    def grow(self):
        if self.head_o.pos.collidepoint(self.grow_o.pos.center[0],self.grow_o.pos.center[1])>0:
            self.grow_place()
            self.add()
    def speed(self):
        for o in self.speed_o:
            if self.head_o.pos.collidepoint(o.pos.center[0],o.pos.center[1])>0:
                self.speed_place()
                self.head_o.speed_add(1)
    def grow_place(self):
        try:
            self.grow_o.remove()
        except:
            pass
        x,y=(random.randint(10,self.parent.size[0]-40),random.randint(10,self.parent.size[1]-40))            
        i=random.randint(0,0)
        self.grow_o=display.object(self.grow_i[i],x,y,0,layer=1)        
    def speed_place(self):
        for o in self.speed_o:
            o.remove()
        self.speed_o=[]
        for i in range(0,self.diff):
            random.seed()
            x,y=(random.randint(10,self.parent.size[0]-40),random.randint(10,self.parent.size[1]-40))
            i=random.randint(0,8)
            self.speed_o.append(display.object(self.speed_i[i],x,y,0,layer=1))
    def score(self):
        self.score_o.img_set(self.parent.font.render("Score: "+str(self.count-1),True,[200,50,50]))
    def add(self):
        self.over=0
        self.part_lst.append(display.object(self.part_i,layer=2))
        if self.count==0:self.parent.trace.add_trace(self.head_o,25,self.part_lst[0])
        else:self.parent.trace.add_trace(self.part_lst[self.count-1],25,self.part_lst[self.count])
        self.count+=1
    def collcheck(self):
        try:
            if self.over==0:
                self.collrect_lst=[]
                for i in range(1,len(self.part_lst)-1):
                    self.collrect_lst.append(self.part_lst[i].pos)
                if self.head_o.pos.collidelist(self.collrect_lst) > -1 or self.parent.bounds.contains(self.head_o.pos)<1:
                    self.gameover=1
                    self.collrect_lst=[]
                    self.head_o.speed_set(0)
        except:
            pass

class game:
    def __init__(self):
        self.diff=0
        self.fcol=(50,50,50)
        self.fselcol=(50,50,200)
        self.relcontrol=True
        self.control_angle=10
        self.sensible=0
        self.speed=7
        self.img=[]
        self.text=[]
        self.ptim=0
        self.font=pygame.font.Font("DejaVuSans.ttf", 30)
        display.vars.font=self.font
        global gfx;gfx="gfx"
        pygame.init()
        self.size=(1024,800)
        self.bounds=pygame.Rect(0,0,self.size[0],self.size[1])
        display.init(self.size)
        self.menu_back=pygame.transform.smoothscale(pygame.image.load(path.join(gfx,'menu.jpg')).convert(),self.size)
        self.gameback = pygame.transform.smoothscale(pygame.image.load(path.join(gfx,"background.jpg")),self.size)
        self.fpslimit=40
        self.trace=display.trace()    
        self.option=[]
        self.sel=0
        self.menu()
        self.loop()
    def menu(self):
        self.purge()
        self.img.append(display.object(self.menu_back))
        self.option.append(display.font_wid(['pySnake'],'self.pysnake()',['center'],off=(-200,0)))
        self.option.append(display.font_wid(['pySnake Retro'],'self.game_classic()',['center'],off=(-200,0)))
        self.option.append(display.font_wid(['Options'],'self.settings()',['center'],off=(-200,0)))
        self.option.append(display.font_wid(['Highscores'],'self.show_high()',['center'],off=(-200,0)))
        self.option.append(display.font_wid(['Exit'],'sys.exit()',['center'],off=(-200,0)))        
    def loop(self):
        self.option[self.sel].select()
        maxlen=len(self.option)-1
        while True:
            for e in pygame.event.get():
                if e.type==pygame.QUIT:sys.exit()
                elif e.type==pygame.KEYDOWN:
                    self.option[self.sel].deselect()
                    if e.key==pygame.K_RETURN:exec(self.option[self.sel].meta);maxlen=len(self.option)-1
                    if e.key==pygame.K_UP:self.sel-=1
                    if e.key==pygame.K_DOWN:self.sel+=1
                    if self.sel < 0:self.sel=maxlen
                    if self.sel > maxlen:self.sel=0
                    self.option[self.sel].select()
            display.show()
    def purge(self):
        display.font_wid.evade=[]
        for o in self.option:
            o.object.remove()
        for o in self.img:
            o.remove
        for f in self.text:
            f.object.remove()
        self.option=[];self.text=[];self.img=[];self.sel=0
        display.clear()
    def show_high(self):
        self.purge()
        self.img.append(display.object(self.menu_back))
        self.option.append(display.font_wid(['Back'],'self.menu()',['center'],off=(0,300)))
        conn=sqlite3.connect('highdat')
        try:
            c=conn.cursor();c.execute('select * from stocks order by score DESC')
            for high in enumerate(c):
                text=str(high[0]+1)+'.'+str(high[1][0])+'        '+str(high[1][1])
                self.text.append(display.font_wid([text],do=['center'],off=(-50,0)))
                if high[0]>=15:break
        except:
            pass # no highdat file present...
        c.close()
        self.loop()
    def settings(self):
        self.purge()
        self.img.append(display.object(self.menu_back))
        self.option.append(display.font_wid(['Absolute Movement','Relative Movement'],'self.relcontrol=not self.relcontrol;self.option[self.sel].index=self.relcontrol',['center'],off=(-50,0)))
        if self.relcontrol==True:self.option[len(self.option)-1].cycle()
        self.text.append(display.font_wid(['Speed'],do=['center'],off=(-100,0)))
        self.text.append(display.font_wid(['Difficulty'],do=['center'],off=(-100,0)))
        self.text.append(display.font_wid(['FPS-Limit'],do=['center'],off=(-100,0)))        
        self.option.append(display.font_wid(['Back'],'self.menu()',['center'],off=(-50,0)))
        self.option.insert(1,display.font_wid([str(self.fpslimit)],'self.fpslimit=self.setvar(3,self.fpslimit)',['alignv','centerh'],targetv=3,off=(0,0)))        
        self.option.insert(1,display.font_wid([str(self.diff)],'self.diff=self.setvar(2,self.diff)',['alignv','centerh'],targetv=5,off=(0,0),stackv=True))
        self.option.insert(1,display.font_wid([str(self.speed)],'self.speed=self.setvar(1,self.speed)',['alignv','centerh'],targetv=7,off=(0,0)))
    def game_classic(self):
        pass
    def setvar(self,index=0,int=0):
        finite=False
        x=int
        while finite==False:
            if pygame.time.get_ticks()-self.ptim>250:
                if self.option[index].text==[str(x)]:self.option[index].text=['_']
                else:self.option[index].text=[str(x)]
                self.option[index].select();self.option[index].render();self.ptim=pygame.time.get_ticks()
            for e in pygame.event.get():
                if e.type==pygame.QUIT:sys.exit()
                elif e.type==pygame.KEYDOWN:
                    if e.key==pygame.K_UP:x+=1
                    elif e.key==pygame.K_DOWN:x-=1
                    elif e.key==pygame.K_RETURN:pygame.event.clear();finite=True
            display.show()
        self.option[index].text=[str(x)]
        return x
    def get_str(self,index=0):
        finite=False
        x=''
        while finite==False:
            if pygame.time.get_ticks()-self.ptim>200:
                if self.option[index].text==[x]:self.option[index].text=['_']
                else:self.option[index].text=[x]
                self.option[index].select();self.option[index].centerh(),self.option[index].render();self.ptim=pygame.time.get_ticks()
            for e in pygame.event.get():
                if e.type==pygame.QUIT:sys.exit()
                elif e.type==pygame.KEYDOWN:
                    if e.key==pygame.K_RETURN and len(x)!=0:pygame.event.clear();finite=True
                    elif e.key==pygame.K_BACKSPACE:x=x[0:len(x)-1] 
                    elif len(x)<10: x+=e.unicode
            display.show()
        self.option[index].text=[x]
        return x
    def get_high(self):
        self.text.append(display.font_wid(['Your Score was: '+str(self.snake.count-1)],do=['centerh','centerv'],off=(0,-70)))
        self.option.append(display.font_wid(['Please Enter your Name'],'self.submit_high(self.get_str(),self.snake.count)',['center'],))
        self.option.append(display.font_wid(['Back to Menu'],'self.menu()',['center']))
        self.loop()
    def submit_high(self,name='noname',score=0):
        conn=sqlite3.connect('highdat')
        c=conn.cursor()
        try:
            c.execute('select * from stocks order by score DESC')
        except:c.execute('create table stocks (name,score)') #if no highdat is present (means no table) a new will be created
        c.execute("""insert into stocks values (?,?)""",(name,score-1))
        try:
            while c.execute('select * from stocks order by score DESC').rowcount >10:c.execute('delete from stocks where rowid=11') #cuts off all entries above 10
        except:pass
        conn.commit()
        c.close()
        self.menu()
    def pysnake(self):
        self.purge()
        display.fps_init(self.fpslimit)
        self.snake=snake_new(self,self.diff,self.speed)
        black =  0, 0, 0
        self.back = display.object(self.gameback,layer=0)
        self.snake.add()
        while 1:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
                if event.type==pygame.KEYDOWN: 
                    if event.key==pygame.K_ESCAPE:self.snake.gameover=1
                    elif event.key==pygame.K_SPACE:self.relcontrol=not self.relcontrol
                    if self.relcontrol==False:
                        for c in self.snake.plcontrol:
                            if event.key==pygame.K_UP:c.speed_rot(setangle=270)
                            elif event.key==pygame.K_DOWN:c.speed_rot(setangle=90)
                            elif event.key==pygame.K_LEFT:c.speed_rot(setangle=180)
                            elif event.key==pygame.K_RIGHT:c.speed_rot(setangle=0)            
            kp=pygame.key.get_pressed()
            if pygame.time.get_ticks()-self.ptim> self.sensible and self.relcontrol==True:
                self.ptim=pygame.time.get_ticks()
                for c in self.snake.plcontrol:
                    if kp[275]>0:c.speed_rot(self.control_angle*1)
                    elif kp[276]>0:c.speed_rot(self.control_angle*-1)
            if self.snake.gameover==1:
                self.trace.reset()
                self.get_high()
                self.purge()
                self.menu()
                self.loop()
            else:
                self.snake.grow()
                self.snake.speed()
                self.snake.score()
                self.snake.collcheck()
                self.trace.update_track()
                self.trace.update_trace()
                display.tick(self.fpslimit,1)
                display.show()
game=game()