from z3 import *

# Scientists: botanists [F, G, H], chemists [K, L, M], zoologists [P, Q, R]
# Assign indices: F=0, G=1, H=2, K=3, L=4, M=5, P=6, Q=7, R=8
sel = [Bool(f"sel_{i}") for i in range(9)]

# Base solver
solver = Solver()

# Panel-size constraint: exactly 5 scientists selected
solver.add(Sum([If(s, 1, 0) for s in sel]) == 5)

# Type-completeness constraint: at least one of each type
solver.add(Or(sel[0], sel[1], sel[2]))  # at least one botanist
solver.add(Or(sel[3], sel[4], sel[5]))  # at least one chemist
solver.add(Or(sel[6], sel[7], sel[8]))  # at least one zoologist

# Botanist-zoologist constraint: if more than one botanist, then at most one zoologist
bot_count = Sum([If(sel[i], 1, 0) for i in range(3)])
zoologist_count = Sum([If(sel[i], 1, 0) for i in range(6, 9)])
# bot_count > 1 → zoologist_count <= 1
solver.add(Implies(bot_count >= 2, zoologist_count <= 1))

# F and K cannot both be selected (F=0, K=3)
solver.add(Not(And(sel[0], sel[3])))

# K and M cannot both be selected (K=3, M=5)
solver.add(Not(And(sel[3], sel[5])))

# If M is selected, both P and R must be selected (M=5, P=6, R=8)
solver.add(Implies(sel[5], And(sel[6], sel[8])))

# Answer choices
answer_choices = [
    ['F', 'G', 'K', 'P', 'Q'],  # indices: F=0, G=1, K=3, P=6, Q=7
    ['G', 'H', 'K', 'L', 'M'],  # indices: G=1, H=2, K=3, L=4, M=5
    ['G', 'H', 'K', 'L', 'R'],  # indices: G=1, H=2, K=3, L=4, R=8
    ['H', 'K', 'M', 'P', 'R'],  # indices: H=2, K=3, M=5, P=6, R=8
    ['H', 'L', 'M', 'P', 'Q']   # indices: H=2, L=4, M=5, P=6, Q=7
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
    
    # Assert exactly the scientists in this choice are selected
    selected_indices = [name_to_idx[name] for name in choice]
    
    # Selected scientists must be True
    for i in selected_indices:
        s_chk.add(sel[i])
    
    # Non-selected scientists must be False
    for i in range(9):
        if i not in selected_indices:
            s_chk.add(Not(sel[i]))
    
    # Check satisfiability
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)