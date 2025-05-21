from z3 import *

# Variables
schedule = Array('schedule', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
# Constraint 0 (Domain)
i = Int('i')  # Define i
solver.add(ForAll([i], Implies(And(i >= 0, i < 7), And(schedule[i] >= 0, schedule[i] < 7))))

# Constraint 1 (Distinctness)
solver.add(Distinct([schedule[i] for i in range(7)]))

# Constraint 2 (J in Evening)
solver.add(Or(schedule[5] == 0, schedule[6] == 0))

# Constraint 3 (K not in Morning)
solver.add(And(schedule[0] != 1, schedule[1] != 1))

# Constraint 4 (L after K)
k = Int('k')
l = Int('l')
solver.add(ForAll([k, l], Implies(And(k >= 0, k < 7, l >= 0, l < 7, schedule[k] == 1, schedule[l] == 2), k < l)))

# Constraint 5 (L before M)
l = Int('l')
m = Int('m')
solver.add(ForAll([l, m], Implies(And(l >= 0, l < 7, m >= 0, m < 7, schedule[l] == 2, schedule[m] == 3), l < m)))


# Answer Choices
options = [
    Not(Or(schedule[5] == 1, schedule[6] == 1)),  # A
    Not(Or(schedule[2] == 2, schedule[3] == 2, schedule[4] == 2)),  # B
    Not(Or(schedule[5] == 2, schedule[6] == 2)),  # C
    Not(Or(schedule[0] == 3, schedule[1] == 3)),  # D
    Not(Or(schedule[2] == 3, schedule[3] == 3, schedule[4] == 3))   # E
]

for i in range(len(options)):
    solver.push()
    solver.add(options[i])
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
