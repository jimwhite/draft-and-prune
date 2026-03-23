from z3 import *

# Accomplice indices: Peters=0, Quinn=1, Rovero=2, Stanton=3, Tao=4, Villas=5, White=6
names = ["Peters", "Quinn", "Rovero", "Stanton", "Tao", "Villas", "White"]
pos = [Int(f"pos_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: positions 1-7, all distinct
for i in range(7):
    solver.add(pos[i] >= 1, pos[i] <= 7)
solver.add(Distinct(*pos))

# Fixed constraint: Peters is recruited fourth
solver.add(pos[0] == 4)

# Order constraints:
# Quinn before Rovero
solver.add(pos[1] < pos[2])
# Villas immediately before White
solver.add(pos[5] + 1 == pos[6])
# Stanton not adjacent to Tao
solver.add(Abs(pos[3] - pos[4]) != 1)

# Answer choices
answer_choices = [
    ['Quinn', 'Tao', 'Stanton', 'Peters', 'Villas', 'White', 'Rovero'],
    ['Quinn', 'White', 'Rovero', 'Peters', 'Stanton', 'Villas', 'Tao'],
    ['Villas', 'White', 'Quinn', 'Stanton', 'Peters', 'Tao', 'Rovero'],
    ['Villas', 'White', 'Stanton', 'Peters', 'Quinn', 'Tao', 'Rovero'],
    ['Villas', 'White', 'Stanton', 'Peters', 'Rovero', 'Tao', 'Quinn']
]

# Check each answer choice
valid_indices = []
for idx, sequence in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add position constraints based on the sequence
    for i, name in enumerate(sequence):
        if name == "Peters":
            s_chk.add(pos[0] == i + 1)
        elif name == "Quinn":
            s_chk.add(pos[1] == i + 1)
        elif name == "Rovero":
            s_chk.add(pos[2] == i + 1)
        elif name == "Stanton":
            s_chk.add(pos[3] == i + 1)
        elif name == "Tao":
            s_chk.add(pos[4] == i + 1)
        elif name == "Villas":
            s_chk.add(pos[5] == i + 1)
        elif name == "White":
            s_chk.add(pos[6] == i + 1)
    
    if s_chk.check() == sat:
        valid_indices.append(idx)

print(valid_indices[0] if valid_indices else -1)