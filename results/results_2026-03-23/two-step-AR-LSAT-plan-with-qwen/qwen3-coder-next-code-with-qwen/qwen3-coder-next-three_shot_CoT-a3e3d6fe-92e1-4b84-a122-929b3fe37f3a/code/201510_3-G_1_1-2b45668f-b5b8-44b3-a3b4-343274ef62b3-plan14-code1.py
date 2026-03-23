from z3 import *

# Accomplice indices
(QUINN, ROVERO, STANTON, TAO, VILLAS, WHITE, PETERS) = range(7)

# Position variables: pos[i] = recruitment position (1-7)
pos = [Int(f"pos_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: positions between 1 and 7
for i in range(7):
    solver.add(pos[i] >= 1, pos[i] <= 7)

# Uniqueness constraint
solver.add(Distinct(pos))

# Fixed position: Peters is recruited fourth
solver.add(pos[PETERS] == 4)

# Villas immediately before White: pos[White] = pos[Villas] + 1
solver.add(pos[WHITE] == pos[VILLAS] + 1)

# Quinn recruited earlier than Rovero
solver.add(pos[QUINN] < pos[ROVERO])

# Stanton not adjacent to Tao: |pos[Stanton] - pos[Tao]| != 1
solver.add(Or(pos[STANTON] < pos[TAO] - 1, pos[STANTON] > pos[TAO] + 1))

# Answer choices
answer_choices = [
    ["Quinn", "Tao", "Stanton", "Peters", "Villas", "White", "Rovero"],
    ["Quinn", "White", "Rovero", "Peters", "Stanton", "Villas", "Tao"],
    ["Villas", "White", "Quinn", "Stanton", "Peters", "Tao", "Rovero"],
    ["Villas", "White", "Stanton", "Peters", "Quinn", "Tao", "Rovero"],
    ["Villas", "White", "Stanton", "Peters", "Rovero", "Tao", "Quinn"]
]

# Map names to indices
name_to_idx = {
    "Quinn": QUINN,
    "Rovero": ROVERO,
    "Stanton": STANTON,
    "Tao": TAO,
    "Villas": VILLAS,
    "White": WHITE,
    "Peters": PETERS
}

# Check each answer choice
valid_indices = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add position constraints based on the choice
    for pos_idx, name in enumerate(choice):
        s_chk.add(pos[name_to_idx[name]] == pos_idx + 1)
    
    if s_chk.check() == sat:
        valid_indices.append(idx)

# Output the first valid index (as per question format)
print(valid_indices[0] if valid_indices else -1)