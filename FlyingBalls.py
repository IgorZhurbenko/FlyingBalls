import tkinter as tk
import pdb
class Ball():
    def __init__(self,x,y,r,vx=0,vy=0):
        self.x = x;self.y=y;self.r=r;self.code = 0
        self.vx=vx;self.vy=vy
        self.type='ball';self.moveable=True
    def show(self,space):
        self.code = space.create_oval(self.x-self.r,self.y-self.r,self.x+self.r,self.y+self.r)
        self.owner = space
    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.owner.move(self.code,self.vx,self.vy)
    def is_within(self,x,y):
        return (abs(x-self.x)<=self.r and abs(y-self.y)<=self.r)
    def collides(obj):
        if type(obj) == Ball:
            return (((self.x-obj.x)**2+(self.y-obj.y)**2)**0.5<=obj.r+self.r)
        if type(obj) == Cage:
            return null
        
class Cage:
    def __init__(self,space, coords):
        self.width = width
        self.height = heigt
        self.owner = space
        self.coords = coords
        self.moveable = False
    def show():
        space.create_polygon(coords)
        
class System(dict):
    def __init__(self,owner):
        self.owner = owner
    def show(self,space):
        for objects in self:
            for obj in self[objects]:
                obj.show(space)
    def move(self):
        print('pass')
        pdb.set_trace()
        for objects in self:
            for obj in self[objects]:
                if obj.moveable:
                    obj.move()
    
    
def tick(system):
    system.move()
    system.owner.after(100000,tick(system))

def repeat(root):
    print('Something')
    root.after(10, repeat(root))

def main():
    root = tk.Tk()
    root.geometry('250x250')
    system = System(root)
    space = tk.Canvas(root,width=200,height=200,bg='white')
    space.pack()
    system['balls'] = [Ball(40+i*30,40+i*15,10,3,-3) for i in range(5)]
    system.show(space)
    #repeat(root)
    tick(system)
    
    print(system.owner)
    root.mainloop()

if __name__ == '__main__':
    main()

    
        
    
