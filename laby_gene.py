import random

def liens_dico(dico):
    dico_liens = dict()
    for element in dico:
        liens_fait = 0
        for i in element:
            if element[1]:
                liens_fait += 1
        dico_liens[element] = [len(element), liens_fait]
    return dico_liens

 def aleatoire(proba=0.5):
    n = random.randint(0,100)
    if n < proba*100:
        return True
    else:
        return False

def init_graphe(x, y):
    noeud_faits = 0
    dico_sommets = dict()
    for i in range(x):
        for j in range(y):
            dico_sommets[(i,j)] = [[0,False],[]]  
            # [liste nb lien et plus de lien possible, liste des adjacences coord et lien fait]
            if i != 0:
                dico_sommets[(i,j)][1].append([(i-1,j), False])
                dico_sommets[(i,j)][0][1] += 1
            if i != x-1:
                dico_sommets[(i,j)][1].append([(i+1,j), False])
                dico_sommets[(i,j)][0][1] += 1
            if j != 0:
                dico_sommets[(i,j)][1].append([(i,j-1), False])
                dico_sommets[(i,j)][0][1] += 1
            if j != y-1:
                dico_sommets[(i,j)][1].append([(i,j+1), False])
                dico_sommets[(i,j)][0][1] += 1

    while noeud_faits < len(dico_sommets):
        for element, adjacences in dico_sommets:
            if not element[1]:   
                #revoir cette partie pour utiliser le second bool
                for chemin in adjacences:
                    if chemin[1] and aleatoire(1/len(adjacences)):
                        

                if aleatoire(((element[0]-len(adjacences))**2)/(4*len(adjacences)-7)):
                    element[0] += 1
                    direction = random.randint(0,len(adjacences))
                    adjacences[direction][1] = True
                    case_liee = adjacences[direction][0]
                    dico_sommets[case_liee][0][0] += 1 
                    dico_sommets[case_liee][0][0] += 1


    return dico_sommets

print(init_graphe(1,2))

