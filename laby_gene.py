import random
import json 

def aleatoire(proba): # entre 0 et 1
    """
    retourne True ou False avec une probabilité rentrée entre 0 et 1 
    """
    n = random.randint(0,100)
    if n < proba*100:
        return True
    else:
        return False
    
def choix(l):
    """
    choisi aléatoirment entre les élements d'une liste
    """
    if len(l) == 1:
        return l[0]
    elif len(l) == 2:
        if aleatoire(0.99):
            return l[0]
        else:
            return l[1]
    elif len(l) == 3:
        if aleatoire(0.99):
            return l[0]
        elif aleatoire(0.99):
            return l[1]
        else:
            return l[2]

def init_graphe(x, y):
    """
    créer un labyrinthe sous forme d'une grille et renvoie un dictionnaire d'adjacence
    """
    dico_sommets = dict()
    dico_adj = dict()
    # initialisation des dictionnaires de sommets et d'adjacences
    for i in range(x):
        for j in range(y):
            dico_sommets[(i,j)] = [0, 0, [False, False, False, False]]
            #  nb lien possible et lien fait, liste gauche, droite, haut bas
            if i != x-1:
                dico_adj[((i,j),(i+1,j))] = False
                dico_sommets[(i,j)][2][1] = True
                dico_sommets[(i,j)][0] += 1
            if i != 0:
                dico_sommets[(i,j)][2][0] = True
                dico_sommets[(i,j)][0] += 1
            if j != 0:
                dico_sommets[(i,j)][2][2] = True
                dico_sommets[(i,j)][0] += 1
            if j != y-1:
                dico_adj[((i,j),(i,j+1))] = False
                dico_sommets[(i,j)][2][3] = True
                dico_sommets[(i,j)][0] += 1

    liste_sommets = list(dico_sommets.keys())
    
    # créer les adjacences procéduralement
    for _ in range(len(dico_sommets.keys())):
        sommet = random.choice(liste_sommets)
        liste_sommets.remove(sommet)
        x1, y1 = sommet
        possible, deja_fait, card = dico_sommets[sommet]
        list_a_faire = []
        for i in range(possible-1):
            list_a_faire.append(i+2-deja_fait)
        a_faire = choix(list_a_faire)
        fait = 0
        l = [p for p in range(4)]
        while (a_faire != fait) and (l != []):
            direction = random.choice(l)
            l.remove(direction)
            if card[direction]:
                if (direction == 0) and not dico_adj[((x1-1,y1),sommet)]: #gauche
                    dico_adj[((x1-1,y1),sommet)] = True
                    dico_sommets[(x1-1,y1)][1] += 1
                    fait += 1 
                if (direction == 1) and not dico_adj[(sommet,(x1+1,y1))]: #droite
                    dico_adj[(sommet,(x1+1,y1))] = True
                    dico_sommets[(x1+1,y1)][1] += 1
                    fait += 1 
                if (direction == 2) and not dico_adj[((x1,y1-1),sommet)]: #haut
                    dico_adj[((x1,y1-1),sommet)] = True
                    dico_sommets[(x1,y1-1)][1] += 1
                    fait += 1
                if (direction == 3) and not dico_adj[(sommet,(x1,y1+1))]: #bas
                    dico_adj[(sommet,(x1,y1+1))] = True
                    dico_sommets[(x1,y1+1)][1] += 1
                    fait += 1
            
    return dico_adj

def tableau_gen(x,y):
    """
    transforme la labyrinthe obtenu avec la fonction précédente pour la rendre lisible par le programme principale
    """
    # créer un premier tableau de petite taille à partir d'un labyrinthe généré procéduralement avec les symboles utilisés par le programme principal
    dico_adj = init_graphe(x,y)
    tableau = [["X" for i in range(2*x+1)] for j in range(2*y+1)]
    for i in range(x):
        for j in range(y):
            tableau[2*j+1][2*i+1] = " "
    for (x1,y1), (x2,y2) in dico_adj:
        if dico_adj[(x1,y1), (x2,y2)]:
            tableau[(y1+y2)+1][(x1+x2)+1] = " "
    
    # créer un nouveau tableau qui peut être utilisé par le programme principal
    # agrandit le tableau affin qu'il soit plus aéré dans le jeu
    tableau_propre = []
    for i_ligne in range(len(tableau)):
        a = ""
        for i_element in range(len(tableau[i_ligne])):
            a += tableau[i_ligne][i_element]
            if i_element != 0 and i_element != len(tableau[i_ligne])-1 and i_element%2 == 0 :
                a += tableau[i_ligne][i_element]
                a += tableau[i_ligne][i_element]
        tableau_propre.append(a)
        if i_ligne != 0 and i_ligne != len(tableau)-1 and i_ligne%2 == 0 :
            tableau_propre.append(a)
            tableau_propre.append(a)
    return tableau_propre

# créer un dictionnaire de 30 labyrinthes
dico_tableaux = dict()
for i in range(30):
    dico_tableaux[i] = tableau_gen(7,7)

# lignes qui permettent de mettre de nouveaux labyrinthe dans le fichier json
"""
with open("dico_labyrinthe.json","w", encoding='utf-8') as f:
    json.dump(dico_tableaux, f, indent = 4)
"""