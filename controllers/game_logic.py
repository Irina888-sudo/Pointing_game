import tkinter as tk
from tkinter import ttk
from models import config
from models.database import sauvegarder_partie
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
    
    
def verifier_alignement(x, y, couleur_joueur, dx, dy):
    """Compte les pions identiques dans une direction donnée (dx, dy)"""
    compte = 0
    nx, ny = x + dx, y + dy
    
    while 0 <= nx <= n and 0 <= ny <= n and grille[nx][ny] == couleur_joueur:
        compte += 1
        nx += dx
        ny += dy
    return compte, nx - dx, ny - dy



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
        
        
def bind_canon(root, canvas_grille):
    """Bind la souris sur la grille et Ctrl+1~9"""
    
    canvas_grille.bind("<Motion>", move_canon)

    for i in range(1, 10):
        root.bind(f"<Control-Key-{i}>", lambda e, p=i: fire_canon(p))


def terminer_partie(config):
    s1, s2 = config.score_j1, config.score_j2
    n1, n2 = config.j1, config.j2

    if s1 > s2:
        gagnant_msg = f"{n1} gagne avec {s1} point(s) !"
    elif s2 > s1:
        gagnant_msg = f"{n2} gagne avec {s2} point(s) !"
    else:
        gagnant_msg = f"Égalité ! ({s1} partout)"
    
    sauvegarder_partie(n1, n2, s1, s2)
    messagebox.showinfo("Fin de partie", gagnant_msg)