import numpy as np
import tkinter as tk
from PIL import Image,ImageTk
import json
import random
import copy
import time
from tkinter import PhotoImage


root=tk.Tk()

#####https://itnext.io/how-to-create-pac-man-in-python-in-300-lines-of-code-or-less-part-1-288d54baf939
def choix_labyrinthe():
        with open("dico_labyrinthe.json","r") as f:
            liste_tab = json.load(f)
            random_maze = random.choice(list(liste_tab.values()))
        return random_maze
ascii_maze = choix_labyrinthe()
class main_menu():
    def __init__(self, ascii_maze):
        
        self.ascii_maze= ascii_maze
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
        #self.adj[(14,27)]=[(14,0),(14,26)]
        # self.adj[(14,self.col-1)]=[(14,0),(14,26)]
        #self.adj[(14,0)]=[(14,self.col-1),(14,1)]
        
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
#adj[(14,27)]=[(14,0),(14,26)]
adj1=copy.deepcopy(adj)
adj2=copy.deepcopy(adj)

class labyrinthe(tk.Canvas):
    def __init__(self):
        super().__init__(width=20*len(list(ascii_maze[0])),height=20*len(list(ascii_maze)),background='black',highlightthickness=0)
        self.timer_label = tk.Label(self, text="Time: 0", font=("Arial", 16), bg="black", fg="white")
        self.create_window(275, 305, window=self.timer_label)
        self.start_time = time.time()
        self.col=len(list(ascii_maze[0]))
        self.line=len(list(ascii_maze))
        self.w=20*len(list(ascii_maze[0]))
        self.h=20*len(list(ascii_maze))
        self.pac_pos=(20,20)
        self.last_pac_pos=self.pac_pos
        self.direction="Right"
        self.MOVE_INCREMENT=0
        self.enemy_pos=(20,20*(self.col-2))
        self.ghost_pos=(20*(self.line-2),20*(self.col-2))
        self.radius=20
        self.matrix=np.zeros((self.line,self.col))
        for i in range(self.line):
            for j in range(self.col):
                if ascii_maze[i][j]==" ":
                    self.matrix[i][j]=1
        self.pac_is_dead=False    
        self.pac_won = False
        self.enemy1_frozen=False
        self.enemy2_frozen=False
        self.possess_gem=False
        self.data=[
            ['Name', 'Score' ],
            ['John', 25],
            ['Sarah', 30 ],
            ['Mike', 21 ]
        ]
        self.flakes_list=[1]
        self.score=0        
        self.available=[]
        self.list_of_coordinates=[(i,j) for i in range(0,self.w,20) for j in range(0,self.h,20)]
        self.load_assets()
        self.create_labyrinthe()
        self.B=adj[(self.enemy_pos[1]//20,self.enemy_pos[0]//20)].copy()
        self.K=adj2[(self.ghost_pos[1]//20,self.enemy_pos[0]//20)].copy()
        self.create_coins()
        self.create_pacr()
        self.bind_all("<Key>",self.on_key_press)
        self.bind_all("<KeyRelease>",self.on_key_release)
        self.perform_actions1()
        self.create_enemy()
        self.L=self.BFS((self.enemy_pos[1]//20,self.enemy_pos[0]//20),(self.pac_pos[1]//20,self.pac_pos[0]//20),adj)
        self.H=self.BFS((self.ghost_pos[1]//20,self.ghost_pos[0]//20),(self.pac_pos[1]//20,self.pac_pos[0]//20),adj2)
        if self.pac_is_dead==False and self.pac_won==False:
            self.move_randomly_or_follow()
            self.move_randomly_or_follow1()
        # self.draw_path()   #####FONCTION POUR TESTER LE PARCOUR DE GRAPHE
        self.coin_eaten()
      
        
        self.game_over()
        self.you_won()
    def load_assets(self):
        self.wall_image=Image.open("wall.png")
        self.wall_body=ImageTk.PhotoImage(self.wall_image)
        
        self.wall2_image=Image.open("wall2.png")
        self.wall2_body=ImageTk.PhotoImage(self.wall2_image)
        
        self.pac_image=Image.open("pacmanr.png")
        self.pac_body=ImageTk.PhotoImage(self.pac_image)
        
        self.pacleft_image=Image.open("pacman left.png")
        self.pacleft_body=ImageTk.PhotoImage(self.pacleft_image)
        
        self.pacup_image=Image.open("pacman up.png")
        self.pacup_body=ImageTk.PhotoImage(self.pacup_image)
        
        self.pacdown_image=Image.open("pacman down.png")
        self.pacdown_body=ImageTk.PhotoImage(self.pacdown_image)
        
        self.enemy_image=Image.open("enemy1.png")
        self.enemy_body=ImageTk.PhotoImage(self.enemy_image)
        
        self.coin_image=Image.open("coin2.png")
        self.coin_body=ImageTk.PhotoImage(self.coin_image)
        
        self.ghost_image=Image.open("ghost.png")
        self.ghost_body=ImageTk.PhotoImage(self.ghost_image)
        
        self.flakes1_image=Image.open("flakes1.png")
        self.flakes1_body=ImageTk.PhotoImage(self.flakes1_image)
        
        self.flakes2_image=Image.open("flakes2.png")
        self.flakes2_body=ImageTk.PhotoImage(self.flakes2_image)
        
        self.gem_image=Image.open("gem.png")
        self.gem_body=ImageTk.PhotoImage(self.gem_image)
        
        self.game_over_image=Image.open("GAME_OVER.png")
        self.game_over_body=ImageTk.PhotoImage(self.game_over_image)
        
        self.Victory_image=Image.open("victory (2).png")
        self.Victory_body=ImageTk.PhotoImage(self.Victory_image)
        
    def create_labyrinthe(self):
        for i,j in self.list_of_coordinates:
            if (j//20<self.line) and (i//20 <self.col) :
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
       if self.pac_is_dead==False and self.pac_won == False:
        if self.direction=="Right":  
            self.delete("pacman")
            self.create_image(*self.pac_pos,image=self.pac_body,tag='pacman')
        if self.direction=="Left":
            self.delete("pacman")
            self.create_image(*self.pac_pos,image=self.pacleft_body,tag='pacman')
        if self.direction=="Up":    
            self.delete("pacman")
            self.create_image(*self.pac_pos,image=self.pacup_body,tag='pacman')
        if self.direction=="Down":
            self.delete("pacman")
            self.create_image(*self.pac_pos,image=self.pacdown_body,tag='pacman')
        self.after(80,self.create_pacr)
            
    
    def move_pac(self):
      if self.pac_is_dead==False and self.pac_won == False:
        x_pos=self.pac_pos[0]
        y_pos=self.pac_pos[1]
        
        if self.direction=='Right':
            if (y_pos//20,(x_pos//20)+1) in adj1[(y_pos//20,x_pos//20)]:
                 x_pos=x_pos+self.MOVE_INCREMENT
        if self.direction=='Up':
            if (y_pos//20 -1,(x_pos//20)) in adj1[(y_pos//20,x_pos//20)]:
                 y_pos=y_pos-self.MOVE_INCREMENT
        if self.direction=="Down":
            if (y_pos//20 +1,(x_pos//20)) in adj1[(y_pos//20,x_pos//20)]:
                y_pos=y_pos+self.MOVE_INCREMENT
        if self.direction=='Left':
            if (y_pos//20 ,(x_pos//20)-1) in adj1[(y_pos//20,x_pos//20)]:
                x_pos=x_pos-self.MOVE_INCREMENT
        self.last_pac_pos=self.pac_pos
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
        self.update_timer()
        self.after(80, self.perform_actions1)
    def create_enemy(self):
        self.create_image(*self.enemy_pos,image=self.enemy_body,tag='enemy')
        self.create_image(*self.ghost_pos,image=self.ghost_body,tag='ghost')
        
    def move_randomly_or_follow(self):
        # fait le chemin entre l'ennemi et le pacman
        
        self.L=self.BFS((self.enemy_pos[1]//20,self.enemy_pos[0]//20),(self.pac_pos[1]//20,self.pac_pos[0]//20),adj1)
        
        if (len(self.L)>1 and self.pac_is_dead==False and self.pac_won==False):
            if len(self.L)<self.radius: # si le pacman est suffisament proche l'ennemi se rapproche
                if len(self.L) in [self.radius-1,self.radius-2]:
                    self.B=adj1[(self.enemy_pos[1]//20,self.enemy_pos[0]//20)].copy()
                self.enemy_pos=(self.L[1][1]*20,self.L[1][0]*20)
                self.coords('enemy',(self.enemy_pos[0],self.enemy_pos[1]))
                self.L.pop(0)
            else: # sinon l'ennemi bouge aléatoirement
                self.a,self.b=random.choice(self.B)
                self.coords('enemy',self.b*20,self.a*20)
                self.B=adj1[(self.a,self.b)].copy()
                if (self.enemy_pos[1]//20,self.enemy_pos[0]//20) in self.B:
                    self.B.remove((self.enemy_pos[1]//20,self.enemy_pos[0]//20))
                self.enemy_pos=(self.b*20,self.a*20)
        elif len(self.L)<=1:
            self.pac_is_dead=True
      
        self.after(170,self.move_randomly_or_follow)
        
    def move_randomly_or_follow1(self):
                # fait le chemin entre l'ennemi et le pacman
        self.H=self.BFS((self.ghost_pos[1]//20,self.ghost_pos[0]//20),(self.pac_pos[1]//20,self.pac_pos[0]//20),adj1)
        if (len(self.H)>1 and self.pac_is_dead==False and self.pac_won==False):
            if len(self.H)<self.radius: # si le pacman est suffisament proche l'ennemi se rapproche
                if len(self.H) in [18,19]:
                    self.K=adj1[(self.ghost_pos[1]//20,self.ghost_pos[0]//20)].copy()
                self.ghost_pos=(self.H[1][1]*20,self.H[1][0]*20)
                self.coords('ghost',(self.ghost_pos[0],self.ghost_pos[1]))
                self.H.pop(0)
            else: # sinon l'ennemi bouge aléatoirement
                self.a,self.b=random.choice(self.K)
                self.coords('ghost',self.b*20,self.a*20)
                self.K=adj1[(self.a,self.b)].copy()
                if (self.ghost_pos[1]//20,self.ghost_pos[0]//20) in self.K:
                    self.K.remove((self.ghost_pos[1]//20,self.ghost_pos[0]//20))
                self.ghost_pos=(self.b*20,self.a*20)
        elif (len(self.H)<=1 ):
            self.pac_is_dead=True
        
        self.after(170,self.move_randomly_or_follow1)    
        
        
    def create_coins(self):
     self.coins = {}
     for (i, j) in adj1.keys():
        x = 20 * j
        y = 20 * i
        tag = f"{i},{j}"
        self.create_image(x, y, image=self.coin_body, tag=tag)
        self.coins[tag] = (i, j)
        
        
    def coin_eaten(self):
     x_pos = self.pac_pos[0]
     y_pos = self.pac_pos[1]
     coin_tag = f"{y_pos//20},{x_pos//20}"
     if coin_tag in self.coins:
        self.available.append(self.coins[coin_tag])
        del self.coins[coin_tag]
        self.delete(coin_tag)
     if self.coins:
        self.after(80, self.coin_eaten)


            
    def update_timer(self):
      if self.pac_is_dead==False and self.pac_won==False:
        elapsed_time = int((time.time() - self.start_time) // 1)
        self.timer_label.config(text=f"Time: {elapsed_time}")
        self.score=elapsed_time


    
    def game_over(self):
        if self.enemy_pos==self.pac_pos or self.ghost_pos==self.pac_pos:
            self.pac_is_dead=True
            self.create_image(270,220,image=self.game_over_body,tag='game_over')
        self.after(80,self.game_over)
    
    def you_won(self):
        if len(self.coins.keys())==0 and self.pac_is_dead == False:
            self.pac_won == True
            
            self.create_image(270,220,image=self.Victory_body,tag='Victory')
            self.delete('pacman')
            self.pac_pos = (2000,2000)
        self.after(80,self.you_won)

board=labyrinthe()
def open_new_window():
    button.destroy()
    board.pack()
    
def quit_game():
    root.destroy()
    
def open_rules():
    
    img=PhotoImage(file="consignes.png")

    racine2=tk.Toplevel(root, height = 500, width = 500)
    label1 = tk.Label(racine2, image = img)
    label1.place(x = 0, y = 0)
    board2 = racine2
    button3.destroy()
    board2.pack()
    


start_image = 'START_BUTTON.png'
start_image_for_button =tk.PhotoImage(file=start_image)
button = tk.Button(root, command=open_new_window,image=start_image_for_button)
button.pack()

quit_image = Image.open='quit.png'
quit_image_for_button =tk.PhotoImage(file=quit_image)
button2=tk.Button(root,command=quit_game,image=quit_image_for_button)
button2.pack()

rule_image = 'howtoplay.png'
rule_image_for_button =tk.PhotoImage(file=rule_image)
button3=tk.Button(root, command = open_rules, image= rule_image_for_button )
button3.pack()

  
root.mainloop()