from z3 import *

# People indices
people = ["Peters", "Quinn", "Rovero", "Stanton", "Tao", "Villas", "White"]
pos = {p: Int(f"pos_{p}") for p in people}

# Base solver
solver = Solver()

# Domain constraints: positions 1-7, all distinct
for p in people:
    solver.add(pos[p] >= 1, pos[p] <= 7)
solver.add(Distinct(*[pos[p] for p in people]))

# Fixed constraint: Peters recruited fourth
solver.add(pos["Peters"] == 4)

# Villas immediately before White
solver.add(pos["Villas"] + 1 == pos["White"])

# Quinn earlier than Rovero
solver.add(pos["Quinn"] < pos["Rovero"])

# Conditional constraint: Quinn immediately before Rovero (assumed for this question)
solver.add(pos["Quinn"] + 1 == pos["Rovero"])

# Stanton not adjacent to Tao
solver.add(Abs(pos["Stanton"] - pos["Tao"]) != 1)

# Answer choices: positions [1,2,3,5,7]
answer_positions = [1, 2, 3, 5, 7]

# Check each position for Stanton
answer_index_list = []
for idx, p in enumerate(answer_positions):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assume Stanton is at position p
    s_chk.add(pos["Stanton"] == p)
    
    if s_chk.check() == unsat:
        answer_index_list.append(p)

print(answer_index_list)