from z3 import *

# Define variables
lecture_historian = Array('lecture_historian', IntSort(), IntSort())
historian_topic = Array('historian_topic', IntSort(), IntSort())

# Farley (F=0), Garcia (G=1), Holden (H=2), Jiang (J=3)
# Lithographs (L=0), Oil Paintings (O=1), Sculptures (S=2), Watercolors (W=3)

solver = Solver()

# Constraint 1: Distinct Lecture Historians
solver.add(Distinct([lecture_historian[i] for i in range(4)]))

# Constraint 2: Distinct Historian Topics
solver.add(Distinct([historian_topic[i] for i in range(4)]))

# Constraint 3: Oil and Watercolors before Lithographs
solver.add(Sum([If(historian_topic[lecture_historian[i]] == 1, 1, 0) for i in range(4)]) < Sum([If(historian_topic[lecture_historian[i]] == 0, 1, 0) for i in range(4)]))
solver.add(Sum([If(historian_topic[lecture_historian[i]] == 3, 1, 0) for i in range(4)]) < Sum([If(historian_topic[lecture_historian[i]] == 0, 1, 0) for i in range(4)]))


# Constraint 4: Farley before Oil Paintings
solver.add(Sum([If(lecture_historian[i] == 0, i, 4) for i in range(4)]) < Sum([If(historian_topic[lecture_historian[i]] == 1, i, 4) for i in range(4)]))

# Constraint 5: Holden before Garcia and Jiang
solver.add(Sum([If(lecture_historian[i] == 2, i, 4) for i in range(4)]) < Sum([If(lecture_historian[i] == 1, i, 4) for i in range(4)]))
solver.add(Sum([If(lecture_historian[i] == 2, i, 4) for i in range(4)]) < Sum([If(lecture_historian[i] == 3, i, 4) for i in range(4)]))

# Constraint 6: Garcia gives Sculptures lecture
solver.add(historian_topic[1] == 2)

# Answer choices
options = [
    "historian_topic[lecture_historian[2]] == 0",  # A. Lithographs lecture is third
    "historian_topic[lecture_historian[2]] == 1",  # B. Oil paintings lecture is third
    "historian_topic[lecture_historian[0]] == 2",  # C. Sculptures lecture is first
    "historian_topic[lecture_historian[1]] == 2",  # D. Sculptures lecture is second
    "historian_topic[lecture_historian[1]] == 3",  # E. Watercolors lecture is second
]

for i in range(len(options)):
    solver.push()
    solver.add(eval(options[i]))
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()