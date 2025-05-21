from z3 import *

# Variables
owner = Array('owner', IntSort(), IntSort())
building_class = Array('building_class', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraint 0: Initial Ownership
solver.add(owner[0] == 0)
solver.add(owner[1] == 0)
solver.add(owner[2] == 0)
solver.add(owner[3] == 1)
solver.add(owner[4] == 1)
solver.add(owner[5] == 2)
solver.add(owner[6] == 2)
solver.add(owner[7] == 2)

# Constraint 1: Building Classes
solver.add(building_class[0] == 0)
solver.add(building_class[1] == 2)
solver.add(building_class[2] == 2)
solver.add(building_class[3] == 0)
solver.add(building_class[4] == 1)
solver.add(building_class[5] == 1)
solver.add(building_class[6] == 1)
solver.add(building_class[7] == 1)

# Constraint 2: Trustcorp Owns No Class 2 Buildings
b = Int('b')
solver.add(ForAll([b], Implies(And(b >= 0, b < 8, building_class[b] == 1), owner[b] != 2)))


# Helper function for counting buildings of a class owned by a company
def count_class(company_id, class_id):
    return Sum([If(And(owner[b] == company_id, building_class[b] == class_id), 1, 0) for b in range(8)])

# Constraint 3: Invariant - Total Class Counts
solver.add(count_class(0, 0) + count_class(1, 0) + count_class(2, 0) == 2)
solver.add(count_class(0, 1) + count_class(1, 1) + count_class(2, 1) == 4)
solver.add(count_class(0, 2) + count_class(1, 2) + count_class(2, 2) == 2)

# Constraint 4: Valid Owners
solver.add(ForAll([b], Implies(And(b >= 0, b < 8), Or(owner[b] == 0, owner[b] == 1, owner[b] == 2))))

# Check answer choices
negations = [
    And(owner[0] != 0, owner[3] != 0),  # Not A
    Exists([b], Implies(And(b >= 0, b < 8, owner[b] == 1), building_class[b] != 1)),  # Not B
    And(owner[5] != 1, owner[6] != 1, owner[7] != 1, owner[4] != 2),  # Not C
    owner[0] != 2,  # Not D
    owner[2] != 2   # Not E
]

for i, negation in enumerate(negations):
    solver.push()
    solver.add(negation)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()