from z3 import *

# Define variables
target_days = [[Int("target_days_%s_%s" % (c, r)) for r in range(2)] for c in range(3)]

solver = Solver()

# Constraint 1: Domain of Target Days
for c in range(3):
    for r in range(2):
        solver.add(And(target_days[c][r] >= 1, target_days[c][r] <= 3))

# Constraint 2: Website Target <= Voicemail Target
for c in range(3):
    solver.add(target_days[c][0] <= target_days[c][1])

# Constraint 3: Image Voicemail < Other Voicemails
solver.add(target_days[0][1] < target_days[1][1])
solver.add(target_days[0][1] < target_days[2][1])

# Constraint 4: Solide Website < Truvest Website
solver.add(target_days[1][0] < target_days[2][0])

# Constraint 5: No Voicemail Target is 3
for c in range(3):
    solver.add(target_days[c][1] != 3)

# Check answer choices
answer_choices = [
    (0, 0, 1),  # Image's website target is 1 day.
    (1, 0, 2),  # Solide's website target is 2 days.
    (1, 1, 2),  # Solide's voicemail target is 2 days.
    (2, 0, 2),  # Truvest's website target is 2 days.
    (2, 1, 2)   # Truvest's voicemail target is 2 days.
]

for i, (c, r, days) in enumerate(answer_choices):
    solver.push()
    solver.add(target_days[c][r] != days)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()