from z3 import *

# Define variables
birds = [Int('bird_%i' % i) for i in range(5)]  # 0:O, 1:P, 2:R, 3:S, 4:T
locations = Array('location', IntSort(), IntSort()) # 0:G, 1:H

solver = Solver()

# Constraint 0: Bird uniqueness
solver.add(Distinct(birds))
for i in range(5):
    solver.add(And(birds[i] >= 1, birds[i] <= 5))

# Constraint 1: First lecture in Gladwyn
solver.add(locations[1] == 0)

# Constraint 2: Fourth lecture in Howard
solver.add(locations[4] == 1)

# Constraint 3: Three lectures in Gladwyn
solver.add(Sum([If(locations[i] == 0, 1, 0) for i in range(1, 6)]) == 3)

# Helper function to get lecture number from bird
def get_lecture(bird_index):
    for i in range(1, 6):
        solver.push()
        solver.add(birds[bird_index] == i)
        if solver.check() == sat:
            solver.pop()
            return i
        solver.pop()
    return -1 # Should not reach here


# Constraint 4: Sandpiper in Howard
solver.add(locations[get_lecture(3)] == 1)

# Constraint 5: Sandpiper before Oystercatcher
solver.add(get_lecture(3) < get_lecture(0))

# Constraint 6: Tern before Petrel
solver.add(get_lecture(4) < get_lecture(1))

# Constraint 7: Petrel in Gladwyn
solver.add(locations[get_lecture(1)] == 0)

# Check answer choices
choices = [
    [locations[2] == 0],  # A
    [locations[2] == 1, locations[3] == 1],  # B
    [locations[2] == 0, locations[5] == 0],  # C
    [locations[3] == 1],  # D
    [locations[3] == 0, locations[5] == 0]   # E
]

for i, choice in enumerate(choices):
    solver.push()
    solver.add(choice)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()