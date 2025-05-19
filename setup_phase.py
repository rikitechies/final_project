import tkinter as tk
from tkinter import messagebox
from game_engine import Ship, Player

class SetupPhase:
    def __init__(self, master, player: Player, on_setup_complete):
        self.master = master
        self.player = player
        self.on_setup_complete = on_setup_complete

        self.cell_size = 30
        self.selected_ship_size = None
        self.ship_orientation = "horizontal"
        self.ships_to_place = {4: 1, 3: 2, 2: 3, 1: 4}

        self.setup_frame = tk.Frame(self.master)
        self.setup_frame.pack()

        self.create_widgets()

    def create_widgets(self):
        """Створення віджетів для вибору кораблів і розміщення"""
        # Інформація
        self.info_label = tk.Label(self.setup_frame, text="Оберіть корабель", font=("Arial", 12))
        self.info_label.grid(row=0, column=0, columnspan=4, pady=10)

        # Лічильники кораблів
        self.ship_counters_frame = tk.Frame(self.setup_frame)
        self.ship_counters_frame.grid(row=1, column=0, columnspan=4)
        self.ship_counters = {}

        for i, size in enumerate([4, 3, 2, 1]):
            frame = tk.Frame(self.ship_counters_frame)
            frame.pack(side=tk.LEFT, padx=10)
            tk.Label(frame, text=f"Кораблі ({size}):").pack()
            counter = tk.Label(frame, text=str(self.ships_to_place[size]), font=("Arial", 12, "bold"))
            counter.pack()
            self.ship_counters[size] = counter

        # Кнопки вибору кораблів
        self.ship_buttons = []
        for i, size in enumerate([4, 3, 2, 1]):
            btn = tk.Button(self.setup_frame, text=f"Корабель ({size})", 
                            command=lambda s=size: self.select_ship_size(s),
                            state=tk.NORMAL if self.ships_to_place[size] > 0 else tk.DISABLED)
            btn.grid(row=2, column=i, padx=5)
            self.ship_buttons.append(btn)

        # Орієнтація
        self.orientation_btn = tk.Button(self.setup_frame, text="Орієнтація: Горизонтальна",
                                         command=self.toggle_orientation)
        self.orientation_btn.grid(row=3, column=0, columnspan=4, pady=10)

        # Поле гравця
        self.player_board_canvas = tk.Canvas(self.setup_frame, width=320, height=320, bg="blue")
        self.player_board_canvas.grid(row=4, column=0, columnspan=4)
        self.draw_board(self.player_board_canvas, self.player.board)
        self.player_board_canvas.bind("<Button-1>", self.place_ship_click)
        self.player_board_canvas.bind("<Motion>", self.show_ship_preview)

        # Кнопка старту гри
        self.start_button = tk.Button(self.setup_frame, text="Почати гру",
                                      command=self.complete_setup, state=tk.DISABLED)
        self.start_button.grid(row=5, column=0, columnspan=4, pady=10)

    def update_ship_counters(self):
        for size, counter in self.ship_counters.items():
            counter.config(text=str(self.ships_to_place[size]))
        for i, size in enumerate([4, 3, 2, 1]):
            self.ship_buttons[i].config(
                state=tk.NORMAL if self.ships_to_place[size] > 0 else tk.DISABLED)

    def select_ship_size(self, size):
        self.selected_ship_size = size
        self.update_info_label()

    def toggle_orientation(self):
        self.ship_orientation = "vertical" if self.ship_orientation == "horizontal" else "horizontal"
        self.orientation_btn.config(
            text=f"Орієнтація: {'Вертикальна' if self.ship_orientation == 'vertical' else 'Горизонтальна'}")

    def update_info_label(self):
        if self.selected_ship_size:
            self.info_label.config(text=f"Оберіть позицію для корабля ({self.selected_ship_size})")
        else:
            remaining = sum(self.ships_to_place.values())
            if remaining > 0:
                self.info_label.config(text=f"Оберіть корабель (залишилось: {remaining})")
            else:
                self.info_label.config(text="Всі кораблі розміщені!")

    def draw_board(self, canvas: tk.Canvas, board, hide_ships: bool = False):
        """Малює поле гравця та попередній перегляд кораблів"""
        canvas.delete("all")
        cs = self.cell_size

        # Нумерація
        for col in range(board.size):
            x = col * cs + cs // 2 + 20
            canvas.create_text(x, 10, text=chr(65 + col), font=("Arial", 10), fill="white")
        for row in range(board.size):
            y = row * cs + cs // 2 + 20
            canvas.create_text(10, y, text=str(row + 1), font=("Arial", 10), fill="white")

        # Клітинки
        for row in range(board.size):
            for col in range(board.size):
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

    def show_ship_preview(self, event):
        """Попередній перегляд корабля"""
        if not self.selected_ship_size:
            return

        self.draw_board(self.player_board_canvas, self.player.board)
        col = (event.x - 20) // self.cell_size
        row = (event.y - 20) // self.cell_size

        if col < 0 or row < 0:
            return

        if self.ship_orientation == "horizontal":
            if col + self.selected_ship_size > 10: return
            positions = [(row, col + i) for i in range(self.selected_ship_size)]
        else:
            if row + self.selected_ship_size > 10: return
            positions = [(row + i, col) for i in range(self.selected_ship_size)]

        for r, c in positions:
            x1 = c * self.cell_size + 20
            y1 = r * self.cell_size + 20
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            self.player_board_canvas.create_rectangle(
                x1, y1, x2, y2, fill="gray", outline="white", stipple="gray50")

    def place_ship_click(self, event):
        """Розміщення корабля за кліком миші"""
        if not self.selected_ship_size:
            return

        col = (event.x - 20) // self.cell_size
        row = (event.y - 20) // self.cell_size

        if not (0 <= row < 10 and 0 <= col < 10):
            return

        if self.ship_orientation == "horizontal":
            if col + self.selected_ship_size > 10:
                messagebox.showerror("Помилка", "Корабель виходить за межі поля!")
                return
            positions = [(row, col + i) for i in range(self.selected_ship_size)]
        else:
            if row + self.selected_ship_size > 10:
                messagebox.showerror("Помилка", "Корабель виходить за межі поля!")
                return
            positions = [(row + i, col) for i in range(self.selected_ship_size)]

        ship = Ship(self.selected_ship_size, positions)
        if self.player.board.place_ship(ship):
            self.ships_to_place[self.selected_ship_size] -= 1
            self.selected_ship_size = None
            self.update_ship_counters()
            self.update_info_label()
            self.draw_board(self.player_board_canvas, self.player.board)

            if sum(self.ships_to_place.values()) == 0:
                self.start_button.config(state=tk.NORMAL)
        else:
            messagebox.showerror("Помилка", "Неможливо розмістити корабель тут!")

    def complete_setup(self):
        """Завершення фази розміщення"""
        self.setup_frame.pack_forget()
        self.on_setup_complete()
