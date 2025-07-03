# config.py

# Sekwencja aminokwasów dla ubikwityny w modelu HP
# 'E' na końcu sekwencji jest traktowane jako znacznik końca, ignorowany w modelu.
SEQUENCE_UBIQUITIN = "PHPHHHHHPHPHPHPHHPPPPPHPPPPHHHPPPPPHPPPHHPHPHHHHPPPPHHEHPHPHHHHHHHHHPPHHPP"

# --- Parametry symulowanego wyżarzania ---
INITIAL_TEMP = 10.0
FINAL_TEMP = 1.0
ALPHA = 0.999
NUM_STEPS = 10000

# --- Parametry inicjalizacji ---
INITIALIZATION_METHOD = 'random'

# --- Parametry animacji ---
# Czy tworzyć animację procesu zwijania?
CREATE_ANIMATION = False
# Zapisuj klatkę animacji co N kroków
ANIMATION_FRAME_INTERVAL = 100