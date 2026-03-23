from z3 import *

# Accomplice position variables: pos[name] = recruitment position (1-7)
names = ["Peters", "Quinn", "Rovero", "Stanton", "Tao", "Villas", "White"]
pos = {name: Int(f"pos_{name}") for name in names}

# Base solver
solver = Solver()

# Domain constraints: positions 1-7, all distinct
for name in names:
    solver.add(pos[name] >= 1, pos[name] <= 7)
solver.add(Distinct(*[pos[name] for name in names]))

# Fixed constraint: Peters is recruited fourth
solver.add(pos["Peters"] == 4)

# Villas-White constraint: Villas immediately before White
solver.add(pos["Villas"] + 1 == pos["White"])

# Quinn-Rovero constraint (premise): Quinn immediately before Rovero
solver.add(pos["Quinn"] + 1 == pos["Rovero"])

# Stanton-Tao separation constraint: not adjacent
solver.add(Abs(pos["Stanton"] - pos["Tao"]) != 1)

# Answer choices: positions that Stanton CANNOT have
answer_positions = [1, 2, 3, 5, 7]  # first, second, third, fifth, seventh

# Check each position
answer_index_list = []
for idx, p in enumerate(answer_positions):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert Stanton is in position p
    s_chk.add(pos["Stanton"] == p)
    
    # If UNSAT, Stanton cannot be in this position
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)