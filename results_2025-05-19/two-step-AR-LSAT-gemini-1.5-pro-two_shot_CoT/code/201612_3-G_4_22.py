from z3 import *

# Buildings: Garza Tower (0), Yates House (1), Zimmer House (2), Flores Tower (3), Lynch Building (4), King Building (5), Meyer Building (6), Ortiz Building (7)
# Companies: RealProp (0), Southco (1), Trustcorp (2)
# Classes: Class 1 (0), Class 2 (1), Class 3 (2)

owner = Array('owner', IntSort(), IntSort())
building_class = Array('building_class', IntSort(), IntSort())

solver = Solver()

# Constraint 0: Initial Ownership
solver.add(owner[0] == 0)  # Garza Tower (0) owned by RealProp (0)
solver.add(owner[1] == 0)  # Yates House (1) owned by RealProp (0)
solver.add(owner[2] == 0)  # Zimmer House (2) owned by RealProp (0)
solver.add(owner[3] == 1)  # Flores Tower (3) owned by Southco (1)
solver.add(owner[4] == 1)  # Lynch Building (4) owned by Southco (1)
solver.add(owner[5] == 2)  # King Building (5) owned by Trustcorp (2)
solver.add(owner[6] == 2)  # Meyer Building (6) owned by Trustcorp (2)
solver.add(owner[7] == 2)  # Ortiz Building (7) owned by Trustcorp (2)


# Constraint 1: Building Classes
solver.add(building_class[0] == 0)  # Garza Tower (0) is Class 1 (0)
solver.add(building_class[3] == 0)  # Flores Tower (3) is Class 1 (0)
solver.add(building_class[4] == 1)  # Lynch Building (4) is Class 2 (1)
solver.add(building_class[5] == 1)  # King Building (5) is Class 2 (1)
solver.add(building_class[6] == 1)  # Meyer Building (6) is Class 2 (1)
solver.add(building_class[7] == 1)  # Ortiz Building (7) is Class 2 (1)
solver.add(building_class[1] == 2)  # Yates House (1) is Class 3 (2)
solver.add(building_class[2] == 2)  # Zimmer House (2) is Class 3 (2)

# Constraint 2: Trustcorp owns no class 2 buildings
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 0, i < 8, building_class[i] == 1), owner[i] != 2)))


# Answer choices and their negations
options = [
    Not(Or(owner[0] == 0, owner[3] == 0)),  # A: RealProp does *not* own a class 1 building
    Not(And(owner[4] == 1, Not(Or(owner[0] == 1, owner[1] == 1, owner[2] == 1, owner[3] == 1, owner[5] == 1, owner[6] == 1, owner[7] == 1)))),  # B: Southco does *not* own only class 2 buildings
    Not(Or(owner[5] == 1, owner[6] == 1, owner[7] == 1, owner[4] == 2, owner[1] == 2, owner[2] == 2, owner[0] == 2, owner[3] == 2)), # C: No trade between Southco and Trustcorp
    owner[0] != 2,  # D: Trustcorp does *not* own Garza Tower
    owner[2] != 2   # E: Trustcorp does *not* own Zimmer House
]

option_labels = ['A', 'B', 'C', 'D', 'E']

for i in range(len(options)):
    solver.push()
    solver.add(options[i])
    if solver.check() == unsat:
        print(f"Option {option_labels[i]} is correct")
        exit()
    solver.pop()