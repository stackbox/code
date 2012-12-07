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

import math

class point:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.exact=2
    def move(self,x=None,y=None,mode=0):
        if mode==0:
            if x!=None:
                self.x=x
            if y!=None:
                self.y=y
        elif mode==1:
            if x!=None:
                self.x+=x
            if y!=None:
                self.y+=y
    def xy(self):
        return (self.x,self.y)
    def x(self):
        return self.x
    def y(self):
        return self.y
    def endpoint(self,length,angle,exact=10):
        return point(round(self.x+math.cos(math.radians(angle))*length,exact),round(self.y+math.sin(math.radians(angle))*length,exact))
class curve:
    def __init__(self):
        self.curvedat=[]
        self.dirty=0
        self.pnull=point(0,0)
    def add_line(self,length,angle):
        self.regen()
        p1=self.curvedat[self.get_lastid()][3]
        p3=p1.endpoint(length,angle)
        self.curvedat.append([p1,length,angle,p3])
    def add_point(self,x,y,xs=0,ys=0):
        self.regen()
        last=self.get_lastid()
        if last > -1:
            p1=self.curvedat[last][3]
        else:
            p1=point(xs,ys)
        p2=point(x,y)
        length,angle=line(p1,p2)
        self.curvedat.append([p1,length,angle,p2])
    def len_line(self,id,deflen,mode=0):
        if mode==0:
            self.curvedat[id][1]=deflen
        elif mode==1:
            self.curvedat[id][1]+=deflen
        self.dirt(id)
    def get_angle(self,id):
        return self.curvedat[id][3]
    def dirt(self,id):
        if id < self.dirty:
            self.dirty=id
    def undirt(self,id):
        if id > self.dirty:
            self.dirty=id
    def dirtid(self):
        return self.dirty
    def get_point(self,id=0,pos=1):
        self.regen()
        if pos==1:
            return (self.curvedat[id][3].xy())
        elif pos==0:
            return (self.curvedat[id][0].xy())
        elif pos==3:
            return (self.curvedat[id][0].xy(),self.curvedat[id][3].xy())
    def get_startpoint(self):
        return self.curvedat[0][0].xy()
    def get_endpoint(self):
        return self.curvedat[self.get_lastid()][3].xy()
    def get_angle(self,id=0):
        return self.curvedat[id][2]
    def get_len(self,id=0):
        return self.curvedat[id][1]
    def get_len_curve(self):
        length=0
        for i in self.curvedat:
            length+=i[1]
        return length
    def get_lastid(self):
        return len(self.curvedat)-1
    def crop_curve(self,curvelen=0,anchor=0):
        i=0
        if anchor==0:
            i=self.get_lastid()
        self.regen()
        while curvelen>0 and i <= len(self.curvedat)-1:
            linelen=self.get_len(i)
            if curvelen>=linelen:
                curvelen-=linelen
                del self.curvedat[i]
                continue
            else:
                self.len_line(i,linelen-curvelen,0)
                break
            if anchor==0:
                i-=1
            else:
                i+=1
        self.dirt(0)
        self.regen(0,anchor)
    def resize(self,length,anchor=0):
        cropsize=self.get_len_curve()-length
        if cropsize<0:
            if anchor==0:
                self.curvedat[self.get_lastid()][1]-=cropsize
                return 1
            else:
                self.curvedat[0][1]-=cropsize
        self.crop_curve(cropsize,anchor)
        return 1
    def defrag(self):
        if len(self.curvedat)>2:
            i=0
            while True:
                self.regen()
                try:                
                    if round(self.get_len(i),2)==0:
                        del self.curvedat[i]
                        continue
                    if round(self.get_angle(i),0)==round(self.get_angle(i+1),0):
                        self.len_line(i,self.get_len(i)+self.get_len(i+1))
                        self.dirt(i+1)
                        del self.curvedat[i+1]
                        self.regen(i)
                        continue
                except:
                   break
                i+=1
    def regenid(self,id=0,anchor=0):
        if anchor==0:
            if id>0:
                self.curvedat[id][0]=self.curvedat[id-1][3]
                self.curvedat[id][3]=self.curvedat[id][0].endpoint(self.curvedat[id][1],self.curvedat[id][2])
            else:
                self.curvedat[id][3]=self.curvedat[id][0].endpoint(self.curvedat[id][1],self.curvedat[id][2])
        elif anchor==1:
            if id<self.get_lastid():
                self.curvedat[id][3]=self.curvedat[id+1][0]
            self.curvedat[id][0]=self.curvedat[id][3].endpoint(self.curvedat[id][1],revangle(self.curvedat[id][2]))
        self.undirt(id)
    def regen(self,id=-1,anchor=0):
        dirty=self.dirtid()
        ids=self.get_lastid()
        if id>ids or id==-1:
            id=ids
        elif id<dirty and anchor==0:
            return 0
        for i in range(dirty,id+1):
            self.regenid(i,anchor)
            
def line(p1,p2):
    x=p2.x-p1.x
    y=p2.y-p1.y
    length=hyp(x,y)
    try:
        angle=180-math.degrees(math.acos((x*-1)/length))*(y/abs(y))
    except:
        try:
            angle=180-math.degrees(math.acos((x*-1)/length))*1    
        except:
            angle=0
    return (length,angle)
def hyp(x,y):
    return math.sqrt(math.pow(x,2)+math.pow(y,2))
def revangle(angle):
    angle+=180
    if angle>360:
        angle-=360
    return angle

