import tkinter as tk

from sympy import root  
        
def create_game_window(n, root): 
    
    for widget in root.winfo_children():
        widget.destroy()

   
    root.geometry("800x600") 

    
    main_frame = tk.Frame(root, bg="#1a1a1a") 
    main_frame.pack(expand=True, fill="both") 

  
    frame_canon = tk.Frame(main_frame, bg="#060A3F", width=100, height=400)
    frame_canon.pack(side="left", padx=40, pady=40)

    
    canvas_grille = tk.Canvas(main_frame, width=400, height=400, bg="white", highlightthickness=2, highlightbackground="#00ccff")
    canvas_grille.pack(side="left", padx=20)
    
    
    draw_grid(canvas_grille, n, 400)
    return canvas_grille

def draw_grid(canvas, n, total_size):
    pas = total_size / n
    for i in range(n + 1):
        
        canvas.create_line(0, i * pas, total_size, i * pas, fill="black")
      
        canvas.create_line(i * pas, 0, i * pas, total_size, fill="black")