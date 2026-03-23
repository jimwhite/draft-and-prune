from z3 import *

# Movie indices: 0=horror, 1=mystery, 2=romance, 3=sci-fi, 4=western
# Screen indices: 0=screen1, 1=screen2, 2=screen3
# Time values: 7, 8, 9

movies = ["horror", "mystery", "romance", "sci-fi", "western"]
screen_vars = [Int(f"screen_{i}") for i in range(5)]
time_vars = [Int(f"time_{i}") for i in range(5)]

solver = Solver()

# Domain constraints
for i in range(5):
    solver.add(screen_vars[i] >= 0, screen_vars[i] <= 2)
    solver.add(Or(time_vars[i] == 7, time_vars[i] == 8, time_vars[i] == 9))

# Capacity constraints
solver.add(Sum([If(screen_vars[i] == 0, 1, 0) for i in range(5)]) == 2)  # screen1: 2 movies
solver.add(Sum([If(screen_vars[i] == 1, 1, 0) for i in range(5)]) == 2)  # screen2: 2 movies
solver.add(Sum([If(screen_vars[i] == 2, 1, 0) for i in range(5)]) == 1)  # screen3: 1 movie

# Time-slot consistency constraints
for i in range(5):
    # Screen 1 movies must be at 7 or 9
    solver.add(Implies(screen_vars[i] == 0, Or(time_vars[i] == 7, time_vars[i] == 9)))
    # Screen 2 movies must be at 7 or 9
    solver.add(Implies(screen_vars[i] == 1, Or(time_vars[i] == 7, time_vars[i] == 9)))
    # Screen 3 movie must be at 8
    solver.add(Implies(screen_vars[i] == 2, time_vars[i] == 8))

# Temporal ordering constraints
# Western before horror: time[western] < time[horror]
solver.add(time_vars[4] < time_vars[0])

# Sci-fi not on screen 3
solver.add(screen_vars[3] != 2)

# Romance not on screen 2
solver.add(screen_vars[2] != 1)

# Horror and mystery on different screens
solver.add(screen_vars[0] != screen_vars[1])

# Answer choices (screen 1 assignments: [7PM movie, 9PM movie])
answer_choices = [
    (3, 0),  # sci-fi at 7PM, horror at 9PM
    (3, 1),  # sci-fi at 7PM, mystery at 9PM
    (4, 0),  # western at 7PM, horror at 9PM
    (4, 1),  # western at 7PM, mystery at 9PM
    (4, 3)   # western at 7PM, sci-fi at 9PM
]

answer_index_list = []
for idx, (first_movie, second_movie) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Screen 1 has exactly these two movies at specified times
    s_chk.add(screen_vars[first_movie] == 0, time_vars[first_movie] == 7)
    s_chk.add(screen_vars[second_movie] == 0, time_vars[second_movie] == 9)
    
    # Ensure the two movies are different
    s_chk.add(first_movie != second_movie)
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)