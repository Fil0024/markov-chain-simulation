# simulation.py
import math
import random
from tqdm import tqdm
from protein import Protein
import config

class MetropolisSimulation:
    """
    Zarządza symulacją zwijania białek za pomocą algorytmu Metropolisa
    i symulowanego wyżarzania.
    """
    def __init__(self, protein: Protein):
        self.protein = protein
        self.temp = config.INITIAL_TEMP
        
        self.energy_history = []
        self.conformation_history = []  # <<< NOWOŚĆ: Lista do przechowywania klatek
        
        self.accepted_moves = {'end': 0, 'corner': 0, 'crankshaft': 0}
        self.proposed_moves = {'end': 0, 'corner': 0, 'crankshaft': 0}

    def run(self):
        """Uruchamia główną pętlę symulacji."""
        print(f"Rozpoczynanie symulacji dla {config.NUM_STEPS} kroków...")
        
        # Zapisz klatkę początkową
        if config.CREATE_ANIMATION:
            self.conformation_history.append(self.protein.coords.copy())

        for step in tqdm(range(config.NUM_STEPS), desc="Symulacja"):
            current_energy = self.protein.energy
            
            
            new_coords = None
            while new_coords is None:
                move_type = random.choice(['end', 'corner', 'crankshaft'])
                if move_type == 'end':
                    new_coords = self.protein.try_end_move()
                elif move_type == 'corner':
                    new_coords = self.protein.try_corner_move()
                elif move_type == 'crankshaft':
                    new_coords = self.protein.try_crankshaft_move()

            self.proposed_moves[move_type] += 1

            if new_coords is not None:
                temp_protein = self.protein.get_updated_copy(new_coords)
                new_energy = temp_protein.energy
                delta_e = new_energy - current_energy
                
                if delta_e <= 0 or random.random() < math.exp(-delta_e / self.temp):
                    self.protein = temp_protein
                    self.accepted_moves[move_type] += 1
            
            self.energy_history.append(self.protein.energy)
            
            # <<< NOWOŚĆ: Zapisywanie klatki co N kroków
            if config.CREATE_ANIMATION and (step + 1) % config.ANIMATION_FRAME_INTERVAL == 0:
                self.conformation_history.append(self.protein.coords.copy())

            self.temp = max(config.FINAL_TEMP, self.temp * config.ALPHA)
            
        print("Symulacja zakończona.")
        print(f"Końcowa energia: {self.protein.energy}")
        print(f"Statystyki ruchów (proponowane / zaakceptowane):")
        for move in self.proposed_moves:
            print(f" - {move.capitalize()}: {self.proposed_moves[move]} / {self.accepted_moves[move]}")