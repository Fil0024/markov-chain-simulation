# config.py
import time

# Sekwencja aminokwasów dla ubikwityny w modelu HP
# 'E' na końcu sekwencji jest traktowane jako znacznik końca, ignorowany w modelu.
SEQUENCE_UBIQUITIN = "PHPHHHHHPHPHPHPHHPPPPPHPPPPHHHPPPPPHPPPHHPHPHHHHPPPPHHEHPHPHHHHHHHHHPPHHPP"

# --- Parametry symulowanego wyżarzania ---
INITIAL_TEMP = 2
FINAL_TEMP = 0.5
ALPHA = 0.999
NUM_STEPS = 10000

TIMEID = str(time.strftime("%Y%m%d-%H%M%S"))

# --- Parametry inicjalizacji ---
INITIALIZATION_METHOD = 'seed'  # 'linear', 'random' , 'seed'

SEED_TIMEID = r"20250717-211526"

# --- Parametry animacji ---
# Czy tworzyć animację procesu zwijania?
CREATE_ANIMATION = True
# Zapisuj klatkę animacji co N kroków
ANIMATION_FRAME_INTERVAL = 100