import tkinter as tk
from tkinter import ttk


def create_form(main_window):

    main_window.title("Game configuration")
    main_window.geometry("420x300")
    main_window.resizable(False, False)

    lbl_titre = tk.Label(
        main_window,
        text="Game configuration",
        font=("Arial", 16, "bold"),
        pady=15
    )
    lbl_titre.pack()

    
    frame_champs = ttk.Frame(main_window, padding="20 10")
    frame_champs.pack(fill="both", expand=True)

   
    lbl_name1 = ttk.Label(frame_champs, text="Player 1's Name :")
    lbl_name1.grid(row=0, column=0, sticky="e", padx=10, pady=8)

    entry_name1 = ttk.Entry(frame_champs, width=35)
    entry_name1.grid(row=0, column=1, pady=8)
    entry_name1.focus()   

   
    lbl_name2 = ttk.Label(frame_champs, text="Player 2's Name :")
    lbl_name2.grid(row=1, column=0, sticky="e", padx=10, pady=8)

    entry_name2 = ttk.Entry(frame_champs, width=35)
    entry_name2.grid(row=1, column=1, pady=8)

   
    lbl_grids = ttk.Label(frame_champs, text="Grid Size :")
    lbl_grids.grid(row=2, column=0, sticky="e", padx=10, pady=8)
    entry_grids = ttk.Entry(frame_champs, width=35)
    entry_grids.grid(row=2, column=1, pady=8)

   
    btn_confirm = ttk.Button(
        frame_champs,
        text="Play",
        style="Accent.TButton",
        width=20
    )
    btn_confirm.grid(row=3, column=0, columnspan=2, pady=25)

    return {
        "entry_name1": entry_name1,
        "entry_name2": entry_name2,
        "entry_grids": entry_grids,
        "btn_confirm": btn_confirm
    }