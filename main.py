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
    
    protein_chain = Protein(config.SEQUENCE_UBIQUITIN, config.INITIALIZATION_METHOD)
    print(f"Energia początkowa: {protein_chain.energy}")
    
    simulation = MetropolisSimulation(protein_chain)
    simulation.run()
    
    final_protein = simulation.protein
    
    # Zapisanie wyników i wizualizacje
    plotter.save_conformation(final_protein)
    plotter.plot_energy_history(simulation.energy_history)
    plotter.plot_3d_conformation(final_protein)
    
    # <<< NOWOŚĆ: Wywołanie funkcji tworzącej animację >>>
    if config.CREATE_ANIMATION and simulation.conformation_history:
        plotter.create_animation(simulation.conformation_history, final_protein.sequence)
    
    print("--- Koniec programu ---")

if __name__ == "__main__":
    main()