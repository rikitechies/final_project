import tkinter as tk
from game_engine import Player, AI
from setup_phase import SetupPhase
from game_phase import GamePhase

class BattleshipGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Морський бій")
        self.player = Player("Гравець")
        self.ai = AI()

        self.setup = SetupPhase(self.root, self.player, self.start_game)
        self.root.mainloop()

    def start_game(self):
        self.game = GamePhase(self.root, self.player, self.ai)

if __name__ == "__main__":
    BattleshipGame()
