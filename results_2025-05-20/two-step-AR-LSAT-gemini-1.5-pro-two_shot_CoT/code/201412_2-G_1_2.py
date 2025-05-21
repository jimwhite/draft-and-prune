from z3 import *

# Define variables
solo_order = Array('solo_order', IntSort(), IntSort())

# Create solver
solver = Solver()

# Constraints
solver.add(And([And(solo_order[i] >= 0, solo_order[i] <= 5) for i in range(6)])) # Constraint 0
solver.add(Distinct([solo_order[i] for i in range(6)])) # Constraint 1
solver.add(solo_order[3] != 0) # Constraint 2

i, j, k = Ints('i j k')
solver.add(Exists([i, j], And(solo_order[i] == 2, solo_order[j] == 1, i < j))) # Constraint 3
solver.add(Exists([i, j, k], And(solo_order[i] == 5, solo_order[j] == 1, solo_order[k] == 0, i < j, j < k))) # Constraint 4
solver.add(Exists([k], And(solo_order[k] == 3, Xor(Exists([i], And(solo_order[i] == 2, i < k)), Exists([j], And(solo_order[j] == 4, j < k)))))) # Constraint 5
solver.add(Exists([i, j], And(solo_order[i] == 2, solo_order[j] == 3, i < j))) # Constraint 6


# Answer choices
choice_A = (solo_order[0] == 2)
choice_B = (solo_order[1] == 2)
choice_C = Exists([i, j], And(solo_order[i] == 5, solo_order[j] == 3, i < j))
choice_D = Exists([i, j], And(solo_order[i] == 2, solo_order[j] == 4, i < j))
choice_E = Exists([i, j], And(solo_order[i] == 3, solo_order[j] == 1, i < j))

choices = [choice_A, choice_B, choice_C, choice_D, choice_E]
option_letters = ['A', 'B', 'C', 'D', 'E']

for i in range(len(choices)):
    solver.push()
    solver.add(Not(choices[i]))
    if solver.check() == unsat:
        print(f"Option {option_letters[i]} is correct")
        exit()
    solver.pop()