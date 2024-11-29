import pygame
import sys
import math
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os

screen = pygame.display.set_mode((600, 600))

screencolor = [224, 224, 224]
screen.fill(screencolor)
pygame.display.set_caption("DEV19")

class point:
    def __init__(personal, x, y):
        personal.i = x
        personal.j = y
        personal.f = 0
        personal.g = 0
        personal.h = 0
        personal.adjacents = []
        personal.previous = None
        personal.obs = False
        personal.closed = False
        personal.value = 1

    def display(personal, color, st):
        if personal.closed == False :
            pygame.draw.rect(screen, color, (personal.i * w, personal.j * h, w, h), st)
            pygame.display.update()
    def movement(personal, color, st):
        pygame.draw.rect(screen, color, (personal.i * w, personal.j * h, w, h), st)
        pygame.display.update()
    def addadjacents(personal, grid):
        i = personal.i
        j = personal.j
        if i < cols-1 and grid[personal.i + 1][j].obs == False:
            personal.adjacents.append(grid[personal.i + 1][j])
        if i > 0 and grid[personal.i - 1][j].obs == False:
            personal.adjacents.append(grid[personal.i - 1][j])
        if j < row-1 and grid[personal.i][j + 1].obs == False:
            personal.adjacents.append(grid[personal.i][j + 1])
        if j > 0 and grid[personal.i][j - 1].obs == False:
            personal.adjacents.append(grid[personal.i][j - 1])

cols = 30
grid = [0 for i in range(cols)]

row = 30

openSet = []
closedSet = []

red = (255, 0, 0)
purple = (153,51, 255)
blue = (0, 102, 204)

bordercolor = (0, 102,51)
w = 600 / cols
h = 600 / row
cameFrom = []

boxborder= (0,204,102)


for i in range(cols):
    grid[i] = [0 for i in range(row)]


for i in range(cols):
    for j in range(row):
        grid[i][j] = point(i, j)


start = grid[7][5]
end = grid[20][16]

for i in range(cols):
    for j in range(row):
        grid[i][j].display((boxborder), 1)

for i in range(0,row): 
    grid[cols-1][i].obs = True
    grid[cols-1][i].display(bordercolor, 0)
    grid[i][row-1].display(bordercolor, 0)
    grid[i][0].display(bordercolor, 0)
    grid[i][0].obs = True
    grid[i][row-1].obs = True
    grid[0][i].display(bordercolor, 0)
    grid[0][i].obs = True


def onsubmit():
    global start
    global end


    st = startBox.get().split(',')
    ed = endBox.get().split(',')
    start = grid[int(st[0])][int(st[1])]
    end = grid[int(ed[0])][int(ed[1])]
    window.quit()
    window.destroy()
    


window = Tk()
window.configure(background='black')
label = Label(window, text='ENTER Starting Points : x,y (must be between 1,1 and 29,29)',fg='white', bg='black')
startBox = Entry(window)
label1 = Label(window, text='ENTER Ending Points : x,y (must be between 1,1 and 29,29)',fg='white', bg='black')
endBox = Entry(window)
var = IntVar()
displaymovement = ttk.Checkbutton(window, text='Click for step by step demo', onvalue=1, offvalue=0, variable=var )
submit = Button(window, text='Enter',bg='blue', fg='white', command=onsubmit)


displaymovement.grid(columnspan=3, row=3)
submit.grid(columnspan=4, row=4)
label1.grid(row=1, pady=4)
endBox.grid(row=1, column=1, pady=3)
startBox.grid(row=0, column=1, pady=3)
label.grid(row=0, pady=4)

window.update()
mainloop()

def printSomething():
    
    button.destroy()
    label = Label(root, text= "(1)- First add obstacles between point using 'mouse press or the mouse drag'\n\n  (2)- Then Press the 'ENTER Key' once you are done adding obstacles.\n\n (close this Dialogue Box to Continue)")
    
    label.pack() 

root = Tk()

button = Button(root, text="Guidence \nClick HERE",bg='blue', fg='white', command=printSomething) 
button.pack()
root.mainloop()

pygame.init()
openSet.append(start)

def mousePress(x):
    t = x[0]
    w = x[1]
    g1 = t // (600 // cols)
    g2 = w // (600 // row)
    acess = grid[g1][g2]
    if acess != start and acess != end:
        if acess.obs == False:
            acess.obs = True
            acess.display((255, 255, 20), 0)

end.display((255, 127, 0), 0)
start.display((255, 127,0), 0)

loop = True
while loop:

    ev = pygame.event.get()
    for event in ev:

        if event.type == pygame.QUIT:
            pygame.quit()

        if pygame.mouse.get_pressed()[0]:
            try:
                pos = pygame.mouse.get_pos()
                mousePress(pos)
            except AttributeError:
                pass

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                loop = False
                break

for i in range(cols):
    for j in range(row):
        grid[i][j].addadjacents(grid)


def heurisitic(n, e):
    d = math.sqrt((n.i - e.i)**2 + (n.j - e.j)**2)
    
    return d

def main():
    end.display((255, 255, 255), 0)
    start.display((255, 255, 255), 0)
    if len(openSet) > 0:
        lowestIndex = 0
        for i in range(len(openSet)):
            if openSet[i].f < openSet[lowestIndex].f:
                lowestIndex = i

        current = openSet[lowestIndex]
        if current == end:
            print('done', current.f)
            start.display((255,255, 255),0)
            temp = current.f
            for i in range(round(current.f)):

                current.closed = False
                current.display((0,0,0), 0)
                current = current.previous
            end.display((255, 255, 255), 0)

            Tk().wm_withdraw()
            result = messagebox.showinfo('Program Finished', ('The shortest distance to find the route is' + str(temp) + ' blocks...\n\n DEV'))

            ag = True
            while ag:
                ev = pygame.event.get()
                for event in ev:
                    if event.type == pygame.KEYDOWN:
                        ag = False
            pygame.quit()

        openSet.pop(lowestIndex)
        closedSet.append(current)
        
        adjacents = current.adjacents
        for i in range(len(adjacents)):
            neighbor = adjacents[i]
            if neighbor not in closedSet:
                tempG = current.g + current.value
                if neighbor in openSet:
                    if neighbor.g > tempG:
                        neighbor.g = tempG
                else:
                    neighbor.g = tempG
                    openSet.append(neighbor)

            neighbor.h = heurisitic(neighbor, end)
            neighbor.f = neighbor.g + neighbor.h

            if neighbor.previous == None:
                neighbor.previous = current
    if var.get():
        for i in range(len(openSet)):
            openSet[i].display(purple, 0)

        for i in range(len(closedSet)):
            if closedSet[i] != start:
                closedSet[i].display(blue, 0)
    current.closed = True

while True:
    ev = pygame.event.poll()
    if ev.type == pygame.QUIT:
        pygame.quit()
    pygame.display.update()
    main()
