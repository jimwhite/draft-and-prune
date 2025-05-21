from z3 import *

# Define constants for movies, screens, and times
H, M, R, S, W = 0, 1, 2, 3, 4
S1, S2, S3 = 0, 1, 2
T7, T8, T9 = 0, 1, 2

# Define Z3 variables
movie_screen = Array('movie_screen', IntSort(), IntSort())
movie_time = Array('movie_time', IntSort(), IntSort())

solver = Solver()

# Constraint 1: Screen Assignment Bounds
for m in range(5):
    solver.add(And(movie_screen[m] >= 0, movie_screen[m] <= 2))

# Constraint 2: Time Assignment Bounds
for m in range(5):
    solver.add(And(movie_time[m] >= 0, movie_time[m] <= 2))

# Constraint 3: Unique Screen-Time Slots
# Use Datatype to create tuples for distinct constraint
ScreenTime = Datatype('ScreenTime')
ScreenTime.declare('st', ('screen', IntSort()), ('time', IntSort()))
ScreenTime = ScreenTime.create()
solver.add(Distinct([ScreenTime.st(movie_screen[m], movie_time[m]) for m in range(5)]))


# Constraint 4: Screen Capacity
solver.add(Sum([If(movie_screen[m] == S1, 1, 0) for m in range(5)]) == 2)
solver.add(Sum([If(movie_screen[m] == S2, 1, 0) for m in range(5)]) == 2)
solver.add(Sum([If(movie_screen[m] == S3, 1, 0) for m in range(5)]) == 1)

# Constraint 5: Screen 3 Time
for m in range(5):
    solver.add(Implies(movie_screen[m] == S3, movie_time[m] == T8))

# Constraint 6: Western before Horror
solver.add(movie_time[W] < movie_time[H])

# Constraint 7: Sci-fi not on Screen 3
solver.add(movie_screen[S] != S3)

# Constraint 8: Romance not on Screen 2
solver.add(movie_screen[R] != S2)

# Constraint 9: Horror and Mystery Different Screens
solver.add(movie_screen[H] != movie_screen[M])

# Check answer choices
choices = [
    (S, T7, H, T9),  # Sci-fi, Horror
    (S, T7, M, T9),  # Sci-fi, Mystery
    (S, T7, W, T9),  # Sci-fi, Western
    (W, T7, H, T9),  # Western, Horror
    (W, T7, M, T9)   # Western, Mystery
]

for i, (m1, t1, m2, t2) in enumerate(choices):
    solver.push()
    solver.add(And(movie_screen[m1] == S2, movie_time[m1] == t1,
                   movie_screen[m2] == S2, movie_time[m2] == t2))
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
