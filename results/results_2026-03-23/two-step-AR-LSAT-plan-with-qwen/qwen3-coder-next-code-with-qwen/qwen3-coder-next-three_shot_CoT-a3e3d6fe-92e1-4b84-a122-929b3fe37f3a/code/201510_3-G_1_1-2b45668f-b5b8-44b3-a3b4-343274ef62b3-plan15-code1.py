from z3 import *

# Accomplice indices
(PETERS, QUINN, ROVERO, STANTON, TAO, VILLAS, WHITE) = range(7)

# Position variables: pos[person] = recruitment position (1-7)
pos = [Int(f"pos_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: positions 1-7 and all distinct
for i in range(7):
    solver.add(pos[i] >= 1, pos[i] <= 7)
solver.add(Distinct(*pos))

# Fixed constraint: Peters is recruited fourth
solver.add(pos[PETERS] == 4)

# Villas immediately before White: pos[WHITE] = pos[VILLAS] + 1
solver.add(pos[WHITE] == pos[VILLAS] + 1)

# Quinn earlier than Rovero
solver.add(pos[QUINN] < pos[ROVERO])

# Stanton not adjacent to Tao: |pos[STANTON] - pos[TAO]| != 1
# This is equivalent to: (pos[STANTON] - pos[TAO] != 1) AND (pos[STANTON] - pos[TAO] != -1)
solver.add(pos[STANTON] - pos[TAO] != 1, pos[STANTON] - pos[TAO] != -1)

# Answer choices (each is a list of accomplice names in order)
choices = [
    ["QUINN", "TAO", "STANTON", "PETERS", "VILLAS", "WHITE", "ROVERO"],
    ["QUINN", "WHITE", "ROVERO", "PETERS", "STANTON", "VILLAS", "TAO"],
    ["VILLAS", "WHITE", "QUINN", "STANTON", "PETERS", "TAO", "ROVERO"],
    ["VILLAS", "WHITE", "STANTON", "PETERS", "QUINN", "TAO", "ROVERO"],
    ["VILLAS", "WHITE", "STANTON", "PETERS", "ROVERO", "TAO", "QUINN"]
]

# Map names to indices
name_to_idx = {
    "PETERS": PETERS,
    "QUINN": QUINN,
    "ROVERO": ROVERO,
    "STANTON": STANTON,
    "TAO": TAO,
    "VILLAS": VILLAS,
    "WHITE": WHITE
}

# Check each choice
answer_index_list = []
for idx, choice in enumerate(choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assign positions based on the sequence (1-indexed)
    for i, name in enumerate(choice):
        person_idx = name_to_idx[name]
        s_chk.add(pos[person_idx] == i + 1)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)