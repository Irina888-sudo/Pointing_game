import tkinter as tk
from tkinter import ttk, messagebox
from models.config import GameConfig 

def create_form(main_window, on_submit_callback):
    main_window.title("Game configuration")
    main_window.geometry("420x340") 
    main_window.resizable(False, False)

    
    lbl_titre = tk.Label(main_window, text="Game configuration", font=("Arial", 16, "bold"), pady=15)
    lbl_titre.pack()

    frame_champs = ttk.Frame(main_window, padding="20 10")
    frame_champs.pack(fill="both", expand=True)

    # --- TES CHAMPS ---
    lbl_name1 = ttk.Label(frame_champs, text="Player 1's Name :")
    lbl_name1.grid(row=0, column=0, sticky="e", padx=10, pady=8)
    entry_name1 = ttk.Entry(frame_champs, width=35)
    entry_name1.grid(row=0, column=1, pady=8)

    lbl_name2 = ttk.Label(frame_champs, text="Player 2's Name :")
    lbl_name2.grid(row=1, column=0, sticky="e", padx=10, pady=8)
    entry_name2 = ttk.Entry(frame_champs, width=35)
    entry_name2.grid(row=1, column=1, pady=8)

    lbl_grids = ttk.Label(frame_champs, text="Grid Size :")
    lbl_grids.grid(row=2, column=0, sticky="e", padx=10, pady=8)
    entry_grids = ttk.Entry(frame_champs, width=35)
    entry_grids.grid(row=2, column=1, pady=8)

    # --- LA LOGIQUE DE VALIDATION ---
    def valider():
        try:
            
            n_val = int(entry_grids.get())
            nom1 = entry_name1.get().strip() or "Joueur 1"
            nom2 = entry_name2.get().strip() or "Joueur 2"

            if n_val < 5 or n_val > 30:
                raise ValueError("La taille doit être entre 5 et 30.")

           
            config = GameConfig(nom1, nom2, n_val)
            
           
            on_submit_callback(config)

        except ValueError as e:
            messagebox.showerror("Erreur", f"Entrée invalide : {e}")

    # --- LE BOUTON ---
    btn_confirm = ttk.Button(
        frame_champs,
        text="Play",
        width=20,
        command=valider 
    )
    btn_confirm.grid(row=3, column=0, columnspan=2, pady=25)

   