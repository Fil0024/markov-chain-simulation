# plotter.py
import matplotlib.pyplot as plt
from protein import Protein

def save_conformation(protein: Protein, filename: str = "final_conformation.txt"):
    """
    [cite_start]Zapisuje końcowe współrzędne do pliku tekstowego w formacie "x y z". [cite: 63]
    """
    with open(filename, 'w') as f:
        for coord in protein.coords:
            f.write(f"{coord[0]} {coord[1]} {coord[2]}\n")
    print(f"Zapisano końcową konformację do pliku {filename}")

def plot_energy_history(energies: list, filename: str = "energy_history.png"):
    """
    [cite_start]Tworzy i zapisuje wykres historii zmian energii. [cite: 62]
    """
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
    """
    [cite_start]Generuje wizualizację 3D końcowej struktury białka. [cite: 62]
    """
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    h_coords = [protein.coords[i] for i, acid in enumerate(protein.sequence) if acid == 'H']
    p_coords = [protein.coords[i] for i, acid in enumerate(protein.sequence) if acid == 'P']
    
    # Rozpakowanie współrzędnych
    if h_coords:
        hx, hy, hz = zip(*h_coords)
        ax.scatter(hx, hy, hz, c='red', s=100, label='Hydrofobowy (H)')
    if p_coords:
        px, py, pz = zip(*p_coords)
        ax.scatter(px, py, pz, c='blue', s=100, label='Polarny (P)')
        
    # Rysowanie łańcucha
    all_x, all_y, all_z = zip(*protein.coords)
    ax.plot(all_x, all_y, all_z, c='gray', linestyle='-', marker='')

    ax.set_title("Końcowa konformacja białka")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.legend()
    plt.savefig(filename)
    plt.close()
    print(f"Zapisano wizualizację 3D do pliku {filename}")