from z3 import *

# Variables
bird_at_lecture = Array('bird_at_lecture', IntSort(), IntSort())
location_at_lecture = Array('location_at_lecture', IntSort(), IntSort())
lecture_of_bird = Array('lecture_of_bird', IntSort(), IntSort())

solver = Solver()

# Constraint 1 (Consistency and Uniqueness)
for i in range(1, 6):
    solver.add(And(bird_at_lecture[i] >= 0, bird_at_lecture[i] <= 4))
    solver.add(And(location_at_lecture[i] >= 0, location_at_lecture[i] <= 1))

for b in range(0, 5):
    solver.add(And(lecture_of_bird[b] >= 1, lecture_of_bird[b] <= 5))

solver.add(Distinct([bird_at_lecture[i] for i in range(1, 6)]))
solver.add(Distinct([lecture_of_bird[b] for b in range(0, 5)]))

for i in range(1, 6):
    solver.add(lecture_of_bird[bird_at_lecture[i]] == i)


# Constraint 2 (First Lecture Location)
solver.add(location_at_lecture[1] == 0)

# Constraint 3 (Fourth Lecture Location)
solver.add(location_at_lecture[4] == 1)

# Constraint 4 (Three Lectures in Gladwyn)
solver.add(Sum([If(location_at_lecture[i] == 0, 1, 0) for i in range(1, 6)]) == 3)

# Constraint 5 (Sandpipers in Howard)
solver.add(location_at_lecture[lecture_of_bird[3]] == 1)

# Constraint 6 (Sandpipers before Oystercatchers)
solver.add(lecture_of_bird[3] < lecture_of_bird[0])

# Constraint 7 (Terns before Petrels)
solver.add(lecture_of_bird[4] < lecture_of_bird[1])

# Constraint 8 (Petrels in Gladwyn)
solver.add(location_at_lecture[lecture_of_bird[1]] == 0)

# Check answer choices
choices = [
    (0, 0),  # Oystercatchers, Gladwyn
    (1, 1),  # Petrels, Howard
    (2, 1),  # Rails, Howard
    (3, 1),  # Sandpipers, Howard
    (4, 0)   # Terns, Gladwyn
]

for i, (bird, location) in enumerate(choices):
    solver.push()
    solver.add(bird_at_lecture[5] == bird)
    solver.add(location_at_lecture[5] == location)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()