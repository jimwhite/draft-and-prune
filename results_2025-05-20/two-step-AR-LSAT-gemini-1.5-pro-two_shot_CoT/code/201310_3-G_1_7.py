from z3 import *

# 1. Entities (Band IDs and Slot Indices as defined in the plan)
U = 0
V = 1
W = 2
X = 3
Y = 4
Z = 5

# 2. Variables
band_at_slot = Array('band_at_slot', IntSort(), IntSort())

# 3. Constraints
i = Int('i')
j = Int('j')

# Constraint 0 (Domain)
Constraint_0 = ForAll(i, Implies(And(i >= 0, i < 6), And(band_at_slot[i] >= 0, band_at_slot[i] < 6)))

# Constraint 1 (Distinctness)
Constraint_1 = Distinct([band_at_slot[k] for k in range(6)])

# Constraint 2 (V before Z)
Constraint_2 = ForAll([i, j], Implies(And(band_at_slot[i] == V, band_at_slot[j] == Z), i < j))

# Constraint 5 (U in last three)
Constraint_5 = Or(band_at_slot[3] == U, band_at_slot[4] == U, band_at_slot[5] == U)

# Constraint 6 (Y in first three)
Constraint_6 = Or(band_at_slot[0] == Y, band_at_slot[1] == Y, band_at_slot[2] == Y)

# Base Constraints
C_base = And(Constraint_0, Constraint_1, Constraint_2, Constraint_5, Constraint_6)

# Original Constraints
Constraint_3 = ForAll([i, j], Implies(And(band_at_slot[i] == W, band_at_slot[j] == X), i < j))
Constraint_4 = ForAll([i, j], Implies(And(band_at_slot[i] == Z, band_at_slot[j] == X), i < j))
C_orig = And(Constraint_3, Constraint_4)


# 4. Alternative Constraints
C_alt_A = ForAll([i, j], Implies(And(band_at_slot[i] != U, band_at_slot[j] == X), i < j))
C_alt_B = And(ForAll([i, j], Implies(And(band_at_slot[i] == V, band_at_slot[j] == W), i < j)), ForAll([i, j], Implies(And(band_at_slot[i] == W, band_at_slot[j] == Z), i < j)))
C_alt_C = And(ForAll([i, j], Implies(And(band_at_slot[i] == V, band_at_slot[j] == X), i < j)), ForAll([i, j], Implies(And(band_at_slot[i] == W, band_at_slot[j] == X), i < j)))
C_alt_D = ForAll(i, Implies(band_at_slot[i] == X, Or(And(i > 0, band_at_slot[i - 1] == U), And(i < 5, band_at_slot[i + 1] == U))))
C_alt_E = Or(band_at_slot[4] == X, band_at_slot[5] == X)

alt_constraints = [C_alt_A, C_alt_B, C_alt_C, C_alt_D, C_alt_E]

# 5. Answering the Question
solver = Solver()

for idx, C_alt in enumerate(alt_constraints):
    option = chr(65 + idx)

    solver.push()
    solver.add(C_base, C_alt, Not(C_orig))
    check1 = solver.check()
    solver.pop()

    solver.push()
    solver.add(C_base, C_orig, Not(C_alt))
    check2 = solver.check()
    solver.pop()

    if check1 == unsat and check2 == unsat:
        print(f"Option {option} is correct")
        exit()