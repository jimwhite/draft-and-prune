from z3 import *

# Define constants for movies, screens, and times
H = 0
M = 1
R = 2
S = 3
W = 4

# Define Z3 variables
movie_screen = Array('movie_screen', IntSort(), IntSort())
movie_time = Array('movie_time', IntSort(), IntSort())

solver = Solver()

# Constraint 1: Screen Assignment
for m in range(5):
    solver.add(Or(movie_screen[m] == 1, movie_screen[m] == 2, movie_screen[m] == 3))

# Constraint 2: Time Assignment
for m in range(5):
    solver.add(Or(movie_time[m] == 7, movie_time[m] == 8, movie_time[m] == 9))

# Constraint 3: Screen Capacity
solver.add(Sum([If(movie_screen[m] == 1, 1, 0) for m in range(5)]) == 2)
solver.add(Sum([If(movie_screen[m] == 2, 1, 0) for m in range(5)]) == 2)
solver.add(Sum([If(movie_screen[m] == 3, 1, 0) for m in range(5)]) == 1)

# Constraint 4: Time Slots per Screen
solver.add(Sum([If(And(movie_screen[m] == 1, movie_time[m] == 7), 1, 0) for m in range(5)]) == 1)
solver.add(Sum([If(And(movie_screen[m] == 1, movie_time[m] == 9), 1, 0) for m in range(5)]) == 1)
solver.add(Sum([If(And(movie_screen[m] == 2, movie_time[m] == 7), 1, 0) for m in range(5)]) == 1)
solver.add(Sum([If(And(movie_screen[m] == 2, movie_time[m] == 9), 1, 0) for m in range(5)]) == 1)
solver.add(Sum([If(And(movie_screen[m] == 3, movie_time[m] == 8), 1, 0) for m in range(5)]) == 1)


# Constraint 5: Distinctness
solver.add(Distinct([movie_screen[m] * 10 + movie_time[m] for m in range(5)]))

# Constraint 6: Western before Horror
solver.add(movie_time[W] < movie_time[H])

# Constraint 7: Sci-fi not on Screen 3
solver.add(movie_screen[S] != 3)

# Constraint 8: Romance not on Screen 2
solver.add(movie_screen[R] != 2)

# Constraint 9: Horror and Mystery on different screens
solver.add(movie_screen[H] != movie_screen[M])

# Check answer choices
options = [
    [S, H],
    [S, M],
    [W, H],
    [W, M],
    [W, S]
]

for i, option in enumerate(options):
    solver.push()
    solver.add(And(movie_screen[option[0]] == 1, movie_time[option[0]] == 7,
                   movie_screen[option[1]] == 1, movie_time[option[1]] == 9))
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()