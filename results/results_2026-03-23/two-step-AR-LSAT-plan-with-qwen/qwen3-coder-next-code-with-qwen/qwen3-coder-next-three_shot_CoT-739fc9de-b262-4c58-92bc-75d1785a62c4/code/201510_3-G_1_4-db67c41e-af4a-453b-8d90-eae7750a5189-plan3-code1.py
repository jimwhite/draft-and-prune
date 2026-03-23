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

# Quinn-Rovero constraint: Quinn earlier than Rovero
solver.add(pos["Quinn"] < pos["Rovero"])

# Conditional hypothesis: Quinn immediately before Rovero
solver.add(pos["Quinn"] + 1 == pos["Rovero"])

# Stanton-Tao constraint: not adjacent
solver.add(Abs(pos["Stanton"] - pos["Tao"]) != 1)

# Answer choices positions: first=1, second=2, third=3, fifth=5, seventh=7
answer_positions = [1, 2, 3, 5, 7]
answer_index_list = []

for idx, p in enumerate(answer_positions):
    s_chk = Solver()
    # Add all base constraints and hypothesis
    for a in solver.assertions():
        s_chk.add(a)
    
    # Add constraint that Stanton is at position p
    s_chk.add(pos["Stanton"] == p)
    
    # If UNSAT, Stanton cannot be at position p
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)