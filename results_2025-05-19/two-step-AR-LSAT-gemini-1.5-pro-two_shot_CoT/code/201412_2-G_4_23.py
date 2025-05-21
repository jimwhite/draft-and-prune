from z3 import *

# Define variables
assigned = Array('assigned', IntSort(), IntSort())

# Define solver
solver = Solver()

# Constraint 0 (Domain)
p = Int('p')
solver.add(ForAll([p], Implies(And(p >= 0, p < 6), Or(assigned[p] == 0, assigned[p] == 1, assigned[p] == -1))))

# Constraint 1 (At least two at each university)
s_count = Sum([If(assigned[i] == 0, 1, 0) for i in range(6)])
t_count = Sum([If(assigned[i] == 1, 1, 0) for i in range(6)])
solver.add(And(s_count >= 2, t_count >= 2))

# Constraint 2 (No photographer at both)
p = Int('p')
solver.add(ForAll([p], Implies(Or(assigned[p] == 0, assigned[p] == 1), assigned[p] != 1 - assigned[p])))


# Constraint 3 (Frost with Heideck)
solver.add(Or(And(assigned[0] == 0, assigned[2] == 0), And(assigned[0] == 1, assigned[2] == 1)))

# Constraint 4 (Lai and Mays separate)
solver.add(Implies(And(assigned[4] != -1, assigned[5] != -1), assigned[4] != assigned[5]))

# Constraint 5 (Gonzalez at Silva -> Lai at Thorne)
solver.add(Implies(assigned[1] == 0, assigned[4] == 1))

# Constraint 6 (Original)
constraint6 = Implies(assigned[3] != 1, And(assigned[2] == 1, assigned[5] == 1))

# Answer choices
choices = [
    Implies(assigned[3] == 0, Not(And(assigned[2] == 0, assigned[5] == 0))),  # A
    Implies(assigned[3] == 0, assigned[4] == 0),  # B
    Implies(assigned[3] != 1, And(assigned[0] == 1, assigned[5] == 1)),  # C
    Implies(assigned[3] != 1, Not(assigned[2] == assigned[4])),  #D
    Implies(Not(Or(assigned[2] == 1, assigned[5] == 1)), assigned[3] == 1)  # E
]

choice_letter = 'A'
for choice in choices:
    solver.push()
    solver.add(constraint6)
    original_models = []
    while solver.check() == sat:
        model = solver.model()
        original_models.append(model)
        block = []
        for i in range(6):
            if assigned[i] in model:  # Check if assigned[i] is in the model
                block.append(assigned[i] != model[assigned[i]])
        solver.add(Or(block))
    solver.pop()

    solver.push()
    solver.add(choice)
    choice_models = []
    while solver.check() == sat:
        model = solver.model()
        choice_models.append(model)
        block = []
        for i in range(6):
            if assigned[i] in model:  # Check if assigned[i] is in the model
                block.append(assigned[i] != model[assigned[i]])
        solver.add(Or(block))
    solver.pop()

    if len(original_models) == len(choice_models) and all(any(all(m1[assigned[i]] == m2[assigned[i]] for i in range(6) if assigned[i] in m1 and assigned[i] in m2) for m2 in choice_models) for m1 in original_models) and all(any(all(m1[assigned[i]] == m2[assigned[i]] for i in range(6) if assigned[i] in m1 and assigned[i] in m2) for m1 in original_models) for m2 in choice_models):
        print(f"Option {choice_letter} is correct")
        exit()

    choice_letter = chr(ord(choice_letter) + 1)

