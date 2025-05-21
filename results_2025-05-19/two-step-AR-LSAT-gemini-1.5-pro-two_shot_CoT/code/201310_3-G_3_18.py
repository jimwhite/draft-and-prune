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

# Constraint 3: Screen Capacity
solver.add(Sum([If(movie_screen[m] == 1, 1, 0) for m in movies]) == 2)
solver.add(Sum([If(movie_screen[m] == 2, 1, 0) for m in movies]) == 2)
solver.add(Sum([If(movie_screen[m] == 3, 1, 0) for m in movies]) == 1)

# Constraint 4: Time Slots per Screen
solver.add(Sum([If(And(movie_screen[m] == 1, movie_time[m] == 7), 1, 0) for m in movies]) == 1)
solver.add(Sum([If(And(movie_screen[m] == 1, movie_time[m] == 9), 1, 0) for m in movies]) == 1)
solver.add(Sum([If(And(movie_screen[m] == 2, movie_time[m] == 7), 1, 0) for m in movies]) == 1)
solver.add(Sum([If(And(movie_screen[m] == 2, movie_time[m] == 9), 1, 0) for m in movies]) == 1)
solver.add(Sum([If(And(movie_screen[m] == 3, movie_time[m] == 8), 1, 0) for m in movies]) == 1)

# Constraint 5: Distinct Movie Assignments
solver.add(Distinct([movie_screen[m] * 10 + movie_time[m] for m in movies]))

# Constraint 6: Western before Horror
solver.add(movie_time[W] < movie_time[H])

# Constraint 7: Sci-fi not on Screen 3
solver.add(movie_screen[S] != 3)

# Constraint 8: Romance not on Screen 2
solver.add(movie_screen[R] != 2)

# Constraint 9: Horror and Mystery on different screens
solver.add(movie_screen[H] != movie_screen[M])

# Constraint 10: Sci-fi and Romance on same screen
solver.add(movie_screen[S] == movie_screen[R])

# Check answer choices
answer_choices = [
    (W, 7), (S, 9), (M, 8), (R, 9), (H, 8)
]
for i, (movie, time) in enumerate(answer_choices):
    solver.push()
    solver.add(movie_time[movie] != time)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()