from z3 import *

# Variables
RP_C1, RP_C2, RP_C3 = Ints('RP_C1 RP_C2 RP_C3')
SC_C1, SC_C2, SC_C3 = Ints('SC_C1 SC_C2 SC_C3')
TC_C1, TC_C2, TC_C3 = Ints('TC_C1 TC_C2 TC_C3')

solver = Solver()

# Constraint 1: Non-negativity
solver.add(RP_C1 >= 0, RP_C2 >= 0, RP_C3 >= 0,
           SC_C1 >= 0, SC_C2 >= 0, SC_C3 >= 0,
           TC_C1 >= 0, TC_C2 >= 0, TC_C3 >= 0)

# Constraint 2: Total Conservation
solver.add(RP_C1 + SC_C1 + TC_C1 == 2)
solver.add(RP_C2 + SC_C2 + TC_C2 == 4)
solver.add(RP_C3 + SC_C3 + TC_C3 == 2)

# Constraint 3: C3 Pair Ownership Invariant
solver.add(Or(And(RP_C3 == 2, SC_C3 == 0, TC_C3 == 0),
               And(RP_C3 == 0, SC_C3 == 2, TC_C3 == 0),
               And(RP_C3 == 0, SC_C3 == 0, TC_C3 == 2)))

# Constraint 4: C2 Parity Reachability Invariant
solver.add(Or(And(RP_C2 % 2 == 0, SC_C2 % 2 == 1, TC_C2 % 2 == 1),
               And(RP_C2 % 2 == 1, SC_C2 % 2 == 0, TC_C2 % 2 == 1),
               And(RP_C2 % 2 == 1, SC_C2 % 2 == 1, TC_C2 % 2 == 0),
               And(RP_C2 % 2 == 0, SC_C2 % 2 == 0, TC_C2 % 2 == 0)))

# Check answer choices
choices = [
    [RP_C1 == 2, RP_C2 == 0, RP_C3 == 0],  # A
    [SC_C1 == 1, SC_C2 == 1, SC_C3 == 0],  # B
    [SC_C1 == 1, SC_C2 == 1, SC_C3 == 0],  # C
    [TC_C1 == 1, TC_C2 == 1, TC_C3 == 0],  # D
    [TC_C1 == 1, TC_C2 == 1, TC_C3 == 0]   # E
]

for i, choice in enumerate(choices):
    solver.push()
    solver.add(choice)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()