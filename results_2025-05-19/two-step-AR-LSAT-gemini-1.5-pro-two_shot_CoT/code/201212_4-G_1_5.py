from z3 import *

# Variables
schedule = Array('schedule', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
i = Int('i')
k = Int('k')
l = Int('l')
m = Int('m')

solver.add(ForAll([i], And(schedule[i] >= 0, schedule[i] <= 6))) # Constraint 0
solver.add(Distinct([schedule[i] for i in range(7)])) # Constraint 1
solver.add(Or(schedule[5] == 0, schedule[6] == 0)) # Constraint 2
solver.add(Not(Or(schedule[0] == 1, schedule[1] == 1))) # Constraint 3
solver.add(ForAll([k, l, m], Implies(And(schedule[k] == 1, schedule[l] == 2, schedule[m] == 3), And(k < l, l < m)))) # Constraint 4
solver.add(Or(schedule[2] == 6, schedule[3] == 6, schedule[4] == 6)) # Constraint 5


# Answer choices
options = [
    Not(schedule[6] == 0), # J is shown seventh
    Not(schedule[2] == 1), # K is shown third
    Not(schedule[0] == 4), # N is shown first
    Not(Or(schedule[2] == 3, schedule[3] == 3, schedule[4] == 3)), # M is shown in the afternoon
    Not(Or(schedule[0] == 5, schedule[1] == 5)) # O is shown in the morning
]

for i in range(len(options)):
    solver.push()
    solver.add(options[i])
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()