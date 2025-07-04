# main.py
import config
import os
from protein import Protein
from simulation import MetropolisSimulation
import plotter
import csv

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
    
    file_folder = str(config.INITIALIZATION_METHOD)+"_intemp"+str(config.INITIAL_TEMP) + "_fin" + str(config.FINAL_TEMP) + "_alpha" + str(config.ALPHA) + "_steps" + str(config.NUM_STEPS)
    results_path = os.path.join("results", file_folder)
    os.makedirs(results_path, exist_ok=True)  # Upewnij się, że folder istnieje
    plotter.save_conformation(final_protein, os.path.join(results_path, "final_conformation.txt"))
    plotter.plot_energy_history(simulation.energy_history, os.path.join(results_path, "energy_history.png"))
    plotter.plot_3d_conformation(final_protein, os.path.join(results_path, "3d_conformation.png"))
    
    # <<< NOWOŚĆ: Wywołanie funkcji tworzącej animację >>>
    if config.CREATE_ANIMATION and simulation.conformation_history:
        plotter.create_animation(simulation.conformation_history, final_protein.sequence, os.path.join(results_path, "folding_animation.gif"))
    
    os.makedirs("results", exist_ok=True)
    all_results_file = os.path.join("results", "all_results.csv")
    new_result = [config.INITIALIZATION_METHOD, config.INITIAL_TEMP, config.FINAL_TEMP, config.ALPHA, config.NUM_STEPS, initial_energy, final_energy]

    with open(all_results_file, 'a', newline='') as plik_csv:
        writer = csv.writer(plik_csv)
        writer.writerow(new_result)


    print("--- Koniec programu ---")

if __name__ == "__main__":
    main()