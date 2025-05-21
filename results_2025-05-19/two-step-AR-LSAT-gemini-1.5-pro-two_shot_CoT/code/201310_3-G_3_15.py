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

# Constraint 2: Time Assignment
for m in range(5):
    solver.add(Or(movie_time[m] == 7, movie_time[m] == 8, movie_time[m] == 9))

# Constraint 3: Distinct Movies per Screen/Time
for m1 in range(5):
    for m2 in range(5):
        solver.add(Implies(And(movie_screen[m1] == movie_screen[m2], movie_time[m1] == movie_time[m2]), m1 == m2))

# Constraint 4: Screen 3 - One Movie at 8 PM
for m in range(5):
    solver.add(Implies(movie_screen[m] == 3, movie_time[m] == 8))

# Constraint 5: Screens 1 & 2 - Two Movies Each at 7 and 9 PM
for m in range(5):
    solver.add(Implies(Or(movie_screen[m] == 1, movie_screen[m] == 2), Or(movie_time[m] == 7, movie_time[m] == 9)))

# Constraint 6: Western before Horror
solver.add(movie_time[W] < movie_time[H])

# Constraint 7: Sci-fi not on Screen 3
solver.add(movie_screen[S] != 3)

# Constraint 8: Romance not on Screen 2
solver.add(movie_screen[R] != 2)

# Constraint 9: Horror and Mystery on different screens
solver.add(movie_screen[H] != movie_screen[M])

# Constraint 10: Western and Sci-fi on same screen
solver.add(movie_screen[W] == movie_screen[S])

# Check answer choices
answer_choices = [
    (movie_screen[H] == 2, 'A'),
    (movie_time[M] == 9, 'B'),
    (movie_screen[R] == 3, 'C'),
    (movie_time[S] == 7, 'D'),
    (movie_time[W] == 8, 'E')
]

for constraint, option in answer_choices:
    solver.push()
    solver.add(constraint)
    if solver.check() == sat:
        print(f"Option {option} is correct")
        exit()
    solver.pop()