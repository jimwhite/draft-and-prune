from z3 import *

# Define variables
targets = Array('targets', IntSort(), IntSort(), IntSort())

# Create solver
solver = Solver()

# Constraint 1: Target Values
solver.add(ForAll([c, r], And(targets[c][r] >= 1, targets[c][r] <= 3)))

# Constraint 2: Website <= Voicemail
solver.add(ForAll([c], targets[c][0] <= targets[c][1]))

# Constraint 3: Image Voicemail < Others Voicemail
solver.add(And(targets[0][1] < targets[1][1], targets[0][1] < targets[2][1]))

# Constraint 4: Solide Website < Truvest Website
solver.add(targets[1][0] < targets[2][0])

# Constraint 5: No 3-day Voicemail
solver.add(And(targets[0][1] != 3, targets[1][1] != 3, targets[2][1] != 3))


# Check answer choices
answer_choices = [
    (0, 0, 1),  # A: Image's website target is 1 day
    (1, 0, 2),  # B: Solide's website target is 2 days
    (1, 1, 2),  # C: Solide's voicemail target is 2 days
    (2, 0, 2),  # D: Truvest's website target is 2 days
    (2, 1, 2)   # E: Truvest's voicemail target is 2 days
]

for i, (client, request_type, target_time) in enumerate(answer_choices):
    solver.push()
    solver.add(targets[client][request_type] != target_time)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
