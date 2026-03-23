from z3 import *

# Movie indices: horror=0, mystery=1, romance=2, sci-fi=3, western=4
movies = ["horror", "mystery", "romance", "sci-fi", "western"]
n_movies = 5

# Variables
screen = [Int(f"screen_{i}") for i in range(n_movies)]
time = [Int(f"time_{i}") for i in range(n_movies)]

solver = Solver()

# Screen capacity constraints
screen_counts = [Sum([If(screen[i] == s, 1, 0) for i in range(n_movies)]) for s in range(3)]
solver.add(screen_counts[0] == 2)  # screen1
solver.add(screen_counts[1] == 2)  # screen2
solver.add(screen_counts[2] == 1)  # screen3

# Time consistency with screens
for i in range(n_movies):
    # Screen 0 (screen1): time must be 0 or 2
    solver.add(Implies(screen[i] == 0, Or(time[i] == 0, time[i] == 2)))
    # Screen 1 (screen2): time must be 0 or 2
    solver.add(Implies(screen[i] == 1, Or(time[i] == 0, time[i] == 2)))
    # Screen 2 (screen3): time must be 1
    solver.add(Implies(screen[i] == 2, time[i] == 1))

# No two movies share both screen and time
for i in range(n_movies):
    for j in range(i + 1, n_movies):
        solver.add(Implies(screen[i] == screen[j], time[i] != time[j]))

# Global ordering constraints
# Western before horror: time[western] < time[horror]
solver.add(time[4] < time[0])

# Sci-fi not on screen 3
solver.add(screen[3] != 2)

# Romance not on screen 2
solver.add(screen[2] != 1)

# Horror and mystery on different screens
solver.add(screen[0] != screen[1])

# Answer choices: pairs (first_movie, second_movie) for screen 1
answer_choices = [
    (3, 0),  # sci-fi, horror
    (3, 1),  # sci-fi, mystery
    (4, 0),  # western, horror
    (4, 1),  # western, mystery
    (4, 3)   # western, sci-fi
]

# Check each answer choice
answer_index_list = []
for idx, (first, second) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Both movies on screen 1
    s_chk.add(screen[first] == 0)
    s_chk.add(screen[second] == 0)
    
    # First movie at 7PM (time=0), second at 9PM (time=2)
    s_chk.add(time[first] == 0)
    s_chk.add(time[second] == 2)
    
    # No other movies on screen 1
    for i in range(n_movies):
        if i != first and i != second:
            s_chk.add(screen[i] != 0)
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)