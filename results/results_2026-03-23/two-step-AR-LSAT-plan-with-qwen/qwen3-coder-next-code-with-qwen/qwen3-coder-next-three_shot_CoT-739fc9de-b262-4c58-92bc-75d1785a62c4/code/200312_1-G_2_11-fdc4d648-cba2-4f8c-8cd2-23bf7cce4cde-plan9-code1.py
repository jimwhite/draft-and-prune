from z3 import *

# Cargo type indices: 0-fuel, 1-grain, 2-livestock, 3-machinery, 4-produce, 5-textiles
FUEL, GRAIN, LIVESTOCK, MACHINERY, PRODUCE, TEXTILES = range(6)

# Bay variables: b[i] is the bay number (1-6) for cargo type i
b = [Int(f"b_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: each bay number is between 1 and 6, all distinct
solver.add(Distinct(*b))
for i in range(6):
    solver.add(b[i] >= 1, b[i] <= 6)

# Ordering constraints
solver.add(b[GRAIN] > b[LIVESTOCK])      # grain > livestock
solver.add(b[LIVESTOCK] > b[TEXTILES])   # livestock > textiles
solver.add(b[PRODUCE] > b[FUEL])         # produce > fuel

# Textiles adjacent to produce
solver.add(Or(b[TEXTILES] == b[PRODUCE] + 1, b[TEXTILES] == b[PRODUCE] - 1))

# Additional condition: produce is next to livestock
solver.add(Or(b[PRODUCE] == b[LIVESTOCK] + 1, b[PRODUCE] == b[LIVESTOCK] - 1))

# Answer choices
answer_choices = [
    ("Bay 2 is holding fuel.", b[FUEL] == 2),
    ("Bay 4 is holding produce.", b[PRODUCE] == 4),
    ("Bay 4 is holding textiles.", b[TEXTILES] == 4),
    ("Bay 5 is holding grain.", b[GRAIN] == 5),
    ("Bay 5 is holding machinery.", b[MACHINERY] == 5)
]

# Check each answer choice
answer_index_list = []
for idx, (desc, constraint) in enumerate(answer_choices):
    s_chk = Solver()
    # Add all base constraints plus the produce-livestock adjacency condition
    s_chk.add(solver.assertions())
    
    # Add the specific constraint for this choice
    s_chk.add(constraint)
    
    # If UNSAT, this choice cannot be true (EXCEPT answer)
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)