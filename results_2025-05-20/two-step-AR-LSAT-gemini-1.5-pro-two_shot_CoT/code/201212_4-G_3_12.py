from z3 import *

# Define variables
target_days = [[Int(f"target_days[{c}][{r}]") for r in range(2)] for c in range(3)]

# Create solver
solver = Solver()

# Clients: Image (0), Solide (1), Truvest (2)
# Request Types: Website (0), Voicemail (1)

# Constraint 1: Domain of target_days
for c in range(3):
    for r in range(2):
        solver.add(And(target_days[c][r] >= 1, target_days[c][r] <= 3))

# Constraint 2: Website target not longer than voicemail target
for c in range(3):
    solver.add(target_days[c][0] <= target_days[c][1])

# Constraint 3: Image's voicemail target shorter than others
solver.add(And(target_days[0][1] < target_days[1][1], target_days[0][1] < target_days[2][1]))

# Constraint 4: Solide's website target shorter than Truvest's
solver.add(target_days[1][0] < target_days[2][0])

# Constraint 5: Truvest's website target shorter than voicemail target
solver.add(target_days[2][0] < target_days[2][1])

# Answer choices and their negations
answer_choices = [
    target_days[0][1] == 2,  # A
    target_days[0][0] == 2,  # B
    target_days[0][0] == 1,  # C
    target_days[1][0] == 2,  # D
    target_days[1][0] == 1   # E
]

for i in range(len(answer_choices)):
    solver.push()
    solver.add(Not(answer_choices[i]))
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
