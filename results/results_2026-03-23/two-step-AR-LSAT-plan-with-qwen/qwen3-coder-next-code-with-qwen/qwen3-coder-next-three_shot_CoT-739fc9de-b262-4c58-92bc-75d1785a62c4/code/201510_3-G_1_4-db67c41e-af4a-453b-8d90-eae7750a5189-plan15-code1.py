from z3 import *

# Accomplice indices (0-6)
PETERS, QUINN, ROVERO, STANTON, TAO, VILLAS, WHITE = range(7)

# Position variables (1 to 7)
pos = [Int(f"pos_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: each position between 1 and 7, all distinct
for i in range(7):
    solver.add(pos[i] >= 1, pos[i] <= 7)
solver.add(Distinct(*pos))

# Fixed constraint: Peters is recruited fourth
solver.add(pos[PETERS] == 4)

# Villas immediately before White: pos_Villas + 1 == pos_White
solver.add(pos[VILLAS] + 1 == pos[WHITE])

# Quinn earlier than Rovero: pos_Quinn < pos_Rovero
solver.add(pos[QUINN] < pos[ROVERO])

# Extra constraint for the conditional: Quinn immediately before Rovero
solver.add(pos[QUINN] + 1 == pos[ROVERO])

# Stanton not immediately before or after Tao: |pos_Stanton - pos_Tao| != 1
solver.add(Abs(pos[STANTON] - pos[TAO]) != 1)

# Answer choices: first=1, second=2, third=3, fifth=5, seventh=7
answer_positions = [1, 2, 3, 5, 7]
# Map positions to indices: first->0, second->1, third->2, fifth->3, seventh->4
answer_index_list = []

for idx, target_pos in enumerate(answer_positions):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert Stanton is recruited at this position
    s_chk.add(pos[STANTON] == target_pos)
    
    # If UNSAT, Stanton cannot be at this position
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)