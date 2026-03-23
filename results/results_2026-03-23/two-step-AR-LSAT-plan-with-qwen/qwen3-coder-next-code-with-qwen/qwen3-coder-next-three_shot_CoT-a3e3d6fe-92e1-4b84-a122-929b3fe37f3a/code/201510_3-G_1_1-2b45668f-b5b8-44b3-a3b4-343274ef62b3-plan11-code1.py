from z3 import *

# Accomplice indices: Peters=0, Quinn=1, Rovero=2, Stanton=3, Tao=4, Villas=5, White=6
accomplices = ["Peters", "Quinn", "Rovero", "Stanton", "Tao", "Villas", "White"]

# Position variables: pos[i] = position (1-7) of accomplice i
pos = [Int(f"pos_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: positions 1-7, all distinct
for i in range(7):
    solver.add(pos[i] >= 1, pos[i] <= 7)
solver.add(Distinct(*pos))

# Fixed constraint: Peters is recruited fourth
solver.add(pos[0] == 4)

# Villas immediately before White: pos[Villas] + 1 == pos[White]
solver.add(pos[5] + 1 == pos[6])

# Quinn earlier than Rovero: pos[Quinn] < pos[Rovero]
solver.add(pos[1] < pos[2])

# Stanton and Tao not adjacent: |pos[Stanton] - pos[Tao]| != 1
solver.add(Abs(pos[3] - pos[4]) != 1)

# Answer choices
choices = [
    ['Quinn', 'Tao', 'Stanton', 'Peters', 'Villas', 'White', 'Rovero'],
    ['Quinn', 'White', 'Rovero', 'Peters', 'Stanton', 'Villas', 'Tao'],
    ['Villas', 'White', 'Quinn', 'Stanton', 'Peters', 'Tao', 'Rovero'],
    ['Villas', 'White', 'Stanton', 'Peters', 'Quinn', 'Tao', 'Rovero'],
    ['Villas', 'White', 'Stanton', 'Peters', 'Rovero', 'Tao', 'Quinn']
]

# Check each choice
valid_indices = []
for idx, choice in enumerate(choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Map each accomplice to their position in the choice (1-indexed)
    for i, name in enumerate(choice):
        pos_val = i + 1
        if name == "Peters":
            s_chk.add(pos[0] == pos_val)
        elif name == "Quinn":
            s_chk.add(pos[1] == pos_val)
        elif name == "Rovero":
            s_chk.add(pos[2] == pos_val)
        elif name == "Stanton":
            s_chk.add(pos[3] == pos_val)
        elif name == "Tao":
            s_chk.add(pos[4] == pos_val)
        elif name == "Villas":
            s_chk.add(pos[5] == pos_val)
        elif name == "White":
            s_chk.add(pos[6] == pos_val)
    
    if s_chk.check() == sat:
        valid_indices.append(idx)

# Output the valid choice string
if len(valid_indices) == 1:
    print(choices[valid_indices[0]])
else:
    # In case multiple or none, output the list of valid indices for debugging
    print(valid_indices)