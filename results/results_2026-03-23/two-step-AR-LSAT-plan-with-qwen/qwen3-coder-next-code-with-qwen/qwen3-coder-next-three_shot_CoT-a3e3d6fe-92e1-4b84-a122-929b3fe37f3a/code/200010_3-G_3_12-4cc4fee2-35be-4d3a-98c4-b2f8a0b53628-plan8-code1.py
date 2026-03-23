from z3 import *

# Compositions indices: F=0, H=1, L=2, O=3, P=4, R=5, S=6, T=7
compositions = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']

# Create position variables
pos = {c: Int(f"pos_{c}") for c in compositions}

# Base solver
solver = Solver()

# Domain constraints: each position between 1 and 8
for c in compositions:
    solver.add(pos[c] >= 1, pos[c] <= 8)

# All positions distinct
solver.add(Distinct(*[pos[c] for c in compositions]))

# Condition a: T is performed either immediately before F or immediately after R
solver.add(Or(pos['T'] == pos['F'] - 1, pos['T'] == pos['R'] + 1))

# Condition b: At least two compositions between F and R
solver.add(Or(pos['F'] <= pos['R'] - 3, pos['F'] >= pos['R'] + 3))

# Condition c: O is first or fifth
solver.add(Or(pos['O'] == 1, pos['O'] == 5))

# Condition d: Eighth composition is L or H
solver.add(Or(pos['L'] == 8, pos['H'] == 8))

# Condition e: P before S
solver.add(pos['P'] < pos['S'])

# Condition f: At least one composition between O and S
solver.add(Or(pos['O'] <= pos['S'] - 2, pos['O'] >= pos['S'] + 2))

# Answer choices
answer_choices = [
    ['L', 'P', 'S', 'R', 'O', 'T', 'F', 'H'],
    ['O', 'T', 'P', 'F', 'S', 'H', 'R', 'L'],
    ['P', 'T', 'F', 'S', 'L', 'R', 'O', 'H'],
    ['P', 'T', 'F', 'S', 'O', 'R', 'L', 'H'],
    ['T', 'F', 'P', 'R', 'O', 'L', 'S', 'H']
]

# Check each answer choice
valid_indices = []
for idx, seq in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert positions based on the sequence (0-indexed position i means slot i+1)
    for i, c in enumerate(seq):
        s_chk.add(pos[c] == i + 1)
    
    if s_chk.check() == sat:
        valid_indices.append(idx)

# Output the first valid index (as per typical multiple choice format)
if valid_indices:
    print(valid_indices[0])
else:
    print(-1)