from z3 import *

# Movie indices: 0=horror, 1=mystery, 2=romance, 3=sci-fi, 4=western
HORROR, MYSTERY, ROMANCE, SCIFI, WESTERN = range(5)

# Screen variables: screen[m] = which screen (1, 2, or 3) movie m is shown on
screen = [Int(f"screen_{m}") for m in range(5)]

# Time variables: time[m] = start time (0=7PM, 1=8PM, 2=9PM) for movie m
time = [Int(f"time_{m}") for m in range(5)]

# Base solver
solver = Solver()

# Screen count constraints: screen 1 and 2 each show exactly two movies; screen 3 shows exactly one
screen_counts = [0, 0, 0]  # indices 0,1,2 correspond to screens 1,2,3
for m in range(5):
    solver.add(Or(screen[m] == 1, screen[m] == 2, screen[m] == 3))

# Exactly two movies on screen 1
solver.add(Sum([If(screen[m] == 1, 1, 0) for m in range(5)]) == 2)
# Exactly two movies on screen 2
solver.add(Sum([If(screen[m] == 2, 1, 0) for m in range(5)]) == 2)
# Exactly one movie on screen 3
solver.add(Sum([If(screen[m] == 3, 1, 0) for m in range(5)]) == 1)

# Time assignment constraints
# Screen 1: one movie at 7PM (time=0), one at 9PM (time=2)
# Screen 2: one movie at 7PM (time=0), one at 9PM (time=2)
# Screen 3: exactly one movie at 8PM (time=1)

# For screen 1 movies: time must be either 0 or 2
for m in range(5):
    solver.add(Implies(screen[m] == 1, Or(time[m] == 0, time[m] == 2)))
# For screen 2 movies: time must be either 0 or 2
for m in range(5):
    solver.add(Implies(screen[m] == 2, Or(time[m] == 0, time[m] == 2)))
# For screen 3 movies: time must be 1
for m in range(5):
    solver.add(Implies(screen[m] == 3, time[m] == 1))

# Time uniqueness per screen: on each screen, the two movies must have different times
for m1 in range(5):
    for m2 in range(m1+1, 5):
        solver.add(Implies(And(screen[m1] == screen[m2], screen[m1] != 3), time[m1] != time[m2]))

# Ordering constraint: western begins before horror
solver.add(time[WESTERN] < time[HORROR])

# Screen restriction: sci-fi not on screen 3
solver.add(screen[SCIFI] != 3)

# Screen restriction: romance not on screen 2
solver.add(screen[ROMANCE] != 2)

# Horror and mystery on different screens
solver.add(screen[HORROR] != screen[MYSTERY])

# Answer choices: each is a pair (first=7PM, second=9PM) for screen 1
answer_choices = [
    (SCIFI, HORROR),   # "the sci-fi film, the horror film"
    (SCIFI, MYSTERY),  # "the sci-fi film, the mystery"
    (WESTERN, HORROR), # "the western, the horror film"
    (WESTERN, MYSTERY),# "the western, the mystery"
    (WESTERN, SCIFI)   # "the western, the sci-fi film"
]

# Check each answer choice
answer_index_list = []
for idx, (first_movie, second_movie) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraints for screen 1: first_movie at 7PM, second_movie at 9PM
    s_chk.add(screen[first_movie] == 1)
    s_chk.add(time[first_movie] == 0)
    s_chk.add(screen[second_movie] == 1)
    s_chk.add(time[second_movie] == 2)
    
    # Check if this configuration is possible
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)