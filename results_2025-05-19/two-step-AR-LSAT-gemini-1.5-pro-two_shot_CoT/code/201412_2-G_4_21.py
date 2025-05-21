from z3 import *

# Variables
assigned = Array('assigned', IntSort(), BoolSort())
university = Array('university', IntSort(), IntSort())

solver = Solver()

# Constraints
# Constraint 1 (At least two at each university)
solver.add(Sum([If(And(assigned[i], university[i] == 0), 1, 0) for i in range(6)]) >= 2)
solver.add(Sum([If(And(assigned[i], university[i] == 1), 1, 0) for i in range(6)]) >= 2)

# Constraint 2 (Exactly four assigned)
solver.add(Sum([If(assigned[i], 1, 0) for i in range(6)]) == 4)

# Constraint 3 (No photographer at both)
# Fixed: Correct usage of ForAll
solver.add(ForAll(i, Implies(assigned[i], Or(university[i] == 0, university[i] == 1))) for i in range(6))

# Constraint 4 (Frost with Heideck)
solver.add(assigned[0] == assigned[2])
solver.add(Implies(assigned[0], university[0] == university[2]))

# Constraint 5 (Lai and Mays different)
solver.add(Implies(And(assigned[4], assigned[5]), university[4] != university[5]))

# Constraint 6 (Gonzalez at Silva -> Lai at Thorne)
solver.add(Implies(And(assigned[1], university[1] == 0), And(assigned[4], university[4] == 1)))

# Constraint 7 (Knutson not at Thorne -> Heideck and Mays at Thorne)
solver.add(Implies(Not(And(assigned[3], university[3] == 1)), And(assigned[2], university[2] == 1, assigned[5], university[5] == 1)))


# Answer choices
photographers = ["Frost", "Gonzalez", "Heideck", "Knutson", "Lai", "Mays"]
for i in range(len(photographers)):
    solver.push()
    solver.add(Or(Not(assigned[i]), university[i] != 0)) # Force photographer i not to be at Silva (university 0)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
