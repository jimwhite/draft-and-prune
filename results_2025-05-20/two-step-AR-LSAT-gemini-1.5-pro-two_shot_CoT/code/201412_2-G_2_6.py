from z3 import *

# Define variables
lecture_topic = Array('lecture_topic', IntSort(), IntSort())
lecture_historian = Array('lecture_historian', IntSort(), IntSort())

solver = Solver()

# Constraint 1: Distinct Topics
solver.add(Distinct([lecture_topic[i] for i in range(4)]))

# Constraint 2: Distinct Historians
solver.add(Distinct([lecture_historian[i] for i in range(4)]))

# Constraint 3: Oil and Watercolors before Lithographs
i = Int('i')
j = Int('j')
k = Int('k')
solver.add(ForAll([i, j, k], Implies(And(lecture_topic[i] == 1, lecture_topic[j] == 3, lecture_topic[k] == 0, 0 <= i, i < 4, 0 <= j, j < 4, 0 <= k, k < 4), And(i < k, j < k))))


# Constraint 4: Farley before Oil Paintings
i = Int('i')
j = Int('j')
solver.add(ForAll([i, j], Implies(And(lecture_historian[i] == 0, lecture_topic[j] == 1, 0 <= i, i < 4, 0 <= j, j < 4), i < j)))

# Constraint 5: Holden before Garcia and Jiang
i = Int('i')
j = Int('j')
k = Int('k')
solver.add(ForAll([i, j, k], Implies(And(lecture_historian[i] == 2, lecture_historian[j] == 1, lecture_historian[k] == 3, 0 <= i, i < 4, 0 <= j, j < 4, 0 <= k, k < 4), And(i < j, i < k))))

# Answer choices
choices = [
    [(0, 2), (2, 0), (1, 1), (3, 3)],  # A
    [(0, 3), (3, 1), (2, 2), (1, 0)],  # B
    [(1, 2), (0, 3), (2, 1), (3, 0)],  # C
    [(2, 1), (3, 3), (0, 0), (1, 2)],  # D
    [(2, 2), (0, 3), (3, 1), (1, 0)]   # E
]

for choice_index, choice in enumerate(choices):
    solver.push()
    for historian, topic in choice:
        solver.add(lecture_historian[choice.index((historian, topic))] == historian)
        solver.add(lecture_topic[choice.index((historian, topic))] == topic)

    if solver.check() == sat:
        print(f"Option {chr(65 + choice_index)} is correct")
        exit()
    solver.pop()