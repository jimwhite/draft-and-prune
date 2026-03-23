from z3 import *

# Recruit indices: 0-Peters, 1-Quinn, 2-Rovero, 3-Stanton, 4-Tao, 5-Villas, 6-White
pos = [Int(f"pos_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: positions 1-7
for i in range(7):
    solver.add(pos[i] >= 1, pos[i] <= 7)

# Distinctness constraint
solver.add(Distinct(pos))

# Fixed constraint: Peters was recruited fourth
solver.add(pos[0] == 4)

# Villas immediately before White: pos[5] + 1 == pos[6]
solver.add(pos[5] + 1 == pos[6])

# Quinn before Rovero
solver.add(pos[1] < pos[2])

# Hypothetical: Quinn immediately before Rovero
solver.add(pos[1] + 1 == pos[2])

# Stanton-Tao non-adjacency constraint
solver.add(Abs(pos[3] - pos[4]) != 1)

# Answer choices: first=1, second=2, third=3, fifth=5, seventh=7
candidate_positions = [1, 2, 3, 5, 7]
forbidden_positions = []

for candidate in candidate_positions:
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint that Stanton is at this position
    s_chk.add(pos[3] == candidate)
    
    # If UNSAT, Stanton cannot be at this position
    if s_chk.check() == unsat:
        forbidden_positions.append(candidate)

print(forbidden_positions)