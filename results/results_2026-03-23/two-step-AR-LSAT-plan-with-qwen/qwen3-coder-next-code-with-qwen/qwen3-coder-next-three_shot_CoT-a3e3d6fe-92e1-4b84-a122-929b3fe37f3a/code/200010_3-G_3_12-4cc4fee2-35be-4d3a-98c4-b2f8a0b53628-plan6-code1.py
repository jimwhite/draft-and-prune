from z3 import *

# Compositions and their indices
compositions = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']
comp_indices = {c: i for i, c in enumerate(compositions)}

# Position variables
pos = {c: Int(f"pos_{c}") for c in compositions}

# Base solver
solver = Solver()

# Distinctness constraint: all positions are distinct (0-7)
solver.add(Distinct(*pos.values()))
for c in compositions:
    solver.add(pos[c] >= 0, pos[c] <= 7)

# T-F-R adjacency constraint: T immediately before F OR T immediately after R
solver.add(Or(pos['T'] + 1 == pos['F'], pos['R'] + 1 == pos['T']))

# Gap constraint: at least two compositions between F and R
solver.add(Or(pos['F'] + 2 <= pos['R'], pos['R'] + 2 <= pos['F']))

# O position constraint: O is first (0) or fifth (4)
solver.add(Or(pos['O'] == 0, pos['O'] == 4))

# Eighth position constraint: L or H is eighth (position 7)
solver.add(Or(pos['L'] == 7, pos['H'] == 7))

# P before S constraint
solver.add(pos['P'] < pos['S'])

# O-S separation constraint: at least one composition between O and S
solver.add(Or(pos['O'] + 1 <= pos['S'], pos['S'] + 1 <= pos['O']))

# Answer choices
answer_choices = [
    ['L', 'P', 'S', 'R', 'O', 'T', 'F', 'H'],
    ['O', 'T', 'P', 'F', 'S', 'H', 'R', 'L'],
    ['P', 'T', 'F', 'S', 'L', 'R', 'O', 'H'],
    ['P', 'T', 'F', 'S', 'O', 'R', 'L', 'H'],
    ['T', 'F', 'P', 'R', 'O', 'L', 'S', 'H']
]

# Check each choice
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraints that match the exact positions from the choice
    for i, comp in enumerate(choice):
        s_chk.add(pos[comp] == i)
    
    if s_chk.check() == sat:
        print(idx)
        break