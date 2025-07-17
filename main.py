# main.py
import config
import os
from protein import Protein
from simulation import MetropolisSimulation
import plotter
import csv
import pandas as pd

def main():

    print("--- Modelowanie zwijania białek w modelu HP ---")
    print(f"Sekwencja: {config.SEQUENCE_UBIQUITIN}")
    print(f"Metoda inicjalizacji: {config.INITIALIZATION_METHOD}")
    print(f"Parametry: T0={config.INITIAL_TEMP}, T_final={config.FINAL_TEMP}, alpha={config.ALPHA}, kroki={config.NUM_STEPS}")
    
    protein_chain = Protein(config.SEQUENCE_UBIQUITIN, config.INITIALIZATION_METHOD)
    initial_energy = protein_chain.energy
    print(f"Energia początkowa: {initial_energy}")
    


    simulation = MetropolisSimulation(protein_chain)
    simulation.run()
    final_energy = simulation.protein.energy
    
    final_protein = simulation.protein
    
    file_folder = str(config.TIMEID)
    results_path = os.path.join("results", file_folder)
    os.makedirs(results_path, exist_ok=True)  # Upewnij się, że folder istnieje
    plotter.save_conformation(final_protein, os.path.join(results_path, "final_conformation.txt"))
    plotter.plot_energy_history(simulation.energy_history, os.path.join(results_path, "energy_history.png"))
    plotter.plot_3d_conformation(final_protein, os.path.join(results_path, "3d_conformation.png"))
    
    if config.CREATE_ANIMATION and simulation.conformation_history:
        plotter.create_animation(simulation.conformation_history, final_protein.sequence, os.path.join(results_path, "folding_animation.gif"))
    
    current_resutls_file = os.path.join(results_path, "results.txt")
    with open(current_resutls_file, 'w') as file:
        file.write(f"Parametry symulacji:\n")
        file.write(f"Metoda inicjalizacji: {config.INITIALIZATION_METHOD}\n")
        file.write(f"Temperatura poczatkowa: {config.INITIAL_TEMP}\n")
        file.write(f"Temperatura koncowa: {config.FINAL_TEMP}\n")
        file.write(f"Wspolczynnik schladzania alpha: {config.ALPHA}\n")
        file.write(f"Liczba krokow: {config.NUM_STEPS}\n")
        file.write(f"Energia poczatkowa: {initial_energy}\n")
        file.write(f"Energia koncowa: {final_energy}\n")
        file.write(f"Statystyki ruchow (proponowane / zaakceptowane):")
        for move in simulation.proposed_moves:
            file.write(f"\n {move.capitalize()}: {simulation.proposed_moves[move]} / {simulation.accepted_moves[move]}")
        file.write("\n All moves: " + str(sum(simulation.proposed_moves.values())) + " / " + str(sum(simulation.accepted_moves.values())) + "\n")
        if config.INITIALIZATION_METHOD == 'seed':
            file.write(f"Plik z konformacją początkową: {config.SEED_TIMEID}\n")
    all_results_file = os.path.join("results", "all_results.csv")
    accepted_steps = sum(simulation.accepted_moves.values())
    new_result = [config.TIMEID, config.INITIALIZATION_METHOD, config.INITIAL_TEMP, config.FINAL_TEMP, config.ALPHA, config.NUM_STEPS, accepted_steps, initial_energy, final_energy]

    with open(all_results_file, 'a', newline='') as plik_csv:
        writer = csv.writer(plik_csv)
        writer.writerow(new_result)

    print("--- Koniec programu ---")

if __name__ == "__main__":
    main()