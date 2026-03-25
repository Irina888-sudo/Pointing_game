import tkinter as tk
from models.database import get_historique

def create_game_window(root, config, terminer_callback):
    from controllers.game_logic import charger_partie_selectionnee
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("800x600")
    main_frame = tk.Frame(root, bg="#1a1a1a")
    main_frame.pack(expand=True, fill="both")
    
    # 1. Canvas Canon
    config.canvas_canon = tk.Canvas(main_frame, width=100, height=400, bg="#060A3F", highlightthickness=0)
    config.canvas_canon.pack(side="left", padx=10, pady=40)
    draw_canon(config.canvas_canon, 200)

    # 2. Frame Scores & Labels
    frame_scores = tk.Frame(main_frame, bg="#1a1a1a")
    frame_scores.pack(side="left", fill="y", padx=5)

    config.label_score_j1 = tk.Label(frame_scores, text=f"{config.j1} : 0", fg="blue", bg="#1a1a1a", font=("Arial", 14))
    config.label_score_j1.pack(pady=10)

    config.label_score_j2 = tk.Label(frame_scores, text=f"{config.j2} : 0", fg="red", bg="#1a1a1a", font=("Arial", 14))
    config.label_score_j2.pack(pady=10)
    
    config.label_tour = tk.Label(frame_scores, text=f"Tour : {config.j1}", fg="black", bg="#5afdda", font=("Arial", 12))
    config.label_tour.pack(pady=10)

    # 3. Canvas Grille
    config.canvas = tk.Canvas(main_frame, width=400, height=400, bg="white", highlightthickness=2, highlightbackground="#00ccff")
    config.canvas.pack(side="left", padx=20)
    
    
    draw_grid(config.canvas, config.n, 400)
    
    
    btn_terminer = tk.Button(main_frame, text="Terminer", command=terminer_callback)
    btn_terminer.pack(side="bottom", pady=10)
    
   
    btn_history = tk.Button(
        main_frame, 
        text="Historique", 
        command=lambda: show_history_window(root, lambda p: charger_partie_selectionnee(p, root, config))
    )
    btn_history.pack(side="bottom", pady=5)

def draw_canon(canvas_canon, y_pixel):
    """Dessine le canon centré sur y_pixel"""
    canvas_canon.delete("canon")
    canvas_canon.create_rectangle(10, y_pixel - 10, 60, y_pixel + 10,
                                   fill="#aaaaaa", outline="white", tags="canon")
    canvas_canon.create_rectangle(55, y_pixel - 5, 90, y_pixel + 5,
                                   fill="#cccccc", outline="white", tags="canon")
    canvas_canon.create_oval(15, y_pixel + 8, 35, y_pixel + 22,
                              fill="#555555", outline="white", tags="canon")
    canvas_canon.create_oval(40, y_pixel + 8, 60, y_pixel + 22,
                              fill="#555555", outline="white", tags="canon")


def draw_grid(canvas, n, total_size):
    pas = total_size / n
    for i in range(n + 1):
        canvas.create_line(0, i * pas, total_size, i * pas, fill="black")
        canvas.create_line(i * pas, 0, i * pas, total_size, fill="black")
        
    

def show_history_window(root, on_load_callback):
    history_win = tk.Toplevel(root)
    history_win.title("Historique des parties")
    history_win.geometry("400x400")

    listbox = tk.Listbox(history_win, font=("Arial", 10))
    listbox.pack(fill="both", expand=True, padx=10, pady=10)

    parties = get_historique()
    for p in parties:
        n_taille = p.get('n', 'Inconnue')
        label = f"{p['date']} : {p['joueur1']} vs {p['joueur2']} (Taille: {n_taille})"
        listbox.insert(tk.END, label)
    
    def selectionner():
        index = listbox.curselection()
        if index:
            partie_choisie = parties[index[0]]
            history_win.destroy()
            on_load_callback(partie_choisie)
    
    btn_load = tk.Button(history_win, text="Reprendre", command=selectionner)
    btn_load.pack(pady=10)
    
    
            
