from z3 import *

# Performer indices: 0-guitarist, 1-keyboard player, 2-percussionist, 
#                   3-saxophonist, 4-trumpeter, 5-violinist
pos = [Int(f"pos_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: each position between 1 and 6, all distinct
for i in range(6):
    solver.add(pos[i] >= 1, pos[i] <= 6)
solver.add(Distinct(pos))

# Guitarist constraint: does not perform fourth
solver.add(pos[0] != 4)

# Percussionist < keyboard player
solver.add(pos[2] < pos[1])

# Violinist < keyboard player < guitarist
solver.add(pos[5] < pos[1])
solver.add(pos[1] < pos[0])

# Saxophonist after exactly one of (percussionist, trumpeter)
after_p = pos[3] > pos[2]
after_t = pos[3] > pos[4]
solver.add(Xor(after_p, after_t))

# Answer choices indices: guitarist(0), keyboard player(1), saxophonist(3), trumpeter(4), violinist(5)
answer_choices = [0, 1, 3, 4, 5]

# Check each answer choice
forbidden_indices = []
for idx in answer_choices:
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert this performer is third
    s_chk.add(pos[idx] == 3)
    
    if s_chk.check() == unsat:
        forbidden_indices.append(idx)

# Map index to performer name
performer_names = [
    "guitarist", 
    "keyboard player", 
    "percussionist", 
    "saxophonist", 
    "trumpeter", 
    "violinist"
]

# Print the performer name that cannot be third
print(performer_names[forbidden_indices[0]])