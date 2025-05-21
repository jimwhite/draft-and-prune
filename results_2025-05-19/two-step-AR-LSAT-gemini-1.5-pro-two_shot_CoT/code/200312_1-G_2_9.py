from z3 import *

# Variables
bay_cargo = Array('bay_cargo', IntSort(), IntSort())

# Cargo type mapping (0-indexed)
# F=0, G=1, L=2, M=3, P=4, T=5

# Solver
solver = Solver()

# Constraint 0 (Domain)
solver.add(ForAll(i, Implies(And(i >= 1, i <= 6), And(bay_cargo[i] >= 0, bay_cargo[i] <= 5))) for i in Ints('i'))

# Constraint 1 (Distinctness)
solver.add(Distinct([bay_cargo[i] for i in range(1, 7)]))

# Constraint 2 (Grain > Livestock)
solver.add(ForAll([i, j], Implies(And(i >= 1, i <= 6, j >= 1, j <= 6, bay_cargo[i] == 1, bay_cargo[j] == 2), i > j)) for i in Ints('i') for j in Ints('j'))

# Constraint 3 (Livestock > Textiles)
solver.add(ForAll([i, j], Implies(And(i >= 1, i <= 6, j >= 1, j <= 6, bay_cargo[i] == 2, bay_cargo[j] == 5), i > j)) for i in Ints('i') for j in Ints('j'))

# Constraint 4 (Produce > Fuel)
solver.add(ForAll([i, j], Implies(And(i >= 1, i <= 6, j >= 1, j <= 6, bay_cargo[i] == 4, bay_cargo[j] == 0), i > j)) for i in Ints('i') for j in Ints('j'))

# Constraint 5 (Textiles next to Produce)
solver.add(Or([And(bay_cargo[i] == 5, bay_cargo[i+1] == 4) for i in range(1, 6)]))

# Constraint 6 (Produce next to Textiles)
solver.add(Or([And(bay_cargo[i] == 4, bay_cargo[i+1] == 5) for i in range(1, 6)]))


# Answer choices and corresponding constraints
answer_choices = [1, 2, 3, 5, 6]  # Bay numbers
for option_index, bay_num in enumerate(answer_choices):
    solver.push()
    solver.add(bay_cargo[bay_num] == 2)  # Livestock in this bay
    if solver.check() == sat:
        print(f"Option {chr(65 + option_index)} is correct")
        exit()
    solver.pop()
