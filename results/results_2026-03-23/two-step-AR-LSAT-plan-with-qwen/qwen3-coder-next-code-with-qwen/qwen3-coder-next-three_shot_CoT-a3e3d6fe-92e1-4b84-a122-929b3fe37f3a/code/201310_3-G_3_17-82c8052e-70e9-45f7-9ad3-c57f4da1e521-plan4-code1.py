from z3 import *

# Movie indices: 0=horror, 1=mystery, 2=romance, 3=sci-fi, 4=western
(HORROR, MYSTERY, ROMANCE, SCI_FI, WESTERN) = range(5)

# Time slot indices: 0=(1,7), 1=(1,9), 2=(2,7), 3=(2,9), 4=(3,8)
# Screen mapping: slot 0,1 -> screen 1; slot 2,3 -> screen 2; slot 4 -> screen 3
pos = [Int(f"pos_{i}") for i in range(5)]

# Base solver
solver = Solver()

# Uniqueness constraint: each movie assigned to exactly one slot
solver.add(Distinct(pos))

# Screen and time constraints encoded via position indices:
# pos 0,1 -> screen 1; pos 2,3 -> screen 2; pos 4 -> screen 3
def get_screen(slot_idx):
    if slot_idx == 0 or slot_idx == 1:
        return 1
    elif slot_idx == 2 or slot_idx == 3:
        return 2
    else:  # slot_idx == 4
        return 3

# Ordering constraint: western before horror => pos_western < pos_horror
solver.add(pos[WESTERN] < pos[HORROR])

# Sci-fi not on screen 3 => sci-fi position != 4
solver.add(pos[SCI_FI] != 4)

# Romance not on screen 2 => romance position not in {2,3}
solver.add(pos[ROMANCE] != 2)
solver.add(pos[ROMANCE] != 3)

# Horror and mystery on different screens
solver.add(get_screen(pos[HORROR]) != get_screen(pos[MYSTERY]))

# Answer choices (screen 1: [7PM, 9PM] = slots 0 and 1)
answer_choices = [
    (SCI_FI, HORROR),   # 'the sci-fi film, the horror film'
    (SCI_FI, MYSTERY),  # 'the sci-fi film, the mystery'
    (WESTERN, HORROR),  # 'the western, the horror film'
    (WESTERN, MYSTERY), # 'the western, the mystery'
    (WESTERN, SCI_FI)   # 'the western, the sci-fi film'
]

# Check each answer choice
answer_index_list = []
for idx, (movie1, movie2) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assign movie1 to slot 0 (7PM) and movie2 to slot 1 (9PM)
    s_chk.add(pos[movie1] == 0)
    s_chk.add(pos[movie2] == 1)
    
    # Ensure no other movie is assigned to slots 0 or 1
    for m in range(5):
        if m != movie1 and m != movie2:
            s_chk.add(pos[m] != 0)
            s_chk.add(pos[m] != 1)
    
    # If UNSAT, this list CANNOT be accurate
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)