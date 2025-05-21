from z3 import *

# Define constants for movies, screens, and times
H = 0
M = 1
R = 2
S = 3
W = 4

S1 = 0
S2 = 1
S3 = 2

T7 = 0
T8 = 1
T9 = 2

# Define Z3 variables
movie_screen = Array('movie_screen', IntSort(), IntSort())
movie_time = Array('movie_time', IntSort(), IntSort())
m = Int('m')

# Create solver and add constraints
solver = Solver()

# Constraint 1 & 2 (Domains)
solver.add(ForAll([m], And(movie_screen[m] >= 0, movie_screen[m] <= 2)))
solver.add(ForAll([m], And(movie_time[m] >= 0, movie_time[m] <= 2)))

# Constraint 3 (Unique Screen/Time)
solver.add(Distinct([movie_screen[m] * 3 + movie_time[m] for m in range(5)]))

# Constraint 4, 5, 6 (Screen Movie Counts)
solver.add(Sum([If(movie_screen[m] == S1, 1, 0) for m in range(5)]) == 2)
solver.add(Sum([If(movie_screen[m] == S2, 1, 0) for m in range(5)]) == 2)
solver.add(Sum([If(movie_screen[m] == S3, 1, 0) for m in range(5)]) == 1)

# Constraint 7-10 (Specific Movie Constraints)
solver.add(movie_time[W] < movie_time[H])
solver.add(movie_screen[S] != S3)
solver.add(movie_screen[R] != S2)
solver.add(movie_screen[H] != movie_screen[M])

# Constraint 11 & 12 (Screen Time Constraints)
solver.add(ForAll([m], Implies(Or(movie_screen[m] == S1, movie_screen[m] == S2), Or(movie_time[m] == T7, movie_time[m] == T9))))
solver.add(ForAll([m], Implies(movie_screen[m] == S3, movie_time[m] == T8)))


# Check answer choices
options = [
    [(R, S1, T7), (H, S1, T9), (W, S2, T7), (S, S2, T9), (M, S3, T8)],
    [(M, S1, T7), (R, S1, T9), (H, S2, T7), (S, S2, T9), (W, S3, T8)],
    [(W, S1, T7), (S, S1, T9), (M, S2, T7), (H, S2, T9), (R, S3, T8)],
    [(R, S1, T7), (M, S1, T9), (W, S2, T7), (H, S2, T9), (S, S3, T8)],
    [(W, S1, T7), (M, S1, T9), (S, S2, T7), (R, S2, T9), (H, S3, T8)]
]

for i, option in enumerate(options):
    solver.push()
    for movie, screen, time in option:
        solver.add(movie_screen[movie] == screen)
        solver.add(movie_time[movie] == time)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()