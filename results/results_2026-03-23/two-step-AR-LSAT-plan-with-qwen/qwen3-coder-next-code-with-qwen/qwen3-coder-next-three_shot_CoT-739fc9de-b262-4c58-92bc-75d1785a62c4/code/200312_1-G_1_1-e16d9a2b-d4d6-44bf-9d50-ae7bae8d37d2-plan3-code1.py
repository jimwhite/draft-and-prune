from z3 import *

# Scientist indices: botanists F=0, G=1, H=2; chemists K=3, L=4, M=5; zoologists P=6, Q=7, R=8
s = [Bool(f"s_{i}") for i in range(9)]

# Base solver
solver = Solver()

# Panel size constraint: exactly 5 scientists selected
solver.add(Sum([If(s[i], 1, 0) for i in range(9)]) == 5)

# Type coverage constraints
solver.add(Or(s[0], s[1], s[2]))  # at least one botanist
solver.add(Or(s[3], s[4], s[5]))  # at least one chemist
solver.add(Or(s[6], s[7], s[8]))  # at least one zoologist

# Conditional constraint: if more than one botanist, then at most one zoologist
botanist_count = Sum([If(s[i], 1, 0) for i in range(3)])
zoologist_count = Sum([If(s[i], 1, 0) for i in range(6, 9)])
solver.add(Implies(botanist_count >= 2, zoologist_count <= 1))

# Mutual exclusion constraints
solver.add(Not(And(s[0], s[3])))  # F and K cannot both be selected
solver.add(Not(And(s[3], s[5])))  # K and M cannot both be selected

# Implication constraint: if M is selected, then P and R must be selected
solver.add(Implies(s[5], And(s[6], s[8])))

# Answer choices
answer_choices = [
    ['F', 'G', 'K', 'P', 'Q'],
    ['G', 'H', 'K', 'L', 'M'],
    ['G', 'H', 'K', 'L', 'R'],
    ['H', 'K', 'M', 'P', 'R'],
    ['H', 'L', 'M', 'P', 'Q']
]

# Map scientist names to indices
name_to_idx = {
    'F': 0, 'G': 1, 'H': 2,
    'K': 3, 'L': 4, 'M': 5,
    'P': 6, 'Q': 7, 'R': 8
}

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Set selected scientists to true, others to false
    for i in range(9):
        name = choice[i] if i < len(choice) else None
        if name is not None and name in name_to_idx:
            s_chk.add(s[name_to_idx[name]])
        else:
            s_chk.add(Not(s[i]))
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)