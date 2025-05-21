from z3 import *

# Define variables
birds = {'O': 0, 'P': 1, 'R': 2, 'S': 3, 'T': 4}
locations = {'G': 0, 'H': 1}
lecture_bird = Array('lecture_bird', IntSort(), IntSort())
lecture_location = Array('lecture_location', IntSort(), IntSort())

solver = Solver()

# Constraint 1: Bird Uniqueness
solver.add(Distinct([lecture_bird[i] for i in range(1, 6)]))

# Constraint 2: First Lecture Location
solver.add(lecture_location[1] == locations['G'])

# Constraint 3: Fourth Lecture Location
solver.add(lecture_location[4] == locations['H'])

# Constraint 4: Gladwyn Count
solver.add(Sum([If(lecture_location[i] == locations['G'], 1, 0) for i in range(1, 6)]) == 3)

# Constraint 5: Sandpipers Location and before Oystercatchers
# Use implications instead of ArrayRef.index which doesn't exist
for i in range(1, 6):
    solver.add(Implies(lecture_bird[i] == birds['S'], lecture_location[i] == locations['H']))
    for j in range(1, 6):
        solver.add(Implies(And(lecture_bird[i] == birds['S'], lecture_bird[j] == birds['O']), i < j))


# Constraint 6: Terns before Petrels and Petrels in Gladwyn
for i in range(1, 6):
    for j in range(1, 6):
        solver.add(Implies(And(lecture_bird[i] == birds['T'], lecture_bird[j] == birds['P']), i < j))
    solver.add(Implies(lecture_bird[i] == birds['P'], lecture_location[i] == locations['G']))

# Constraint 7: Terns Location - Howard Auditorium
for i in range(1, 6):
    solver.add(Implies(lecture_bird[i] == birds['T'], lecture_location[i] == locations['H']))


# Check answer choices
answer_choices = [
    ("O", "G"),  # A
    ("R", "H"),  # B
    ("R", "G"),  # C
    ("S", "H"),  # D
    ("T", "H")   # E
]

for i, (bird, location) in enumerate(answer_choices):
    solver.push()
    solver.add(lecture_bird[3] == birds[bird])
    solver.add(lecture_location[3] == locations[location])
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
