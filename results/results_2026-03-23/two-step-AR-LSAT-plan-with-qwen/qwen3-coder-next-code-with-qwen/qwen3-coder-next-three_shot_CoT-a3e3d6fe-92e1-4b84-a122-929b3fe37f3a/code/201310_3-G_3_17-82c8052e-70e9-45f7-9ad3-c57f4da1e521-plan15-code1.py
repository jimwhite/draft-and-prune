from z3 import *

# Movie indices: 0=horror, 1=mystery, 2=romance, 3=sci-fi, 4=western
(HORROR, MYSTERY, ROMANCE, SCIFI, WESTERN) = range(5)

# Variables: screen[i] = screen number (1,2,3), slot[i] = time slot (0=7pm, 1=8pm, 2=9pm)
screen = [Int(f"screen_{i}") for i in range(5)]
slot = [Int(f"slot_{i}") for i in range(5)]

solver = Solver()

# Domain constraints
for i in range(5):
    solver.add(screen[i] >= 1, screen[i] <= 3)
    solver.add(slot[i] >= 0, slot[i] <= 2)

# Screen capacity constraints
# Exactly two movies on screen 1, exactly two on screen 2, exactly one on screen 3
screen_counts = [Sum([If(screen[i] == s, 1, 0) for i in range(5)]) for s in [1, 2, 3]]
solver.add(screen_counts[0] == 2, screen_counts[1] == 2, screen_counts[2] == 1)

# Screen 1 and 2 must have time slots {0,2} (7pm and 9pm), screen 3 has slot 1 (8pm)
# For each movie on screen 1 or 2, slot must be 0 or 2
for i in range(5):
    solver.add(Implies(screen[i] == 1, Or(slot[i] == 0, slot[i] == 2)))
    solver.add(Implies(screen[i] == 2, Or(slot[i] == 0, slot[i] == 2)))
    solver.add(Implies(screen[i] == 3, slot[i] == 1))

# Within each screen, time slots must be distinct
for s in [1, 2]:
    for i in range(5):
        for j in range(i + 1, 5):
            solver.add(Implies(And(screen[i] == s, screen[j] == s), slot[i] != slot[j]))

# Ordering constraint: western begins before horror film
solver.add(Or(
    And(slot[WESTERN] < slot[HORROR]),
    And(slot[WESTERN] == slot[HORROR], screen[WESTERN] < screen[HORROR])
))

# Sci-fi film is not on screen 3
solver.add(screen[SCIFI] != 3)

# Romance is not on screen 2
solver.add(screen[ROMANCE] != 2)

# Horror and mystery are on different screens
solver.add(screen[HORROR] != screen[MYSTERY])

# Answer choices for screen 1: [movie_at_7pm, movie_at_9pm]
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
    
    # Screen 1 must have exactly these two movies at slots 0 and 2 respectively
    s_chk.add(screen[movie0] == 1, slot[movie0] == 0)
    s_chk.add(screen[movie1] == 1, slot[movie1] == 2)
    
    # Ensure no other movie is on screen 1
    for i in range(5):
        if i != movie0 and i != movie1:
            s_chk.add(screen[i] != 1)
    
    # Check feasibility
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)