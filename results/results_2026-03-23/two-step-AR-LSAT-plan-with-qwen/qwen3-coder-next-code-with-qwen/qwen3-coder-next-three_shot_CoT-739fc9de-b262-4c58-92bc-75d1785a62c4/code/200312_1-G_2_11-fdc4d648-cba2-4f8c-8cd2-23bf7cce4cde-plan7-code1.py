from z3 import *

# Cargo type indices: fuel=0, grain=1, livestock=2, machinery=3, produce=4, textiles=5
(fuel, grain, livestock, machinery, produce, textiles) = range(6)

# bay[i] represents the bay number (1-6) where cargo type i is stored
bay = [Int(f"bay_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: each bay number between 1 and 6, all distinct
for i in range(6):
    solver.add(bay[i] >= 1, bay[i] <= 6)
solver.add(Distinct(*bay))

# Initial ordering constraints
solver.add(bay[grain] > bay[livestock])  # grain > livestock
solver.add(bay[livestock] > bay[textiles])  # livestock > textiles
solver.add(bay[produce] > bay[fuel])  # produce > fuel
solver.add(Or(
    bay[textiles] == bay[produce] + 1,
    bay[textiles] == bay[produce] - 1
))  # textiles adjacent to produce

# Hypothetical condition: produce is next to livestock
solver.add(Or(
    bay[produce] == bay[livestock] + 1,
    bay[produce] == bay[livestock] - 1
))

# Answer choices: check which one CANNOT be true (EXCEPT question)
answer_choices = [
    ("Bay 2 is holding fuel", bay[fuel] == 2),
    ("Bay 4 is holding produce", bay[produce] == 4),
    ("Bay 4 is holding textiles", bay[textiles] == 4),
    ("Bay 5 is holding grain", bay[grain] == 5),
    ("Bay 5 is holding machinery", bay[machinery] == 5)
]

answer_index_list = []
for idx, (_, constraint) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(constraint)
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)