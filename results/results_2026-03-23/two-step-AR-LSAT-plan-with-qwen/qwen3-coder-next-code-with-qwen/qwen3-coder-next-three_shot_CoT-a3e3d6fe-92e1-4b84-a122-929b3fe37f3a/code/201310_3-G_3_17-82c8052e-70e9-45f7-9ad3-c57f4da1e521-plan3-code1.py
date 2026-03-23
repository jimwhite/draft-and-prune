from z3 import *

# Movie indices: horror=0, mystery=1, romance=2, sci-fi=3, western=4
MOVIES = ["horror", "mystery", "romance", "sci-fi", "western"]
(horror, mystery, romance, scifi, western) = range(5)

# Screen variables for each movie
screen = [Int(f"screen_{m}") for m in range(5)]

# Time slot variables: time[m] = absolute time (7, 8, or 9)
time = [Int(f"time_{m}") for m in range(5)]

# Base solver
solver = Solver()

# Screen assignment constraints
# Each movie assigned to exactly one screen (1, 2, or 3)
for m in range(5):
    solver.add(Or(screen[m] == 1, screen[m] == 2, screen[m] == 3))

# Screen capacity constraints:
# - Screen 1: exactly 2 movies
solver.add(Sum([If(screen[m] == 1, 1, 0) for m in range(5)]) == 2)
# - Screen 2: exactly 2 movies
solver.add(Sum([If(screen[m] == 2, 1, 0) for m in range(5)]) == 2)
# - Screen 3: exactly 1 movie
solver.add(Sum([If(screen[m] == 3, 1, 0) for m in range(5)]) == 1)

# Time slot constraints:
# Screen 1: one movie at 7PM, one at 9PM
# Screen 2: one movie at 7PM, one at 9PM
# Screen 3: one movie at 8PM

# Create boolean variables for each movie at each time slot
t7 = [Bool(f"t7_{m}") for m in range(5)]  # movie m at 7PM
t8 = [Bool(f"t8_{m}") for m in range(5)]  # movie m at 8PM
t9 = [Bool(f"t9_{m}") for m in range(5)]  # movie m at 9PM

# Each movie assigned to exactly one time slot
for m in range(5):
    solver.add(Or(t7[m], t8[m], t9[m]))
    solver.add(Not(And(t7[m], t8[m])))
    solver.add(Not(And(t7[m], t9[m])))
    solver.add(Not(And(t8[m], t9[m])))

# Time slot capacity constraints:
# - 7PM: exactly two movies (screen1@7 and screen2@7)
solver.add(Sum([If(t7[m], 1, 0) for m in range(5)]) == 2)
# - 8PM: exactly one movie (screen3@8)
solver.add(Sum([If(t8[m], 1, 0) for m in range(5)]) == 1)
# - 9PM: exactly two movies (screen1@9 and screen2@9)
solver.add(Sum([If(t9[m], 1, 0) for m in range(5)]) == 2)

# Link screen and time:
# Screen1: movies at t7 or t9
# Screen2: movies at t7 or t9
# Screen3: movie at t8

for m in range(5):
    # If movie is on screen3, it must be at 8PM
    solver.add(Implies(screen[m] == 3, t8[m]))
    # If movie is at 8PM, it must be on screen3
    solver.add(Implies(t8[m], screen[m] == 3))
    # If movie is on screen1 or screen2, it must be at 7PM or 9PM
    solver.add(Implies(Or(screen[m] == 1, screen[m] == 2), Or(t7[m], t9[m])))

# Screen-type constraints:
# Sci-fi not shown on screen 3
solver.add(screen[scifi] != 3)
# Romance not shown on screen 2
solver.add(screen[romance] != 2)

# Relative timing constraint: western before horror
# time(western) < time(horror)
solver.add(Or(
    And(t7[western], Or(t8[horror], t9[horror])),
    And(t8[western], t9[horror])
))

# Horror and mystery on different screens
solver.add(screen[horror] != screen[mystery])

# Now check each answer choice for screen 1 (7PM, 9PM)
answer_choices = [
    ("sci-fi", "horror"),   # index 0
    ("sci-fi", "mystery"),  # index 1
    ("western", "horror"),  # index 2
    ("western", "mystery"), # index 3
    ("western", "sci-fi")   # index 4
]

# Map choice strings to movie indices
choice_map = {
    "horror": horror,
    "mystery": mystery,
    "romance": romance,
    "sci-fi": scifi,
    "western": western
}

forbidden_list_index = []

for idx, (first, second) in enumerate(answer_choices):
    s_chk = Solver()
    # Add all base constraints
    for a in solver.assertions():
        s_chk.add(a)
    
    # Add screen 1 constraint: first movie at 7PM, second movie at 9PM
    f_idx = choice_map[first]
    s_idx = choice_map[second]
    
    # First movie must be on screen 1 and at 7PM
    s_chk.add(screen[f_idx] == 1)
    s_chk.add(t7[f_idx])
    
    # Second movie must be on screen 1 and at 9PM
    s_chk.add(screen[s_idx] == 1)
    s_chk.add(t9[s_idx])
    
    # Ensure no other movie is on screen 1
    for m in range(5):
        if m != f_idx and m != s_idx:
            s_chk.add(screen[m] != 1)
    
    # Check if this configuration is possible
    if s_chk.check() == unsat:
        forbidden_list_index.append(idx)

print(forbidden_list_index)