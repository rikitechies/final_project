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
