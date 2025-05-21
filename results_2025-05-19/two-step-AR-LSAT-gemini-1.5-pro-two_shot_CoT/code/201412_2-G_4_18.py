from z3 import *

# Variables
assigned = Array('assigned', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraint 0 (Domain)
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 0, i < 6), Or(assigned[i] == 0, assigned[i] == 1, assigned[i] == -1))))

# Constraint 1 (At least two at each)
i = Int('i')
j = Int('j')
solver.add(Exists([i, j], And(i != j, assigned[i] == 0, assigned[j] == 0)))  # Silva
solver.add(Exists([i, j], And(i != j, assigned[i] == 1, assigned[j] == 1)))  # Thorne

# Constraint 2 (No photographer at both)
i = Int('i')
solver.add(ForAll([i], Implies(And(assigned[i] != -1, assigned[i] != 0), assigned[i] == 1)))

# Constraint 3 (Frost with Heideck)
solver.add(Or(And(assigned[0] == 0, assigned[2] == 0), And(assigned[0] == 1, assigned[2] == 1)))

# Constraint 4 (Lai and Mays different)
solver.add(Implies(And(assigned[4] != -1, assigned[5] != -1), assigned[4] != assigned[5]))

# Constraint 5 (Gonzalez Silva -> Lai Thorne)
solver.add(Implies(assigned[1] == 0, assigned[4] == 1))

# Constraint 6 (Knutson not Thorne -> Heideck and Mays Thorne)
solver.add(Implies(assigned[3] != 1, And(assigned[2] == 1, assigned[5] == 1)))

# Constraint 7 (Heideck and Lai together)
solver.add(Or(And(assigned[2] == 0, assigned[4] == 0), And(assigned[2] == 1, assigned[4] == 1)))

# Answer choices
choices = [
    assigned[0] == 1,  # A
    assigned[1] == 0,  # B
    assigned[1] == -1, # C
    assigned[3] == 1,  # D
    assigned[4] == 1   # E
]

for i in range(len(choices)):
    solver.push()
    solver.add(choices[i])
    if solver.check() == sat:
        solver.pop()
        solver.push()
        solver.add(Not(choices[i]))
        if solver.check() == unsat:
            print(f"Option {chr(65 + i)} is correct")
            exit()
        solver.pop()
    else:
        solver.pop()