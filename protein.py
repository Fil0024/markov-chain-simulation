# protein.py
import random
import numpy as np
import config
import sys
import os

class Protein:
    """
    Reprezentuje łańcuch białkowy w modelu HP na siatce 3D.
    """
    def __init__(self, sequence: str, init_method: str = 'linear'):
        self.sequence = sequence.replace('E', '')
        self.length = len(self.sequence)
        self.coords = np.zeros((self.length, 3), dtype=int)
        
        if init_method == 'linear':
            self._initialize_linear()
        elif init_method == 'random':
            self._initialize_random_walk()
        elif init_method == 'seed':
            self._initialize_with_seed()
        else:
            raise ValueError("Nieznana metoda inicjalizacji. Wybierz 'linear' lub 'random'.")

        self.energy = self.calculate_energy()

    def _initialize_linear(self):
        for i in range(1, self.length):
            self.coords[i] = self.coords[i-1] + [1, 0, 0]

    def _initialize_random_walk(self):
        occupied = {tuple(self.coords[0])}
        directions = [
            np.array([1, 0, 0]), np.array([-1, 0, 0]),
            np.array([0, 1, 0]), np.array([0, -1, 0]),
            np.array([0, 0, 1]), np.array([0, 0, -1]),
        ]

        for i in range(1, self.length):
            random.shuffle(directions)
            for move in directions:
                new_pos = tuple(self.coords[i-1] + move)
                if new_pos not in occupied:
                    self.coords[i] = new_pos
                    occupied.add(new_pos)
                    break
            else:
                print("Ostrzeżenie: losowe błądzenie utknęło, próba ponowna.")
                self.__init__(self.sequence, 'random')
                return
            
    def _initialize_with_seed(self):
        try:
            seed_path = os.path.join(os.path.dirname(__file__), "results", config.SEED_TIMEID, "final_conformation.txt")
            with open(seed_path, 'r') as f:
                lines = f.readlines()
                # Sprawdź, czy liczba wierszy w pliku odpowiada długości łańcucha
                if len(lines) != self.length:
                    print(f"Ostrzeżenie: Długość łańcucha ({self.length}) nie zgadza się "
                            f"z liczbą wierszy w pliku seed ({len(lines)}).")
                    # Możesz tutaj dodać obsługę tego błędu, np. przerwać działanie
                    # lub dostosować długość łańcucha.
                    # W tym przykładzie, współrzędne zostaną wczytane,
                    # ale mogą być niekompletne lub nadmiarowe.

                read_coords = []
                for line in lines:
                    parts = line.strip().split()
                    if len(parts) == 3:
                        try:
                            # Konwertuj każdą część na liczbę całkowitą i dodaj do listy
                            read_coords.append([int(p) for p in parts])
                        except ValueError:
                            print(f"Ostrzeżenie: Pomięto nieprawidłową linię w pliku seed: {line.strip()}")
                
                # Ustaw współrzędne obiektu na podstawie wczytanych danych
                self.coords = np.array(read_coords, dtype=int)

        except FileNotFoundError:
            print(f"Błąd: Nie znaleziono pliku pod ścieżką: {config.SEED_PATH}")
            sys.exit("Program nie może kontynuować bez pliku seed.")
        except Exception as e:
            print(f"Wystąpił nieoczekiwany błąd podczas wczytywania pliku seed: {e}")
            sys.exit()


    def calculate_energy(self) -> int:
        energy = 0
        occupied_coords = {tuple(pos): i for i, pos in enumerate(self.coords)}
        
        for i in range(self.length):
            if self.sequence[i] == 'H':
                for dx, dy, dz in [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]:
                    neighbor_pos = tuple(self.coords[i] + [dx, dy, dz])
                    if neighbor_pos in occupied_coords:
                        j = occupied_coords[neighbor_pos]
                        if self.sequence[j] == 'H' and abs(i - j) > 1:
                            energy += -1
        return energy // 2

    def get_updated_copy(self, new_coords: np.ndarray):
        new_protein = Protein(self.sequence)
        new_protein.coords = new_coords
        new_protein.energy = new_protein.calculate_energy()
        return new_protein

    def try_end_move(self) -> np.ndarray | None:
        new_coords = self.coords.copy()
        end_idx = 0 if random.random() < 0.5 else self.length - 1
        pivot_idx = 1 if end_idx == 0 else self.length - 2
        pivot_pos = new_coords[pivot_idx]
        
        directions = [
            np.array([1, 0, 0]), np.array([-1, 0, 0]),
            np.array([0, 1, 0]), np.array([0, -1, 0]),
            np.array([0, 0, 1]), np.array([0, 0, -1]),
        ]
        move = random.shuffle(directions)
        
        for move in directions:
            new_pos = pivot_pos + move
            if not any(np.array_equal(new_pos, c) for c in np.delete(new_coords, end_idx, axis=0)):
                new_coords[end_idx] = new_pos
                return new_coords
        return None

    def try_corner_move(self) -> np.ndarray | None:
        new_coords = self.coords.copy()
        potential_corners = []
        for i in range(1, self.length - 1):
            v1 = new_coords[i] - new_coords[i-1]
            v2 = new_coords[i+1] - new_coords[i]
            if np.dot(v1, v2) == 0:
                potential_corners.append(i)
        
        if not potential_corners:
            return None
            
        i = random.choice(potential_corners)
        new_pos_B = new_coords[i-1] + (new_coords[i+1] - new_coords[i])
        
        if not any(np.array_equal(new_pos_B, c) for c in new_coords):
            new_coords[i] = new_pos_B
            return new_coords
        return None

    def try_crankshaft_move(self) -> np.ndarray | None:
        """
        Poprawiona implementacja ruchu 'crankshaft'.
        Szuka fragmentów A-B-C-D tworzących "U-kształtny" równoległobok,
        który nie jest linią prostą, i odwraca wewnętrzną parę B-C.
        """
        candidates = []
        for i in range(self.length - 3):
            p0, p1, p2, p3 = self.coords[i:i+4]
            # Warunek 1: Musi tworzyć równoległobok (wektorowo A+D = B+C)
            if np.array_equal(p0 + p3, p1 + p2):
                # Warunek 2: Nie może być linią prostą (wektory AB i BC nie mogą być takie same)
                if not np.array_equal(p1 - p0, p2 - p1):
                    candidates.append(i)

        if not candidates:
            return None

        i = random.choice(candidates)
        p0, p1, p2, p3 = self.coords[i:i+4]

        # Oblicz nowe, "odwrócone" pozycje dla wewnętrznej pary
        p1_new = p0 + p3 - p2
        p2_new = p0 + p3 - p1
        
        # Sprawdź kolizje z resztą łańcucha
        # Stwórz zbiór wszystkich zajętych współrzędnych do szybkiego sprawdzania
        occupied_coords = {tuple(c) for c in self.coords}
        # Usuń współrzędne pary, którą ruszamy, bo ich miejsca będą wolne
        occupied_coords.remove(tuple(p1))
        occupied_coords.remove(tuple(p2))

        # Jeśli nowe pozycje nie są zajęte przez resztę łańcucha...
        if tuple(p1_new) not in occupied_coords and tuple(p2_new) not in occupied_coords:
            new_coords = self.coords.copy()
            new_coords[i+1] = p1_new
            new_coords[i+2] = p2_new
            return new_coords
        
        return None # Kolizja lub inny błąd