import tkinter as tk
from tkinter import messagebox
from models.config import GameConfig
from models.database import tester_connexion
from views.setup_view import create_form
from views.game_view import create_game_window
from controllers.game_logic import manage_click
from controllers.game_logic import move_canon
from controllers.game_logic import fire_canon
from controllers.game_logic import terminer_partie

def start_game(root, config):
   
    def finir():
        terminer_partie(config)
        root.destroy()

    create_game_window(root, config, finir)
   
    config.canvas.bind("<Button-1>", lambda e: manage_click(e, config))
    
   
    config.canvas.bind("<Motion>", lambda e: move_canon(e, config))

    for i in range(1, 10):
        root.bind(f"<Control-Key-{i}>", lambda e, p=i: fire_canon(p, config))
    root.protocol("WM_DELETE_WINDOW", finir)
  
def start_app():
    root = tk.Tk()
    root.title("Morpion Expert")

    if not tester_connexion():
        messagebox.showwarning("Mode Hors-ligne", 
            "MongoDB est inaccessible. Vos scores ne seront pas sauvegardés.")

    create_form(root, lambda config: start_game(root, config))
    
    root.mainloop()

if __name__ == "__main__":
    start_app()