from z3 import *

# Define constants for movies, screens, and times
H, M, R, S, W = 0, 1, 2, 3, 4
movies = [H, M, R, S, W]

# Define Z3 variables
movie_screen = Array('movie_screen', IntSort(), IntSort())
movie_time = Array('movie_time', IntSort(), IntSort())

solver = Solver()

# Constraint 1: Screen Assignment
for m in movies:
    solver.add(Or(movie_screen[m] == 1, movie_screen[m] == 2, movie_screen[m] == 3))

# Constraint 2: Time Assignment
for m in movies:
    solver.add(Or(movie_time[m] == 7, movie_time[m] == 8, movie_time[m] == 9))

# Constraint 3: Screen 1 and 2 Times
for m in movies:
    solver.add(Implies(Or(movie_screen[m] == 1, movie_screen[m] == 2), Or(movie_time[m] == 7, movie_time[m] == 9)))

# Constraint 4: Screen 3 Time
for m in movies:
    solver.add(Implies(movie_screen[m] == 3, movie_time[m] == 8))

# Constraint 5: Unique Slots
for m1 in movies:
    for m2 in movies:
        if m1 != m2:
            solver.add(Or(movie_screen[m1] != movie_screen[m2], movie_time[m1] != movie_time[m2]))

# Constraint 6: Western before Horror
solver.add(movie_time[W] < movie_time[H])

# Constraint 7: Sci-fi not on Screen 3
solver.add(movie_screen[S] != 3)

# Constraint 8: Romance not on Screen 2
solver.add(movie_screen[R] != 2)

# Constraint 9: Horror and Mystery Different Screens
solver.add(movie_screen[H] != movie_screen[M])

# Answer choices
choices = [
    [(R, 1, 7), (H, 1, 9), (W, 2, 7), (S, 2, 9), (M, 3, 8)],
    [(M, 1, 7), (R, 1, 9), (H, 2, 7), (S, 2, 9), (W, 3, 8)],
    [(W, 1, 7), (S, 1, 9), (M, 2, 7), (H, 2, 9), (R, 3, 8)],
    [(R, 1, 7), (M, 1, 9), (W, 2, 7), (H, 2, 9), (S, 3, 8)],
    [(W, 1, 7), (M, 1, 9), (S, 2, 7), (R, 2, 9), (H, 3, 8)]
]

# Check each answer choice
for i, choice in enumerate(choices):
    solver.push()
    for movie, screen, time in choice:
        solver.add(movie_screen[movie] == screen)
        solver.add(movie_time[movie] == time)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()