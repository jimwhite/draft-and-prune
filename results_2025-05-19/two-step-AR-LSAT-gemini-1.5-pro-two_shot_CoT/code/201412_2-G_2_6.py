from z3 import *

# Entities (as integers)
F = 0
G = 1
H = 2
J = 3
L = 0
O = 1
S = 2
W = 3

# Variables
lecture_historian = Array('lecture_historian', IntSort(), IntSort())
lecture_topic = Array('lecture_topic', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraint 1: Distinct Historians per Slot
solver.add(Distinct([lecture_historian[i] for i in range(4)]))

# Constraint 2: Distinct Topics per Slot
solver.add(Distinct([lecture_topic[i] for i in range(4)]))

# Constraint 3: Oil and Watercolors before Lithographs
i = Int('i')
j = Int('j')
solver.add(ForAll([i], Implies(lecture_topic[i] == L, And(Exists([j], And(lecture_topic[j] == O, j < i)), Exists([j], And(lecture_topic[j] == W, j < i))))) # Fixed missing parenthesis and corrected logic

# Constraint 4: Farley before Oil Paintings
solver.add(ForAll([i], Implies(lecture_topic[i] == O, Exists([j], And(lecture_historian[j] == F, j < i)))))

# Constraint 5: Holden before Garcia and Jiang
solver.add(ForAll([i], Implies(lecture_historian[i] == G, Exists([j], And(lecture_historian[j] == H, j < i)))))
solver.add(ForAll([i], Implies(lecture_historian[i] == J, Exists([j], And(lecture_historian[j] == H, j < i)))))


# Answer Choices
choices = [
    [(F, S), (H, L), (G, O), (J, W)],
    [(F, W), (J, O), (H, S), (G, L)],
    [(G, S), (F, W), (H, O), (J, L)],
    [(H, O), (J, W), (F, L), (G, S)],
    [(H, S), (F, W), (J, O), (G, L)]
]

# Check each answer choice
for idx, choice in enumerate(choices):
    solver.push()
    for i, (historian, topic) in enumerate(choice):
        solver.add(lecture_historian[i] == historian)
        solver.add(lecture_topic[i] == topic)
    if solver.check() == sat:
        print(f"Option {chr(65 + idx)} is correct")
        exit()
    solver.pop()
