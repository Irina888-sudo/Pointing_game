
class GameConfig:
    def __init__(self, j1, j2, n):
        self.j1 = j1
        self.j2 = j2
        self.n = n
        self.joueur_actuel = 1
        self.score_j1 = 0
        self.score_j2 = 0
        self.grille = [[0 for _ in range(n + 1)] for _ in range(n + 1)]
        
        
        self.label_score_j1 = None
        self.label_score_j2 = None
        self.label_tour = None
        self.canvas = None
        