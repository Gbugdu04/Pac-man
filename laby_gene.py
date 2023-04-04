def liens_dico(dico):
    dico_liens = dict()
    for element in dico:
        liens_fait = 0
        for i in element:
            if element[1]:
                liens_fait += 1
        dico_liens[element] = [len(element), liens_fait]
    return dico_liens

def init_graphe(x, y):
    noeud_faits = 0
    dico_sommets = dict()
    for i in range(x):
        for j in range(y):
            dico_sommets[(i,j)] = []
            if i != 0:
                dico_sommets[(i,j)].append([(i-1,j), False])
            if i != x-1:
                dico_sommets[(i,j)].append([(i+1,j), False])
            if j != 0:
                dico_sommets[(i,j)].append([(i,j-1), False])
            if i != y-1:
                dico_sommets[(i,j)].append([(i,j+1), False])

    while noeud_faits < len(dico_sommets):
        for liste_adj in dico_sommets:
    return dico_sommets


