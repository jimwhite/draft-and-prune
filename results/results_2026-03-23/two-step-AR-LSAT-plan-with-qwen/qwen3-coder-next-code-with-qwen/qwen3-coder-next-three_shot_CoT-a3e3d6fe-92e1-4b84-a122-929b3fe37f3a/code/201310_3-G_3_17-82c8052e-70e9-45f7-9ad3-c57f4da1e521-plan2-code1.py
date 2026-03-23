from z3 import *

# Movie indices: 0-horror, 1-mystery, 2-romance, 3-sci-fi, 4-western
HORROR, MYSTERY, ROMANCE, SCIFI, WESTERN = range(5)

# Screen indices: 1, 2, 3
# Time slots per screen:
#   Screen 1: slot0 (7 PM), slot1 (9 PM)
#   Screen 2: slot0 (7 PM), slot1 (9 PM)
#   Screen 3: slot0 (8 PM)

# Create variables for each movie
screen = [Int(f"screen_{i}") for i in range(5)]
slot = [Int(f"slot_{i}") for i in range(5)]

# Base solver
solver = Solver()

# Domain constraints: screen ∈ {1,2,3}, slot depends on screen
for i in range(5):
    solver.add(screen[i] >= 1, screen[i] <= 3)
    # If screen is 1 or 2, slot must be 0 or 1; if screen is 3, slot must be 0
    solver.add(Implies(screen[i] == 1, Or(slot[i] == 0, slot[i] == 1)))
    solver.add(Implies(screen[i] == 2, Or(slot[i] == 0, slot[i] == 1)))
    solver.add(Implies(screen[i] == 3, slot[i] == 0))

# Distinctness constraints: each (screen, slot) pair used at most once
# Create unique identifiers for (screen, slot) pairs: screen*10 + slot
pair_id = [screen[i] * 10 + slot[i] for i in range(5)]
solver.add(Distinct(*pair_id))

# Capacity constraints: Screen 1 has exactly 2 movies, Screen 2 has exactly 2, Screen 3 has exactly 1
screen_counts = [Sum([If(screen[i] == s, 1, 0) for i in range(5)]) for s in [1, 2, 3]]
solver.add(screen_counts[0] == 2)  # Screen 1
solver.add(screen_counts[1] == 2)  # Screen 2
solver.add(screen_counts[2] == 1)  # Screen 3

# Time mapping: assign absolute time values
# Screen 1, slot0 -> 7; Screen 1, slot1 -> 9
# Screen 2, slot0 -> 7; Screen 2, slot1 -> 9
# Screen 3, slot0 -> 8
time_expr = [
    If(screen[i] == 1,
       If(slot[i] == 0, 7, 9),
       If(screen[i] == 2,
          If(slot[i] == 0, 7, 9),
          8)) for i in range(5)
]

# Ordering constraint: western before horror
solver.add(time_expr[WESTERN] < time_expr[HORROR])

# Screen-specific constraints
solver.add(screen[SCIFI] != 3)      # Sci-fi not on screen 3
solver.add(screen[ROMANCE] != 2)   # Romance not on screen 2
solver.add(screen[HORROR] != screen[MYSTERY])  # Horror and mystery on different screens

# Answer choices (screen 1 schedule: [7 PM movie, 9 PM movie])
answer_choices = [
    (SCIFI, HORROR),   # sci-fi, horror
    (SCIFI, MYSTERY),  # sci-fi, mystery
    (WESTERN, HORROR), # western, horror
    (WESTERN, MYSTERY),# western, mystery
    (WESTERN, SCIFI)   # western, sci-fi
]

# Check each answer choice
answer_index_list = []
for idx, (movie0, movie1) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraints for screen 1 schedule: movie0 at 7 PM, movie1 at 9 PM
    s_chk.add(screen[movie0] == 1, slot[movie0] == 0)
    s_chk.add(screen[movie1] == 1, slot[movie1] == 1)
    
    # Check if this configuration is possible
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)