import tkinter as tk
from tkinter import ttk
from models import config
from models.database import mettre_a_jour_partie, sauvegarder_partie
from views.game_view import create_game_window, draw_grid
from tkinter import messagebox
from views.game_view import draw_canon


canon_y_pixel = 200

def calculate_placement_point(x_clic, y_clic, pas, marge=15):
    hint_x = round(x_clic / pas)
    hint_y = round(y_clic / pas)
    
    x_intersection = hint_x * pas
    y_intersection = hint_y * pas
    
    distance_x = abs(x_clic - x_intersection)
    distance_y = abs(y_clic - y_intersection)
    
    if distance_x <= marge and distance_y <= marge:
        return hint_x, hint_y
    else:
        return None


def compter_direction(x, y, dx, dy, config): 
    compte = 0
    nx, ny = x + dx, y + dy
    
    while 0 <= nx <= config.n and 0 <= ny <= config.n and config.grille[nx][ny] == config.joueur_actuel:
        compte += 1
        nx += dx
        ny += dy
    return compte, nx - dx, ny - dy



def manage_click(event, config):
    
    pas = 400 / config.n
    resultat = calculate_placement_point(event.x, event.y, pas)

    if resultat is None:
        return

    hx, hy = resultat
    
    if 0 <= hx <= config.n and 0 <= hy <= config.n and config.grille[hx][hy] == 0:
        
        couleur = "blue" if config.joueur_actuel == 1 else "red"
        r = 5
        
        config.canvas.create_oval(hx*pas-r, hy*pas-r, hx*pas+r, hy*pas+r, fill=couleur)
        config.grille[hx][hy] = config.joueur_actuel

        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        win_found = False
        
        for dx, dy in directions:
            
            nb1, x1, y1 = compter_direction(hx, hy, dx, dy, config)
            nb2, x2, y2 = compter_direction(hx, hy, -dx, -dy, config)

            if (nb1 + nb2 + 1) >= 5:
                config.canvas.create_line(x1*pas, y1*pas, x2*pas, y2*pas, fill="#00ccff", width=5)
                
                if config.joueur_actuel == 1: 
                    config.score_j1 += 1
                else: 
                    config.score_j2 += 1
                win_found = True

        if win_found:
            
            config.label_score_j1.config(text=f"J1 : {config.score_j1}")
            config.label_score_j2.config(text=f"J2 : {config.score_j2}")
            messagebox.showinfo("Gagné !", f"Joueur {config.joueur_actuel} marque un point !")
    
        config.joueur_actuel = 3 - config.joueur_actuel
        nom_actuel = config.j1 if config.joueur_actuel == 1 else config.j2
        config.label_tour.config(text=f"Tour : {nom_actuel}")
    


def move_canon(event, config):
    y_pixel = event.y
    draw_canon(config.canvas_canon, y_pixel)

    config.canon_y_pixel = y_pixel

def fire_canon(puissance, config):
    """
    Règle : Ctrl + (1 à 9) définit la puissance (colonne visée).
    """
    pas = 400 / config.n
    
    col_x = round((puissance - 1) * config.n / 8)

    y_actuel = getattr(config, 'canon_y_pixel', 200)
    ligne_y = round(y_actuel / pas)
    
    ligne_y = max(0, min(config.n, ligne_y))

    id_adverse = 2 if config.joueur_actuel == 1 else 1

    if config.grille[col_x][ligne_y] == id_adverse:
     
        x_pixel = col_x * pas
        y_pixel = ligne_y * pas
        
        items = config.canvas.find_closest(x_pixel, y_pixel)
        
        if items:
            config.canvas.delete(items[0]) 
        config.grille[col_x][ligne_y] = 0
    
    config.joueur_actuel = 3 - config.joueur_actuel
    config.label_tour.config(text=f"Tour : {config.j2 if config.joueur_actuel == 2 else config.j1}")
        
    


def terminer_partie(config):
    s1, s2 = config.score_j1, config.score_j2
    n1, n2 = config.j1, config.j2

    if s1 > s2:
        gagnant_msg = f"{n1} gagne avec {s1} point(s) !"
    elif s2 > s1:
        gagnant_msg = f"{n2} gagne avec {s2} point(s) !"
    else:
        gagnant_msg = f"Égalité ! ({s1} partout)"

    if config.partie_id is not None:
        mettre_a_jour_partie(config)  
    else:
        sauvegarder_partie(config)    

    messagebox.showinfo("Fin de partie", gagnant_msg)
def restaurer_visuel_grille(config):
    """Parcourt la config.grille et dessine les pions correspondants"""
    pas = 400 / config.n
    r = 5 
    
    for x in range(config.n + 1):
        for y in range(config.n + 1):
            valeur = config.grille[x][y]
            if valeur != 0:
               
                px = x * pas
                py = y * pas
                couleur = "blue" if valeur == 1 else "red"
                
               
                config.canvas.create_oval(px-r, py-r, px+r, py+r, fill=couleur)
        
def charger_partie_selectionnee(donnees_mongo, root, config_actuelle):
 
    config_actuelle.n = donnees_mongo['n']
    config_actuelle.grille = donnees_mongo['grille']
    config_actuelle.joueur_actuel = donnees_mongo['joueur_actuel']
    config_actuelle.j1 = donnees_mongo['joueur1']
    config_actuelle.j2 = donnees_mongo['joueur2']
    config_actuelle.score_j1 = donnees_mongo.get('score_j1', 0)
    config_actuelle.score_j2 = donnees_mongo.get('score_j2', 0)
    config_actuelle.partie_id = donnees_mongo['_id']
    
    from views.game_view import create_game_window
    def finir():
        terminer_partie(config_actuelle)
        root.destroy()
    
    create_game_window(root, config_actuelle, finir)


    restaurer_visuel_grille(config_actuelle)
    config_actuelle.canvas.bind("<Button-1>", lambda e: manage_click(e, config_actuelle))
    
    config_actuelle.canvas.bind("<Motion>", lambda e: move_canon(e, config_actuelle))

    for i in range(1, 10):
        root.bind(f"<Control-Key-{i}>", lambda e, p=i: fire_canon(p, config_actuelle))
    