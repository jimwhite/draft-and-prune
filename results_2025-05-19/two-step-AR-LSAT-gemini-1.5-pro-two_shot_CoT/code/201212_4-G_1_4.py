from z3 import *

# Variables
schedule = Array('schedule', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 0, i <= 6), And(schedule[i] >= 0, schedule[i] <= 6)))) # Constraint 0
solver.add(Distinct([schedule[i] for i in range(7)])) # Constraint 1
solver.add(Or(schedule[5] == 0, schedule[6] == 0)) # Constraint 2
solver.add(Not(Or(schedule[0] == 1, schedule[1] == 1))) # Constraint 3
i = Int('i')
j = Int('j')
k = Int('k')
solver.add(Exists([i, j, k], And(schedule[i] == 1, schedule[j] == 2, schedule[k] == 3, i < j, j < k, And(i >=0, i <=6, j>=0, j<=6, k>=0, k<=6)))) # Constraint 4


# Answer choices
choices = [
    # Removed strings from the tuples, only Z3 expressions are needed
    Exists([i, j], And(schedule[i] == 0, schedule[j] == 1, i < j, And(i >=0, i <=6, j>=0, j<=6))),
    Exists([i, j], And(schedule[i] == 0, schedule[j] == 2, i < j, And(i >=0, i <=6, j>=0, j<=6))),
    Exists([i, j], And(schedule[i] == 0, schedule[j] == 6, i < j, And(i >=0, i <=6, j>=0, j<=6))),
    Exists([i, j, k], And(schedule[i] == 3, schedule[j] == 4, schedule[k] == 5, i < j, i < k, And(i >=0, i <=6, j>=0, j<=6, k>=0, k<=6))),
    Exists([i, j, k], And(schedule[i] == 1, schedule[j] == 4, schedule[k] == 6, i < j, i < k, And(i >=0, i <=6, j>=0, j<=6, k>=0, k<=6)))
]

for option, constraint in zip(["A", "B", "C", "D", "E"], choices):
    solver.push()
    solver.add(constraint)
    if solver.check() == sat:
        print(f"Option {option} is correct")
        exit()
    solver.pop()
