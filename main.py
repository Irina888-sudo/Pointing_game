from models.config import GameConfig
import tkinter as tk
from views.setup_view import create_form
from controllers.game_logic import configure_button


def start_app():
    root = tk.Tk()
    root.title("Game configuration")

    form_elements = create_form(root)


    configure_button(form_elements, root)

    root.mainloop()

if __name__ == "__main__":
    start_app()