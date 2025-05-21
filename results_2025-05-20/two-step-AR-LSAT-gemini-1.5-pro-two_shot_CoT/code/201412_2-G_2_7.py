from z3 import *

# Variables
historian_slot = Array('historian_slot', IntSort(), IntSort())
topic_slot = Array('topic_slot', IntSort(), IntSort())
i = Int('i')

# Solver
solver = Solver()

# Constraints
solver.add(Distinct([historian_slot[i] for i in range(4)]))
solver.add(Distinct([topic_slot[i] for i in range(4)]))
solver.add(ForAll(i, Implies(And(i >= 0, i <= 3), And(historian_slot[i] >= 0, historian_slot[i] <= 3))))
solver.add(ForAll(i, Implies(And(i >= 0, i <= 3), And(topic_slot[i] >= 0, topic_slot[i] <= 3))))
solver.add(And(topic_slot[1] < topic_slot[0], topic_slot[3] < topic_slot[0]))
solver.add(historian_slot[0] < topic_slot[1])
solver.add(And(historian_slot[2] < historian_slot[1], historian_slot[2] < historian_slot[3]))

# Answer choices
choices = [
    historian_slot[0] < topic_slot[2],  # A
    historian_slot[2] < topic_slot[0],  # B
    topic_slot[2] < historian_slot[1],  # C
    topic_slot[2] < historian_slot[3],  # D
    topic_slot[3] < historian_slot[1]   # E
]

# Check each choice
for i, choice in enumerate(choices):
    solver.push()
    solver.add(Not(choice))
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()