#!/usr/bin/python
# -*- coding: utf-8 -*-
u"""
@brief: Path Planning Sample Code with Randamized Rapidly-Exploring Random Trees (RRT) 

@author: AtsushiSakai

@license: MIT

"""

import random
import math
import copy
from scipy import misc
import glob
import numpy as np
import matplotlib
import subprocess


iframe = 0
donothing = False


def save_frame():
    """
    Save a frame for movie
    """
    import matplotlib.pyplot as plt
    donothing = False
    if not donothing:
        global iframe
        plt.savefig("recoder" + '{0:04d}'.format(iframe) + '.png')
        iframe += 1

def save_last_frame():
    """
    Save a frame for movie
    """
    import matplotlib.pyplot as plt


    plt.savefig("last_frame" + '.png')


def save_movie(fname, d_pause):
    """
    Save movie as gif
    """
    import subprocess
    donothing = False

    if not donothing:
        cmd = "convert -delay " + str(int(d_pause * 100)) + \
            " recoder*.png " + fname
        subprocess.call(cmd, shell=True)
        cmd = "rm recoder*.png"
        subprocess.call(cmd, shell=True)

class RRT():
    u"""
    Class for RRT Planning
    """

    def __init__(self, start, goal, obstacleList,randArea,expandDis=20,goalSampleRate=5,maxIter=300):
        u"""
        Setting Parameter

        start:Start Position [x,y]
        goal:Goal Position [x,y]
        obstacleList:obstacle Positions [[x,y,size],...]
        randArea:Ramdom Samping Area [min,max]

        """
        self.start=Node(start[0],start[1])
        self.end=Node(goal[0],goal[1])
        self.minrand = randArea[0]
        self.maxrand = randArea[1]
        self.expandDis = expandDis
        self.goalSampleRate = goalSampleRate
        self.maxIter = maxIter

    def Planning(self,animation=True):
        u"""
        Pathplanning 

        animation: flag for animation on or off
        """

        self.nodeList = [self.start]
        while True:
            # Random Sampling
            if random.randint(0, 100) > self.goalSampleRate:
                rnd = [random.uniform(self.minrand, self.maxrand), random.uniform(self.minrand, self.maxrand)]
            else:
                rnd = [self.end.x, self.end.y]

            # Find nearest node
            nind = self.GetNearestListIndex(self.nodeList, rnd)
            # print(nind)

            # expand tree
            nearestNode =self.nodeList[nind]
            theta = math.atan2(rnd[1] - nearestNode.y, rnd[0] - nearestNode.x)

            newNode = copy.deepcopy(nearestNode)
            newNode.x += self.expandDis * math.cos(theta)
            newNode.y += self.expandDis * math.sin(theta)
            newNode.parent = nind

            if not self.__CollisionCheck(newNode, obstacleList):
                continue

            self.nodeList.append(newNode)

            # check goal
            dx = newNode.x - self.end.x
            dy = newNode.y - self.end.y
            d = math.sqrt(dx * dx + dy * dy)
            if d <= self.expandDis:
                print("Goal!!")
                break

            if animation:
                self.DrawGraph(rnd)

            
        path=[[self.end.x,self.end.y]]
        lastIndex = len(self.nodeList) - 1
        while self.nodeList[lastIndex].parent is not None:
            node = self.nodeList[lastIndex]
            path.append([node.x,node.y])
            lastIndex = node.parent
        print path
        return path

    def DrawGraph(self,rnd=None):
        import matplotlib.pyplot as plt
        plt.clf()
        if rnd is not None:
            plt.plot(rnd[0], rnd[1], "^k")
        for node in self.nodeList:
            if node.parent is not None:
                plt.plot([node.x, self.nodeList[node.parent].x], [node.y, self.nodeList[node.parent].y], "-g")
                #save_frame()  # save each frame
                plt.axis([0, 800, 0, 800])   ####################################### aqui
                plt.grid(True)
        for (x,y,size) in obstacleList:
            self.PlotCircle(x,y,size)

        plt.plot(self.start.x, self.start.y, "xr")
        plt.plot(self.end.x, self.end.y, "xr")
        #plt.axis([0, 800, 0, 800])
        plt.grid(True)
        plt.pause(0.001)

    def PlotCircle(self,x,y,size):
        deg=range(0,360,5)
        deg.append(0)
        xl=[x+size*math.cos(math.radians(d)) for d in deg]
        yl=[y+size*math.sin(math.radians(d)) for d in deg]
        plt.plot(xl, yl, "-k")

    def GetNearestListIndex(self, nodeList, rnd):
        dlist = [(node.x - rnd[0]) ** 2 + (node.y - rnd[1]) ** 2 for node in nodeList]
        minind = dlist.index(min(dlist))
        return minind

    def __CollisionCheck(self, node, obstacleList):

        for (ox, oy, size) in obstacleList:
            dx = ox - node.x
            dy = oy - node.y
            d = math.sqrt(dx * dx + dy * dy)
            if d <= size:
                return False  # collision

        return True  # safe

class Node():
    u"""
    RRT Node
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None


def GetPathLength(path):
    l = 0
    for i in range(len(path) - 1):
        dx = path[i + 1][0] - path[i][0]
        dy = path[i + 1][1] - path[i][1]
        d = math.sqrt(dx * dx + dy * dy)
        l += d

    return l


def GetTargetPoint(path, targetL):
    l = 0
    ti = 0
    lastPairLen = 0
    for i in range(len(path) - 1):
        dx = path[i + 1][0] - path[i][0]
        dy = path[i + 1][1] - path[i][1]
        d = math.sqrt(dx * dx + dy * dy)
        l += d
        if l >= targetL:
            ti = i-1
            lastPairLen = d
            break

    partRatio = (l - targetL) / lastPairLen
    #  print(partRatio)
    #  print((ti,len(path),path[ti],path[ti+1]))

    x = path[ti][0] + (path[ti + 1][0] - path[ti][0]) * partRatio
    y = path[ti][1] + (path[ti + 1][1] - path[ti][1]) * partRatio
    #  print((x,y))

    return [x, y, ti]


def LineCollisionCheck(first, second, obstacleList):
    # Line Equation

    x1=first[0]
    y1=first[1]
    x2=second[0]
    y2=second[1]

    try:
        a=y2-y1
        b=-(x2-x1)
        c=y2*(x2-x1)-x2*(y2-y1)
    except ZeroDivisionError:
        return False

    #  print(first)
    #  print(second)

    for (ox,oy,size) in obstacleList:
        d=abs(a*ox+b*oy+c)/(math.sqrt(a*a+b*b))
        #  print((ox,oy,size,d))
        if d<=(size):
            #  print("NG")
            return False

    #  print("OK")

    return True  # OK


def PathSmoothing(path, maxIter, obstacleList):
    #  print("PathSmoothing")

    l = GetPathLength(path)

    for i in range(maxIter):
        # Sample two points
        pickPoints = [random.uniform(0, l), random.uniform(0, l)]
        pickPoints.sort()
        #  print(pickPoints)
        first = GetTargetPoint(path, pickPoints[0])
        #  print(first)
        second = GetTargetPoint(path, pickPoints[1])
        #  print(second)

        if first[2]<=0 or second[2]<=0:
            continue

        if (second[2]+1) > len(path):
            continue

        if second[2]==first[2]:
            continue

        # collision check
        if not LineCollisionCheck(first, second, obstacleList):
            continue

        #Create New path
        newPath=[]
        newPath.extend(path[:first[2]+1])
        newPath.append([first[0],first[1]])
        newPath.append([second[0],second[1]])
        newPath.extend(path[second[2]+1:])
        path=newPath
        l = GetPathLength(path)

    return path


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    #====Search Path with RRT====
    # Parameter

    for image_path in glob.glob("/home/osmaralg/Desktop/RompiBot/hola.png"):
        image = misc.imread(image_path)
    print (image.shape)
    print (image.dtype)



    png = []
    for image_path in glob.glob("/home/osmaralg/Desktop/RompiBot/hola.png"):
        png.append(misc.imread(image_path))

    im = np.asarray(png)

    ocupado = []
    print 'Importing done...', im.shape
    
    print im
    size = 800 # number of the pixels of the image
    resolution = 2  # step size pixel, if 1 evaluates every pixel if 4  every 4 pixels obstacle sambple
    obstaclesize = 10 # radious of the obstacle circle
    darkness = 127   # gray scale if 127 gray equals obstacle if 0 only black equals obstacle
    for j in range(0,size,resolution):
        for i in range(0,size,resolution):
            if im[0,i,j]<darkness:
                im[0,i,j]=obstaclesize
                istr=str(i)
                jstr=str(j)
            
            

                coordenada = j,i,obstaclesize
                ocupado.append(coordenada)
            else:
                im[0,i,j]=0
            #print "espacio libre ",i,j

    obstacleList = ocupado
    print "la lenght de ocupado es : "
    print len(ocupado)

    rrt=RRT(start=[800,800],goal=[400,400],randArea=[0,size],obstacleList=obstacleList)
    path=rrt.Planning(animation=False)
    #save_frame()  # save each frame
    # Draw final path
    rrt.DrawGraph()
    plt.plot([x for (x,y) in path], [y for (x,y) in path],'-r')
    plt.axis([0, size, 0, size])
    #Path smoothing
    maxIter=5
    smoothedPath = PathSmoothing(path, maxIter, obstacleList)
    plt.plot([x for (x,y) in smoothedPath], [y for (x,y) in smoothedPath],'-b')

    plt.axis([0, size, 0, size])
    plt.grid(True)
    plt.axis([0, size, 0, size])
    #plt.pause(0.001)  # Need for Mac
    #save_movie("animation.gif", 0.1)
    plt.show()
