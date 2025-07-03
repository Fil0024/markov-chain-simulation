# protein.py
import random
import numpy as np

class Protein:
    """
    Reprezentuje łańcuch białkowy w modelu HP na siatce 3D.
    """
    def __init__(self, sequence: str, init_method: str = 'linear'):
        self.sequence = sequence#.replace('E', '') # Usuwamy znacznik końca 'E'
        self.length = len(self.sequence)
        self.coords = np.zeros((self.length, 3), dtype=int)
        
        if init_method == 'linear':
            self._initialize_linear()
        elif init_method == 'random':
            self._initialize_random_walk()
        else:
            raise ValueError("Nieznana metoda inicjalizacji. Wybierz 'linear' lub 'random'.")

        self.energy = self.calculate_energy()

    def _initialize_linear(self):
        """Inicjalizuje łańcuch w prostej linii wzdłuż osi X."""
        for i in range(1, self.length):
            self.coords[i] = self.coords[i-1] + [1, 0, 0]

    def _initialize_random_walk(self):
        """Inicjalizuje łańcuch przez losowe błądzenie bez samoprzecięć."""
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
                # Jeśli utknęliśmy (bardzo rzadkie dla krótkich łańcuchów), zaczynamy od nowa
                print("Ostrzeżenie: losowe błądzenie utknęło, próba ponowna.")
                self.__init__(self.sequence, 'random')
                return

    def calculate_energy(self) -> int:
        """
        Oblicza energię konformacji.
        Energia to -1 za każdą parę niesąsiadujących w łańcuchu aminokwasów 'H',
        które sąsiadują ze sobą na siatce (odległość 1).
        """
        energy = 0
        occupied_coords = {tuple(pos): i for i, pos in enumerate(self.coords)}
        
        for i in range(self.length):
            if self.sequence[i] == 'H':
                # Sprawdź 6 sąsiadów na siatce
                for dx, dy, dz in [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]:
                    neighbor_pos = tuple(self.coords[i] + [dx, dy, dz])
                    
                    if neighbor_pos in occupied_coords:
                        j = occupied_coords[neighbor_pos]
                        # Sprawdź czy sąsiad to 'H' i nie jest bezpośrednim sąsiadem w łańcuchu
                        if self.sequence[j] == 'H' and abs(i - j) > 1:
                            energy += -1
        
        # Każda para jest liczona dwukrotnie, więc dzielimy przez 2
        return energy // 2

    def get_updated_copy(self, new_coords: np.ndarray):
        """Tworzy nową instancję Protein z zaktualizowanymi współrzędnymi."""
        new_protein = Protein(self.sequence)
        new_protein.coords = new_coords
        new_protein.energy = new_protein.calculate_energy()
        return new_protein

    def _is_valid(self, new_coords: np.ndarray) -> bool:
        """Sprawdza, czy nowe współrzędne nie mają kolizji."""
        unique_coords = set(tuple(pos) for pos in new_coords)
        return len(unique_coords) == self.length

    # Implementacja trzech wymaganych ruchów

    def try_end_move(self) -> np.ndarray | None:
        """Próba wykonania ruchu końca łańcucha."""
        new_coords = self.coords.copy()
        
        # Wybierz losowy koniec
        end_idx = 0 if random.random() < 0.5 else self.length - 1
        pivot_idx = 1 if end_idx == 0 else self.length - 2
        
        pivot_pos = new_coords[pivot_idx]
        
        # Lista możliwych nowych pozycji
        directions = [
            np.array([1, 0, 0]), np.array([-1, 0, 0]),
            np.array([0, 1, 0]), np.array([0, -1, 0]),
            np.array([0, 0, 1]), np.array([0, 0, -1]),
        ]
        random.shuffle(directions)
        
        for move in directions:
            new_pos = pivot_pos + move
            # Sprawdź, czy nowa pozycja nie koliduje z resztą łańcucha
            if not any(np.array_equal(new_pos, c) for c in np.delete(new_coords, end_idx, axis=0)):
                new_coords[end_idx] = new_pos
                return new_coords
                
        return None # Nie znaleziono prawidłowego ruchu

    def try_corner_move(self) -> np.ndarray | None:
        """Próba wykonania obrotu narożnika."""
        new_coords = self.coords.copy()
        
        # Znajdź potencjalne narożniki
        potential_corners = []
        for i in range(1, self.length - 1):
            v1 = new_coords[i] - new_coords[i-1]
            v2 = new_coords[i+1] - new_coords[i]
            # Sprawdź czy wektory są prostopadłe (iloczyn skalarny = 0)
            if np.dot(v1, v2) == 0:
                potential_corners.append(i)
        
        if not potential_corners:
            return None
            
        i = random.choice(potential_corners)
        
        # Oblicz nową pozycję: A + (C - B)
        # A = coords[i-1], B = coords[i], C = coords[i+1]
        # Nowa pozycja dla B: B' = A + (C-B)
        new_pos_B = new_coords[i-1] + (new_coords[i+1] - new_coords[i])
        
        # Sprawdź czy nowa pozycja jest wolna
        if not any(np.array_equal(new_pos_B, c) for c in new_coords):
            new_coords[i] = new_pos_B
            return new_coords
            
        return None

    def try_crankshaft_move(self) -> np.ndarray | None:
        """Próba wykonania obrotu 'crankshaft'. Wersja uproszczona."""
        # Pełna implementacja tego ruchu jest złożona.
        # Ta funkcja może być rozbudowana.
        # Zazwyczaj szuka się fragmentów A-B-C-D tworzących kwadrat.
        # Poniżej znajduje się placeholder, który można zaimplementować.
        return None # Placeholder - do implementacji