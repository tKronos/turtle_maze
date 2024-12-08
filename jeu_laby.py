import turtle as tt
import time
import os

# Activer le traçage automatique
tt.tracer(True)

# Fonction pour lire un labyrinthe à partir d'un fichier et le convertir en une liste de listes
def lire_labyrinthe(fichier):
    with open(fichier, 'r') as fichier_labyrinthe:
        labyrinthe = []
        entree = None
        sortie = None
        ligne_index = 0

        for ligne in fichier_labyrinthe:
            ligne_labyrinthe = []
            colonne_index = 0

            for caractere in ligne.strip():  # Ajout de .strip() pour enlever les "\n"
                # Case vide
                if caractere == ".":
                    ligne_labyrinthe.append(0)
                # Mur
                elif caractere == "#":
                    ligne_labyrinthe.append(1)
                # Entrée
                elif caractere == "x":
                    ligne_labyrinthe.append(0)
                    entree = [ligne_index, colonne_index]
                # Sortie
                elif caractere == "X":
                    ligne_labyrinthe.append(0)
                    sortie = [ligne_index, colonne_index]
                colonne_index += 1

            labyrinthe.append(ligne_labyrinthe)
            ligne_index += 1

    return labyrinthe, entree, sortie

# Chargement du labyrinthe depuis un fichier
choix_laby = input("Quel labyrinthe voulez-vous utiliser: ")
laby_directory = "maps/" + choix_laby + ".laby"

# Vérifier si le fichier existe
if not os.path.isfile(laby_directory):
    print(f"Le fichier {laby_directory} n'existe pas.")
    exit()

labyrinthe, entree, sortie = lire_labyrinthe(laby_directory)

# Stocker les données du jeu dans un dictionnaire
dicoJeu = {
    "labyrinthe": labyrinthe,  # chaque list est une ligne du labyrinthe (y), chaque élément de la liste est une colonne du labyrinthe (x)
    "entree": entree,          # [ligne, colonne]
    "sortie": sortie,          # [ligne, colonne]
    "taille_case": 30,         # Taille d'une case en pixels
    "debut": [-200, 200],
    "mur_epaisseur": 5,
}

# Affichage textuel du labyrinthe sous forme de matrice
print("Matrice du labyrinthe :")
for ligne in labyrinthe:
    print(ligne)

print("Entrée : ", entree)
print("Sortie : ", sortie)

# Affichage textuel du labyrinthe sous une forme lisible
def afficher_labyrinthe_texte(labyrinthe, entree, sortie):
    """
    Affiche le labyrinthe sous une forme lisible avec des symboles.
    - '#' pour les murs
    - ' ' pour les cases vides
    - 'x' pour l'entrée
    - 'O' pour la sortie
    """
    pos_x, pos_y = 0, 0

    for ligne in labyrinthe:
        resultat = ""
        for case in ligne:
            if case == 1:
                resultat += "#"
            elif case == 0:
                if [pos_y, pos_x] == entree:
                    resultat += "x"
                elif [pos_y, pos_x] == sortie:
                    resultat += "O"
                else:
                    resultat += " "
            pos_x += 1
        pos_y += 1
        pos_x = 0
        print(resultat)

afficher_labyrinthe_texte(labyrinthe, entree, sortie)

# Recois les coordonnees pixel de la tortue et les convertis en coordonnees de case dans le labyrinthe
def pixel2cell(x, y, dicoJeu):
    '''
    - Ce code prends une variable x, une variable y, et le dictionnaire, ce qu'il fait est:

        - Definit les coordonnees d'origines du point gauche superieur du labyrinthe, et la taille d'une case du labyrinthe
        - Recupere la position actuelle de la tortue en pixels
        - Convertit les coordonnees pixels en indices de case en utilisant la formule: (coordonnee_pixel - coordonnee_origine) // taille_case
        - S'assure que ces coordonnees sont comprises dans le labyrinthes, sinon il ne renvoie rien (utile pour le clic, car la tortue reste toujours dans le laby)

        Ce code peut etre utiliser ou pour convertir la position de la tortue en coordonnes ligne et colonnes, ou convertir la position du clic en ligne et colonne
    '''
    taille_case = dicoJeu["taille_case"]
    # Coordonnées du coin supérieur gauche du labyrinthe
    debut_x, debut_y = dicoJeu["debut"]  

    # Conversion des coordonnées pixels en indices de case, on fait +1 pour que le compteur commence de 1 et pas de 0
    # On utilise "//" car ca arrondit vers l'entier inferieur ce qui est demande pour mesurer les colonnes
    colonne = int((x - debut_x) // taille_case) + 1 
    # L'axe Y est inversé dans Turtle
    ligne = int((debut_y - y) // taille_case)  + 1 

    # Vérification si les coordonnées sont dans les limites du labyrinthe
    if 0 <= ligne -1 < len(dicoJeu["labyrinthe"]) and 0 <= colonne -1 < len(dicoJeu["labyrinthe"][0]): 
        return ligne, colonne
    else:
        return None    

def testClic(x, y):
    case = pixel2cell(x, y, dicoJeu)
    if case: # si ça renvoie une case, donc si le clic est dans le labyrinthe
        # affiche la case sur laquelle on a cliqué, case [0] c'est la ligne et case [1] c'est la colonne        
        print(f"Clic détecté sur la cellule: Ligne {case[0]}, Colonne {case[1]}") 
    else:
        print("Clic hors du labyrinthe!")
    return case

def cell2pixel(ligne, colonne):
    taille_case = dicoJeu["taille_case"]
    debut_x, debut_y = dicoJeu["debut"]

    # Calcul des coordonnées en pixels
    # on fait "-1" car on a fait +1 avant
    x = (debut_x + colonne * taille_case + taille_case // 2) - 1 
    # on soustrait car l'axe y est inverse, et on divise par 2 pour avoir le centre de la case
    y = (debut_y - ligne * taille_case - taille_case // 2) - 1 

    return y, x

tt.onscreenclick(testClic) 

def typeCellule(ligne, colonne):
    labyrinthe = dicoJeu["labyrinthe"]
    entree = dicoJeu["entree"]
    sortie = dicoJeu["sortie"]

    # Déterminer les cas spéciaux : entrée et sortie
    if [ligne, colonne] == entree:
        return "entrée"
    elif [ligne, colonne] == sortie:
        return "sortie"
    
    # Déterminer si c'est un mur
    if labyrinthe[ligne][colonne] == 1:
        return "mur"
    
    # Si ce n'est ni une entrée, sortie, ni un mur, c'est un passage
    voisins = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Haut, bas, gauche, droite
    
    # Compte les voisins non-murs
    for d in directions:
        voisin_ligne, voisin_colonne = ligne + d[0], colonne + d[1]
        if 0 <= voisin_ligne < len(labyrinthe) and 0 <= voisin_colonne < len(labyrinthe[0]):
            # Non-mur
            if labyrinthe[voisin_ligne][voisin_colonne] == 0 and labyrinthe[ligne][colonne]!=1:  
                voisins += 1

    # Determine le type de passage en fonction du nombre de voisins
    if voisins == 1:
        return "impasse"
    elif voisins == 2:
        return "passage standard"
    elif voisins > 2:
        return "carrefour"

# ----- Initialisation des tortues ------

# Tortue pour dessiner le laby
drawer = tt.Turtle() # cree la tortue du dessin
drawer.hideturtle() # cacher la tortue du dessein
drawer.speed(0) # 0 est la plus haute vitesse de la tortue

# Tortue pour le joueur
player = tt.Turtle() # Creer la tortue du joueur
player.shape("turtle") # Change la forme de la tortue en une forme de tortue
player.color("black") # Lui mettre une couleur noir
player.penup() # Pour qu'elle bouge sans dessiner
player.speed(1) 

# Tortue pour afficher les messages
message_turtle = tt.Turtle()
message_turtle.hideturtle()  # Cacher la tortue, car on ne dessine pas
message_turtle.penup()
message_turtle.speed(0)  # Vitesse maximale pour éviter les lenteurs

# Affichage graphique du labyrinthe avec Turtle
def afficher_labyrinthe_graphique(labyrinthe=dicoJeu["labyrinthe"], 
    mur_epaisseur=dicoJeu["mur_epaisseur"], taille_case=dicoJeu["taille_case"], 
    debut_x=dicoJeu["debut"][0], debut_y=dicoJeu["debut"][1]):

    drawer.pensize(mur_epaisseur) # Pensize represente l'epaisseur des murs
    drawer.penup()
    drawer.goto(debut_x, debut_y) # se dirige vers le coordonnees de debut, d'origine du labyrinthe

    '''
    On fais un iteration sur chaque ligne, et chaque colonne dans chaque 
    ligne, on determine les coordonnés de chaque case, 
    et on dessine un carré si c'est un mur, et on dessine un point rouge 
    si c'est l'entree, et un point vert si c'est la sortie, 
    et un point bleu si c'est un carrefour, et rien si c'est un passage 
    standard ou une impasse.

    J'ai trouve que c'est plus efficace de dessiner graduellement en avançant
    '''
    for ligne in range(len(labyrinthe)):
        for colonne in range(len(labyrinthe[ligne])):
            # Déterminer le type de la case
            case_type = typeCellule(ligne, colonne) 
            
            y, x = cell2pixel(ligne, colonne)
             # Position en haut à gauche de la case
            drawer.goto(x - taille_case/2, y + taille_case/2) 
            
            if case_type == "mur":
                drawer.begin_fill()
                for _ in range(4):
                    drawer.forward(taille_case)
                    drawer.right(90)
                drawer.end_fill()
            elif case_type == "entrée":
                drawer.color("red")
                drawer.goto(x, y)
                drawer.stamp()
                drawer.color("black")
            elif case_type == "sortie":
                drawer.color("green")
                drawer.goto(x, y)
                drawer.stamp()
                drawer.color("black")
            elif case_type == "carrefour":
                drawer.color("blue")
                drawer.goto(x, y)
                drawer.stamp()
                drawer.color("black")
            # Pour les impasses et passages standards, rien à dessiner

    # Positionner la tortue (Player pas Drawer) au point d'entrée
    entree_y, entree_x = cell2pixel(entree[0], entree[1])
    player.goto(entree_x, entree_y)  

afficher_labyrinthe_graphique(labyrinthe)

def reset_couleur():
    player.color("black")

chemin_liste = []

def gauche():
    chemin_liste.append("gauche") # Ajout Gauche a la liste de chemin
    x, y = player.pos() # cherche les coordonnees du joueur et les mets dans x et y
    case = pixel2cell(x, y, dicoJeu) # les transfrome en coordonnes case et les mets dans la var case
    if case is not None:
        ligne, colonne = case 
        # Vérifie à gauche si tout d'abord ce n'est pas la fin du laby, et si il ya un mur (-2 et -1, car il faut soustraire 1 aux deux valeurs vu que j'en est ajoute dans  pixel2cell())
        if colonne > 1 and dicoJeu["labyrinthe"][ligne-1][colonne-2] == 0:  
            player.setheading(180) # personal note: replace without using this function later
            player.forward(dicoJeu["taille_case"])
            verifier_case()
        else:
            print("Mur à gauche !")
            # Donne une colour rouge si joueur essaye d'heurter un mur
            player.color("red") 
            # attends 0.5 secondes avant de remettre la couleur noire
            tt.ontimer(reset_couleur, 500)

def droite():
    chemin_liste.append("droit")
    x, y = player.pos()
    case = pixel2cell(x, y, dicoJeu)
    if case is not None:
        ligne, colonne = case
        # Vérifie à droite (-1 initial pour avoir les vrai valeurs, et +1 pour colonne, pour marcher vers la droite)
        if colonne < len(dicoJeu["labyrinthe"][0]) and dicoJeu["labyrinthe"][ligne-1][colonne] == 0:  
            player.setheading(0)
            player.forward(dicoJeu["taille_case"])
            verifier_case()
        else:
            print("Mur à droite !")
            # Donne une colour rouge si joueur essaye d'heurter un mur
            player.color("red") 
            # attends 0.5 secondes avant de remettre la couleur noire
            tt.ontimer(reset_couleur, 500)

def haut():
    chemin_liste.append("haut")
    x, y = player.pos()
    case = pixel2cell(x, y, dicoJeu)
    if case is not None:
        ligne, colonne = case
        if ligne > 1 and dicoJeu["labyrinthe"][ligne-2][colonne-1] == 0:  # Vérifie en haut si c'est pas la fin du labyrinthe et si c'est un passage et non un mur
            player.setheading(90)
            player.forward(dicoJeu["taille_case"])
            verifier_case()
        else:
            print("Mur en haut !")
            # Donne une colour rouge si joueur essaye d'heurter un mur
            player.color("red") 
            # attends 0.5 secondes avant de remettre la couleur noire
            tt.ontimer(reset_couleur, 500)

def bas():
    chemin_liste.append("bas")
    x, y = player.pos()
    case = pixel2cell(x, y, dicoJeu)
    if case is not None:
        ligne, colonne = case
        # Vérifie en bas si c'est pas la fin du labyrinthe et si c'est un passage et non un mur
        if ligne < len(dicoJeu["labyrinthe"]) and dicoJeu["labyrinthe"][ligne][colonne-1] == 0:  
            player.setheading(270)
            player.forward(dicoJeu["taille_case"])
            verifier_case()
        else:
            print("Mur en bas !")
            # Donne une colour rouge si joueur essaye d'heurter un mur
            player.color("red") 
            # attends 0.5 secondes avant de remettre la couleur noire
            tt.ontimer(reset_couleur, 500)

def verifier_case():
    x, y = player.pos() # prends position actuelle de la tortue, associe a x et y
    case = pixel2cell(x, y, dicoJeu) # traduit x et y en ligne et colonne 
    # (ligne, colonne) = case
    
    if case: # si la case est true (donc si la tortue est dans le labyrinthe et non en dehors ou sur les bords du labyrinthe)
        ligne, colonne = case # associe les coordonnees de la case a une ligne et une colonne

        type_case = typeCellule(ligne-1, colonne-1)  # Indices ajustés (on a ajoute +1 avant car je repete, le code compte les cases en commencent de 0, on veut les compter en commencent de 1)
        if type_case == "impasse": 
            player.color("blue")
            statistiques["nombre_impasses"] += 1
            afficher_message("Impasse rencontrée.")
            afficher_statistiques()
        elif type_case == "carrefour":
            player.color("purple")
            statistiques["nombre_carrefours"] += 1
            # On utilise afficher_message pour afficher le message sur le graphe
            afficher_message("Carrefour rencontré.")
            afficher_statistiques()
        elif type_case == "sortie":
            player.color("green")
            afficher_message("Victoire ! Sortie trouvée.")
            # Calculer les statistiques (pour l'extension)
            # time.time(): retourne le timestamp actuel en secondes
            # start_time: C'est une variable qui enregistre le moment où l'exploration a commencé. Elle est initialisée avec start_time = time.time() au début de l'exploration.
            # if start_time else 0 : Si start_time est défini (c'est-à-dire qu'il n'est pas None ou une valeur équivalente à False), alors calcule time.time() - start_time.
            # Pourquoi? Cela empêche une erreur si start_time n'a pas encore été défini
            statistiques["temps_exploration"] = time.time() - start_time if start_time else 0
            afficher_statistiques()
        else:
            player.color("black")

print("Chemin suivi :", chemin_liste)

def suivreChemin(li):
    """
    Suivre une liste de commandes pour déplacer la tortue de manière asynchrone.
    - g : gauche
    - d : droite
    - h : haut
    - b : bas
    """
    def move_next(index):
        if index < len(li):
            commande = li[index]
            if commande == "g": 
                gauche()
            elif commande == "d":
                droite()
            elif commande == "h":
                haut()
            elif commande == "b":
                bas()
            else:
                afficher_message(f"Commande inconnue: {commande}")
                return
            # Planifier le prochain mouvement après 300 ms
            tt.ontimer(lambda: move_next(index + 1), 300)
        else:
            afficher_message("Exploration automatique terminée.")
            # Calculer les statistiques à la fin de l'exploration
            statistiques["temps_exploration"] = time.time() - start_time if start_time else 0
            afficher_statistiques()
            global mode
            mode = "manuel"  # Retourner en mode manuel après l'exploration automatique

    # Démarrer le mouvement avec l'index 0
    move_next(0)

def inverserChemin(li):
    """
    Suit un chemin donné en sens inverse.
    - g (gauche) devient d (droite)
    - d (droite) devient g (gauche)
    - h (haut) devient b (bas)
    - b (bas) devient h (haut)
    """
    inverse = [] # cree une liste ou on vas inserer le chemin inverse
    for i in range(len(li)-1, -1, -1):  # Commence par le terme len(li)-1 de la liste, s'arrete avant le terme -1 (donc au terme 0), et prends -1 pas chaque iteration

        commande = li[i] # chaque nombre associe a index i (qui commence du dernier) associe a commande
        
        # Ajoute la direction qui commence du derner index a la liste inverse
        if commande == "g":
            inverse.append("d")
        elif commande == "d":
            inverse.append("g")
        elif commande == "h":
            inverse.append("b")
        elif commande == "b":
            inverse.append("h")
        else:
            print("Commande inconnue :", commande)
            return

    suivreChemin(inverse)

tt.listen()  




# Fait que quand on presse sur les fleches du clavier ca bouge la tortue dans sa direction correspondante
tt.onkeypress(gauche,"Left")
tt.onkeypress(droite,"Right")
tt.onkeypress(haut,"Up")
tt.onkeypress(bas,"Down")


# -------------------------- Exploration ---------------------------------

def explorer(labyrinthe=labyrinthe, entree=dicoJeu["entree"], sortie=dicoJeu["sortie"]):
    """
    Entree: C'est une liste contenant les coordonnées [ligne, colonne] du point de départ.
    Sortie: C'est aussi une liste contenant les coordonnées [ligne, colonne] de la sortie.
    - La sortie de la fonction
        Si un chemin est trouvé : retourne une liste de positions (le chemin).
        Si aucun chemin n’est trouvé : retourne None.

    Logique de l'algorithme:
        1. Commencer à l'entrée.
        2. Tester les directions possibles autour (haut, bas, gauche, droite).
        3. Avancer sur un chemin libre (cellule 0) et garder une trace du chemin parcouru.
        4. Reculer si on atteint une impasse (mur ou déjà visité).
        5. Arrêter dès qu’on trouve la sortie ou si toutes les possibilités sont explorées.

    C'est une pile utilisée pour suivre les positions à explorer. Chaque élément de la pile contient :
        La position actuelle (Actuelle).
        Le chemin parcouru jusqu'à cette position (Chemin).
        Une liste de positions que l'algorithme a déjà explorées pour éviter de revisiter les mêmes cases (Visitee)
    """
    pile = [[entree, [entree]]]  # C'est une pile utilisée pour suivre les positions à explorer. Chaque élément de la pile contient; La position actuelle (actuelle) et Le chemin parcouru jusqu'à cette position (chemin).
    visitee = []  # Liste des positions visitées

    while pile: # continue a iterer dans que la liste stack n'est pas vide (une list vide est evaluee comme false)
        actuelle, chemin = pile.pop() # Prendre un elemet de la pile (le dernier ajoute) et le supprime de la pile
        # Si current est égal à la sortie, on retourne "chemin", car on a trouvé le chemin.
        if actuelle == sortie:
            return chemin
        # Si current est déjà dans la liste visitee, on passe directement à la prochaine itération.
        if actuelle in visitee: 
            continue # empeche toute la suite du code dans la boucle while de s'exécuter si la position current est déjà dans la liste visitee (passe a l'iteration while prochaine).

        # Marque la position comme visitée (si elle n'est ni sortie, ni visitee deja)
        visitee.append(actuelle)
        ligne, colonne = actuelle

        # On explore les voisins, Ordre des directions : haut, bas, gauche, droite
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for d_l, d_c in directions: # chaque direction est un deplacement ligne (d_l) ou deplacement colonne (d_c)
            voisin = [ligne + d_l, colonne + d_c] # calculer la position voisine
            # Verifier si le voisin est un mouvement valide (reste dans les limites du laby, passage libre, pas deja visite)
            if (0 <= voisin[0] < len(labyrinthe) and
                0 <= voisin[1] < len(labyrinthe[0]) and
                labyrinthe[voisin[0]][voisin[1]] == 0 and
                voisin not in visitee):
                # Ajouter le voisin à la pile avec le chemin mis à jour
                nouveau_chemin = chemin.copy()
                nouveau_chemin.append(voisin)
                pile.append([voisin, nouveau_chemin])
    return None  # Aucun chemin trouve

def chemin_to_mouvement(chemin):
    """
    Convertit une liste de cellules en une liste de mouvements.
    
    Args:
        chemin (list): Liste des cellules traversées, chaque cellule étant [ligne, colonne].
    
    Returns:
        list: Liste des mouvements correspondants ('g', 'd', 'h', 'b').
    """
    mouvements = []
    for i in range(1, len(chemin)):
        # La fonction parcourt le chemin en comparant chaque cellule avec la cellule précédente.
        precedent = chemin[i-1]
        actuel = chemin[i]
        # On calcule le déplacement en termes de : difference de colonnes, et difference de lignes
        d_l = actuel[0] - precedent[0]
        d_c = actuel[1] - precedent[1]
        # Les conditions suivantes déterminent le mouvement à partir des différences calculées et ajoutent le mouvement correspondant à la liste des mouvements.
        if d_l == -1 and d_c == 0:
            mouvements.append("h")  # haut
        elif d_l == 1 and d_c == 0:
            mouvements.append("b")  # bas
        elif d_l == 0 and d_c == -1:
            mouvements.append("g")  # gauche
        elif d_l == 0 and d_c == 1:
            mouvements.append("d")  # droite
    return mouvements

def optimiser_chemin(mouvements):
    """
    La fonction optimiser_chemin sert à simplifier une liste de mouvements en 
    supprimant les mouvements qui s'annulent mutuellement. Par exemple :
        Si tu avances à droite ('d') puis à gauche ('g'), tu reviens au point 
        de départ, donc ces deux mouvements peuvent être supprimés.
    """
    opposes = {'g': 'd', 'd': 'g', 'h': 'b', 'b': 'h'} # Ce dictionnaire associe chaque mouvement à son opposé
    optimise = [] # C'est une liste vide qui contiendra les mouvements optimisés.
    for move in mouvements:
        if optimise: # si optimise n'est pas vide
            dernier_move = optimise[-1]
            # Vérifier si le mouvement actuel annule ce dernier mouvement 
            if opposes.get(move) == dernier_move:
                optimise.pop() # Si c’est le cas, on retire le dernier mouvement avec pop()
                continue
        optimise.append(move) # Si le mouvement actuel ne s'annule pas avec le précédent, on l'ajoute à la liste optimisée
    return optimise

# --------------------------------------------------- Extensions ---------------------------------------------------------------

# ------------------------ Définir les Boutons --------------------------

# Liste pour stocker les boutons
boutons = []

def dessiner_bouton(x, y, width, height, texte, action):
    """
    Dessine un bouton et ajoute ses informations à la liste des boutons.
    """
    drawer.penup()
    drawer.goto(x, y)  # Coin supérieur gauche du bouton
    drawer.pendown()
    drawer.fillcolor("lightgray")
    drawer.begin_fill()
    for _ in range(2):
        drawer.forward(width)
        drawer.right(90)
        drawer.forward(height)
        drawer.right(90)
    drawer.end_fill()
    
    # Écrire le texte au centre du bouton
    drawer.penup()
    drawer.goto(x + width / 2, y - height / 2 - 5)  # Centre du bouton (-5 car ca affichait trops bas)
    drawer.color("black")
    drawer.write(texte, align="center", font=("Arial", 12, "normal"))
    
    # Ajouter le bouton à la liste
    boutons.append({
        "x1": x,            # x Coin supérieur gauche du bouton
        "y1": y - height,  # y Coin inférieur gauche du bouton 
        "x2": x + width,    # x du Coin supérieur droit du bouton
        "y2": y,            # y du Coin inférieur droit du bouton
        "action": action,   # action a effectuer quand on clique sur le boutton
        "texte": texte      # ça c'est le texte qui est affiché sur le boutton
    })

# Variables globales pour les statistiques
statistiques = {
    "temps_exploration": 0,
    "nombre_pas": 0,
    "nombre_demi_tours": 0,
    "nombre_impasses": 0,
    "nombre_carrefours": 0
}

start_time = None # utilise pour calculer temps_exploration

def afficher_message(message):
    """
    Affiche un message dans la fenêtre graphique en utilisant la tortue 'message_turtle'.
    """
    message_turtle.clear()  # Efface les messages précédents
    message_turtle.penup()
    message_turtle.goto(-150, 250)  # Position en bas de l'écran (ajustez selon vos besoins)
    message_turtle.color("black")
    message_turtle.write(message, align="left", font=("Arial", 14, "normal"))


start_time = time.time()

def reset_exploration():
    """
    Redémarre l'exploration du labyrinthe.
    """
    global chemin_liste, start_time # utilise des variables globales hors de cette fonction
    chemin_liste = []

    # Décomposer les coordonnées retournées par cell2pixel
    entree_y, entree_x = cell2pixel(dicoJeu["entree"][0], dicoJeu["entree"][1])
    
    # Utiliser l'ordre correct (x, y) pour goto
    player.goto(entree_x, entree_y)
    player.setheading(0) # tortue regarde a l'est
    afficher_message("Exploration redémarrée.")
    statistiques["nombre_pas"] = 0
    statistiques["nombre_demi_tours"] = 0
    start_time = time.time()


def lancer_exploration_automatique():
    """
    Lance l'exploration automatique du labyrinthe de manière asynchrone.
    """
    global start_time
    start_time = time.time()
    afficher_message("Mode automatique activé.")
    exploration = explorer(labyrinthe, entree, sortie)
    if exploration:
        chemin = chemin_to_mouvement(exploration)
        print("Chemin trouve:", chemin)
        # Optimisation du chemin (Bonus)
        chemin_optimise = optimiser_chemin(chemin)
        print("Chemin optimisé :", chemin_optimise)
        suivreChemin(chemin_optimise)
    else:
        afficher_message("Aucun chemin trouvé.") 

def lancer_exploration_manuel():
    """
    Active le mode manuel.
    """
    afficher_message("Mode manuel activé.")

# Liste des fichiers de labyrinthes dans le dossier 'maps'
labyrinthes_disponibles = [f for f in os.listdir("maps") if f.endswith(".laby")]

# Vérifier qu'il y a au moins un labyrinthe
if not labyrinthes_disponibles:
    print("Aucun labyrinthe trouvé dans le dossier 'maps'.")
    exit()

# Variable pour suivre l'index du labyrinthe actuel
# on en a besoin pour changer de labys apres
current_labyrinthe_index = 0

def charger_nouveau_labyrinthe():
    """
    Charge un nouveau labyrinthe depuis le dossier 'maps'.
    Charge le labyrinthe suivant dans la liste des labyrinthes disponibles.
    Si le dernier labyrinthe est atteint, revient au premier.
    """
    global labyrinthe, entree, sortie, dicoJeu, current_labyrinthe_index, boutons
    # Réinitialiser la liste des boutons
    boutons = []
    
    # Le modulo est utilisé pour s'assurer que l'index reste dans les limites de la liste. 
    # Si current_labyrinthe_index + 1 est égal au nombre de labyrinthes disponibles, 
    # le résultat sera 0, revenant ainsi au premier labyrinthe.
    current_labyrinthe_index = (current_labyrinthe_index + 1) % len(labyrinthes_disponibles)
    # Rejoins le folder maps et le nom du labyrinthe pour charger le labyrinthe
    fichier = os.path.join("maps", labyrinthes_disponibles[current_labyrinthe_index])
    
    # Charger le nouveau labyrinthe et mise a jour dicojeu
    # (comme on la fait pour celui ci au debut du code)
    labyrinthe, entree, sortie = lire_labyrinthe(fichier)
    dicoJeu["labyrinthe"] = labyrinthe
    dicoJeu["entree"] = entree
    dicoJeu["sortie"] = sortie
    
    # Redessiner le labyrinthe (meme manier qu'on a fait au debut du code)
    drawer.clear()
    afficher_labyrinthe_graphique(labyrinthe)
    
    # Repositionner la tortue au point d'entrée
    entree_y, entree_x = cell2pixel(entree[0], entree[1])
    player.goto(entree_x, entree_y)
    player.setheading(0)
    
    # Afficher un message
    afficher_message(f"Nouveau labyrinthe chargé : {labyrinthes_disponibles[current_labyrinthe_index]}")
    
    # Réinitialiser les statistiques
    statistiques["temps_exploration"] = 0
    statistiques["nombre_pas"] = 0
    statistiques["nombre_demi_tours"] = 0
    statistiques["nombre_impasses"] = 0
    statistiques["nombre_carrefours"] = 0
    afficher_statistiques()
    # Afficher les boutons de nouveau
    afficher_bouton()
    start_time = time.time()


# -------------------------------- STATISTIQUES --------------------------------
stats_turtle = tt.Turtle()
stats_turtle.hideturtle()
stats_turtle.penup()
stats_turtle.speed(0)

def afficher_statistiques():
    stats_turtle.clear()
    stats_turtle.goto(50, -200)
    stats_turtle.write(
        f"Temps d'exploration: {statistiques['temps_exploration']:.2f} sec\n"
        f"Nombre de pas: {statistiques['nombre_pas']}\n"
        f"Nombre de demi-tours: {statistiques['nombre_demi_tours']}\n"
        f"Nombre d'impasses: {statistiques['nombre_impasses']}\n"
        f"Nombre de carrefours: {statistiques['nombre_carrefours']}",
        align="left", font=("Arial", 12, "normal")
    )


# -------------------- CREER LES BOUTONS ----------------------------

# Créer les boutons
def afficher_bouton():
    dessiner_bouton(-250, 0, 100, 40, "Recommencer", reset_exploration)
    dessiner_bouton(-250, -50, 100, 40, "Auto", lancer_exploration_automatique)
    dessiner_bouton(-250, -100, 100, 40, "Manuel", lancer_exploration_manuel)
    dessiner_bouton(-250, -200, 100, 40, "Charger", charger_nouveau_labyrinthe)

# ------- DETECTER LES CLICS SUR LES BOUTONS -----------------------

def gestion_clic(x, y):
    """
    Gère les clics sur les boutons.

    - ca prends la position x et y ou on a clique
    - fait iteration pour chaque bouton afin de voir si on a clique dessus
     - si on a clique dessus, ca execute l'action du bouton
    """
    for bouton in boutons:

        if bouton["x1"] <= x <= bouton["x2"] and bouton["y1"] <= y <= bouton["y2"]:
            bouton["action"]()
            return  # Sortir après avoir trouvé le bouton cliqué
    # Si le clic n'est pas sur un bouton,il ignore     
    testClic(x, y)


# Remplacer l'ancien binding de clic par la nouvelle fonction
tt.onscreenclick(gestion_clic)

# Assurez-vous d'appeler afficher_bouton() pour dessiner les boutons
afficher_bouton()

# -------------------------------- Exploration Automatique ---------------------------------





tt.mainloop()
