from z3 import *

# Variables
made = [[[Bool('made_%i_%i_%i' % (d, c, b)) for b in range(3)] for c in range(3)] for d in range(5)]

# Constraints
solver = Solver()
# Constraint 1: Each batch exactly once per week
for c in range(3):
    for b in range(3):
        solver.add(Sum([If(made[d][c][b], 1, 0) for d in range(5)]) == 1)

# Constraint 2: No two batches of same kind on same day
for d in range(5):
    for c in range(3):
        solver.add(Sum([If(made[d][c][b], 1, 0) for b in range(3)]) <= 1)

# Constraint 3: At least one batch on Monday
solver.add(Sum([If(made[0][c][b], 1, 0) for c in range(3) for b in range(3)]) >= 1)

# Constraint 4: Oatmeal 2nd and Peanut Butter 1st on same day
for d in range(5):
    solver.add(made[d][0][1] == made[d][1][0])

# Constraint 5: Sugar 2nd on Thursday
solver.add(made[3][2][1] == True)

# Answering the question
possible_days_count = 0
for d in range(5):
    temp_solver = Solver()
    temp_solver.add(solver.assertions())
    batches_on_day_d = Sum([If(made[d][c][b], 1, 0) for c in range(3) for b in range(3)])
    temp_solver.add(batches_on_day_d <= 2)
    if temp_solver.check() == sat:
        possible_days_count += 1

answer_choices = ["one", "two", "three", "four", "five"]
print(f"Option {chr(65 + answer_choices.index(answer_choices[possible_days_count -1]))} is correct")