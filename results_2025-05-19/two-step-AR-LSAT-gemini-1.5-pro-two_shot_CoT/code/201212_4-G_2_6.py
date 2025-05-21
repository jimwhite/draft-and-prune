from z3 import *

# Variables
schedule = Array('schedule', IntSort(), IntSort())
solver = Solver()

# Witness IDs: F=0, G=1, H=2, I=3, J=4
# Day IDs: M=0, T=1, W=2

# Constraints
w = Int('w')
solver.add(ForAll([w], And(schedule[w] >= 0, schedule[w] <= 2))) # Constraint 1: Domain
solver.add(Distinct([schedule[0], schedule[1], schedule[2], schedule[3], schedule[4]])) # Constraint 2: One day per witness
solver.add(schedule[0] != schedule[1]) # Constraint 3: Franco != Garcia
solver.add(schedule[3] == 2) # Constraint 4: Iturbe on Wednesday
solver.add(Sum([If(schedule[w] == 1, 1, 0) for w in range(5)]) == 2) # Constraint 5: Two on Tuesday
solver.add(schedule[2] != 0) # Constraint 6: Hong not on Monday
solver.add(Sum([If(schedule[w] == 0, 1, 0) for w in range(5)]) >= 1) # Constraint 7: At least one on Monday


# Answer choices
choices = [
    [0, 2, 3, 1, 4],  # A: M:F, T:H,I, W:G,J. Index represents witness, value represents day.
    [0, 2, 3, 4, 1],  # B
    [1, 0, 3, 2, 4],  # C
    [1, 4, 0, 2, 3],  # D
    [1, 4, 2, 0, 3]   # E
]

for i, choice in enumerate(choices):
    solver.push()
    for j in range(5):
        solver.add(schedule[j] == choice[j] // 2)  # Add constraints for the current choice. Integer division to map witness to day ID.
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()