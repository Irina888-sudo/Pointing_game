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


# def configure_button(form_elements, root):
    
#     def action_clic():
#         global grille, joueur_actuel, n, canvas_grille
#         try:
#             nom1 = form_elements["entry_name1"].get()
#             nom2 = form_elements["entry_name2"].get()
#             n = int(form_elements["entry_grids"].get())
#             joueur_actuel = 1
#             grille = [[0 for _ in range(n + 1)] for _ in range(n + 1)]

#             if n < 9:
#                 messagebox.showwarning("Trop petit !", "La grille doit faire au moins 9.")
#                 return

#             for widget in root.winfo_children():
#                 widget.destroy()

#             canvas_canon = tk.Canvas(root, width=100, height=500, bg="grey")
#             canvas_canon.pack(side="left")

#             canvas_grille = tk.Canvas(root, width=500, height=500, bg="white")
#             canvas_grille.pack(side="right", expand=True)

#             # ✅ On bind le clic AVANT d'appeler create_game_window
#             canvas_grille.bind("<Button-1>", manage_click)

#             # ✅ On passe canvas_grille à create_game_window pour qu'elle
#             #    dessine sur CE canvas et ne le recrée pas
#             create_game_window(n, root, canvas_grille)

#         except ValueError:
#             messagebox.showerror("Erreur", "La taille de la grille doit être un nombre !")

#     form_elements["btn_confirm"].config(command=action_clic)

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

            # ✅ On récupère le canvas_grille retourné par create_game_window
            canvas_grille = create_game_window(n, root)

            # ✅ On binde le clic sur le bon canvas
            canvas_grille.bind("<Button-1>", manage_click)

        except ValueError:
            messagebox.showerror("Erreur", "La taille de la grille doit être un nombre !")

    form_elements["btn_confirm"].config(command=action_clic)