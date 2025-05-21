from z3 import *

# Define variables
bird_lecture = Array('bird_lecture', IntSort(), IntSort())
location_lecture = Array('location_lecture', IntSort(), IntSort())
i = Int('i')
j = Int('j')

# Create solver
solver = Solver()

# Bird Mappings: O=0, P=1, R=2, S=3, T=4
# Location Mappings: G=0, H=1

# Constraint 1: Bird Uniqueness
solver.add(Distinct([bird_lecture[i] for i in range(1, 6)]))

# Constraint 2: Location Domain
solver.add(ForAll(i, Implies(And(i >= 1, i <= 5), Or(location_lecture[i] == 0, location_lecture[i] == 1))))

# Constraint 3: First Lecture in Gladwyn
solver.add(location_lecture[1] == 0)

# Constraint 4: Fourth Lecture in Howard
solver.add(location_lecture[4] == 1)

# Constraint 5: Three lectures in Gladwyn
solver.add(Sum([If(location_lecture[i] == 0, 1, 0) for i in range(1, 6)]) == 3)

# Constraint 6: Sandpiper in Howard
solver.add(ForAll(i, Implies(And(i >= 1, i <= 5, bird_lecture[i] == 3), location_lecture[i] == 1)))

# Constraint 7: Sandpiper before Oystercatcher
solver.add(Exists(i, Exists(j, And(i >= 1, i <= 5, j >= 1, j <= 5, bird_lecture[i] == 3, bird_lecture[j] == 0, i < j))))

# Constraint 8: Tern before Petrel
solver.add(Exists(i, Exists(j, And(i >= 1, i <= 5, j >= 1, j <= 5, bird_lecture[i] == 4, bird_lecture[j] == 1, i < j))))

# Constraint 9: Petrel in Gladwyn
solver.add(ForAll(i, Implies(And(i >= 1, i <= 5, bird_lecture[i] == 1), location_lecture[i] == 0)))

# Constraint 10: Third lecture is on Sandpipers
solver.add(bird_lecture[3] == 3)

# Derived Location Constraints
solver.add(location_lecture[3] == 1)
solver.add(location_lecture[2] == 0)
solver.add(location_lecture[5] == 0)


# Check answer choices
choices = [
    ([bird_lecture[2] == 0, location_lecture[2] == 0], 'A'),  # Oystercatchers in Gladwyn (2nd lecture)
    ([bird_lecture[5] == 0, location_lecture[5] == 0], 'B'),  # Oystercatchers in Howard (5th lecture) - Corrected location
    ([bird_lecture[2] == 2, location_lecture[2] == 0], 'C'),  # Rails in Howard (2nd lecture) - Corrected location
    ([bird_lecture[2] == 4, location_lecture[2] == 0], 'D'),  # Terns in Gladwyn (2nd lecture)
    ([bird_lecture[4] == 4, location_lecture[4] == 1], 'E')   # Terns in Howard (4th lecture)
]

for choice, option in choices:
    solver.push()
    solver.add(choice)
    if solver.check() == sat:
        print(f"Option {option} is correct")
        exit()
    solver.pop()