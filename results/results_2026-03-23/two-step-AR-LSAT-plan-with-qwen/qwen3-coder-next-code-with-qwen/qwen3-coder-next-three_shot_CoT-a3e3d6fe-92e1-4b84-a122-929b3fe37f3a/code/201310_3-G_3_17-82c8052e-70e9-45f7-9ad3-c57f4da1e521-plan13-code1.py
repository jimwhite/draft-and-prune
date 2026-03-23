from z3 import *

# Movie indices: 0=horror, 1=mystery, 2=romance, 3=sci-fi, 4=western
movies = ["horror", "mystery", "romance", "sci-fi", "western"]
movie_idx = {m: i for i, m in enumerate(movies)}

# Time slot variables: 0=7pm-s1, 1=7pm-s2, 2=8pm-s3, 3=9pm-s1, 4=9pm-s2
slot = [Int(f"slot_{m}") for m in movies]

# Base solver
solver = Solver()

# Domain constraints: each movie assigned to exactly one slot (0-4)
for i in range(5):
    solver.add(slot[i] >= 0, slot[i] <= 4)

# All movies assigned to distinct slots
solver.add(Distinct(*slot))

# Screen mapping: slot 0,3 -> screen1; slot 1,4 -> screen2; slot 2 -> screen3
def get_screen(slot_val):
    return If(Or(slot_val == 0, slot_val == 3), 1,
              If(Or(slot_val == 1, slot_val == 4), 2, 3))

# Ordering constraint: western begins before horror film
solver.add(slot[movie_idx["western"]] < slot[movie_idx["horror"]])

# Sci-fi not on screen 3 (slot != 2)
solver.add(slot[movie_idx["sci-fi"]] != 2)

# Romance not on screen 2 (slot not in {1,4})
solver.add(And(slot[movie_idx["romance"]] != 1, slot[movie_idx["romance"]] != 4))

# Horror and mystery on different screens
solver.add(get_screen(slot[movie_idx["horror"]]) != get_screen(slot[movie_idx["mystery"]]))

# Answer choices: pairs (first, second) for screen1 (7pm then 9pm)
answer_choices = [
    ("sci-fi", "horror"),
    ("sci-fi", "mystery"),
    ("western", "horror"),
    ("western", "mystery"),
    ("western", "sci-fi")
]

# Check each answer choice
impossible_indices = []
for idx, (first_movie, second_movie) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert first movie is at 7pm (slot0), second movie is at 9pm (slot3)
    s_chk.add(slot[movie_idx[first_movie]] == 0)
    s_chk.add(slot[movie_idx[second_movie]] == 3)
    
    # If UNSAT, this pair cannot be screen1's list
    if s_chk.check() == unsat:
        impossible_indices.append(idx)

print(impossible_indices)