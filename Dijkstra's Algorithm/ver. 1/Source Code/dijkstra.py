#-------------------------------------------------------------------------------
# Name:        DijKstra Algorithm Visualizer
# Purpose:     Software Engineering Project
#
# Author:      Prateek Kumar Jain
#
# Created:     29-03-2014
# Copyright:   (c) Prateek 2014
#-------------------------------------------------------------------------------

import pygame,sys
from heapq import *

# initializes pygame
pygame.init()
# Size of the screen
DISPLAY_SIZE = (800,600)
# size of each block in grid
BLOCK_SIZE = 25
# maximum number of nodes allowed
MAX_NODES = 10
# background color
BG_COLOR = (245,245,245)

# Grid class that places a grid on screen
class Grid:
    def __init__(self, _screen, _color):
        self.gridList = []
        self.color = _color
        self.screen = _screen
        self.grid()

    def grid(self):
        x1,y1,x2,y2 = 0,0,0,DISPLAY_SIZE[1]
        for i in range(DISPLAY_SIZE[0]/BLOCK_SIZE+1):
            self.gridList.append([(x1,y1),(x2,y2)])
            x1 = x1+BLOCK_SIZE
            x2 = x2+BLOCK_SIZE
        x1,y1,x2,y2 = 0,0,DISPLAY_SIZE[0],0
        for i in range(DISPLAY_SIZE[1]/BLOCK_SIZE):
            self.gridList.append([(x1,y1),(x2,y2)])
            y1 = y1+BLOCK_SIZE
            y2 = y2+BLOCK_SIZE

    def Render(self):
        for item in self.gridList:
            pygame.draw.aaline(self.screen,self.color,item[0],item[1])

# Class that displays the co-ordinates of mouse position
class MousePosText:
    def __init__(self, _screen, _color, _textSize):
        self.color = _color
        self.screen = _screen
        self.textSize = _textSize
        self.font = pygame.font.SysFont("comicsansms", self.textSize)
    # takes mouse position as argument and displays it
    def Render(self,pos):
        self.screen.blit(self.font.render(str(pos[0]/BLOCK_SIZE+1)+','+str(pos[1]/BLOCK_SIZE+1), True,self.color),(pos[0]+5,pos[1]+5))


# A Edge class
class Edge:
    def __init__(self, _color, _pos1, _pos2, _screen):
        self.pos1 = _pos1
        self.pos2 = _pos2
        self.color = _color
        self.screen = _screen
        self.font = pygame.font.SysFont("comicsansms", 15)
    # Thise spwans a edge on screen
    def Render(self):
        pygame.draw.aaline(self.screen,self.color,self.pos1,self.pos2)
        self.AddWeights()
    def AddWeights(self):
        dist = ((self.pos1[0]-self.pos2[0])**2 + (self.pos1[1]-self.pos2[1])**2)**(0.5)
        self.screen.blit(self.font.render(str(int(dist)), True,(10,10,10)),((self.pos1[0]+self.pos2[0])/2-5,(self.pos1[1]+self.pos2[1])/2-5))


# A Node class
class Node:
    def __init__(self, _color, _pos, _size, _label, _screen):
        self.pos = _pos
        self.size = _size
        # keeps list of edges connected to node
        self.edgeList = []
        self.nodeList = []
        self.label = _label
        self.color = _color
        self.screen = _screen
        self.font = pygame.font.SysFont("comicsansms", 20)
    # This spwans a node on screen
    def Render(self):
        pygame.draw.circle(self.screen,(200,200,200),self.pos,self.size)
        pygame.draw.circle(self.screen,self.color,self.pos,self.size-3)
        self.screen.blit(self.font.render(str(self.label), True,(0,128,0)),(self.pos[0]-8,self.pos[1]-8))
        # calls Edge.Render() for each edge connected to a node
        for edge in self.edgeList:
            edge.Render()
    # Appends a node that is connected to this node
    def AddNode(self,_idx):
            self.nodeList.append(_idx)
    # Appends an edge connected to node
    def AddEdge(self, _edge,_node):
        self.edgeList.append(_edge)
        self.AddNode(_node)
    # Checks if node already exist
    def IsNodeThere(self,_vrtx):
        for idx in self.nodeList:
            if idx==_vrtx:
                return True
        return False



def dijkstra(source,v,screen,G):
    font = pygame.font.SysFont("comicsansms", 20)
    fontdist = pygame.font.SysFont("comicsansms", 20)
    #screen.blit(font.render("Click on Source Node", True,(0,128,0)),(275,25))
    vis = {}
    dist = []
    for i in range(len(v)):
        vis[i] = 0
        dist.append("INF")
    vis[source] = 1
    dist[source] = 0;
    Q = []
    temp = None
    heappush(Q,(0,source))
    itr = 10
    while(len(Q)!=0):
        temp = heappop(Q)
        v1 = temp[1]
        pos1 = v[v1].pos
        screen.fill(BG_COLOR)
        G.Render()
        #screen.blit(font.render(str(v1+1), True,(0,128,0)),(675,25+itr))
        screen.blit(font.render("(C) Prateek Kumar Jain(pikkupr@yahoo.com)", True,(0,128,0)),(225,550))
        v[v1].color =(255,255,0)
        for i in range(len(v)):
            screen.blit(fontdist.render(str(dist[i]), True,(204,0,0)),(v[i].pos[0]+10,v[i].pos[1]+10))
            v[i].Render()
        pygame.time.delay(2500)
        pygame.display.flip()
        for i in range(len(v[v1].nodeList)):
            v2 = v[v1].nodeList[i]
            pos2 = v[v2].pos
            newdist = temp[0] + (abs(pos1[0]-pos2[0])**2 + abs(pos1[1]-pos2[1])**2)**0.5
            newdist = int(newdist)
            if dist[v2]=="INF" or dist[v2]>newdist:
                dist[v2] = newdist
            if vis[v2]==0:
                heappush(Q,(newdist,v2))
                vis[v2] = 1
        v[v1].color =(155,155,155)
        itr +=30
    v[v1].color =(155,155,155)
    v[v1].Render()
    pygame.display.flip()

def main():
    # display screen of pygame
    screen = pygame.display.set_mode(DISPLAY_SIZE)
    screen.fill(BG_COLOR)

    # initializes grid
    G = Grid(screen,(158,158,158))

    # keeps mouse position
    mousePos = None

    # initializes mouse co-ordinates displayer
    M = MousePosText(screen,(100,100,100),15)

    nodeCount = 0
    renderList = []
    target = None
    runAlgo = False
    nodeStatus = 0
    vertex1 = None
    vertex2 = None
    setEdge = False
    #vrtxIndx = None
    iterator = None
    mouseDown = False
    mousePressed = False
    mouseReleased = False
    font = pygame.font.SysFont("comicsansms", 20)
    # spwans an "set edge" button, which when pressed allows adding edges
    # but restricts adding and changing position of nodes
    setEdgePos = (25,25)
    setEdgeNode = Node((145,25,100),setEdgePos,30,"Set Edge",screen)

    # Pygame state controller
    Running = True
    while(Running):
        mousePos = pygame.mouse.get_pos()
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                Running = False
                break
            # checks if mouse is pressed(and holded)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePressed = True
                mouseDown = True
            # checks if mouse is released
            if event.type == pygame.MOUSEBUTTONUP:
                mouseReleased = True
                mouseDown = False

        if mousePressed == True:

            # checks if mouse pressed on some object or not
            iterator = 0
            for item in renderList:
                if (mousePos[0]+item.size>=(item.pos[0]-item.size) and mousePos[0]-item.size<=(item.pos[0]+item.size) and
                    mousePos[1]+item.size>=(item.pos[1]-item.size) and mousePos[1]-item.size<=(item.pos[1]+item.size) ):
                    target = item
                    break
                iterator += 1

            # stops editing node and allows to add edges
            if (mousePos[0]>=(setEdgePos[0]-30) and mousePos[0]<=(setEdgePos[0]+30) and mousePos[1]>=(setEdgePos[1]-30) and mousePos[1]<=(setEdgePos[1]+30)):
                if setEdge is not True :
                    setEdge = True
                    setEdgeNode.color = (245,245,220)
                    setEdgeNode.label = "Run Algo"
                else:
                    runAlgo = True
                    setEdgeNode.label = "Executing .. "
                    setEdgeNode.color = (245,245,245)
                    break

            # adds a new node if number of nodes are < MAX_NODES
            if target is None and nodeCount<MAX_NODES and setEdge is not True:
                target = Node((145,25,100),mousePos,20,len(renderList)+1,screen)
                renderList.append(target)
                nodeCount += 1

            # undo add edge operation if clicked on empty area
            if target is None and setEdge is True and nodeStatus !=0:
                nodeStatus = 0
                vertex1.color = (145,25,100)
                vertex1 = None
                vrtxIndx = None

            # controls add an edge operation
            if target is not None and setEdge is True:
                # if state is 0 means 1st node is selected
                if nodeStatus == 0:
                    nodeStatus = 1
                    vertex1 = target
                    vertex1.color = (255,255,0)
                # state 1 means 2nd node is selected
                elif nodeStatus == 1:
                    nodeStatus = 0
                    vertex1.color = (145,25,100)
                    # this is to avoid adding same edges over n over again
                    if vertex1.IsNodeThere(iterator) is False:
                        t = Edge((0,153,0),vertex1.pos,target.pos,screen);
                        vertex1.AddEdge(t,iterator)
                        vertex1 = None

        # checks and allows changing of position of a node
        if mouseDown and target is not None and setEdge is not True:
            flag = 1
            # checks if node is not being moved on existing object
            for item in renderList:
                if(item==target):
                    pass
                elif (mousePos[0]+item.size>=(item.pos[0]-item.size) and mousePos[0]-item.size<=(item.pos[0]+item.size) and
                      mousePos[1]+item.size>=(item.pos[1]-item.size) and mousePos[1]-item.size<=(item.pos[1]+item.size)):
                        flag = 0
                        break
            if(flag==1):
                target.pos = mousePos

        if mouseReleased:
            target = None
        mousePressed = False
        mouseReleased = False

        # Render functions called
        screen.fill(BG_COLOR)
        G.Render()
        setEdgeNode.Render()
        for item in renderList:
            item.Render()
        M.Render(mousePos)
        if nodeStatus == 1:
            pygame.draw.aaline(screen,(10,122,162),vertex1.pos,mousePos)
        screen.blit(font.render("(C) Prateek Kumar Jain(pikkupr@yahoo.com)", True,(0,128,0)),(225,550))
        pygame.display.flip()

    if Running is True:
        flag = False
        screen.blit(font.render("Click on Source Node", True,(0,128,0)),(275,25))
        screen.blit(font.render("(C) Prateek Kumar Jain(pikkupr@yahoo.com)", True,(0,128,0)),(225,550))
        pygame.display.flip()
        target = None
        while flag is False and Running is True:
            mousePos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Running = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    iterator = 0
                    for item in renderList:
                        if (mousePos[0]+item.size>=(item.pos[0]-item.size) and mousePos[0]-item.size<=(item.pos[0]+item.size) and
                            mousePos[1]+item.size>=(item.pos[1]-item.size) and mousePos[1]-item.size<=(item.pos[1]+item.size) ):
                            target = item
                            break
                        iterator += 1
                    if target is not None:
                        flag = True
    if Running is True:
        dijkstra(iterator,renderList,screen,G)
    while Running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = False
                break
    pygame.quit()


if __name__ == '__main__':
    main()
