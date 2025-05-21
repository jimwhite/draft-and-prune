from z3 import *

# Variables
bay_cargo = Array('bay_cargo', IntSort(), IntSort())
bay_F, bay_G, bay_L, bay_M, bay_P, bay_T = Ints('bay_F bay_G bay_L bay_M bay_P bay_T')
i = Int('i') # Declare i for use in ForAll

solver = Solver()

# Constraints
solver.add(ForAll(i, Implies(And(i >= 1, i <= 6), And(bay_cargo[i] >= 0, bay_cargo[i] <= 5)))) # Constraint 0: Use ForAll correctly with a declared variable 'i'
solver.add(Distinct([bay_cargo[i] for i in range(1, 7)])) # Constraint 1
solver.add(And(bay_F >= 1, bay_F <= 6, bay_G >= 1, bay_G <= 6, bay_L >= 1, bay_L <= 6, bay_M >= 1, bay_M <= 6, bay_P >= 1, bay_P <= 6, bay_T >= 1, bay_T <= 6)) # Constraint 2
solver.add(Distinct(bay_F, bay_G, bay_L, bay_M, bay_P, bay_T)) # Constraint 3
solver.add(And(bay_cargo[bay_F] == 0, bay_cargo[bay_G] == 1, bay_cargo[bay_L] == 2, bay_cargo[bay_M] == 3, bay_cargo[bay_P] == 4, bay_cargo[bay_T] == 5)) # Constraint 4
solver.add(bay_G > bay_L) # Constraint 5
solver.add(bay_L > bay_T) # Constraint 6
solver.add(bay_P > bay_F) # Constraint 7
solver.add(Abs(bay_T - bay_P) == 1) # Constraint 8

# Check answer choices
choices = [
    Abs(bay_F - bay_M) == 1,  # A
    Abs(bay_G - bay_M) == 1,  # B
    Abs(bay_L - bay_F) == 1,  # C
    Abs(bay_P - bay_L) == 1,  # D
    Abs(bay_T - bay_F) == 1   # E
]

for i in range(len(choices)):
    solver.push()
    solver.add(choices[i])
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
