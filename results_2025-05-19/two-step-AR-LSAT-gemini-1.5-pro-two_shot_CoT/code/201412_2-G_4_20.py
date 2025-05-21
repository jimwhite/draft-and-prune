from z3 import *

# Define variables
assigned = Array('assigned', IntSort(), BoolSort())
university = Array('university', IntSort(), IntSort())

solver = Solver()

# Constraint 1 (At least two at each university)
solver.add(Sum([If(And(assigned[i], university[i] == 0), 1, 0) for i in range(6)]) >= 2)
solver.add(Sum([If(And(assigned[i], university[i] == 1), 1, 0) for i in range(6)]) >= 2)

# Constraint 2 (No photographer at both)
i = Int('i') # Define i for the ForAll quantifier
solver.add(ForAll([i], Implies(assigned[i], Or(university[i] == 0, university[i] == 1))))
# Removed redundant constraint, already enforced by subsequent constraints

# Constraint 3 (Frost with Heideck)
solver.add(assigned[0] == assigned[2])
solver.add(Implies(assigned[0], university[0] == university[2]))

# Constraint 4 (Lai and Mays different)
solver.add(Implies(And(assigned[4], assigned[5]), university[4] != university[5]))

# Constraint 5 (Gonzalez at Silva -> Lai at Thorne)
solver.add(Implies(And(assigned[1], university[1] == 0), And(assigned[4], university[4] == 1)))

# Constraint 6 (Knutson not at Thorne -> Heideck and Mays at Thorne)
solver.add(Implies(Not(And(assigned[3], university[3] == 1)), And(And(assigned[2], university[2] == 1), And(assigned[5], university[5] == 1))))

# Answer choices
options = [
    [0, 2],  # Frost, Heideck
    [0, 2, 3],  # Frost, Heideck, Knutson
    [0, 2, 3, 4],  # Frost, Heideck, Knutson, Lai
    [0, 1, 2],  # Frost, Gonzalez, Heideck
    [0, 1, 2, 5]  # Frost, Gonzalez, Heideck, Mays
]

for option_index, option in enumerate(options):
    solver.push()
    # Add constraints for assigned photographers
    for photographer in option:
        solver.add(assigned[photographer])

    # Check negation of unassigned photographers
    negated_unassigned = [Not(assigned[i]) for i in range(6) if i not in option]
    if solver.check(*negated_unassigned) == unsat:
        solver.pop()
        continue  # This option is incorrect

    print(f"Option {chr(65 + option_index)} is correct")
    exit()
    solver.pop()

