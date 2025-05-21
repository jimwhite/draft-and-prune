from z3 import *

# Variables
schedule = Array('schedule', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
c = Int('c')
b = Int('b')
b1 = Int('b1')
b2 = Int('b2')

solver.add(ForAll([c, b], And(0 <= schedule[c * 3 + b], schedule[c * 3 + b] <= 4))) # Constraint 1: Domain, flattened array access

solver.add(ForAll([c, b1, b2], Implies(b1 != b2, schedule[c * 3 + b1] != schedule[c * 3 + b2]))) # Constraint 2: No two batches of same kind on same day, flattened array access

solver.add(Or(schedule[0] == 0, schedule[1] == 0, schedule[2] == 0, 
             schedule[3] == 0, schedule[4] == 0, schedule[5] == 0,
             schedule[6] == 0, schedule[7] == 0, schedule[8] == 0)) # Constraint 3: At least one batch on Monday, flattened array access

solver.add(schedule[1] == schedule[3]) # Constraint 4: Oatmeal 2nd and Peanut Butter 1st on same day, flattened array access

solver.add(schedule[7] == 3) # Constraint 5: Sugar 2nd on Thursday, flattened array access


# Answer Choices
choices = [
    [[0, 2, 3], [2, 3, 4], [0, 3, 4]],  # A
    [[0, 1, 3], [1, 2, 3], [0, 2, 3]],  # B
    [[1, 2, 3], [2, 3, 4], [1, 3, 4]],  # C
    [[0, 1, 3], [0, 2, 3], [0, 3, 4]],  # D
    [[0, 3, 4], [1, 2, 3], [0, 3, 4]]   # E
]

for i, choice in enumerate(choices):
    solver.push()
    for c_idx, days in enumerate(choice):
        for b_idx, day in enumerate(days):
            solver.add(schedule[c_idx * 3 + b_idx] == day) # Direct assignment, flattened array access
    
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
