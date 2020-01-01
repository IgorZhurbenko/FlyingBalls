#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      user
#
# Created:     25.11.2019
# Copyright:   (c) user 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import tkinter as tk
import pdb
import random
from webcolors import rgb_to_name
from GeneralProcedures import *
#import NumPy as n

minimal_difference = 0.002
m_d = minimal_difference
debug_mode = True

#_______________________________________________________________________

class Ball():
    def __init__(self,owner,x,y,r,vx=0,vy=0,density=10):
        self.x = x;self.y=y;self.r=r;self.code = 0
        self.vx=vx;self.vy=vy; self.density=density; self.mass=density*self.r;
        self.type='ball';self.moveable=True;self.owner = owner; self.reacted = False
    def coords(self):
        return [self.x,self.y]

    def show(self,space):
        self.color = "grey"+str(100-int(self.density))
        #punkt()
        self.code = space.create_oval(self.x-self.r,self.y-self.r,self.x+self.r,self.y+self.r,fill=self.color)
        self.space = space
    def move(self):
        global m_d
        dx = self.vx*self.owner.speed; dy = self.vy*self.owner.speed
        self.x += dx
        self.y += dy
        #print(self.code,self.vx,self.vy)
        try:
            self.space.move(self.code,dx,dy)
        except:
            pass
    def is_within(self,x,y):
        return (abs(x-self.x)<=self.r and abs(y-self.y)<=self.r)
    def collides(self,obj):
        if obj==self:
            return False
        if type(obj) == Ball:
            if (((self.x-obj.x)**2+(self.y-obj.y)**2)**0.5<=obj.r+self.r+m_d) == False:
                return False
            else:
                return True
        if type(obj) == Skeleton:
            #punkt()
            for edge in obj:
                if self.collides(edge):
                    #punkt()
                    return self.collides(edge)
            return False
        if type(obj) == Edge:
            try:
                if distance_segment_point(obj.coords(),self.coords())<=self.r+m_d:
                    return obj
                    #print(self.code,'collided',obj)
                else:
                    return False
            except:
                return False
    def react_to_collision(self,obj):
        if type(obj) == Ball:
                if self.moveable and obj.moveable:
                    v = ball_ball_rebound_velocity(self,obj)
                    self.vx=v[0]; self.vy = v[1]
                    return "Mutual rebound"
                elif self.moveable and not(obj.moveable):
                    self.vx=-self.vx
                    self.vy=-self.vy
                    return "One-sided rebound"
                else:
                    return "Held still"

        if type(obj) == Skeleton:
            self.react_to_collision(self.collides(obj))
        if type(obj) == Edge:
            vv = vector_value([self.vx,self.vy])
            v=edge_rebound_velocity([self.vx,self.vy],obj.coords())
            if vector_value(v) != 0:
                v = [v[0]*vv/vector_value(v),v[1]*vv/vector_value(v)]
            else:
                self.vx = 0; self.vy = 0
            if type(v[0]) != int:
                pass
            self.vx = v[0]; self.vy = v[1]
            return "One-sided rebound"

class Edge:
    def __init__(self,owner,coords):
        self.x1=coords[0];self.x2=coords[2];self.y1=coords[1];self.y2=coords[3]
        self.moveable = False; self.mass = 100; self.owner = owner; self.reacted = False; self.space = False; self.vx=0;self.vy=0
    def show(self,space='no'):
        if space == 'no':
            if self.space != False:
                self.space.delete(self.code)
                self.code = self.space.create_line(self.x1,self.y1,self.x2,self.y2)
        else:
            self.space = space
            self.code = space.create_line(self.x1,self.y1,self.x2,self.y2)
    def collides(self,obj):
        return False #(obj.collides(self))
    def react_to_collision(self,obj):
        if not self.moveable:
            return "Held still"
    def coords(self):
        return [self.x1,self.y1,self.x2,self.y2]
    def lengthen(self,k):
        self.x1*=k;
        self.x2*=k
        self.y1*=k
        self.y2*=k
    def move(self):
        speed = self.owner.owner.speed
        self.x1+=self.vx*speed;self.x2+=self.vx*speed;self.y1+=self.vy*speed;self.y2+=self.vy*speed
        if not self.space:
             self.show()

class Skeleton(list):
    def __init__(self,owner,coords):
        self.owner=owner
        self.moveable = False
        self.reacted = False
        self.vx = 0; self.vy = 0
        for line in coords:
            self.append(Edge(self,line))
    def show(self,space):
        self.space = space
        for edge in self:
            edge.show(space)
    def collides(self,obj):
        for edge in self:
            if edge.collides(obj):
                return edge
        return False
    def enlarge(self,k):
        for edge in self:
            edge.lengthen(k)
            edge.x2*=k
            edge.y1*=k
            edge.y2*=k
    def move(self):
        for edge in self:
            ex = edge.vx; ey = edge.vy
            edge.vx = self.vx
            edge.vy = self.vy
            edge.move()
            edge.vx = ex; edge.vy = ey

class System(dict):
    def __init__(self,owner):
        self.owner = owner
        self.localtime = 0
        self.speed = 0; self.init= False; self.active=False
        self.gravity = 0
        self.air_friction_coef = 0
    def list_all(self):
        array = list()
        for keys in self:
            for obj in self[keys]:
                array.append(obj)
        return array
    def get_by_code(self,code):
        for obj in self.list_all():
            if obj.code==code:
                return obj
        return "Not found"
    def show(self,space):
        self.space=space
        for objects in self:
            for obj in self[objects]:
                obj.show(space)
    def move(self):
        #print('pass')
        #pdb.set_trace()
        for objects in self:
            for obj in self[objects]:
                if obj.moveable:
                    obj.move()
    def operate_collisions(self):
        all_objects = self.list_all()
        for obj1 in all_objects:
            if obj1.moveable:# and not obj1.reacted:
                for obj2 in all_objects:
                    if obj1 != obj2 and obj1.collides(obj2):# and not obj2.reacted:
                        obj1.react_to_collision(obj2)
                        #obj1.reacted = True; obj2.reacted=True
        for obj in all_objects:
            obj.reacted = False

    def apply_gravity(self):
        all_objects = self.list_all()
        for obj in all_objects:
           if obj.moveable:
               obj.vy = obj.vy+self.speed*self.gravity
    def apply_air_friction(self):
        all_objects = self.list_all()
        for obj in all_objects:
           if obj.moveable:
               obj.vy = obj.vy*(1-self.air_friction_coef)
               obj.vx = obj.vx*(1-self.air_friction_coef)

    def animate(self,lifetime=6000,speed=0.1):
        if self.init != True:
            self.lifetime = lifetime
            self.speed = speed
            self.init=True
            self.active=True
        self.localtime += speed*100
        self.operate_collisions()
        self.apply_gravity()
        self.apply_air_friction()
        self.move()
        #print(distance_line_point(self['skeletons'][0][5].coords(),self['balls'][0].coords()))
        if self.localtime<self.lifetime:
            self.owner.after(int(self.speed*100),lambda: self.animate(self.lifetime,self.speed))
        else:
            self.init=False
    def switch(self):
        self.active = not self.active

'''def switcher(event):
    event.widget.'''



def main():
    pass

if __name__ == '__main__':
    main()
