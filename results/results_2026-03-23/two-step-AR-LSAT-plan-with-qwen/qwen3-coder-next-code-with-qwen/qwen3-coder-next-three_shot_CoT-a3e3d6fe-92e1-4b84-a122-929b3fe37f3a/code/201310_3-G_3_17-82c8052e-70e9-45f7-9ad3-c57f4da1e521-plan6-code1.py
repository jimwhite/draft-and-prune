from z3 import *

# Movie indices: 0=horror, 1=mystery, 2=romance, 3=sci-fi, 4=western
movies = ["horror", "mystery", "romance", "sci-fi", "western"]
movie_idx = {m: i for i, m in enumerate(movies)}

# Slot indices: 0=7PM Screen1, 1=9PM Screen1, 2=7PM Screen2, 3=9PM Screen2, 4=8PM Screen3
# slot_movie[s] = movie index assigned to slot s (0-4)
slot_movie = [Int(f"slot_{s}") for s in range(5)]

# Base solver
solver = Solver()

# Domain constraints: each slot gets a movie index 0-4
for s in range(5):
    solver.add(And(slot_movie[s] >= 0, slot_movie[s] <= 4))

# Each movie appears exactly once (all slots have distinct movies)
solver.add(Distinct(slot_movie))

# Ordering constraint: western before horror
solver.add(
    If(slot_movie[0] == movie_idx["western"], 0, 
       If(slot_movie[1] == movie_idx["western"], 1,
          If(slot_movie[2] == movie_idx["western"], 2,
             If(slot_movie[3] == movie_idx["western"], 3, 4)))) <
    If(slot_movie[0] == movie_idx["horror"], 0,
       If(slot_movie[1] == movie_idx["horror"], 1,
          If(slot_movie[2] == movie_idx["horror"], 2,
             If(slot_movie[3] == movie_idx["horror"], 3, 4))))
)

# Screen constraints:
# sci-fi not on screen 3 (slot 4)
solver.add(And(*[slot_movie[s] != movie_idx["sci-fi"] for s in range(5) if s == 4]))

# romance not on screen 2 (slots 2 and 3)
solver.add(And(*[slot_movie[s] != movie_idx["romance"] for s in [2, 3]]))

# horror and mystery on different screens
def get_screen(slot_idx):
    if slot_idx in [0, 1]:
        return 1
    elif slot_idx in [2, 3]:
        return 2
    else:  # slot_idx == 4
        return 3

horror_screen = If(slot_movie[0] == movie_idx["horror"], 1,
                   If(slot_movie[1] == movie_idx["horror"], 1,
                      If(slot_movie[2] == movie_idx["horror"], 2,
                         If(slot_movie[3] == movie_idx["horror"], 2, 3))))
mystery_screen = If(slot_movie[0] == movie_idx["mystery"], 1,
                    If(slot_movie[1] == movie_idx["mystery"], 1,
                       If(slot_movie[2] == movie_idx["mystery"], 2,
                          If(slot_movie[3] == movie_idx["mystery"], 2, 3))))
solver.add(horror_screen != mystery_screen)

# Answer choices (screen1 = slots 0 and 1, in order: 7PM first)
answer_choices = [
    ("sci-fi", "horror"),   # A
    ("sci-fi", "mystery"),  # B
    ("western", "horror"),  # C
    ("western", "mystery"), # D
    ("western", "sci-fi")   # E
]

# Check each answer choice
forbidden_index_list = []
for idx, (slot0_movie, slot1_movie) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraints for screen1 assignment
    s_chk.add(slot_movie[0] == movie_idx[slot0_movie])
    s_chk.add(slot_movie[1] == movie_idx[slot1_movie])
    
    # Check if this assignment is possible
    if s_chk.check() == unsat:
        forbidden_index_list.append(idx)

print(forbidden_index_list)