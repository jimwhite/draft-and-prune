from z3 import *

# Variables
article_at_slot = Array('article_at_slot', IntSort(), IntSort())
i = Int('i')
j = Int('j')
k = Int('k')

# Solver
solver = Solver()

# Constraints
solver.add(ForAll([i], Implies(And(i >= 1, i <= 7), And(article_at_slot[i] >= 0, article_at_slot[i] <= 6)))) # Constraint 0
solver.add(Distinct([article_at_slot[i] for i in range(1, 8)])) # Constraint 1
solver.add(ForAll([i], Implies(And(i >= 1, i <= 6),
    Or(
        And(article_at_slot[i] < 3, article_at_slot[i+1] < 3),
        And(article_at_slot[i] > 2, article_at_slot[i] < 6, article_at_slot[i+1] > 2, article_at_slot[i+1] < 6),
        And(article_at_slot[i] == 6, article_at_slot[i+1] == 6),
        And(article_at_slot[i] < 3, article_at_slot[i + 1] == 6),
        And(article_at_slot[i] == 6, article_at_slot[i + 1] < 3),
        And(article_at_slot[i] > 2, article_at_slot[i] < 6, article_at_slot[i+1] == 6),
        And(article_at_slot[i] == 6, article_at_slot[i+1] > 2, article_at_slot[i+1] < 6)
    )))) # Constraint 2
solver.add(Implies(article_at_slot[3] != 3, ForAll([i,j], Implies(And(i >= 1, i <= 7, j >= 1, j <= 7, article_at_slot[i] == 5, article_at_slot[j] == 3), i < j)))) # Constraint 3
solver.add(ForAll([i,j], Implies(And(i >= 1, i <= 7, j >= 1, j <= 7, article_at_slot[i] == 5, article_at_slot[j] == 6), i < j))) # Constraint 4
solver.add(ForAll([i, j, k], Implies(And(i >= 1, i <= 7, j >= 1, j <= 7, k >= 1, k <= 7, article_at_slot[i] == 2, article_at_slot[j] == 0, article_at_slot[k] == 4), And(i < j, j < k)))) # Constraint 5


# Answer choices
options = [
    (2, 0),  # G is second
    (2, 1),  # H is second
    (2, 5),  # S is second
    (3, 4),  # R is third
    (3, 6)   # Y is third
]

for option_index, (slot, article) in enumerate(options):
    solver.push()
    solver.add(article_at_slot[slot] == article)
    if solver.check() == sat:
        print(f"Option {chr(65 + option_index)} is correct")
        exit()
    solver.pop()