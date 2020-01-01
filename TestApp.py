#-------------------------------------------------------------------------------
'''




'''
#----------------------------------------------

#import tkinter as tk
#import pdb
import random
from GeneralProcedures import *
from PhysicsAndGraphicsRemake import *
#from scipy import array as ar
#import template
#_______________________________________________________________________________
def step_on(system,event):
    if system.active:
        system.animate()
        system.owner.after(1, lambda event=event,system=system: step_on(system,event))
def switch(system,event):
    system.active = not system.active
    if system.active:
        system.animate()
        system.owner.after(1, lambda event=event,system=system: step_on(system,event))
def show_activated(event):
    print('Event activated')

def generate_ball(system,event):
    ball = Ball(system, ar([event.x,event.y]), 15, ar([random.randint(-500,500),random.randint(-500,500)]), 20)
    #ball.show(system.space)

def delete_excessive_balls(number_allowed,system):
    while (len(system['balls']) > number_allowed):
        system['balls'][0].destroy()

def rotate_canon(canon,event):
    canon.rotate_to(ar([event.x,event.y]))


def shoot(system,canon,number_allowed,event):
    canon.shoot()
    delete_excessive_balls(number_allowed,system)


def main():

    root = tk.Tk()
    root.geometry('1024x768')

    instructions = tk.Label(root, text = 'Press Space to switch motion on/off \n Left mouse button to shoot \n Right mouse button to direct the canon')

    instructions.grid(row = 0, column = 0)

    system = System(root)
    space = tk.Canvas(root,width=900,height=600,bg='white')
    space.grid(row = 0, column = 1)


    canon = Canon(system,[700,200],[80,30],700, 150)

    #Ball(system, canon.ball_point(), canon.canonball)#, [0,0], 20)
    #canon.show()

    nodes = list()

    nodes.append([500,10])
    nodes.append([10,10])
    nodes.append([10,500])
    nodes.append([500,500])

    nodes.append([500,100])

    skeleton = Skeleton(system,seq_to_line(nodes))

    '''ball3 = Ball(system, ar([200,100]), 15, ar([-20,-10]), 20)
    ball4 = Ball(system, ar([250,50]), 15, ar([60,60]), 20)
    ball1 = Ball(system, ar([80,20]), 15, ar([0,-30]), 20)'''

    nodes = list()

    nodes.append([500,250])
    nodes.append([400,450])

    skeleton = Skeleton(system,seq_to_line(nodes))

    nodes = list()

    nodes.append([100,250])
    nodes.append([200,450])

    skeleton = Skeleton(system,seq_to_line(nodes))

    system.show(space)
    canon.show()
    print(canon.ball_point())
    system.gravity = 90 #9.8
    system.air_friction_coef = 0.003

    system.animate(6000,0.01)

    space.bind_all('<space>', lambda event,system=system: switch(system,event))
    #space.bind_all('<Button-3>', lambda event,system=system: generate_ball(system,event))
    space.bind_all('<Button-1>', lambda event,system=system, canon = canon, number_allowed = 10: shoot(system,canon,number_allowed,event))
    #space.bind_all('<Button-3>', lambda event,system=system, : delete_excessive_balls (number_allowed,system,event))
    space.bind_all('<Button-3>', lambda event, canon = canon: rotate_canon(canon,event))

    root.mainloop()

if __name__ == '__main__':
    main()
