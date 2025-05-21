from z3 import *

# Define variables
assigned = Array('assigned', IntSort(), IntSort())

# Create solver
solver = Solver()

# Constraint 1: Domain
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 0, i < 6), Or(assigned[i] == 0, assigned[i] == 1, assigned[i] == -1))))

# Constraint 2: At least two at each university
sum_silva = Sum([If(assigned[i] == 0, 1, 0) for i in range(6)])
sum_thorne = Sum([If(assigned[i] == 1, 1, 0) for i in range(6)])
solver.add(And(sum_silva >= 2, sum_thorne >= 2))

# Constraint 3: Frost with Heideck
solver.add(Or(And(assigned[0] == 0, assigned[2] == 0), And(assigned[0] == 1, assigned[2] == 1)))

# Constraint 4: Lai and Mays different
solver.add(Implies(And(assigned[4] != -1, assigned[5] != -1), assigned[4] != assigned[5]))

# Constraint 5: Gonzalez Silva -> Lai Thorne
solver.add(Implies(assigned[1] == 0, assigned[4] == 1))

# Constraint 6: Knutson not Thorne -> Heideck and Mays Thorne
solver.add(Implies(assigned[3] != 1, And(assigned[2] == 1, assigned[5] == 1)))

# Answer choices
choices = [
    [1, 4, 0, 2, 5],  # A
    [1, 5, 3, 4],  # B
    [0, 1, 2, 3, 4, 5],  # C
    [0, 2, 5, 1, 4],  # D
    [0, 2, 5, 1, 3, 4]  # E
]
universities = [
    [0, 0, 1, 1, 1],  # A
    [0, 0, 1, 1],  # B
    [0, 0, 0, 1, 1, 1],  # C
    [0, 0, 0, 1, 1],  # D
    [0, 0, 0, 1, 1, 1]  # E
]

# Check each answer choice
for choice_idx, (choice, univ) in enumerate(zip(choices, universities)):
    solver.push()
    for photographer, university in zip(choice, univ):
        solver.add(assigned[photographer] == university)
    not_assigned = [p for p in range(6) if p not in choice]
    for p in not_assigned:
        solver.add(assigned[p] == -1)

    if solver.check() == sat:
        print(f"Option {chr(65 + choice_idx)} is correct")
        exit()
    solver.pop()