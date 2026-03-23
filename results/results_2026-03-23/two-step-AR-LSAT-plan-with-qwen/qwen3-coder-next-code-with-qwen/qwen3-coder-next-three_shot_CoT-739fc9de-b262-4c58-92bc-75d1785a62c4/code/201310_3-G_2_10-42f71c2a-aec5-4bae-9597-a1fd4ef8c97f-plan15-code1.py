from z3 import *

# Employee indices: Myers, Ortega, Paine, Schmidt, Thomson, Wong, Yoder, Zayre
(MY, OR, PA, SC, TH, WO, YO, ZA) = range(8)

# Boolean variables for selection
selected = [Bool(f"selected_{i}") for i in range(8)]

# Base solver
solver = Solver()

# Global constraint: at least 4 employees selected
solver.add(Sum([If(selected[i], 1, 0) for i in range(8)]) >= 4)

# Conditional constraints
# If Myers is selected, neither Ortega nor Paine can be
solver.add(Implies(selected[MY], And(Not(selected[OR]), Not(selected[PA]))))

# If Schmidt is selected, both Paine and Thomson must be
solver.add(Implies(selected[SC], And(selected[PA], selected[TH])))

# If Wong is selected, both Myers and Yoder must be
solver.add(Implies(selected[WO], And(selected[MY], selected[YO])))

# Assumption: Yoder is NOT selected
solver.add(Not(selected[YO]))

# Answer choices (order matters for indexing)
answer_choices = [
    ZA,  # Zayre
    TH,  # Thomson
    PA,  # Paine
    OR,  # Ortega
    MY   # Myers
]

# Check each answer choice: which one CANNOT be on the team (EXCEPT case)
answer_index_list = []
for idx, emp in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert this employee is selected
    s_chk.add(selected[emp])
    
    # If UNSAT, this employee cannot be on the team (EXCEPT answer)
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)