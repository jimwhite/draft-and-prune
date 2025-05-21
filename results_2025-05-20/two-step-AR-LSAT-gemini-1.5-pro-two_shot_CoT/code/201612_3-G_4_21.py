from z3 import *

# Entities (IDs)
RP = 0
SC = 1
TC = 2
GT = 0
YH = 1
ZH = 2
FT = 3
LB = 4
KB = 5
MB = 6
OB = 7
C1 = 0
C2 = 1
C3 = 2

# Variables
owner = Array('owner', IntSort(), IntSort())
building_class = Array('building_class', IntSort(), IntSort())
b = Int('b')

# Solver
solver = Solver()

# Constraint 0 (Initial Ownership)
solver.add(owner[GT] == RP)
solver.add(owner[YH] == RP)
solver.add(owner[ZH] == RP)
solver.add(owner[FT] == SC)
solver.add(owner[LB] == SC)
solver.add(owner[KB] == TC)
solver.add(owner[MB] == TC)
solver.add(owner[OB] == TC)

# Constraint 1 (Building Classes)
solver.add(building_class[GT] == C1)
solver.add(building_class[YH] == C3)
solver.add(building_class[ZH] == C3)
solver.add(building_class[FT] == C1)
solver.add(building_class[LB] == C2)
solver.add(building_class[KB] == C2)
solver.add(building_class[MB] == C2)
solver.add(building_class[OB] == C2)

# Constraint 2 (RealProp Owns Only Class 2 Buildings After Trades)
solver.add(ForAll([b], Implies(And(owner[b] == RP, b >= 0, b < 8), building_class[b] == C2)))

# Constraint 3 (RealProp's Final Building Counts)
solver.add(Sum([If(And(owner[b] == RP, building_class[b] == C1, b >= 0, b < 8), 1, 0)]) == 0)
solver.add(Sum([If(And(owner[b] == RP, building_class[b] == C2, b >= 0, b < 8), 1, 0)]) == 3)
solver.add(Sum([If(And(owner[b] == RP, building_class[b] == C3, b >= 0, b < 8), 1, 0)]) == 0)


# Constraint 4 (Derived Ownership of Initial C1 Buildings)
solver.add(owner[GT] == TC)
solver.add(owner[FT] == SC)

# Constraint 5 (Derived Ownership of Initial C3 Buildings)
solver.add(owner[YH] != RP)
solver.add(owner[ZH] != RP)


# Check answer choices
answer_choices = [
    ForAll([b], Implies(And(owner[b] == TC, b >= 0, b < 8), building_class[b] != C1)),  # Not A
    owner[MB] != TC,  # Not B
    ForAll([b], Implies(And(owner[b] == SC, b >= 0, b < 8), building_class[b] != C2)),  # Not C
    Not(And(owner[YH] == SC, owner[ZH] == SC)),  # Not D
    owner[FT] != SC  # Not E
]

for i, constraint in enumerate(answer_choices):
    solver.push()
    solver.add(constraint)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()