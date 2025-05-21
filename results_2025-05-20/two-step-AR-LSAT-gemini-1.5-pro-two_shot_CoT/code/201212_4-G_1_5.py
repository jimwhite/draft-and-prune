from z3 import *

# Variables
schedule = Array('schedule', IntSort(), IntSort())
pos_K, pos_L, pos_M = Ints('pos_K pos_L pos_M')

# Solver
solver = Solver()

# Constraints
solver.add(And([And(schedule[i] >= 0, schedule[i] <= 6) for i in range(7)])) # Constraint 0
solver.add(Distinct([schedule[i] for i in range(7)])) # Constraint 1
solver.add(Or(schedule[5] == 0, schedule[6] == 0)) # Constraint 2
solver.add(And(schedule[0] != 1, schedule[1] != 1)) # Constraint 3
solver.add(pos_K < pos_L) # Constraint 4
solver.add(pos_L < pos_M) # Constraint 5
solver.add(Or(schedule[2] == 6, schedule[3] == 6, schedule[4] == 6)) # Constraint 6
solver.add(schedule[pos_K] == 1) # Constraint 7
solver.add(schedule[pos_L] == 2) # Constraint 8
solver.add(schedule[pos_M] == 3) # Constraint 9
solver.add(And(pos_K >= 0, pos_K <= 6)) # Constraint 10
solver.add(And(pos_L >= 0, pos_L <= 6)) # Constraint 11
solver.add(And(pos_M >= 0, pos_M <= 6)) # Constraint 12


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