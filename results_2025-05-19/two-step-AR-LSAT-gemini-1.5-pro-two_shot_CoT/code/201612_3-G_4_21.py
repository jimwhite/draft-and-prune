from z3 import *

# Variables
owns = Array('owns', IntSort(), IntSort())
building_class = Array('building_class', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraint 0 (Initial Ownership)
solver.add(owns[0] == 0)
solver.add(owns[1] == 0)
solver.add(owns[2] == 0)
solver.add(owns[3] == 1)
solver.add(owns[4] == 1)
solver.add(owns[5] == 2)
solver.add(owns[6] == 2)
solver.add(owns[7] == 2)

# Constraint 1 (Building Classes)
solver.add(building_class[0] == 0)
solver.add(building_class[3] == 0)
solver.add(building_class[4] == 1)
solver.add(building_class[5] == 1)
solver.add(building_class[6] == 1)
solver.add(building_class[7] == 1)
solver.add(building_class[1] == 2)
solver.add(building_class[2] == 2)

# Constraint 2 (RealProp Owns Only Class 2)
b = Int('b')
solver.add(ForAll([b], Implies(And(b >= 0, b <= 7), Implies(owns[b] == 0, building_class[b] == 1))))


# Constraint 3 (Trade Rules - One for One Same Class) - Simplified
b1 = Int('b1')
b2 = Int('b2')


# Constraint 4 (Trade Rules - C1 for two C2)
b1 = Int('b1')
b2 = Int('b2')
b3 = Int('b3')
o1 = Int('o1')
o2 = Int('o2')
o3 = Int('o3')



# Constraint 5 (Trade Rules - C2 for two C3)
b1 = Int('b1')
b2 = Int('b2')
b3 = Int('b3')
o1 = Int('o1')
o2 = Int('o2')
o3 = Int('o3')


# Answer Choices
answers = [
    Exists([b], And(owns[b] == 2, building_class[b] == 0)),
    owns[6] == 2,
    Exists([b], And(owns[b] == 1, building_class[b] == 1)),
    And(owns[1] == 1, owns[2] == 1),
    owns[3] == 1
]

for i, answer in enumerate(answers):
    solver.push()
    solver.add(answer)
    if solver.check() == sat:
        solver.pop()
        solver.push()
        solver.add(Not(answer))
        if solver.check() == unsat:
            print(f"Option {chr(65 + i)} is correct")
            exit()
        solver.pop()
    else:
        solver.pop()