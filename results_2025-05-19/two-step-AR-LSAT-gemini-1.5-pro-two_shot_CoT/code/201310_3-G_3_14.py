from z3 import *

# Define variables
H, M, R, S, W = 0, 1, 2, 3, 4
movie_screen = Array('movie_screen', IntSort(), IntSort())
movie_time = Array('movie_time', IntSort(), IntSort())
solver = Solver()

# Constraints 1-5
for m in range(5):
    solver.add(Or(movie_screen[m] == 1, movie_screen[m] == 2, movie_screen[m] == 3))
    solver.add(Or(movie_time[m] == 7, movie_time[m] == 8, movie_time[m] == 9))

solver.add(Sum([If(movie_screen[m] == 1, 1, 0) for m in range(5)]) == 2)
solver.add(Sum([If(movie_screen[m] == 2, 1, 0) for m in range(5)]) == 2)
solver.add(Sum([If(movie_screen[m] == 3, 1, 0) for m in range(5)]) == 1)

solver.add(Sum([If(And(movie_screen[m] == 1, movie_time[m] == 7), 1, 0) for m in range(5)]) == 1)
solver.add(Sum([If(And(movie_screen[m] == 1, movie_time[m] == 9), 1, 0) for m in range(5)]) == 1)
solver.add(Sum([If(And(movie_screen[m] == 2, movie_time[m] == 7), 1, 0) for m in range(5)]) == 1)
solver.add(Sum([If(And(movie_screen[m] == 2, movie_time[m] == 9), 1, 0) for m in range(5)]) == 1)
solver.add(Sum([If(And(movie_screen[m] == 3, movie_time[m] == 8), 1, 0) for m in range(5)]) == 1)

solver.add(Distinct([movie_screen[m] * 10 + movie_time[m] for m in range(5)]))


# Constraints 6-9
solver.add(movie_time[W] < movie_time[H])
solver.add(movie_screen[S] != 3)
solver.add(movie_screen[R] != 2)
solver.add(movie_screen[H] != movie_screen[M])

# Check answer choices
choices = [
    [S, H], [S, M], [S, W], [W, H], [W, M]
]

for i, (m1, m2) in enumerate(choices):
    solver.push()
    solver.add(And(movie_screen[m1] == 2, movie_time[m1] == 7,
                   movie_screen[m2] == 2, movie_time[m2] == 9))
    if solver.check() == unsat:
        print(f'Option {chr(65 + i)} is correct')
        exit()
    solver.pop()