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

# Constraint 3: Distinct Movie Assignments
for m1 in range(5):
    for m2 in range(5):
        if m1 != m2:
            solver.add(Or(movie_screen[m1] != movie_screen[m2], movie_time[m1] != movie_time[m2]))

# Constraint 4: Screen 1 and 2 Capacity
solver.add(Sum([If(movie_screen[m] == 1, 1, 0) for m in range(5)]) == 2)
solver.add(Sum([If(movie_screen[m] == 2, 1, 0) for m in range(5)]) == 2)

# Constraint 5: Screen 3 Capacity
solver.add(Sum([If(movie_screen[m] == 3, 1, 0) for m in range(5)]) == 1)

# Constraint 6: Screen 1 and 2 Time Slots
for t in [7, 9]:
    solver.add(Sum([If(And(movie_screen[m] == 1, movie_time[m] == t), 1, 0) for m in range(5)]) == 1)
    solver.add(Sum([If(And(movie_screen[m] == 2, movie_time[m] == t), 1, 0) for m in range(5)]) == 1)

# Constraint 7: Screen 3 Time Slot
solver.add(Sum([If(And(movie_screen[m] == 3, movie_time[m] == 8), 1, 0) for m in range(5)]) == 1)

# Constraint 8: Western before Horror
solver.add(movie_time[W] < movie_time[H])

# Constraint 9: Sci-fi not on Screen 3
solver.add(movie_screen[S] != 3)

# Constraint 10: Romance not on Screen 2
solver.add(movie_screen[R] != 2)

# Constraint 11: Horror and Mystery different screens
solver.add(movie_screen[H] != movie_screen[M])

# Constraint 12: Romance before Western
solver.add(movie_time[R] < movie_time[W])

# Check answer choices
answer_choices = [
    (movie_screen[H] == 1),  # A
    (movie_time[M] == 7),  # B
    (movie_screen[M] == 2),  # C
    (movie_time[S] == 9),  # D
    (movie_screen[S] == 2)   # E
]

for i in range(len(answer_choices)):
    solver.push()
    solver.add(Not(answer_choices[i]))
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()