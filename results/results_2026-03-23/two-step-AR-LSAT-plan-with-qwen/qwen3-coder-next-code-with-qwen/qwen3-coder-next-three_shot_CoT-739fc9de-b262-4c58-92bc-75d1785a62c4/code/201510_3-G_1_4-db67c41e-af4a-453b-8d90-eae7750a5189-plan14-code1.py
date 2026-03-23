from z3 import *

# Accomplice position variables: pos[name] = recruitment position (1-7)
names = ["Peters", "Quinn", "Rovero", "Stanton", "Tao", "Villas", "White"]
pos = {name: Int(f"pos_{name}") for name in names}

# Base solver
solver = Solver()

# Domain constraints: positions between 1 and 7, all distinct
for name in names:
    solver.add(pos[name] >= 1, pos[name] <= 7)
solver.add(Distinct(*[pos[name] for name in names]))

# Fixed constraint: Peters is recruited fourth
solver.add(pos["Peters"] == 4)

# Villas-White adjacency constraint: Villas immediately before White
solver.add(pos["Villas"] + 1 == pos["White"])

# Quinn-Rovero ordering constraint: Quinn earlier than Rovero
solver.add(pos["Quinn"] < pos["Rovero"])

# Anti-adjacency constraint for Stanton-Tao: |pos_Stanton - pos_Tao| != 1
solver.add(Abs(pos["Stanton"] - pos["Tao"]) != 1)

# Conditional constraint: Quinn immediately before Rovero
solver.add(pos["Quinn"] + 1 == pos["Rovero"])

# Answer choices: positions where Stanton CANNOT be recruited
answer_choices = [1, 2, 3, 5, 7]  # first=1, second=2, third=3, fifth=5, seventh=7

# Check each answer choice
answer_index_list = []
for idx, candidate_pos in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint that Stanton is recruited at candidate position
    s_chk.add(pos["Stanton"] == candidate_pos)
    
    # If UNSAT, Stanton cannot be at this position
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)