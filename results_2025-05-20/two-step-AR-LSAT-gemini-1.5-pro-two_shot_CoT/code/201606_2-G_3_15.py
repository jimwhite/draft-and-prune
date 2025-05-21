from z3 import *

# Variables
day_H, day_L, day_M, day_S, day_T, day_V = Ints('day_H day_L day_M day_S day_T day_V')

# Solver
solver = Solver()

# Constraints
solver.add(Distinct([day_H, day_L, day_M, day_S, day_T, day_V]))
for day in [day_H, day_L, day_M, day_S, day_T, day_V]:
    solver.add(And(day >= 0, day <= 5))
solver.add(day_S != 0)
solver.add(Implies(day_H < day_L, day_M < day_L))
solver.add(day_S < day_M)
solver.add(day_S < day_V)
solver.add(Xor(day_T < day_H, day_T < day_V))

# Antique names for output
antique_names = {day_H: 'the harmonica', day_L: 'the lamp', day_M: 'the mirror', day_S: 'the sundial', day_T: 'the table'}

# Check each answer choice
options = ['the harmonica', 'the lamp', 'the mirror', 'the sundial', 'the table']
for i, option in enumerate(options):
    solver.push()
    antique_var = [k for k, v in antique_names.items() if v == option][0]
    solver.add(day_V - 1 == antique_var)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()