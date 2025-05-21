from z3 import *

# Variables
historian_slot = Array('historian_slot', IntSort(), IntSort())
topic_slot = Array('topic_slot', IntSort(), IntSort())
historian_topic = Array('historian_topic', IntSort(), IntSort())

solver = Solver()

# Constraint 1: Domain Constraints
solver.add(And([And(historian_slot[i] >= 0, historian_slot[i] < 4) for i in range(4)]))
solver.add(And([And(topic_slot[i] >= 0, topic_slot[i] < 4) for i in range(4)]))
solver.add(And([And(historian_topic[i] >= 0, historian_topic[i] < 4) for i in range(4)]))

# Constraint 2: Uniqueness Constraints
solver.add(Distinct([historian_slot[i] for i in range(4)]))
solver.add(Distinct([topic_slot[i] for i in range(4)]))
solver.add(Distinct([historian_topic[i] for i in range(4)]))

# Constraint 3: Consistency Constraint
i = Int('i')
solver.add(ForAll(i, Implies(And(i >= 0, i < 4), topic_slot[historian_topic[i]] == historian_slot[i])))

# Constraint 4: Oil and Watercolors before Lithographs
solver.add(And(topic_slot[1] < topic_slot[0], topic_slot[3] < topic_slot[0]))

# Constraint 5: Farley before Oil Paintings
solver.add(historian_slot[0] < topic_slot[1])

# Constraint 6: Holden before Garcia and Jiang
solver.add(And(historian_slot[2] < historian_slot[1], historian_slot[2] < historian_slot[3]))

# Check answer choices
answer_choices = [
    (0, 0),  # Farley gives the lithographs lecture
    (1, 2),  # Garcia gives the sculptures lecture
    (1, 3),  # Garcia gives the watercolors lecture
    (2, 1),  # Holden gives the oil paintings lecture
    (3, 3)   # Jiang gives the watercolors lecture
]

for option_index, (historian, topic) in enumerate(answer_choices):
    solver.push()
    solver.add(historian_topic[historian] == topic)
    if solver.check() == unsat:
        print(f"Option {chr(65 + option_index)} is correct")
        exit()
    solver.pop()