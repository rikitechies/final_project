import random

class Ship:
    def __init__(self, size: int, positions:[int, int]):
        self.size = size
        self.positions = positions
        self.hits = set()

    def is_sunk(self):
        return len(self.hits) == self.size

    def hit(self, row: int, col: int):
        if (row, col) in self.positions:
            self.hits.add((row, col))
            return True
        return False

class Board:
    def __init__(self, size: int = 10):
        self.size = size
        self.ships = []
        self.shots = set()

    def place_ship(self, ship: Ship):
        for r, c in ship.positions:
            if not (0 <= r < self.size and 0 <= c < self.size):
                return False
            for existing_ship in self.ships:
                for er, ec in existing_ship.positions:
                    if abs(er - r) <= 1 and abs(ec - c) <= 1:
                        return False
        self.ships.append(ship)
        return True

    def receive_shot(self, row: int, col: int):
        if (row, col) in self.shots:
            return False, None
        self.shots.add((row, col))
        for ship in self.ships:
            if ship.hit(row, col):
                return True, ship
        return False, None

    def all_ships_sunk(self):
        return all(ship.is_sunk() for ship in self.ships)

class Player:
    def __init__(self, name: str):
        self.name = name
        self.board = Board()

class AI(Player):
    def __init__(self):
        super().__init__("Комп'ютер")
        self.place_ships_randomly()

    def place_ships_randomly(self):
        ship_sizes = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        for size in ship_sizes:
            placed = False
            while not placed:
                orientation = random.choice(["horizontal", "vertical"])
                if orientation == "horizontal":
                    row = random.randint(0, self.board.size - 1)
                    col = random.randint(0, self.board.size - size)
                    positions = [(row, col + i) for i in range(size)]
                else:
                    row = random.randint(0, self.board.size - size)
                    col = random.randint(0, self.board.size - 1)
                    positions = [(row + i, col) for i in range(size)]
                ship = Ship(size, positions)
                placed = self.board.place_ship(ship)

    def make_move(self, opponent_board: Board):
        while True:
            row = random.randint(0, self.board.size - 1)
            col = random.randint(0, self.board.size - 1)
            if (row, col) not in opponent_board.shots:
                return row, col