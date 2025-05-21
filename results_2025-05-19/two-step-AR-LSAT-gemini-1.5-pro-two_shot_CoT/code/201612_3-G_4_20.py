from z3 import *

# Entities
RP = 0
SC = 1
TC = 2
GZ = 0
YH = 1
ZH = 2
FT = 3
LB = 4
KB = 5
MB = 6
OZ = 7
C1 = 0
C2 = 1
C3 = 2

# Variables
owner = [[Int("owner_%s_%s" % (t, b)) for b in range(8)] for t in range(6)]

# Helper Functions
def SameClass(b1, b2):
    classes = [C1, C3, C3, C1, C2, C2, C2, C2]
    return classes[b1] == classes[b2]

def IsClass(b, c):
    classes = [C1, C3, C3, C1, C2, C2, C2, C2]
    return classes[b] == c

def PreserveOtherOwnerships(t1, t2, *buildings):
    constraints = []
    for b in range(8):
        if b not in buildings:
            constraints.append(owner[t1][b] == owner[t2][b])
    return And(constraints)

# Solver
solver = Solver()

# Constraint 0: Initial Ownership
initial_ownership = [
    owner[0][GZ] == RP, owner[0][YH] == RP, owner[0][ZH] == RP,
    owner[0][FT] == SC, owner[0][LB] == SC,
    owner[0][KB] == TC, owner[0][MB] == TC, owner[0][OZ] == TC
]
solver.add(initial_ownership)

# Constraint 1: Valid Trades - Same Class
for t in range(5):
    for b1 in range(8):
        for b2 in range(8):
            solver.add(Implies(And(b1 != b2, SameClass(b1, b2)),
                               Implies(owner[t][b1] != owner[t][b2],
                                       And(owner[t+1][b1] == owner[t][b2], owner[t+1][b2] == owner[t][b1],
                                           PreserveOtherOwnerships(t, t+1, b1, b2)))))

# Constraint 2: Valid Trades - C1 for 2xC2
for t in range(5):
    for b1 in range(8):
        for b2 in range(8):
            for b3 in range(8):
                solver.add(Implies(And(b1 != b2, b1 != b3, b2 != b3, IsClass(b1, C1), IsClass(b2, C2), IsClass(b3, C2)),
                                   Implies(And(owner[t][b1] != owner[t][b2], owner[t][b1] != owner[t][b3], owner[t][b2] == owner[t][b3]),
                                           And(owner[t+1][b1] == owner[t][b2], owner[t+1][b2] == owner[t][b1], owner[t+1][b3] == owner[t][b1],
                                               PreserveOtherOwnerships(t, t+1, b1, b2, b3)))))

# Constraint 3: Valid Trades - C2 for 2xC3
for t in range(5):
    for b1 in range(8):
        for b2 in range(8):
            for b3 in range(8):
                solver.add(Implies(And(b1 != b2, b1 != b3, b2 != b3, IsClass(b1, C2), IsClass(b2, C3), IsClass(b3, C3)),
                                   Implies(And(owner[t][b1] != owner[t][b2], owner[t][b1] != owner[t][b3], owner[t][b2] == owner[t][b3]),
                                           And(owner[t+1][b1] == owner[t][b2], owner[t+1][b2] == owner[t][b1], owner[t+1][b3] == owner[t][b1],
                                               PreserveOtherOwnerships(t, t+1, b1, b2, b3)))))


# Check Answer Choices
options = [
    ([GZ, FT], RP),  # A
    ([FT, MB], SC),  # B
    ([GZ, LB], SC),  # C
    ([FT, OZ], TC),  # D
    ([GZ, MB], TC)   # E
]

for i, (buildings, company) in enumerate(options):
    solver.push()
    constraints = []
    for b in buildings:
        constraints.append(owner[5][b] == company)
    for b in range(8):
        if b not in buildings:
            constraints.append(owner[5][b] != company)
    solver.add(constraints)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()