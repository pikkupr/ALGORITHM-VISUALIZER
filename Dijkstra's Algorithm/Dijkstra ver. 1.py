#-------------------------------------------------------------------------------
# Name:        DijKstra Algorithm Visualizer
# Purpose:     Project
#
# Author:      Prateek Kumar Jain
#
# Created:     29-03-2014
# Copyright:   (c) Prateek 2014
#-------------------------------------------------------------------------------

import pygame,sys

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
    # Thise spwans a edge on screen
    def Render(self):
        pygame.draw.aaline(self.screen,self.color,self.pos1,self.pos2)

# A Node class
class Node:
    def __init__(self, _color, _pos, _size, _label, _screen):
        self.pos = _pos
        self.size = _size
        # keeps list of edges connected to node
        self.edgeList = []
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
    # Appends an edge connected to node
    def AddEdge(self, _edge):
        self.edgeList.append(_edge)

def main():
    # display screen of pygame
    screen = pygame.display.set_mode(DISPLAY_SIZE)
    screen.fill(BG_COLOR)

    # initializes grid
    G = Grid(screen,(0,0,0))

    # keeps mouse position
    mousePos = None

    # initializes mouse co-ordinates displayer
    M = MousePosText(screen,(100,100,100),15)

    nodeCount = 0
    renderList = []
    target = None
    nodeStatus = 0
    vertex1 = None
    vertex2 = None
    setEdge = False
    mouseDown = False
    mousePressed = False
    mouseReleased = False

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
            for item in renderList:
                if (mousePos[0]+item.size>=(item.pos[0]-item.size) and mousePos[0]-item.size<=(item.pos[0]+item.size) and
                    mousePos[1]+item.size>=(item.pos[1]-item.size) and mousePos[1]-item.size<=(item.pos[1]+item.size) ):
                    target = item
                    break

            # stops editing node and allows to add edges
            if setEdge is not True and (mousePos[0]>=(setEdgePos[0]-30) and mousePos[0]<=(setEdgePos[0]+30) and
               mousePos[1]>=(setEdgePos[1]-30) and mousePos[1]<=(setEdgePos[1]+30)):
                setEdge = True
                setEdgeNode.color = (245,245,220)

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
                    t = Edge((0,0,0),vertex1.pos,target.pos,screen);
                    vertex1.AddEdge(t)

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
        pygame.display.flip()
    pygame.quit()

if __name__ == '__main__':
    main()
