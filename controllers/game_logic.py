import tkinter as tk
from tkinter import ttk
from views.game_view import create_game_window, draw_grid
from tkinter import messagebox


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

def compter_direction(x, y, dx, dy, couleur):
    compte = 0
    nx, ny = x + dx, y + dy
    while 0 <= nx <= n and 0 <= ny <= n and grille[nx][ny] == couleur:
        compte += 1
        nx += dx
        ny += dy
    return compte, nx - dx, ny - dy

def manage_click(event):
    global grille, n, canvas_grille, joueur_actuel, score_j1, score_j2, label_score_j1, label_score_j2
    pas = 400 / n
    resultat = calculate_placement_point(event.x, event.y, pas)

    if resultat is None:
        return

    hx, hy = resultat
    
    if 0 <= hx <= n and 0 <= hy <= n and grille[hx][hy] == 0:
        # 1. Placement du pion
        couleur = "blue" if joueur_actuel == 1 else "red"
        r = 5
        canvas_grille.create_oval(hx*pas-r, hy*pas-r, hx*pas+r, hy*pas+r, fill=couleur)
        grille[hx][hy] = joueur_actuel

        # 2. Liste des directions
        directions = [
            (1, 0),  # Horizontal
            (0, 1),  # Vertical
            (1, 1),  # Diagonale \
            (1, -1)  # Diagonale /
        ]

        win_found = False
        for dx, dy in directions:
           
            nb1, x1, y1 = compter_direction(hx, hy, dx, dy, joueur_actuel)
            nb2, x2, y2 = compter_direction(hx, hy, -dx, -dy, joueur_actuel)

            if (nb1 + nb2 + 1) == 5:
               
                canvas_grille.create_line(x1*pas, y1*pas, x2*pas, y2*pas, fill="#00ccff", width=5)
                
                
                if joueur_actuel == 1: score_j1 += 1
                else: score_j2 += 1
                win_found = True

       
        if win_found:
            label_score_j1.config(text=f"J1 : {score_j1}")
            label_score_j2.config(text=f"J2 : {score_j2}")
            messagebox.showinfo("Gagné !", f"Joueur {joueur_actuel} marque un point !")
        
        else:
         joueur_actuel = 3 - joueur_actuel
    
def configure_button(form_elements, root):

    def action_clic():
        global grille, joueur_actuel, n, canvas_grille, score_j1, score_j2, label_score_j1, label_score_j2
        
        score_j1 = 0
        score_j2 = 0
        try:
            nom1 = form_elements["entry_name1"].get()
            nom2 = form_elements["entry_name2"].get()
            n = int(form_elements["entry_grids"].get())
            joueur_actuel = 1
            grille = [[0 for _ in range(n + 1)] for _ in range(n + 1)]

            if n < 9:
                
                messagebox.showwarning("Trop petit !", "La grille doit faire au moins 9.")
                return

           
            canvas_grille, label_score_j1, label_score_j2 = create_game_window(n, root)

            canvas_grille.bind("<Button-1>", manage_click)

        except ValueError:
            messagebox.showerror("Erreur", "La taille de la grille doit être un nombre !")

    form_elements["btn_confirm"].config(command=action_clic)
    
    
def verifier_alignement(x, y, couleur_joueur, dx, dy):
    """Compte les pions identiques dans une direction donnée (dx, dy)"""
    compte = 0
    nx, ny = x + dx, y + dy
    
    while 0 <= nx <= n and 0 <= ny <= n and grille[nx][ny] == couleur_joueur:
        compte += 1
        nx += dx
        ny += dy
    return compte, nx - dx, ny - dy