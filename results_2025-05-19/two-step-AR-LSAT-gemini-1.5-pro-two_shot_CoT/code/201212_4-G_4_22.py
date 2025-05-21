from z3 import *

# Variables
article_at_slot = Array('article_at_slot', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 1, i <= 7), And(article_at_slot[i] >= 0, article_at_slot[i] <= 6)))) # Constraint 0
solver.add(Distinct([article_at_slot[i] for i in range(1, 8)])) # Constraint 1

solver.add(ForAll([i], Implies(And(i >= 1, i <= 6), Not(Or(
    And(article_at_slot[i] >= 0, article_at_slot[i] <= 2, article_at_slot[i+1] >= 0, article_at_slot[i+1] <= 2),
    And(article_at_slot[i] >= 3, article_at_slot[i] <= 5, article_at_slot[i+1] >= 3, article_at_slot[i+1] <= 5)
))))) # Constraint 2

i = Int('i')
j = Int('j')
solver.add(Implies(Exists([i, j], And(i < j, article_at_slot[i] == 5, article_at_slot[j] == 3)), article_at_slot[3] == 3)) # Constraint 3

i = Int('i')
j = Int('j')
solver.add(Exists([i, j], And(i < j, article_at_slot[i] == 5, article_at_slot[j] == 6))) # Constraint 4

i = Int('i')
j = Int('j')
k = Int('k')
solver.add(Exists([i, j, k], And(i < j, j < k, article_at_slot[i] == 2, article_at_slot[j] == 0, article_at_slot[k] == 4))) # Constraint 5


# Check answer choices
options = ["first", "third", "fourth", "fifth", "sixth"]
for idx, option in enumerate(options):
    solver.push()
    if option == "first":
        solver.add(article_at_slot[1] == 5)
    elif option == "third":
        solver.add(article_at_slot[3] == 5)
    elif option == "fourth":
        solver.add(article_at_slot[4] == 5)
    elif option == "fifth":
        solver.add(article_at_slot[5] == 5)
    elif option == "sixth":
        solver.add(article_at_slot[6] == 5)

    if solver.check() == unsat:
        print(f"Option {chr(65 + idx)} is correct")
        exit()
    solver.pop()