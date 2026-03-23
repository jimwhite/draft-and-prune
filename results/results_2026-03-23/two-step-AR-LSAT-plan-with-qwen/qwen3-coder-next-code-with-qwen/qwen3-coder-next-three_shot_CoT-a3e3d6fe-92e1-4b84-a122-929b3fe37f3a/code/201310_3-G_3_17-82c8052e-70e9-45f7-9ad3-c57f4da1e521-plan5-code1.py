from z3 import *

# Movie indices: horror=0, mystery=1, romance=2, sci-fi=3, western=4
# Screen indices: screen1=0, screen2=1, screen3=2
# Time slot indices: 7pm=0 (screen1/screen2), 8pm=1 (screen3 only), 9pm=2 (screen1/screen2)

movies = ["horror", "mystery", "romance", "sci-fi", "western"]
screen_vars = [Int(f"screen_{m}") for m in range(5)]
slot_vars = [Int(f"slot_{m}") for m in range(5)]

solver = Solver()

# Domain constraints
for m in range(5):
    solver.add(screen_vars[m] >= 0, screen_vars[m] <= 2)
    # Screens 1 and 2 (0,1) only have slots 0 or 2; screen 3 (2) only has slot 1
    if m == 2:  # romance constraint handled separately, but screen domain still applies
        pass

# Screen/time domain constraints
for m in range(5):
    # If screen is 0 or 1, slot must be 0 or 2
    solver.add(Implies(Or(screen_vars[m] == 0, screen_vars[m] == 1),
                       Or(slot_vars[m] == 0, slot_vars[m] == 2)))
    # If screen is 2, slot must be 1
    solver.add(Implies(screen_vars[m] == 2, slot_vars[m] == 1))

# Capacity constraints
solver.add(Sum([If(screen_vars[m] == 0, 1, 0) for m in range(5)]) == 2)
solver.add(Sum([If(screen_vars[m] == 1, 1, 0) for m in range(5)]) == 2)
solver.add(Sum([If(screen_vars[m] == 2, 1, 0) for m in range(5)]) == 1)

# One-to-one assignment constraints (screen-slot combinations)
for s in range(3):
    for t in range(3):
        # Only (0,0), (0,2), (1,0), (1,2), (2,1) are valid combinations
        if s == 0 and t in [0, 2]:
            solver.add(Sum([If(And(screen_vars[m] == s, slot_vars[m] == t), 1, 0) for m in range(5)]) <= 1)
        elif s == 1 and t in [0, 2]:
            solver.add(Sum([If(And(screen_vars[m] == s, slot_vars[m] == t), 1, 0) for m in range(5)]) <= 1)
        elif s == 2 and t == 1:
            solver.add(Sum([If(And(screen_vars[m] == s, slot_vars[m] == t), 1, 0) for m in range(5)]) <= 1)

# Order constraint: western before horror
western = 4
horror = 0
solver.add(Or(slot_vars[western] < slot_vars[horror],
              And(slot_vars[western] == slot_vars[horror], screen_vars[western] < screen_vars[horror])))

# Sci-fi not on screen 3
solver.add(screen_vars[3] != 2)

# Romance not on screen 2
solver.add(screen_vars[2] != 1)

# Horror and mystery on different screens
solver.add(screen_vars[0] != screen_vars[1])

# Answer choices: each is a list of two movies for screen 1 (7pm first, then 9pm)
answer_choices = [
    ("sci-fi", "horror"),   # index 0
    ("sci-fi", "mystery"),  # index 1
    ("western", "horror"),  # index 2
    ("western", "mystery"), # index 3
    ("western", "sci-fi")   # index 4
]

# Map movie names to indices
movie_to_idx = {"horror": 0, "mystery": 1, "romance": 2, "sci-fi": 3, "western": 4}

# Check each answer choice
answer_index_list = []
for idx, (first_movie, second_movie) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assign first movie to screen 0, slot 0 (7pm)
    f_idx = movie_to_idx[first_movie]
    s_chk.add(screen_vars[f_idx] == 0, slot_vars[f_idx] == 0)
    
    # Assign second movie to screen 0, slot 2 (9pm)
    s_idx = movie_to_idx[second_movie]
    s_chk.add(screen_vars[s_idx] == 0, slot_vars[s_idx] == 2)
    
    # Ensure no other movie is assigned to (screen0, slot0) or (screen0, slot2)
    for m in range(5):
        if m != f_idx:
            s_chk.add(Not(And(screen_vars[m] == 0, slot_vars[m] == 0)))
        if m != s_idx:
            s_chk.add(Not(And(screen_vars[m] == 0, slot_vars[m] == 2)))
    
    # Check if this configuration is possible
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

# Output the first (by list order) index that is UNSAT
if answer_index_list:
    print(answer_index_list[0])
else:
    print(-1)