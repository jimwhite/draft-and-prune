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

# Villas immediately before White: pos_White = pos_Villas + 1
solver.add(pos["White"] == pos["Villas"] + 1)

# Quinn earlier than Rovero: pos_Quinn < pos_Rovero
solver.add(pos["Quinn"] < pos["Rovero"])

# Conditional constraint for the question: assume Quinn immediately before Rovero
solver.add(pos["Rovero"] == pos["Quinn"] + 1)

# Stanton not immediately before or after Tao: |pos_Stanton - pos_Tao| != 1
solver.add(Abs(pos["Stanton"] - pos["Tao"]) != 1)

# Answer choices: first=1, second=2, third=3, fifth=5, seventh=7
answer_choices = [1, 2, 3, 5, 7]

# Check each answer choice
answer_index_list = []
for idx, target_pos in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert Stanton is recruited at the candidate position
    s_chk.add(pos["Stanton"] == target_pos)
    
    # If UNSAT, Stanton CANNOT be recruited at that position
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)