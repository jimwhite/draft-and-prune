from z3 import *

# Define constants for historians, topics, and time slots
F = 0
G = 1
H = 2
J = 3
L = 0
O = 1
S = 2
W = 3

# Define Z3 variables
lecture_time = Array('lecture_time', IntSort(), IntSort())
historian_topic = Array('historian_topic', IntSort(), IntSort())

# Create a Z3 solver
solver = Solver()

# Constraint 1: Time Slot Uniqueness
solver.add(Distinct([lecture_time[i] for i in range(4)]))

# Constraint 2: Topic Uniqueness
solver.add(Distinct([historian_topic[i] for i in range(4)]))

# Constraint 3: Oil and Watercolors before Lithographs
solver.add(lecture_time[O] < lecture_time[L])
solver.add(lecture_time[W] < lecture_time[L])

# Constraint 4: Farley before Oil Paintings
solver.add(lecture_time[historian_topic[F]] < lecture_time[O])

# Constraint 5: Holden before Garcia and Jiang
solver.add(lecture_time[historian_topic[H]] < lecture_time[historian_topic[G]])
solver.add(lecture_time[historian_topic[H]] < lecture_time[historian_topic[J]])

# Constraint 6: Watercolors is third
solver.add(lecture_time[W] == 3)

# Constraint 7: Time Slots are 1, 2, 3, 4
solver.add(And([And(lecture_time[i] > 0, lecture_time[i] < 5) for i in range(4)]))


# Check answer choices
answer_choices = [
    (F, W),  # A: Farley gives the watercolors lecture
    (G, O),  # B: Garcia gives the oil paintings lecture
    (G, S),  # C: Garcia gives the sculptures lecture
    (H, S),  # D: Holden gives the sculptures lecture
    (J, L)   # E: Jiang gives the lithographs lecture
]

for i, (historian, topic) in enumerate(answer_choices):
    solver.push()
    solver.add(historian_topic[historian] == topic)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()