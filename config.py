# config.py

# Sekwencja aminokwasów dla ubikwityny w modelu HP
# 'E' na końcu sekwencji jest traktowane jako znacznik końca, ignorowany w modelu.
SEQUENCE_UBIQUITIN = "PHPHHHHHPHPHPHPHHPPPPPHPPPPHHHPPPPPHPPPHHPHPHHHHPPPPHHEHPHPHHHHHHHHHPPHHPP"

# --- Parametry symulowanego wyżarzania ---

# Temperatura początkowa, T_0
INITIAL_TEMP = 10.0

# Temperatura końcowa, T_nieskończoność
FINAL_TEMP = 1.0

# Współczynnik schładzania, alfa
# T_i+1 = max(ALPHA * T_i, FINAL_TEMP)
ALPHA = 0.999

# Liczba kroków w symulacji
NUM_STEPS = 10000

# --- Parametry inicjalizacji ---

# Sposób inicjalizacji początkowej konformacji: 'linear' lub 'random'
INITIALIZATION_METHOD = 'random'