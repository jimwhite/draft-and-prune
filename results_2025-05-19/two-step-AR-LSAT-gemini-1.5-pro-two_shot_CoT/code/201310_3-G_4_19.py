from z3 import *

# Variables
bird_at_slot = Array('bird_at_slot', IntSort(), IntSort())
location_at_slot = Array('location_at_slot', IntSort(), IntSort())
solver = Solver()

# Bird Mappings: oystercatchers (0), petrels (1), rails (2), sandpipers (3), terns (4)
# Location Mappings: Gladwyn Hall (0), Howard Auditorium (1)

# Constraint 1: Distinct Birds
solver.add(Distinct([bird_at_slot[i] for i in range(5)]))

# Constraint 2: First Lecture Location
solver.add(location_at_slot[0] == 0)

# Constraint 3: Fourth Lecture Location
solver.add(location_at_slot[3] == 1)

# Constraint 4: Gladwyn Count
solver.add(Sum([If(location_at_slot[i] == 0, 1, 0) for i in range(5)]) == 3)

# Constraint 5: Sandpipers Location
# Corrected: Use a quantifier with a bound variable
i = Int('i') # Declare i
solver.add(Exists([i], And(bird_at_slot[i] == 3, location_at_slot[i] == 1)))

# Constraint 6: Sandpipers before Oystercatchers
i = Int('i')
j = Int('j') # Declare j
solver.add(Exists([i, j], And(bird_at_slot[i] == 3, bird_at_slot[j] == 0, i < j)))

# Constraint 7: Terns before Petrels
i = Int('i')
j = Int('j') # Declare j
solver.add(Exists([i, j], And(bird_at_slot[i] == 4, bird_at_slot[j] == 1, i < j)))

# Constraint 8: Petrels Location
i = Int('i') # Declare i
solver.add(Exists([i], And(bird_at_slot[i] == 1, location_at_slot[i] == 0)))


# Answer Choices
choices = [
    [0, 1, 2, 3, 4],  # A
    [1, 3, 0, 4, 2],  # B
    [2, 3, 4, 1, 0],  # C
    [3, 4, 0, 2, 1],  # D
    [4, 1, 3, 0, 2]   # E
]

for i, choice in enumerate(choices):
    solver.push()
    for j in range(5):
        solver.add(bird_at_slot[j] == choice[j])
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()

