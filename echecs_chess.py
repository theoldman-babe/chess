from qtido import *

from numpy import logical_xor


# Draw a colored rectangle for a board square (white or dark gray)
def tracer_rectangle_couleur(f,x1,y1,x2,y2,color):
 
    match color:
        case 'blanc':
           couleur(f,1,1,1)
        
        case 'gris':
            couleur(f,0.2,0.2,0.2)
            
            
    rectangle(f,x1,y1,x2,y2)
#j'ai utilisé la fonction de l'exo 2 pour réaliser cette exercice



f=creer(900,900)

# Color a square based on its position (checkerboard pattern)
def dessiner_cases_vides(ligne, colonne, f):
    if (ligne + colonne)%2==0:
        
        return  tracer_rectangle_couleur(f,ligne*100,colonne*100,(ligne+1)*100,(colonne+1)*100,"gris")
    else:
        
        return tracer_rectangle_couleur(f,ligne*100,colonne*100,(ligne+1)*100,(colonne+1)*100,"blanc")


# Draw all 64 squares of the board
def tracer_plateau (f):
    for i in range(8):
        for j in range(8):
            dessiner_cases_vides(i,j,f)

# Pawn: circle (head) + rectangle (body)
def tracer_pion(f, x, y):
    
    disque(f, x + 50, y + 40, 15)
    rectangle(f, x + 35, y + 55, x + 65, y + 80)

# Rook: wide body with a flat platform on top
def tracer_tour(f, x, y):
    
    rectangle(f, x + 30, y + 40, x + 70, y + 80)
    rectangle(f, x + 25, y + 25, x + 75, y + 40)

# Bishop: circle (head) on top of a triangle
def tracer_fou(f, x, y):
    disque(f, x + 50, y + 35, 12)
    polygone(f, [[x + 50, y + 20], [x + 65, y + 80], [x + 35, y + 80]])

# Knight: irregular polygon shaped like a horse head
def tracer_chevalier(f, x, y):
    polygone(f, [[x + 35, y + 80], [x + 65, y + 80], [x + 60, y + 40], [x + 75, y + 35], [x + 65, y + 20], [x + 40, y + 30]])

# Queen: crown-like polygon with a wide base
def tracer_reine(f, x, y):
   
    polygone(f, [[x + 20, y + 20], [x + 35, y + 50], [x + 50, y + 15], [x + 65, y + 50], [x + 80, y+ 20], [x + 70, y + 80], [x + 30, y + 80]])

# King: body with a cross on top
def tracer_roi(f, x, y):

    rectangle(f, x + 35, y + 40, x + 65, y + 80)
    rectangle(f, x + 45, y + 15, x + 55, y + 40)
    rectangle(f, x + 35, y + 25, x + 65, y + 30)
    
# Call the right drawing function based on the piece name
def dessiner(f,s,x,y):
    if "reine"in s :
        tracer_reine(f,x,y)
    elif "roi"in s :
        tracer_roi(f,x,y)
    elif "pion" in s :
        tracer_pion(f,x,y)
    elif "fou" in s :
        tracer_fou(f,x,y)
    elif "cheval" in s :
        tracer_chevalier(f,x,y)
    elif "tour" in s :
        tracer_tour(f,x,y)


# Set up the starting position — N = black pieces, B = white pieces
def initialiser_echiquier ():
     echiquier = [
["tour-N","chevalier-N","fou-N","reine-N","roi-N","fou-N","chevalier-N","tour-N"],
["pion-N","pion-N","pion-N","pion-N","pion-N","pion-N","pion-N","pion-N"],
["","","","","","","",""],
["","","","","","","",""],
["","","","","","","",""],
["","","","","","","",""],
["pion-B","pion-B","pion-B","pion-B","pion-B","pion-B","pion-B","pion-B"],
["tour-B","chevalier-B","fou-B","roi-B","reine-B","fou-B","chevalier-B","tour-B"]
]
     return echiquier

# Display column letters (A-H) and row numbers (1-8) around the board
def afficher_code_cases(f):
    lettres = ["A","B","C","D","E","F","G","H"]

    
    for i in range(8):
        texte(f, i*100 + 50, 850, 20, lettres[i])
    for j in range(8):
        texte(f, 820, j*100 + 50, 20, str(j+1))

        
# Draw the board then place each piece at its current position
def remplir_et_tracer_echiquier (f, echiquier ):
    tracer_plateau(f)
    for j in range(8):
        for i in range(8):
            if echiquier[j][i]!="":
                if   (echiquier[j][i]).endswith('-B'):
                    couleur(f,1,1,0)  # white pieces in yellow
                    dessiner(f,echiquier[j][i], i*100, j*100 )
    
                else:
                    couleur(f,0,0,0)  # black pieces in black
                    dessiner(f,echiquier[j][i], i*100, j*100 )
    afficher_code_cases(f)                
    


# Convert a square code like "A1" into [row, col] array indices
def de_code_a_num_case(s):
    colonne, ligne=s[0],s[1]
    return[(int(ligne)-1),(ord(colonne)-ord('A')) ]

# Move a piece from one square to another and clear the source square
def mise_a_jour_echiquier(echequier,code_a_bouger,code_destination):
    echequier[de_code_a_num_case(code_destination)[0]][de_code_a_num_case(code_destination)[1]]=echequier[de_code_a_num_case(code_a_bouger)[0]][de_code_a_num_case(code_a_bouger)[1]]
    echequier[de_code_a_num_case(code_a_bouger)[0]][de_code_a_num_case(code_a_bouger)[1]]=""
    return echequier



echiquier = initialiser_echiquier()


remplir_et_tracer_echiquier(f, echiquier)

# Check if a move is valid for the current player
def checker_le_move(echiquier,c_initiale:str, c_destination:str ,player:str):
    c_initiale, c_destination=de_code_a_num_case(c_initiale),de_code_a_num_case(c_destination)

    colonne_dep, ligne_dep,colonne_des, ligne_des=c_initiale[1],c_initiale[0],c_destination[1],c_destination[0]
    # Can't move from an empty square
    if echiquier[ligne_dep][colonne_dep]=="":
        return False
    # Can't capture your own piece
    if echiquier[ligne_dep][colonne_dep].endswith('B') and  echiquier[ligne_des][colonne_des].endswith('B'):
        return False
    if echiquier[ligne_dep][colonne_dep].endswith('N') and  echiquier[ligne_des][colonne_des].endswith('N'):
        return False  
    # Destination must be inside the board
    good_values=[0,1,2,3,4,5,6,7]
    if (colonne_dep not in good_values) or (colonne_des not in good_values) or (ligne_dep not in good_values) or (ligne_des not in good_values):
        return False
    x=echiquier[ligne_dep][colonne_dep]
    # Can't move the opponent's piece
    if  not  echiquier[ligne_dep][colonne_dep].endswith(player):
        return False
    match x:
        case "tour-N":
              return logical_xor((colonne_dep == colonne_des) , (ligne_dep == ligne_des))  # straight line only
        case "tour-B":
              return logical_xor((colonne_dep==colonne_des) , (ligne_dep==ligne_des))    
        case "fou-N":
              return ((abs(colonne_dep - colonne_des) == abs(ligne_dep - ligne_des)) )  # diagonal only
        case "fou-B":
              return ((abs(colonne_dep - colonne_des) == abs(ligne_dep - ligne_des)) )  
        case "chevalier-N":
              return (abs(colonne_dep - colonne_des), abs(ligne_dep - ligne_des)) in [(2,1), (1,2)]  # L-shape
        case "chevalier-B":
              return (abs(colonne_dep - colonne_des), abs(ligne_dep - ligne_des)) in [(2,1), (1,2)]
        case "roi-B":
              return (abs(colonne_dep - colonne_des), abs(ligne_dep - ligne_des)) in [(1,1), (1,0),(0,1)]  # one square any direction
        case "roi-N":
              return (abs(colonne_dep - colonne_des), abs(ligne_dep - ligne_des)) in [(1,1), (1,0),(0,1)]
        case "reine-B":
              return((abs(colonne_dep - colonne_des) == abs(ligne_dep - ligne_des))) or ((colonne_dep != colonne_des) and (ligne_dep == ligne_des)) or ((colonne_dep == colonne_des) and (ligne_dep != ligne_des))  # diagonal + straight
        case "reine-N":
              return((abs(colonne_dep - colonne_des) == abs(ligne_dep - ligne_des))) or ((colonne_dep != colonne_des) and (ligne_dep == ligne_des)) or ((colonne_dep == colonne_des) and (ligne_dep != ligne_des))
        case "pion-N":
              # moves forward (increasing row), can capture diagonally, double step from row 1
              return ((((ligne_des-ligne_dep)==1) and (colonne_dep==colonne_des) and (echiquier[ligne_des][colonne_des]=="")) or (((ligne_des-ligne_dep)==1) and (abs(colonne_dep-colonne_des) ==1) and (echiquier[ligne_des][colonne_des]!="")) or (((ligne_des-ligne_dep)==2) and (colonne_dep==colonne_des) and (ligne_dep == 1) )  )
        case "pion-B":
              # moves forward (decreasing row), can capture diagonally, double step from row 6
              return ((((ligne_des-ligne_dep)==-1) and (colonne_dep==colonne_des)and (echiquier[ligne_des][colonne_des]=="")) or (((ligne_des-ligne_dep)==-1) and (abs(colonne_dep-colonne_des) ==1) and (echiquier[ligne_des][colonne_des]!="")) or (((ligne_des-ligne_dep)==-2) and (colonne_dep==colonne_des) and (ligne_dep == 6) )   )                
rep = "oui"


while rep == "oui":

 
    # White player's turn
    print("C'est au tour du joueur BLANC tes pions sont en ligne 7 :")
       
    move=False
    while not move:
        case_a_bouger_j1 = input("Quel est le code de la pièce à déplacer ? ")
        
      
        nouvelle_case_j1 = input("Quel est le code de la case destinataire ? ")
        move = checker_le_move(echiquier,case_a_bouger_j1, nouvelle_case_j1,"B")
        if (not move) :
            print("Coup invalide réessaie")

    mise_a_jour_echiquier(echiquier, case_a_bouger_j1, nouvelle_case_j1)
    remplir_et_tracer_echiquier(f, echiquier) 
    re_afficher(f)
    
    # Black player's turn
    print("C'est au tour du joueur NOIR tes pions sont en ligne 2:")
   
    move2=False
    while not move2:
    
        case_a_bouger_j2 = input("Quel est le code de la pièce à déplacer ? ")

       
        nouvelle_case_j2 = input("Quel est le code de la case destinataire ? ")
        move2 =checker_le_move(echiquier,case_a_bouger_j2, nouvelle_case_j2, "N")
        if (not move2) :
            print("Coup invalide réessaie")

   
    mise_a_jour_echiquier(echiquier, case_a_bouger_j2, nouvelle_case_j2)

    remplir_et_tracer_echiquier(f, echiquier)
    re_afficher(f)
  
    rep = input("Souhaitez-vous continuer ? Taper oui pour continuer, sinon taper non : ")




attendre_fermeture(f)

    
    



        
        
        
