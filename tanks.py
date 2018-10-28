#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 19:18:02 2018

@author: gershow
"""
import numpy as np
import matplotlib.pyplot as plt
import math as mt

tank1Color = 'b'
tank2Color = 'r'
obstacleColor = 'k'

##### functions you need to implement #####
def trajectory (x0,y0,v,theta,g = 9.8, npts = 1000):
    """
    finds the x-y trajectory of a projectile
    
    parameters
    ----------
    x0 : float 
        initial x - position
    y0 : float
        initial y - position, must be >0
        initial velocity
    theta : float
        initial angle (in degrees)
    g : float (default 9.8)
        acceleration due to gravity
    npts : int
        number of points in the sample
    
    returns
    -------
    (x,y) : tuple of np.array of floats
        trajectory of the projectile vs time
    
    notes
    -----
    trajectory is sampled with npts time points between 0 and 
    the time when the y = 0 (regardless of y0)"""
    r = mt.radians(theta)
    sin = mt.sin(r)
    cos = mt.cos(r)
    vy = v*sin
    vx = v*cos
    sqrt = mt.sqrt(((vy/g)**2)+(2*y0/g))
    t_final = vy/g + sqrt
    t = np.linspace(0,t_final, npts)
    y = y0 + (vy*t)-(.5*g*(t**2))
    x = x0 + (vx*t)
    return(x,y)

def firstInBox (x,y,box):
    """
    finds first index of x,y inside box
    
    paramaters
    ----------
    x,y : np array type
        positions to check
    box : tuple
        (left,right,bottom,top)
    
    returns
    -------
    int
        the lowest j such that
        x[j] is in [left,right] and 
        y[j] is in [bottom,top]
        -1 if the line x,y does not go through the box
    """
    list1=[]
    list2=[]
    for num in x:
        if num >= box[0] and num <= box[1]:
            j = x.tolist().index(num)
            list1.append(j)
    for num in list1:
        if y[num] >= box[2] and y[num] <= box[3]:
            list2.append(num)
        else:
            list2.append(-1)
    return(list2[0])
            
            
        
def tankShot (targetBox, obstacleBox, x0, y0, v, theta, g = 9.8):
    """
    executes one tank shot
    
    parameters
    ----------
    targetBox : tuple
        (left,right,bottom,top) location of the target
    obstacleBox : tuple
        (left,right,bottom,top) location of the central obstacle
    x0,y0 :floats
        origin of the shot
    v : float
        velocity of the shot
    theta : float
        angle of the shot
    g : float 
        accel due to gravity (default 9.8)
    returns
    --------
    int
        code: 0 = miss, 1 = hit
        
    hit if trajectory intersects target box before intersecting
    obstacle box
    draws the truncated trajectory in current plot window
    """
    miss = 0 
    hit = 1
    x, y  = trajectory(x0, y0,v,theta)
    f1= firstInBox(x,y,obstacleBox)
    s1 = firstInBox(x,y, targetBox)
    fx,fy = endTrajectoryAtIntersection(x,y, obstacleBox)
    sx,sy= endTrajectoryAtIntersection(x,y, targetBox)
    if f1 == -1:
        if s1 != -1:
            plt.plot(sx,sy)
            return(hit)
        else:
            plt.plot(x,y)
            return(miss)
    else:
        plt.plot(fx,fy)
        return(miss)
    showWindow()

def drawBoard (tank1box, tank2box, obstacleBox, playerNum):
    """
    draws the game board, pre-shot
    parameters
    ----------
    tank1box : tuple
        (left,right,bottom,top) location of player1's tank
    tank2box : tuple
        (left,right,bottom,top) location of player1's tank
    obstacleBox : tuple
        (left,right,bottom,top) location of the central obstacle
    playerNum : int
        1 or 2 -- who's turn it is to shoot
 
    """    
    plt.clf()
    drawBox(tank1box, tank1Color)
    drawBox(tank2box, tank2Color)
    drawBox(obstacleBox,obstacleColor)
    s = 'Player ' + str(playerNum) + "'s " + 'turn: '
    plt.title(s)
    plt.xlim(0,100)
    plt.ylim(0,100)
    showWindow() #this makes the figure window show up

def oneTurn (tank1box, tank2box, obstacleBox, playerNum, g = 9.8):   
    """
    parameters
    ----------
    tank1box : tuple
        (left,right,bottom,top) location of player1's tank
    tank2box : tuple
        (left,right,bottom,top) location of player1's tank
    obstacleBox : tuple
        (left,right,bottom,top) location of the central obstacle
    playerNum : int
        1 or 2 -- who's turn it is to shoot
     g : float 
        accel due to gravity (default 9.8)
    returns
    -------
    int
        code 0 = miss, 1 or 2 -- that player won
    
    clears figure
    draws tanks and obstacles as boxes
    prompts player for velocity and angle
    displays trajectory (shot originates from center of tank)
    returns 0 for miss, 1 or 2 for victory
    """
    total = 0
    while total== 0:
        if playerNum == 1:
            plt.clf()
            drawBoard(tank1box, tank2box, obstacleBox, 1)
            v = getNumberInput('Enter Player 1 velocity > ')
            a = getNumberInput('Enter angle > ')
            centerx = (tank1box[1]-tank1box[0])/2 + tank1box[0]
            centery = (tank1box[3]-tank1box[2])/2 + tank1box[2]
            shot = tankShot(tank2box, obstacleBox,centerx, centery,v,a)
            if shot == 0:
                print('You missed')
                playerNum = 2
            else:
                print('You won')
                total == 1
        if playerNum == 2:
            plt.clf()
            drawBoard(tank1box, tank2box, obstacleBox, 2)
            v = getNumberInput('Enter Player 2 velocity > ')
            a = getNumberInput('Enter angle > ')
            centerx = (tank2box[1]-tank2box[0])/2 + tank2box[0]
            centery = (tank2box[3]+tank2box[2])/2 + tank2box[2]
            shot = tankShot(tank1box, obstacleBox,centerx, centery,v,a)
            if shot == 0:
                print('You missed')
                playerNum = 1
            else:
                print('You won!')
                total == 1
def playGame(tank1box, tank2box, obstacleBox, g = 9.8):
    """
    parameters
    ----------
    tank1box : tuple
        (left,right,bottom,top) location of player1's tank
    tank2box : tuple
        (left,right,bottom,top) location of player1's tank
    obstacleBox : tuple
        (left,right,bottom,top) location of the central obstacle
    playerNum : int
        1 or 2 -- who's turn it is to shoot
     g : float 
        accel due to gravity (default 9.8)
    """
    playerNum = 1
    drawBoard(tank1box, tank2box, obstacleBox, playerNum)
    oneTurn(tank1box,tank2box, obstacleBox, playerNum)
    
    
    
        
##### functions provided to you #####
def getNumberInput (prompt, validRange = [-np.Inf, np.Inf]):
    """displays prompt and converts user input to a number
    
       in case of non-numeric input, re-prompts user for numeric input
       
       Parameters
       ----------
           prompt : str
               prompt displayed to user
           validRange : list, optional
               two element list of form [min, max]
               value entered must be in range [min, max] inclusive
        Returns
        -------
            float
                number entered by user
    """
    while True:
        try:
            num = float(input(prompt))
        except Exception:
            print ("Please enter a number")
            continue
        else:
            if (num >= validRange[0] and num <= validRange[1]):
                return num
            else:
                print ("Please enter a value in the range [", validRange[0], ",", validRange[1], ")") #Python 3 sytanx
    return num    

def showWindow():
    """
    shows the window -- call at end of drawBoard and tankShot
    """
    plt.draw()
    plt.pause(0.001)
    plt.show()


def drawBox(box, color):
    """
    draws a filled box in the current axis
    parameters
    ----------
    box : tuple
        (left,right,bottom,top) - extents of the box
    color : str
        color to fill the box with, e.g. 'b'
    """    
    x = (box[0], box[0], box[1], box[1])
    y = (box[2], box[3], box[3], box[2])
    ax = plt.gca()
    ax.fill(x,y, c = color)
    

def endTrajectoryAtIntersection (x,y,box):
    """
    portion of trajectory prior to first intersection with box
    
    paramaters
    ----------
    x,y : np array type
        position to check
    box : tuple
        (left,right,bottom,top)
    
    returns
    ----------
    (x,y) : tuple of np.array of floats
        equal to inputs if (x,y) does not intersect box
        otherwise returns the initial portion of the trajectory
        up until the point of intersection with the box
    """
    i = firstInBox(x,y,box)
    if (i < 0):
        return (x,y)
    return (x[0:i],y[0:i])


##### fmain -- edit box locations for new games #####
def main():
    tank1box = [10,15,0,5]
    tank2box = [90,95,0,5]
    obstacleBox = [40,60,0,50]
    playGame(tank1box, tank2box, obstacleBox)
    

#don't edit the lines below;
if __name__== "__main__":
    main()  
        
    