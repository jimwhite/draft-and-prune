from z3 import *

# Define constants for movies, screens, and times
H, M, R, S, W = 0, 1, 2, 3, 4
movies = [H, M, R, S, W]

# Define variables
movie_slot = Array('movie_slot', IntSort(), IntSort())

# Define functions for movie_screen and movie_time
def movie_screen(m):
    return If(movie_slot[m] == 0, 1, If(movie_slot[m] == 1, 1, If(movie_slot[m] == 2, 2, If(movie_slot[m] == 3, 2, 3))))

def movie_time(m):
    return If(movie_slot[m] == 0, 7, If(movie_slot[m] == 1, 9, If(movie_slot[m] == 2, 7, If(movie_slot[m] == 3, 9, 8))))

# Create a solver
solver = Solver()

# Add base constraints
solver.add(Distinct([movie_slot[m] for m in movies])) # Each movie gets a unique slot
solver.add(movie_time(W) < movie_time(H))
solver.add(movie_screen(S) != 3)
solver.add(movie_screen(R) != 2)
solver.add(movie_screen(H) != movie_screen(M))

# Add the question condition
solver.add(movie_screen(S) == movie_screen(R))

# Check answer choices
answer_choices = [
    (W, 7), (S, 9), (M, 8), (R, 9), (H, 8)
]
for i, (movie, time) in enumerate(answer_choices):
    solver.push()
    solver.add(movie_time(movie) != time)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()