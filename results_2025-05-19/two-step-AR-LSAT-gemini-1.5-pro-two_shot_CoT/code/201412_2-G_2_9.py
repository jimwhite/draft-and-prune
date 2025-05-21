from z3 import *

# Define variables
lecture_historian = Array('lecture_historian', IntSort(), IntSort())
historian_topic = Array('historian_topic', IntSort(), IntSort())

solver = Solver()

# Constraint 1: Distinct Lecture Historians
solver.add(Distinct([lecture_historian[i] for i in range(4)]))

# Constraint 2: Distinct Historian Topics
solver.add(Distinct([historian_topic[i] for i in range(4)]))

# Constraint 3: Oil and Watercolors before Lithographs
i = Int('i')
k = Int('k')
solver.add(Exists([i], And(historian_topic[lecture_historian[i]] == 1, ForAll([j], Implies(historian_topic[lecture_historian[j]] == 0, i < j)))))
solver.add(Exists([k], And(historian_topic[lecture_historian[k]] == 3, ForAll([l], Implies(historian_topic[lecture_historian[l]] == 0, k < l)))))


# Constraint 4: Farley before Oil Paintings
solver.add(Exists([i], And(lecture_historian[i] == 0, ForAll([j], Implies(historian_topic[lecture_historian[j]] == 1, i < j)))))

# Constraint 5: Holden before Garcia and Jiang
solver.add(ForAll([i], Implies(lecture_historian[i] == 2, ForAll([j], Implies(lecture_historian[j] == 1, i < j)))))
solver.add(ForAll([k], Implies(lecture_historian[k] == 2, ForAll([l], Implies(lecture_historian[l] == 3, k < l)))))


# Answer choices and their negations
answer_choices = [
    (historian_topic[0] != 0),  # Farley gives the lithographs lecture
    (historian_topic[1] != 2),  # Garcia gives the sculptures lecture
    (historian_topic[1] != 3),  # Garcia gives the watercolors lecture
    (historian_topic[2] != 1),  # Holden gives the oil paintings lecture
    (historian_topic[3] != 3)   # Jiang gives the watercolors lecture
]

for i in range(len(answer_choices)):
    solver.push()
    solver.add(answer_choices[i])
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
