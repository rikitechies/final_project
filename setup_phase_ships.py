import tkinter as tk
from tkinter import messagebox
from game_engine import Board, Ship, Player, AI

class GamePhase:
    def init(self, master, player: Player, ai: AI):
        self.master = master
        self.player = player
        self.ai = ai
        self.current_player = "player"  # починає гравець
        self.cell_size = 30

        self.create_widgets()

    def create_widgets(self):
        """Створення ігрових полів гравця та AI"""
        self.game_frame = tk.Frame(self.master)
        self.game_frame.pack()

        # Поле гравця
        player_frame = tk.Frame(self.game_frame)
        player_frame.grid(row=1, column=0, padx=20)
        tk.Label(player_frame, text="Ваше поле", font=("Arial", 12)).pack()
        self.player_canvas = tk.Canvas(player_frame, width=320, height=320, bg="blue")
        self.player_canvas.pack()
        self.draw_board(self.player_canvas, self.player.board)

        # Поле комп'ютера
        ai_frame = tk.Frame(self.game_frame)
        ai_frame.grid(row=1, column=1, padx=20)
        tk.Label(ai_frame, text="Поле комп'ютера", font=("Arial", 12)).pack()
        self.ai_canvas = tk.Canvas(ai_frame, width=320, height=320, bg="blue")
        self.ai_canvas.pack()
        self.draw_board(self.ai_canvas, self.ai.board, hide_ships=True)

        # Обробка кліків
        self.ai_canvas.bind("<Button-1>", self.handle_player_shot)

    def draw_board(self, canvas: tk.Canvas, board: Board, hide_ships: bool = False):
        """Малює поле з кораблями та пострілами"""
        canvas.delete("all")
        size = board.size
        cs = self.cell_size

        # Нумерація
        for col in range(size):
            x = col * cs + cs // 2 + 20
            canvas.create_text(x, 10, text=chr(65 + col), font=("Arial", 10), fill="white")
        for row in range(size):
            y = row * cs + cs // 2 + 20
            canvas.create_text(10, y, text=str(row + 1), font=("Arial", 10), fill="white")

        # Клітинки
        for row in range(size):
            for col in range(size):
                x1 = col * cs + 20
                y1 = row * cs + 20
                x2 = x1 + cs
                y2 = y1 + cs
                canvas.create_rectangle(x1, y1, x2, y2, outline="white")

                # Кораблі
                if not hide_ships:
                    for ship in board.ships:
                        if (row, col) in ship.positions:
                            canvas.create_rectangle(x1, y1, x2, y2, fill="gray", outline="white")

                # Постріли
                if (row, col) in board.shots:
                    if any(ship.hit(row, col) for ship in board.ships):
                        canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="red")
                    else:
                        canvas.create_line(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="white")
                        canvas.create_line(x1 + 5, y2 - 5, x2 - 5, y1 + 5, fill="white")
