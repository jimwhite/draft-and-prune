from z3 import *

# Accomplice indices: 0=Peters, 1=Quinn, 2=Rovero, 3=Stanton, 4=Tao, 5=Villas, 6=White
pos = [Int(f"pos_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: positions 1-7, all distinct
for i in range(7):
    solver.add(pos[i] >= 1, pos[i] <= 7)
solver.add(Distinct(*pos))

# Fixed constraint: Peters is fourth
solver.add(pos[0] == 4)

# Villas-White constraint: Villas immediately before White
solver.add(pos[6] == pos[5] + 1)

# Quinn-Rovero constraint (premise): Quinn immediately before Rovero
solver.add(pos[2] == pos[1] + 1)

# Stanton-Tao constraint: not adjacent
solver.add(Abs(pos[3] - pos[4]) != 1)

# Answer choices positions: first=1, second=2, third=3, fifth=5, seventh=7
answer_positions = [1, 2, 3, 5, 7]
answer_index_list = []

for idx, p in enumerate(answer_positions):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint that Stanton is at position p
    s_chk.add(pos[3] == p)
    
    # If UNSAT, Stanton cannot be at position p
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)