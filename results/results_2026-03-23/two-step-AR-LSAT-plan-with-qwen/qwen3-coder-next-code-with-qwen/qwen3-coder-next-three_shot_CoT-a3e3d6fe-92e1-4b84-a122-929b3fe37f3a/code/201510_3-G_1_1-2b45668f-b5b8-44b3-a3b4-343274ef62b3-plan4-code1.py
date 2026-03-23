from z3 import *

# Accomplice indices
(QUINN, TAO, STANTON, PETERS, VILLAS, WHITE, ROVERO) = range(7)

# Position variables: pos[i] is the recruitment position (1-7) of accomplice i
pos = [Int(f"pos_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: All positions distinct and in [1,7]
solver.add(Distinct(pos))
for i in range(7):
    solver.add(pos[i] >= 1, pos[i] <= 7)

# Fixed constraint: Peters was recruited fourth
solver.add(pos[PETERS] == 4)

# Villas-White adjacency constraint: Villas immediately before White
solver.add(pos[WHITE] == pos[VILLAS] + 1)

# Quinn-Rovero constraint: Quinn recruited earlier than Rovero
solver.add(pos[QUINN] < pos[ROVERO])

# Stanton-Tao non-adjacency constraint: |pos[Stanton] - pos[Tao]| != 1
solver.add(Abs(pos[STANTON] - pos[TAO]) != 1)

# Answer choices as lists of accomplice names
answer_choices = [
    ['Quinn', 'Tao', 'Stanton', 'Peters', 'Villas', 'White', 'Rovero'],
    ['Quinn', 'White', 'Rovero', 'Peters', 'Stanton', 'Villas', 'Tao'],
    ['Villas', 'White', 'Quinn', 'Stanton', 'Peters', 'Tao', 'Rovero'],
    ['Villas', 'White', 'Stanton', 'Peters', 'Quinn', 'Tao', 'Rovero'],
    ['Villas', 'White', 'Stanton', 'Peters', 'Rovero', 'Tao', 'Quinn']
]

# Mapping from name to index
name_to_idx = {
    'Quinn': QUINN,
    'Tao': TAO,
    'Stanton': STANTON,
    'Peters': PETERS,
    'Villas': VILLAS,
    'White': WHITE,
    'Rovero': ROVERO
}

# Check each answer choice
satisfiable_indices = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraints for the specific order in this answer choice
    for position, name in enumerate(choice):
        s_chk.add(pos[name_to_idx[name]] == position + 1)
    
    if s_chk.check() == sat:
        satisfiable_indices.append(idx)

# Output the index of the only satisfiable choice
print(satisfiable_indices[0] if len(satisfiable_indices) == 1 else satisfiable_indices)