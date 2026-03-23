from z3 import *

# Cargo type indices: 0-fuel, 1-grain, 2-live (livestock), 3-mach (machinery), 4-prod (produce), 5-text (textiles)
b_fuel, b_grain, b_live, b_mach, b_prod, b_text = Ints('b_fuel b_grain b_live b_mach b_prod b_text')

# Base solver
solver = Solver()

# Domain constraints: all bays distinct and in range [1, 6]
solver.add(Distinct(b_fuel, b_grain, b_live, b_mach, b_prod, b_text))
solver.add(b_fuel >= 1, b_fuel <= 6)
solver.add(b_grain >= 1, b_grain <= 6)
solver.add(b_live >= 1, b_live <= 6)
solver.add(b_mach >= 1, b_mach <= 6)
solver.add(b_prod >= 1, b_prod <= 6)
solver.add(b_text >= 1, b_text <= 6)

# Base ordering constraints
solver.add(b_grain > b_live)
solver.add(b_live > b_text)
solver.add(b_prod > b_fuel)
# Textiles and produce are adjacent
solver.add(Or(b_text == b_prod + 1, b_text == b_prod - 1))

# Hypothetical condition: produce is next to livestock
solver.add(Or(b_prod == b_live + 1, b_prod == b_live - 1))

# Answer choices conditions
answer_conditions = [
    b_fuel == 2,           # Option 0: Bay 2 is holding fuel
    b_prod == 4,           # Option 1: Bay 4 is holding produce
    b_text == 4,           # Option 2: Bay 4 is holding textiles
    b_grain == 5,          # Option 3: Bay 5 is holding grain
    b_mach == 5            # Option 4: Bay 5 is holding machinery
]

# Check each answer choice
answer_index_list = []
for idx, cond in enumerate(answer_conditions):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(cond)
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)