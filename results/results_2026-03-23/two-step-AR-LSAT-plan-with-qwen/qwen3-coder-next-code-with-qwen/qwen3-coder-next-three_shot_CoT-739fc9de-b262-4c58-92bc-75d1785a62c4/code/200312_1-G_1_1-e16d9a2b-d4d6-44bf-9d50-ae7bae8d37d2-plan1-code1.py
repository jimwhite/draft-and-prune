from z3 import *

# Scientists: F=0, G=1, H=2 (botanists), K=3, L=4, M=5 (chemists), P=6, Q=7, R=8 (zoologists)
b = [Bool(f"b_{i}") for i in range(9)]

# Base solver
solver = Solver()

# Cardinality constraint: exactly 5 scientists selected
solver.add(Sum([If(b[i], 1, 0) for i in range(9)]) == 5)

# Type coverage constraint: at least one of each type
solver.add(Or(b[0], b[1], b[2]))  # at least one botanist
solver.add(Or(b[3], b[4], b[5]))  # at least one chemist
solver.add(Or(b[6], b[7], b[8]))  # at least one zoologist

# Conditional constraint 1: if more than one botanist, then at most one zoologist
botanists_count = Sum([If(b[i], 1, 0) for i in range(3)])
zoologists_count = Sum([If(b[i], 1, 0) for i in range(6, 9)])
solver.add(Or(botanists_count <= 1, zoologists_count <= 1))

# Exclusion constraint 1: F and K cannot both be selected
solver.add(Not(And(b[0], b[3])))

# Exclusion constraint 2: K and M cannot both be selected
solver.add(Not(And(b[3], b[5])))

# Conditional constraint 2: if M is selected, both P and R must be selected
solver.add(Implies(b[5], And(b[6], b[8])))

# Answer choices
answer_choices = [
    ['F', 'G', 'K', 'P', 'Q'],
    ['G', 'H', 'K', 'L', 'M'],
    ['G', 'H', 'K', 'L', 'R'],
    ['H', 'K', 'M', 'P', 'R'],
    ['H', 'L', 'M', 'P', 'Q']
]

# Mapping from name to index
name_to_idx = {
    'F': 0, 'G': 1, 'H': 2,
    'K': 3, 'L': 4, 'M': 5,
    'P': 6, 'Q': 7, 'R': 8
}

# Check each answer choice
acceptable_indices = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert selected scientists are True
    for name in choice:
        s_chk.add(b[name_to_idx[name]] == True)
    
    # Assert unselected scientists are False
    for name, i in name_to_idx.items():
        if name not in choice:
            s_chk.add(b[i] == False)
    
    # Check satisfiability
    if s_chk.check() == sat:
        acceptable_indices.append(idx)

# Output the index of the first acceptable choice (as per typical LSAT format)
if acceptable_indices:
    print(acceptable_indices[0])
else:
    print(-1)