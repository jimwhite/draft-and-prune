from z3 import *

# Cargo type indices: 0-fuel, 1-grain, 2-livestock, 3-machinery, 4-produce, 5-textiles
(fuel, grain, livestock, machinery, produce, textiles) = range(6)

# Position variables: pos[i] = bay number (1-6) for cargo type i
pos = [Int(f"pos_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: positions are 1-6 and all distinct
for i in range(6):
    solver.add(pos[i] >= 1, pos[i] <= 6)
solver.add(Distinct(*pos))

# Base constraints from problem description
# Grain > livestock
solver.add(pos[grain] > pos[livestock])
# Livestock > textiles
solver.add(pos[livestock] > pos[textiles])
# Produce > fuel
solver.add(pos[produce] > pos[fuel])
# Textiles and produce adjacent: |pos_textiles - pos_produce| = 1
solver.add(Or(pos[textiles] == pos[produce] + 1, pos[textiles] == pos[produce] - 1))

# Conditional constraint: produce is next to livestock ⇒ |pos_produce - pos_livestock| = 1
# Since the problem states "If the bay holding produce is next to the bay holding livestock",
# we add this as a constraint for our analysis
solver.add(Or(pos[produce] == pos[livestock] + 1, pos[produce] == pos[livestock] - 1))

# Answer choices: check which cannot be true (EXCEPT)
answer_choices = [
    ("fuel in bay 2", pos[fuel] == 2),
    ("produce in bay 4", pos[produce] == 4),
    ("textiles in bay 4", pos[textiles] == 4),
    ("grain in bay 5", pos[grain] == 5),
    ("machinery in bay 5", pos[machinery] == 5)
]

answer_index_list = []
for idx, (_, constraint) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(constraint)
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)