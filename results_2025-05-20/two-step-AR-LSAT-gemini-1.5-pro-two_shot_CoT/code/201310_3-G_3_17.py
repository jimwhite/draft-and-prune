from z3 import *

# Define variables
movie_screen = Array('movie_screen', IntSort(), IntSort())
movie_time = Array('movie_time', IntSort(), IntSort())
H, M, R, S, W = 0, 1, 2, 3, 4
movies = [H, M, R, S, W]
screens = [1, 2, 3]
times = [7, 8, 9]

solver = Solver()

# Constraints
for m in movies:
    solver.add(Or(movie_screen[m] == 1, movie_screen[m] == 2, movie_screen[m] == 3))
    solver.add(Or(movie_time[m] == 7, movie_time[m] == 8, movie_time[m] == 9))

solver.add(Sum([If(And(movie_screen[m] == 1, movie_time[m] == 7), 1, 0) for m in movies]) == 1)
solver.add(Sum([If(And(movie_screen[m] == 1, movie_time[m] == 9), 1, 0) for m in movies]) == 1)
solver.add(Sum([If(And(movie_screen[m] == 2, movie_time[m] == 7), 1, 0) for m in movies]) == 1)
solver.add(Sum([If(And(movie_screen[m] == 2, movie_time[m] == 9), 1, 0) for m in movies]) == 1)
solver.add(Sum([If(And(movie_screen[m] == 3, movie_time[m] == 8), 1, 0) for m in movies]) == 1)

solver.add(movie_time[W] < movie_time[H])
solver.add(movie_screen[S] != 3)
solver.add(movie_screen[R] != 2)
solver.add(movie_screen[H] != movie_screen[M])

# All movies shown once
for m1 in movies:
    for m2 in movies:
        if m1 != m2:
            solver.add(Or(movie_screen[m1] != movie_screen[m2], movie_time[m1] != movie_time[m2]))


choices = [
    [S, H],
    [S, M],
    [W, H],
    [W, M],
    [W, S]
]

for i, choice in enumerate(choices):
    solver.push()
    solver.add(movie_screen[choice[0]] == 1, movie_time[choice[0]] == 7)
    solver.add(movie_screen[choice[1]] == 1, movie_time[choice[1]] == 9)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()