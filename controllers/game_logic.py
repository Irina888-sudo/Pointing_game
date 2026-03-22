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


def manage_click(event):
    print(f"CLICK DÉTECTÉ : x={event.x}, y={event.y}")
    
    global grille, n, canvas_grille, joueur_actuel
    r = 5
    pas = 400 / n
    resultat = calculate_placement_point(event.x, event.y, pas)

    if resultat is not None:
        hx, hy = resultat
       
        if 0 <= hx <= n and 0 <= hy <= n and grille[hx][hy] == 0:
            x_inter, y_inter = hx * pas, hy * pas
            couleur = "blue" if joueur_actuel == 1 else "red"
            
          
            canvas_grille.create_oval(x_inter-r, y_inter-r, x_inter+r, y_inter+r, fill=couleur)
            
            
            grille[hx][hy] = joueur_actuel
            joueur_actuel = 3 - joueur_actuel
def configure_button(form_elements, root):

    def action_clic():
        global grille, joueur_actuel, n, canvas_grille
        try:
            nom1 = form_elements["entry_name1"].get()
            nom2 = form_elements["entry_name2"].get()
            n = int(form_elements["entry_grids"].get())
            joueur_actuel = 1
            grille = [[0 for _ in range(n + 1)] for _ in range(n + 1)]

            if n < 9:
                
                messagebox.showwarning("Trop petit !", "La grille doit faire au moins 9.")
                return

           
            canvas_grille = create_game_window(n, root)

           
            canvas_grille.bind("<Button-1>", manage_click)

        except ValueError:
            messagebox.showerror("Erreur", "La taille de la grille doit être un nombre !")

    form_elements["btn_confirm"].config(command=action_clic)