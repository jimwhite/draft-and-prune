from z3 import *

# Cargo types indices: 0-fuel, 1-grain, 2-livestock, 3-machinery, 4-produce, 5-textiles
(fuel, grain, livestock, machinery, produce, textiles) = range(6)

# Position variables: pos[c] is the bay number (1-6) for cargo type c
pos = {c: Int(f"pos_{c}") for c in range(6)}

# Base solver
solver = Solver()

# Domain constraints: each cargo type assigned to a unique bay 1-6
for c in range(6):
    solver.add(pos[c] >= 1, pos[c] <= 6)
solver.add(Distinct(*pos.values()))

# Given ordering constraints
solver.add(pos[grain] > pos[livestock])      # grain > livestock
solver.add(pos[livestock] > pos[textiles])   # livestock > textiles
solver.add(pos[produce] > pos[fuel])         # produce > fuel
# textiles adjacent to produce: |pos[textiles] - pos[produce]| = 1
solver.add(Or(pos[textiles] == pos[produce] + 1, pos[textiles] == pos[produce] - 1))

# Additional conditional constraint: produce is next to livestock
solver.add(Or(pos[produce] == pos[livestock] + 1, pos[produce] == pos[livestock] - 1))

# Answer choices: each choice is a condition that could be true
# ['Bay 2 is holding fuel.', 'Bay 4 is holding produce.', 'Bay 4 is holding textiles.',
#  'Bay 5 is holding grain.', 'Bay 5 is holding machinery.']
answer_conditions = [
    pos[fuel] == 2,      # Bay 2 is holding fuel
    pos[produce] == 4,   # Bay 4 is holding produce
    pos[textiles] == 4,  # Bay 4 is holding textiles
    pos[grain] == 5,     # Bay 5 is holding grain
    pos[machinery] == 5  # Bay 5 is holding machinery
]

# Check each condition
impossible_choices = []
for idx, cond in enumerate(answer_conditions):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(cond)
    
    if s_chk.check() == unsat:
        impossible_choices.append(idx)

# Output the EXCEPT answer (the one that cannot be true)
if len(impossible_choices) == 1:
    print(f"['{['Bay 2 is holding fuel.', 'Bay 4 is holding produce.', 'Bay 4 is holding textiles.', 'Bay 5 is holding grain.', 'Bay 5 is holding machinery.'][impossible_choices[0]]}']")
else:
    # According to the problem, exactly one choice is impossible
    # If multiple or none are found, still output the list of indices for debugging
    print(impossible_choices)