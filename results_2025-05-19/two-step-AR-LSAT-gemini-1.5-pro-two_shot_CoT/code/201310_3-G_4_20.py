from z3 import *

# Variables
lecture_bird = Array('lecture_bird', IntSort(), IntSort())
lecture_location = Array('lecture_location', IntSort(), IntSort())

solver = Solver()

# Bird Uniqueness
solver.add(Distinct([lecture_bird[i] for i in range(1, 6)]))

# Location Constraints
solver.add(lecture_location[1] == 0)  # First lecture in Gladwyn
solver.add(lecture_location[4] == 1)  # Fourth lecture in Howard
solver.add(Sum([If(lecture_location[i] == 0, 1, 0) for i in range(1, 6)]) == 3)  # 3 lectures in Gladwyn

# Bird Order and Location Constraints
solver.add(lecture_location[Sum([If(lecture_bird[j] == 3, 1, 0) for j in range(1, 6)])] == 1) # Sandpiper in Howard
solver.add(Sum([If(lecture_bird[j] == 3, 1, 0) for j in range(1, 6)]) < Sum([If(lecture_bird[j] == 0, 1, 0) for j in range(1, 6)])) # Sandpiper before Oystercatcher
solver.add(Sum([If(lecture_bird[j] == 4, 1, 0) for j in range(1, 6)]) < Sum([If(lecture_bird[j] == 1, 1, 0) for j in range(1, 6)])) # Tern before Petrel
solver.add(lecture_location[Sum([If(lecture_bird[j] == 1, 1, 0) for j in range(1, 6)])] == 0) # Petrel in Gladwyn


# Check answer choices
choices = [
    And(lecture_location[1] == 0, lecture_location[2] == 0),
    And(lecture_location[2] == 1, lecture_location[3] == 1),
    And(lecture_location[2] == 0, lecture_location[5] == 0),
    And(lecture_location[3] == 1, lecture_location[4] == 1),
    And(lecture_location[3] == 0, lecture_location[5] == 0)
]

for i, choice in enumerate(choices):
    solver.push()
    solver.add(choice)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()