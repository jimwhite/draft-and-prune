from z3 import *

# Define variables
bird = [Int('bird_%i' % i) for i in range(1, 6)]
location = [Int('location_%i' % i) for i in range(1, 6)]
solver = Solver()

# Bird Mappings: O=0, P=1, R=2, S=3, T=4
# Location Mappings: G=0, H=1

# Constraint 1: Distinct Birds
solver.add(Distinct(bird))

# Constraint 2: First Lecture Location
solver.add(location[0] == 0)

# Constraint 3: Fourth Lecture Location
solver.add(location[3] == 1)

# Constraint 4: Three Lectures in Gladwyn
solver.add(Sum([If(location[i] == 0, 1, 0) for i in range(5)]) == 3)

# Constraint 5: Sandpipers in Howard
# Use Implies to constrain the location based on the sandpiper lecture index
for i in range(5):
    solver.add(Implies(bird[i] == 3, location[i] == 1))


# Constraint 6: Sandpipers before Oystercatchers
for i in range(5):
    for j in range(5):
        solver.add(Implies(And(bird[i] == 3, bird[j] == 0), i < j))

# Constraint 7: Terns before Petrels
for i in range(5):
    for j in range(5):
        solver.add(Implies(And(bird[i] == 4, bird[j] == 1), i < j))

# Constraint 8: Petrels in Gladwyn
for i in range(5):
    solver.add(Implies(bird[i] == 1, location[i] == 0))

# Constraint 9: Third lecture is on Sandpipers
solver.add(bird[2] == 3)

# Check answer choices
options = [
    ([bird[1] == 0, location[1] == 0], "A"),  # Second lecture: Oystercatchers in Gladwyn
    ([bird[4] == 0, location[4] == 1], "B"),  # Fifth lecture: Oystercatchers in Howard
    ([bird[1] == 2, location[1] == 1], "C"),  # Second lecture: Rails in Howard
    ([bird[1] == 4, location[1] == 0], "D"),  # Second lecture: Terns in Gladwyn
    ([bird[3] == 4, location[3] == 1], "E")   # Fourth lecture: Terns in Howard
]

for option, letter in options:
    solver.push()
    solver.add(option)
    if solver.check() == sat:
        print(f"Option {letter} is correct")
        exit()
    solver.pop()
