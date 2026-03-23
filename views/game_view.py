import tkinter as tk


def create_game_window(n, root, terminer_callback):
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("800x600")

    main_frame = tk.Frame(root, bg="#1a1a1a")
    main_frame.pack(expand=True, fill="both")
    
                                                                                                                                                                              
    canvas_canon = tk.Canvas(main_frame, width=100, height=400, bg="#060A3F",
                              highlightthickness=0)
    canvas_canon.pack(side="left", padx=10, pady=40)
    draw_canon(canvas_canon, 200)  # Position initiale au milieu

    frame_scores = tk.Frame(main_frame, bg="#1a1a1a")
    frame_scores.pack(side="left", fill="y", padx=5)

    label_score_j1 = tk.Label(frame_scores, text="J1 : 0", fg="blue",
                               bg="#1a1a1a", font=("Arial", 14))
    label_score_j1.pack(pady=10)

    label_score_j2 = tk.Label(frame_scores, text="J2 : 0", fg="red",
                               bg="#1a1a1a", font=("Arial", 14))
    label_score_j2.pack(pady=10)
    
    label_tour = tk.Label(frame_scores, text="Tour : J", fg="black",
                       bg="#5afdda", font=("Arial", 12))
    label_tour.pack(pady=10)

    canvas_grille = tk.Canvas(main_frame, width=400, height=400, bg="white",
                               highlightthickness=2, highlightbackground="#00ccff")
    canvas_grille.pack(side="left", padx=20)

    draw_grid(canvas_grille, n, 400)
    
    
    btn_terminer = tk.Button(main_frame, text="Terminer", font=("Arial", 12),
                              bg="#46f124", fg="black",
                              command=terminer_callback)
    btn_terminer.pack(side="bottom", pady=10)
    
    
    return canvas_grille, canvas_canon, label_score_j1, label_score_j2, label_tour, btn_terminer

   


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