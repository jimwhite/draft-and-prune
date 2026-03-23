from z3 import *

# Cargo type indices: fuel=0, grain=1, livestock=2, machinery=3, produce=4, textiles=5
fuel, grain, livestock, machinery, produce, textiles = range(6)

# bay[i] represents the bay number (1-6) where cargo type i is held
bay = [Int(f"bay_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: each bay number between 1 and 6, all distinct
for i in range(6):
    solver.add(bay[i] >= 1, bay[i] <= 6)
solver.add(Distinct(*bay))

# Given ordering constraints
solver.add(bay[grain] > bay[livestock])  # grain > livestock
solver.add(bay[livestock] > bay[textiles])  # livestock > textiles
solver.add(bay[produce] > bay[fuel])  # produce > fuel
solver.add(Or(bay[textiles] == bay[produce] + 1, bay[textiles] == bay[produce] - 1))  # textiles adjacent to produce

# Conditional assumption: produce is next to livestock
solver.add(Or(bay[produce] == bay[livestock] + 1, bay[produce] == bay[livestock] - 1))

# Answer choices conditions
answer_conditions = [
    bay[fuel] == 2,           # Bay 2 is holding fuel
    bay[produce] == 4,        # Bay 4 is holding produce
    bay[textiles] == 4,       # Bay 4 is holding textiles
    bay[grain] == 5,          # Bay 5 is holding grain
    bay[machinery] == 5       # Bay 5 is holding machinery
]

# Check each choice for impossibility under the condition
impossible_choices_index_list = []
for idx, cond in enumerate(answer_conditions):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(cond)
    
    if s_chk.check() == unsat:
        impossible_choices_index_list.append(idx)

# Output the corresponding choice string
choices = [
    'Bay 2 is holding fuel.',
    'Bay 4 is holding produce.',
    'Bay 4 is holding textiles.',
    'Bay 5 is holding grain.',
    'Bay 5 is holding machinery.'
]

# Since the question asks for EXCEPT, we want the impossible choice(s)
if len(impossible_choices_index_list) == 1:
    print(choices[impossible_choices_index_list[0]])
else:
    # In case multiple are impossible (though question implies one), print all impossible
    for idx in impossible_choices_index_list:
        print(choices[idx])