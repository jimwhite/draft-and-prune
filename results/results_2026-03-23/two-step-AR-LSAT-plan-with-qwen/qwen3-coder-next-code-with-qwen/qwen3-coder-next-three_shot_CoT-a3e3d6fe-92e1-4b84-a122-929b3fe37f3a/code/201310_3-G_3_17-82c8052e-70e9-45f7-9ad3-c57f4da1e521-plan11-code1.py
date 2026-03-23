from z3 import *

# Movie indices: 0=horror, 1=mystery, 2=romance, 3=sci-fi, 4=western
(HORROR, MYSTERY, ROMANCE, SCIFI, WESTERN) = range(5)
movies = ["horror", "mystery", "romance", "sci-fi", "western"]

# Variables: screen[m] in {1,2,3}, slot[m] in {0,1} (but screen 3 only uses slot 0)
screen = [Int(f"screen_{m}") for m in range(5)]
slot = [Int(f"slot_{m}") for m in range(5)]

solver = Solver()

# Screen domain constraints
for m in range(5):
    solver.add(screen[m] >= 1, screen[m] <= 3)
    # For screens 1 and 2: slot can be 0 or 1; for screen 3: slot must be 0
    solver.add(Or(
        And(screen[m] == 1, Or(slot[m] == 0, slot[m] == 1)),
        And(screen[m] == 2, Or(slot[m] == 0, slot[m] == 1)),
        And(screen[m] == 3, slot[m] == 0)
    ))

# Screen capacity constraints
is_screen1 = [If(screen[m] == 1, 1, 0) for m in range(5)]
is_screen2 = [If(screen[m] == 2, 1, 0) for m in range(5)]
is_screen3 = [If(screen[m] == 3, 1, 0) for m in range(5)]

solver.add(Sum(is_screen1) == 2)
solver.add(Sum(is_screen2) == 2)
solver.add(Sum(is_screen3) == 1)

# Time ordering: define start_time as integer (7=0, 8=1, 9=2)
# For screen 1 or 2 with slot 0: time = 0
# For screen 3 (slot always 0): time = 1
# For screen 1 or 2 with slot 1: time = 2
time_expr = [
    If(And(screen[m] == 1, slot[m] == 0), 0,
       If(And(screen[m] == 2, slot[m] == 0), 0,
          If(screen[m] == 3, 1,
             If(And(screen[m] == 1, slot[m] == 1), 2,
                If(And(screen[m] == 2, slot[m] == 1), 2, -1)
             )
          )
       )
    ) for m in range(5)
]

# Western before horror
solver.add(time_expr[WESTERN] < time_expr[HORROR])

# Sci-fi not on screen 3
solver.add(screen[SCIFI] != 3)

# Romance not on screen 2
solver.add(screen[ROMANCE] != 2)

# Horror and mystery on different screens
solver.add(screen[HORROR] != screen[MYSTERY])

# Answer choices: each is a pair (movie_A at 7 PM, movie_B at 9 PM) for screen 1
answer_choices = [
    (SCIFI, HORROR),   # 'the sci-fi film, the horror film'
    (SCIFI, MYSTERY),  # 'the sci-fi film, the mystery'
    (WESTERN, HORROR), # 'the western, the horror film'
    (WESTERN, MYSTERY),# 'the western, the mystery'
    (WESTERN, SCIFI)   # 'the western, the sci-fi film'
]

answer_index_list = []
for idx, (movie0, movie1) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Screen 1: movie0 at 7 PM (slot=0), movie1 at 9 PM (slot=1)
    s_chk.add(screen[movie0] == 1, slot[movie0] == 0)
    s_chk.add(screen[movie1] == 1, slot[movie1] == 1)
    
    # No other movie on screen 1
    for m in range(5):
        if m != movie0 and m != movie1:
            s_chk.add(screen[m] != 1)
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)