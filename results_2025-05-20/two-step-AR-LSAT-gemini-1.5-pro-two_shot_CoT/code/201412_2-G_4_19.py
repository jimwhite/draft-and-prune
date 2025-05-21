from z3 import *

# Variables
assigned = Array('assigned', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraint 1 (Domain)
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 0, i < 6), Or(assigned[i] == 0, assigned[i] == 1, assigned[i] == -1))))

# Constraint 2 (At least two at each university)
sum_silva = Sum([If(assigned[i] == 0, 1, 0) for i in range(6)])
sum_thorne = Sum([If(assigned[i] == 1, 1, 0) for i in range(6)])
solver.add(And(sum_silva >= 2, sum_thorne >= 2))

# Constraint 3 (Frost and Heideck together)
solver.add(And(assigned[0] != -1, assigned[0] == assigned[2]))

# Constraint 4 (Lai and Mays separate)
solver.add(Implies(And(assigned[4] != -1, assigned[5] != -1), assigned[4] != assigned[5]))

# Constraint 5 (Gonzalez at Silva implies Lai at Thorne)
solver.add(Implies(assigned[1] == 0, assigned[4] == 1))

# Constraint 6 (Knutson not at Thorne implies Heideck and Mays at Thorne)
solver.add(Implies(assigned[3] != 1, And(assigned[2] == 1, assigned[5] == 1)))

# Answer choices
options = [
    [0, 1, 2, 3],
    [0, 1, 2],
    [1, 3],
    [2, 4],
    [3, 5]
]

for option_index, option in enumerate(options):
    solver.push()
    for photographer in range(6):
        if photographer in option:
            solver.add(assigned[photographer] == 0)
        else:
            solver.add(assigned[photographer] != 0)
    if solver.check() == sat:
        print(f"Option {chr(65 + option_index)} is correct")
        exit()
    solver.pop()