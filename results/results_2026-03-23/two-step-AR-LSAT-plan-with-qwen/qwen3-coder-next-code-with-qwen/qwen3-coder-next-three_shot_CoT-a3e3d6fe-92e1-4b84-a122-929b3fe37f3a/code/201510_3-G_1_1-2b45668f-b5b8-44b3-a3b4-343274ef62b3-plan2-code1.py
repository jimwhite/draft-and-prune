from z3 import *

# Accomplice indices: Peters=0, Quinn=1, Rovero=2, Stanton=3, Tao=4, Villas=5, White=6
p = [Int(f"p_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: positions 1-7, all distinct
for i in range(7):
    solver.add(p[i] >= 1, p[i] <= 7)
solver.add(Distinct(*p))

# Fixed constraint: Peters is recruited fourth
solver.add(p[0] == 4)

# Order constraints
# Quinn earlier than Rovero: Quinn=1, Rovero=2
solver.add(p[1] < p[2])

# Villas immediately before White: Villas=5, White=6
solver.add(p[5] + 1 == p[6])

# Stanton and Tao not adjacent: Stanton=3, Tao=4
solver.add(Abs(p[3] - p[4]) != 1)

# Answer choices
choices = [
    ['Quinn', 'Tao', 'Stanton', 'Peters', 'Villas', 'White', 'Rovero'],
    ['Quinn', 'White', 'Rovero', 'Peters', 'Stanton', 'Villas', 'Tao'],
    ['Villas', 'White', 'Quinn', 'Stanton', 'Peters', 'Tao', 'Rovero'],
    ['Villas', 'White', 'Stanton', 'Peters', 'Quinn', 'Tao', 'Rovero'],
    ['Villas', 'White', 'Stanton', 'Peters', 'Rovero', 'Tao', 'Quinn']
]

# Mapping from name to index
name_to_idx = {
    'Peters': 0,
    'Quinn': 1,
    'Rovero': 2,
    'Stanton': 3,
    'Tao': 4,
    'Villas': 5,
    'White': 6
}

# Check each choice
answer_index_list = []
for idx, choice in enumerate(choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add position constraints for this choice
    for pos, name in enumerate(choice, start=1):
        s_chk.add(p[name_to_idx[name]] == pos)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)