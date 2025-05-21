from z3 import *

# Define variables
article_at_slot = Array('article_at_slot', IntSort(), StringSort())
solver = Solver()

# Constraint 0: Distinctness
solver.add(Distinct([article_at_slot[i] for i in range(1, 8)]))

# Constraint 1: Consecutive Topics
topics = {'F': ['G', 'H', 'J'], 'N': ['Q', 'R', 'S'], 'W': ['Y']}
for i in range(1, 7):
    solver.add(
        Or(
            And(article_at_slot[i] in topics['F'], article_at_slot[i + 1] in topics['N'] + topics['W']),
            And(article_at_slot[i] in topics['N'], article_at_slot[i + 1] in topics['F'] + topics['W']),
            And(article_at_slot[i] in topics['W'], article_at_slot[i + 1] in topics['F'] + topics['N'])
        )
    )

# Helper function to get the slot index of an article
def get_index(article):
    for i in range(1, 8):
        if solver.check(article_at_slot[i] == article) == sat:
            return i
    return -1  # Should not happen if constraints are correct

# Constraint 2: S before Q condition
solver.add(Implies(get_index('S') < get_index('Q'), get_index('Q') == 3))

# Constraint 3: S before Y
solver.add(get_index('S') < get_index('Y'))

# Constraint 4: J before G before R
solver.add(get_index('J') < get_index('G'))
solver.add(get_index('G') < get_index('R'))

# Constraint 5: Y is fourth
solver.add(article_at_slot[4] == 'Y')

# Check answer choices
answer_choices = [
    "J is second.",
    "J is third",
    "Q is first.",
    "Q is third",
    "R is seventh."
]
for i, choice in enumerate(answer_choices):
    solver.push()
    if choice == "J is second.":
        solver.add(article_at_slot[2] == 'J')
    elif choice == "J is third":
        solver.add(article_at_slot[3] == 'J')
    elif choice == "Q is first.":
        solver.add(article_at_slot[1] == 'Q')
    elif choice == "Q is third":
        solver.add(article_at_slot[3] == 'Q')
    elif choice == "R is seventh.":
        solver.add(article_at_slot[7] == 'R')

    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()