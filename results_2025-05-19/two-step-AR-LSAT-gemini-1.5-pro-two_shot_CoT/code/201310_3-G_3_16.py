from z3 import *

# Define constants for movies, screens, and times
H = 0
M = 1
R = 2
S = 3
W = 4

# Define variables
movie_screen = Array('movie_screen', IntSort(), IntSort())
movie_time = Array('movie_time', IntSort(), IntSort())

solver = Solver()

# Constraint 1: Screen Assignment
for m in range(5):
    solver.add(Or(movie_screen[m] == 1, movie_screen[m] == 2, movie_screen[m] == 3))

# Constraint 2: Distinct Screens
solver.add(Distinct([movie_screen[m] for m in range(5)]))

# Constraint 3: Time Assignment
for m in range(5):
    solver.add(Or(movie_time[m] == 7, movie_time[m] == 8, movie_time[m] == 9))

# Constraint 4: Screen 1 and 2 Times
for m in range(5):
    solver.add(Implies(Or(movie_screen[m] == 1, movie_screen[m] == 2), Or(movie_time[m] == 7, movie_time[m] == 9)))

# Constraint 5: Screen 3 Time
for m in range(5):
    solver.add(Implies(movie_screen[m] == 3, movie_time[m] == 8))

# Constraint 6: Two Movies per Screen 1 & 2
for s in [1, 2]:
    solver.add(Sum([If(movie_screen[m] == s, 1, 0) for m in range(5)]) == 2)

# Constraint 7: One Movie on Screen 3
solver.add(Sum([If(movie_screen[m] == 3, 1, 0) for m in range(5)]) == 1)

# Constraint 8: Two Movies per Time Slot on Screens 1 & 2
for t in [7, 9]:
    solver.add(Sum([If(And(Or(movie_screen[m] == 1, movie_screen[m] == 2), movie_time[m] == t), 1, 0) for m in range(5)]) == 2)

# Constraint 9: Western before Horror
solver.add(movie_time[W] < movie_time[H])

# Constraint 10: Sci-fi not on Screen 3
solver.add(movie_screen[S] != 3)

# Constraint 11: Romance not on Screen 2
solver.add(movie_screen[R] != 2)

# Constraint 12: Horror and Mystery Different Screens
solver.add(movie_screen[H] != movie_screen[M])

# Constraint 13: Romance before Western
solver.add(movie_time[R] < movie_time[W])

# Check answer choices
choices = [
    (movie_screen[H] != 1, 'A'),
    (movie_time[M] != 7, 'B'),
    (movie_screen[M] != 2, 'C'),
    (movie_time[S] != 9, 'D'),
    (movie_screen[S] != 2, 'E')
]

for constraint, option in choices:
    solver.push()
    solver.add(constraint)
    if solver.check() == unsat:
        print(f"Option {option} is correct")
        exit()
    solver.pop()