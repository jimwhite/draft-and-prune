from z3 import *

# Accomplice indices: Peters=0, Quinn=1, Rovero=2, Stanton=3, Tao=4, Villas=5, White=6
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

# Quinn immediately before Rovero (premise)
solver.add(pos[1] + 1 == pos[2])

# Stanton not immediately before or after Tao: |pos[Stanton] - pos[Tao]| != 1
solver.add(And(pos[3] - pos[4] != 1, pos[4] - pos[3] != 1))

# Answer choices positions: first=1, second=2, third=3, fifth=5, seventh=7
answer_positions = [1, 2, 3, 5, 7]

# Check each position for Stanton
answer_index_list = []
for idx, candidate_pos in enumerate(answer_positions):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint that Stanton is at this position
    s_chk.add(pos[3] == candidate_pos)
    
    # If UNSAT, Stanton cannot be at this position
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)