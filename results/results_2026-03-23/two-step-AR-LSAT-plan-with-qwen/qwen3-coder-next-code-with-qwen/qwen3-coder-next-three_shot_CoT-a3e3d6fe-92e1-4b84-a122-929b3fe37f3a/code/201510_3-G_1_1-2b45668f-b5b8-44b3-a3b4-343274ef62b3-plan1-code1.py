from z3 import *

# Accomplice indices
(PETERS, QUINN, ROVERO, STANTON, TAO, VILLAS, WHITE) = range(7)

# Position variables: pos[i] is the recruitment rank (1-7) of accomplice i
pos = [Int(f"pos_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: positions are 1-7 and all distinct
for i in range(7):
    solver.add(pos[i] >= 1, pos[i] <= 7)
solver.add(Distinct(*pos))

# Peters constraint: recruited fourth
solver.add(pos[PETERS] == 4)

# Villas-White adjacency constraint: Villas immediately before White
solver.add(pos[VILLAS] + 1 == pos[WHITE])

# Quinn-Rovero order constraint: Quinn recruited earlier than Rovero
solver.add(pos[QUINN] < pos[ROVERO])

# Stanton-Tao non-adjacency constraint: |pos[Stanton] - pos[Tao]| != 1
solver.add(Abs(pos[STANTON] - pos[TAO]) != 1)

# Answer choices (each is a list of accomplice names in order from first to last)
answer_choices = [
    ["Quinn", "Tao", "Stanton", "Peters", "Villas", "White", "Rovero"],
    ["Quinn", "White", "Rovero", "Peters", "Stanton", "Villas", "Tao"],
    ["Villas", "White", "Quinn", "Stanton", "Peters", "Tao", "Rovero"],
    ["Villas", "White", "Stanton", "Peters", "Quinn", "Tao", "Rovero"],
    ["Villas", "White", "Stanton", "Peters", "Rovero", "Tao", "Quinn"]
]

# Map names to indices
name_to_idx = {
    "Peters": PETERS,
    "Quinn": QUINN,
    "Rovero": ROVERO,
    "Stanton": STANTON,
    "Tao": TAO,
    "Villas": VILLAS,
    "White": WHITE
}

# Check each answer choice
satisfiable_indices = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the position constraints based on the choice order
    for rank, name in enumerate(choice, start=1):
        s_chk.add(pos[name_to_idx[name]] == rank)
    
    if s_chk.check() == sat:
        satisfiable_indices.append(idx)

print(satisfiable_indices)