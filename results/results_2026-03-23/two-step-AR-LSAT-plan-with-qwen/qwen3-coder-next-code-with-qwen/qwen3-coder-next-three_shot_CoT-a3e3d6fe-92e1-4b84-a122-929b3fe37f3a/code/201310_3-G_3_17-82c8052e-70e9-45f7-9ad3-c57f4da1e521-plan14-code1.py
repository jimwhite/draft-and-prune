from z3 import *

# Movie indices: 0=horror, 1=mystery, 2=romance, 3=sci-fi, 4=western
movies = ["horror", "mystery", "romance", "sci-fi", "western"]
movie_idx = {m: i for i, m in enumerate(movies)}

# Screen variables: screen[i] = which screen movie i is shown on (1, 2, or 3)
screen = [Int(f"screen_{m}") for m in movies]

# Time slot variables: time[i] = time slot (0=7PM, 1=9PM for screens 1&2; 2=8PM for screen 3)
time_slot = [Int(f"time_{m}") for m in movies]

# Start time mapping: 7PM=7, 8PM=8, 9PM=9
start_time = [Int(f"start_{m}") for m in movies]

solver = Solver()

# Screen domain constraints
for i in range(5):
    solver.add(Or(screen[i] == 1, screen[i] == 2, screen[i] == 3))

# Time slot domain constraints
for i in range(5):
    solver.add(Or(time_slot[i] == 0, time_slot[i] == 1, time_slot[i] == 2))

# Start time mapping constraints
for i in range(5):
    solver.add(
        If(screen[i] == 1,
           If(time_slot[i] == 0, start_time[i] == 7, start_time[i] == 9),
           If(screen[i] == 2,
              If(time_slot[i] == 0, start_time[i] == 7, start_time[i] == 9),
              If(screen[i] == 3, start_time[i] == 8, False)
           )
        )
    )

# Screen capacity constraints
solver.add(Sum([If(screen[i] == 1, 1, 0) for i in range(5)]) == 2)
solver.add(Sum([If(screen[i] == 2, 1, 0) for i in range(5)]) == 2)
solver.add(Sum([If(screen[i] == 3, 1, 0) for i in range(5)]) == 1)

# Time slot consistency: screen 3 must be time_slot=2
for i in range(5):
    solver.add(Implies(screen[i] == 3, time_slot[i] == 2))

# Ordering constraint: western begins before horror
solver.add(start_time[movie_idx["western"]] < start_time[movie_idx["horror"]])

# Screen assignment constraints
solver.add(screen[movie_idx["sci-fi"]] != 3)
solver.add(screen[movie_idx["romance"]] != 2)
solver.add(screen[movie_idx["horror"]] != screen[movie_idx["mystery"]])

# Answer choices for screen 1 (7PM first, then 9PM)
answer_choices = [
    ("sci-fi", "horror"),
    ("sci-fi", "mystery"),
    ("western", "horror"),
    ("western", "mystery"),
    ("western", "sci-fi")
]

answer_index_list = []
for idx, (first_movie, second_movie) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraints for screen 1 schedule
    first_i = movie_idx[first_movie]
    second_i = movie_idx[second_movie]
    
    # First movie at 7PM on screen 1
    s_chk.add(screen[first_i] == 1)
    s_chk.add(time_slot[first_i] == 0)
    
    # Second movie at 9PM on screen 1
    s_chk.add(screen[second_i] == 1)
    s_chk.add(time_slot[second_i] == 1)
    
    # Ensure the two movies are different
    s_chk.add(first_i != second_i)
    
    # Check if this configuration is possible
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)