# plotter.py
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from protein import Protein
import config

def save_conformation(protein: Protein, filename: str = "final_conformation.txt"):
    """Zapisuje końcowe współrzędne do pliku tekstowego w formacie "x y z"."""
    with open(filename, 'w') as f:
        for coord in protein.coords:
            f.write(f"{coord[0]} {coord[1]} {coord[2]}\n")
    print(f"Zapisano końcową konformację do pliku {filename}")

def plot_energy_history(energies: list, filename: str = "energy_history.png"):
    """Tworzy i zapisuje wykres historii zmian energii."""
    plt.figure(figsize=(10, 6))
    plt.plot(energies)
    plt.title("Zmiana energii w trakcie symulacji")
    plt.xlabel("Krok symulacji")
    plt.ylabel("Energia")
    plt.grid(True)
    plt.savefig(filename)
    plt.close()
    print(f"Zapisano wykres energii do pliku {filename}")

def plot_3d_conformation(protein: Protein, filename: str = "3d_conformation.png"):
    """Generuje wizualizację 3D końcowej struktury białka."""
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    h_coords = np.array([protein.coords[i] for i, acid in enumerate(protein.sequence) if acid == 'H'])
    p_coords = np.array([protein.coords[i] for i, acid in enumerate(protein.sequence) if acid == 'P'])
    
    if h_coords.size > 0:
        ax.scatter(h_coords[:, 0], h_coords[:, 1], h_coords[:, 2], c='red', s=100, label='Hydrofobowy (H)')
    if p_coords.size > 0:
        ax.scatter(p_coords[:, 0], p_coords[:, 1], p_coords[:, 2], c='blue', s=100, label='Polarny (P)')
        
    ax.plot(protein.coords[:, 0], protein.coords[:, 1], protein.coords[:, 2], c='gray', linestyle='-', marker='')
    
    ax.set_title("Końcowa konformacja białka")
    ax.set_xlabel("X"); ax.set_ylabel("Y"); ax.set_zlabel("Z")
    ax.legend()
    plt.savefig(filename)
    plt.close()
    print(f"Zapisano wizualizację 3D do pliku {filename}")

# <<< NOWA FUNKCJA DO TWORZENIA ANIMACJI >>>
def create_animation(history: list, sequence: str, filename: str = "folding_animation.gif"):
    """Tworzy animację GIF procesu zwijania białka."""
    if not history:
        print("Brak danych do stworzenia animacji.")
        return

    print("Rozpoczynanie tworzenia animacji (to może potrwać)...")
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Przygotowanie danych do kolorowania
    h_indices = [i for i, acid in enumerate(sequence) if acid == 'H']
    p_indices = [i for i, acid in enumerate(sequence) if acid == 'P']

    # Inicjalizacja wykresu pierwszą klatką
    initial_coords = history[0]
    backbone, = ax.plot(initial_coords[:, 0], initial_coords[:, 1], initial_coords[:, 2], c='gray', marker='')
    h_scatter = ax.scatter(initial_coords[h_indices, 0], initial_coords[h_indices, 1], initial_coords[h_indices, 2], c='red', s=100, label='H')
    p_scatter = ax.scatter(initial_coords[p_indices, 0], initial_coords[p_indices, 1], initial_coords[p_indices, 2], c='blue', s=100, label='P')

    ax.legend()
    
    # Funkcja aktualizująca dla każdej klatki
    def update(frame_num):
        coords = history[frame_num]
        
        # Aktualizacja linii szkieletu
        backbone.set_data(coords[:, 0], coords[:, 1])
        backbone.set_3d_properties(coords[:, 2])
        
        # Aktualizacja punktów H i P
        h_scatter._offsets3d = (coords[h_indices, 0], coords[h_indices, 1], coords[h_indices, 2])
        p_scatter._offsets3d = (coords[p_indices, 0], coords[p_indices, 1], coords[p_indices, 2])
        
        # Ustawienie granic osi dynamicznie
        all_coords = np.vstack(history)
        min_c, max_c = all_coords.min(), all_coords.max()
        ax.set_xlim(min_c, max_c)
        ax.set_ylim(min_c, max_c)
        ax.set_zlim(min_c, max_c)

        ax.set_title(f"Krok symulacji: {frame_num * config.ANIMATION_FRAME_INTERVAL}")
        return backbone, h_scatter, p_scatter

    # Stworzenie i zapisanie animacji
    ani = animation.FuncAnimation(fig, update, frames=len(history), interval=100, blit=False)
    
    try:
        ani.save(filename, writer='pillow', fps=10)
        print(f"Zapisano animację do pliku {filename}")
    except Exception as e:
        print(f"Nie udało się zapisać animacji: {e}")
        print("Upewnij się, że masz zainstalowaną bibliotekę 'Pillow': pip install Pillow")
        
    plt.close()