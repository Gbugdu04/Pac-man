import numpy as np
import tkinter as tk
from PIL import Image,ImageTk
import json
import random

root=tk.Tk()
#####https://itnext.io/how-to-create-pac-man-in-python-in-300-lines-of-code-or-less-part-1-288d54baf939
ascii_maze=[                   
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "X            XX            X",
            "X XXXX XXXXX XX XXXXX XXXX X",
            "X XXXX XXXXX XX XXXXX XXXX X",
            "X XXXX XXXXX XX XXXXX XXXX X",
            "X                          X",
            "X XXXX XX XXXXXXXX XX XXXX X",
            "X XXXX XX XXXXXXXX XX XXXX X",
            "X      XX    XX    XX      X",
            "XXXXXX XXXXX XX XXXXX XXXXXX",
            "XXXXXX XXXXX XX XXXXX XXXXXX",
            "XXXXXX XX          XX XXXXXX",
            "XXXXXX XX XXXXXXXX XX XXXXXX",
            "XXXXXX XX XXXXXXXX XX XXXXXX",
            "          XXXXXXXX          ",
            "XXXXXX XX XXXXXXXX XX XXXXXX",
            "XXXXXX XX XXXXXXXX XX XXXXXX",
            "XXXXXX XX          XX XXXXXX",
            "XXXXXX XX XXXXXXXX XX XXXXXX",
            "XXXXXX XX XXXXXXXX XX XXXXXX",
            "X            XX            X",
            "X XXXX XXXXX XX XXXXX XXXX X",
            "X XXXX XXXXX XX XXXXX XXXX X",
            "X   XX                XX   X",
            "XXX XX XX XXXXXXXX XX XX XXX",
            "XXX XX XX XXXXXXXX XX XX XXX",
            "X      XX    XX    XX      X",
            "X XXXXXXXXXX XX XXXXXXXXXX X",
            "X XXXXXXXXXX XX XXXXXXXXXX X",
            "X                          X",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        ]
class main_menu():
    def __init__(self,ascii_maze):
        
        self.ascii_maze=ascii_maze
        self.col=len(list(self.ascii_maze[0]))
        self.line=len(list(self.ascii_maze))
        self.matrix=np.zeros((self.line,self.col))
        for i in range(self.line):
            for j in range(self.col):
                if self.ascii_maze[i][j]==" ":
                    self.matrix[i][j]=1
        self.create_adjacency()
    
    def create_adjacency(self):
        self.adj={}
        
        self.adj[(14,self.col-1)]=[(14,0),(14,26)] 
        self.adj[(14,0)]=[(14,self.col-1),(14,1)]
        
        for i in range(1,self.line):
            for j in range(1,self.col):
                if self.matrix[i][j]==1:
                    self.adj[(i,j)]=[]
                    if self.matrix[i-1][j]==1:
                        self.adj[(i,j)].append((i-1,j))
                        
                    if i+1<self.line:
                        if self.matrix[i+1][j]==1:
                            self.adj[(i,j)].append((i+1,j))
                        
                    if self.matrix[i][j-1]==1:
                        self.adj[(i,j)].append((i,j-1))
                        
                    if j+1<self.col:   
                        if self.matrix[i][j+1]==1:
                            self.adj[(i,j)].append((i,j+1))
                            
                            
MENU=main_menu(ascii_maze)
adj=MENU.adj

class labyrinthe(tk.Canvas):
    def __init__(self):
        super().__init__(width=550,height=610,background='black',highlightthickness=0)
        
        self.w=560
        self.h=620
        self.pac_pos=(40,20)
        self.direction="Right"
        self.MOVE_INCREMENT=0
      
        self.enemy_pos=(500,580)
        self.previous_enemy_pos = self.enemy_pos 
        
        self.col=len(list(ascii_maze[0]))
        self.line=len(list(ascii_maze))
        self.matrix=np.zeros((self.line,self.col))
        
        
        
        
        for i in range(self.line):
            for j in range(self.col):
                if ascii_maze[i][j]==" ":
                    self.matrix[i][j]=1
                    
                    
                    
        self.list_of_coordinates=[(i,j) for i in range(0,self.w,20) for j in range(0,self.h,20)]
        self.load_assets()
        self.create_labyrinthe()
        
        self.B=adj[(self.enemy_pos[1]//20,self.enemy_pos[0]//20)]
        self.create_pacr()
        self.bind_all("<Key>",self.on_key_press)
        self.bind_all("<KeyRelease>",self.on_key_release)
        self.perform_actions1()
        self.create_enemy()
        # self.follow_pac()
        self.move_randomly_or_follow()
        # self.draw_path()   #####FONCTION POUR TESTER LE PARCOUR DE GRAPHE
        
        
    def load_assets(self):
        self.wall_image=Image.open("pixel_art//wall.png")
        
        self.wall_body=ImageTk.PhotoImage(self.wall_image)
        
        self.wall2_image=Image.open("pixel_art//wall2.png")
        self.wall2_body=ImageTk.PhotoImage(self.wall2_image)
        
        self.pac_image=Image.open("pixel_art//pacman.png")
        self.pac_body=ImageTk.PhotoImage(self.pac_image)
        
        self.enemy_image=Image.open("pixel_art//enemy1.png")
        self.enemy_body=ImageTk.PhotoImage(self.enemy_image)
    def create_labyrinthe(self):
        for i,j in self.list_of_coordinates:
            if j//20<31 and i//20 <28:
                if self.matrix[j//20,i//20]==0:
                    self.create_image(i,j,image=self.wall_body,tag='wall')
            
    
    def BFS(self,depart, arrivee,adj):
       a_explorer = [depart]
       deja_collectes = [depart]
       self.chemins = {depart: [depart]}

       while len(a_explorer) != 0:
           courant = a_explorer.pop(0)

           if courant == arrivee:
               return self.chemins[arrivee]

           if courant in adj:
               for sommet in adj[courant]:
                   if sommet not in deja_collectes:
                       a_explorer.append(sommet)
                       deja_collectes.append(sommet)
                       self.chemins[sommet] = self.chemins[courant] + [sommet]
       return None
   
    def draw_path(self):
        for pos in self.BFS((1,2),(29,25)):
            self.create_image(20*pos[1],20*pos[0],image=self.wall2_body,tag='wall2')
        
        
    def create_pacr(self):
        self.create_image(*self.pac_pos,image=self.pac_body,tag='pacman')
    
    def move_pac(self):
        x_pos=self.pac_pos[0]
        y_pos=self.pac_pos[1]
        
        if self.direction=='Right':
            if (y_pos//20,(x_pos//20)+1) in adj[(y_pos//20,x_pos//20)]:
                 x_pos=x_pos+self.MOVE_INCREMENT
        if self.direction=='Up':
            if (y_pos//20 -1,(x_pos//20)) in adj[(y_pos//20,x_pos//20)]:
                 y_pos=y_pos-self.MOVE_INCREMENT
        if self.direction=="Down":
            if (y_pos//20 +1,(x_pos//20)) in adj[(y_pos//20,x_pos//20)]:
                y_pos=y_pos+self.MOVE_INCREMENT
        if self.direction=='Left':
            if (y_pos//20 ,(x_pos//20)-1) in adj[(y_pos//20,x_pos//20)]:
                x_pos=x_pos-self.MOVE_INCREMENT
        
        self.pac_pos=(x_pos,y_pos)
        
        self.coords('pacman',self.pac_pos)
    def on_key_release(self,event):
        self.MOVE_INCREMENT=0
         
    def on_key_press(self,event):
        self.MOVE_INCREMENT=20
        new_order=event.keysym
        all_directions=["Right","Up","Left","Down"]
        if new_order in all_directions:
            self.direction=new_order
        
    def perform_actions1(self):
        self.move_pac()
        
        self.after(80, self.perform_actions1)
        
    def create_enemy(self):
        self.create_image(*self.enemy_pos,image=self.enemy_body,tag='enemy')
        
    # def follow_pac(self):
    #     L=self.BFS((self.enemy_pos[1]//20,self.enemy_pos[0]//20),(self.pac_pos[1]//20,self.pac_pos[0]//20))
    #     if L:
    #      if len(L)<15:
    #         self.enemy_pos=(L[1][1]*20,L[1][0]*20)
    #         self.coords('enemy',(self.enemy_pos[0],self.enemy_pos[1]))
    #         L.pop(0)
    #     self.after(140,self.follow_pac)
    
        
    def move_randomly_or_follow(self):
        L=self.BFS((self.enemy_pos[1]//20,self.enemy_pos[0]//20),(self.pac_pos[1]//20,self.pac_pos[0]//20),adj)
        if L:
         if len(L)<15:
            self.enemy_pos=(L[1][1]*20,L[1][0]*20)
            self.coords('enemy',(self.enemy_pos[0],self.enemy_pos[1]))
            L.pop(0)   
         else:
            a,b=random.choice(self.B)
            self.coords('enemy',b*20,a*20)
            self.B=adj[(a,b)]
            if (self.enemy_pos[1]//20,self.enemy_pos[0]//20) in self.B:
                self.B.remove((self.enemy_pos[1]//20,self.enemy_pos[0]//20))
            self.enemy_pos=(b*20,a*20)
        self.after(140,self.move_randomly_or_follow)
     
         
root.title("pacman with Tkinter")
root.resizable(False,False) 
board=labyrinthe()
board.pack()

root.mainloop()
