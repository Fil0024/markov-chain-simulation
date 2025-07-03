# main.py
import config
from protein import Protein
from simulation import MetropolisSimulation
import plotter

def main():
    """Główna funkcja programu."""
    print("--- Modelowanie zwijania białek w modelu HP ---")
    print(f"Sekwencja: {config.SEQUENCE_UBIQUITIN}")
    print(f"Metoda inicjalizacji: {config.INITIALIZATION_METHOD}")
    print(f"Parametry: T0={config.INITIAL_TEMP}, T_final={config.FINAL_TEMP}, alpha={config.ALPHA}, kroki={config.NUM_STEPS}")
    
    # 1. Inicjalizacja białka
    protein_chain = Protein(config.SEQUENCE_UBIQUITIN, config.INITIALIZATION_METHOD)
    print(f"Energia początkowa: {protein_chain.energy}")
    
    # 2. Uruchomienie symulacji
    simulation = MetropolisSimulation(protein_chain)
    simulation.run()
    
    final_protein = simulation.protein
    
    # [cite_start]3. Zapisanie wyników i wizualizacja [cite: 62, 63, 64]
    plotter.save_conformation(final_protein)
    plotter.plot_energy_history(simulation.energy_history)
    plotter.plot_3d_conformation(final_protein)
    
    print("--- Koniec programu ---")

if __name__ == "__main__":
    main()