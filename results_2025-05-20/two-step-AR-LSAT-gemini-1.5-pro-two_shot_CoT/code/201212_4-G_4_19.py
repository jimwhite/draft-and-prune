from z3 import *

# Variables
article_at_slot = Array('article_at_slot', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
i = Int('i')
j = Int('j')
k = Int('k')

# Constraint 0 (Domain)
solver.add(ForAll([i], Implies(And(i >= 1, i <= 7), And(article_at_slot[i] >= 0, article_at_slot[i] <= 6))))

# Constraint 1 (Distinctness)
solver.add(Distinct([article_at_slot[i] for i in range(1, 8)]))

# Constraint 2 (No consecutive same topic)
solver.add(ForAll([i], Implies(And(i >= 1, i <= 6), 
    Not(Or(
        And(article_at_slot[i] == 0, article_at_slot[i+1] == 1),
        And(article_at_slot[i] == 0, article_at_slot[i+1] == 2),
        And(article_at_slot[i] == 1, article_at_slot[i+1] == 0),
        And(article_at_slot[i] == 1, article_at_slot[i+1] == 2),
        And(article_at_slot[i] == 2, article_at_slot[i+1] == 0),
        And(article_at_slot[i] == 2, article_at_slot[i+1] == 1),
        And(article_at_slot[i] == 3, article_at_slot[i+1] == 4),
        And(article_at_slot[i] == 3, article_at_slot[i+1] == 5),
        And(article_at_slot[i] == 4, article_at_slot[i+1] == 3),
        And(article_at_slot[i] == 4, article_at_slot[i+1] == 5),
        And(article_at_slot[i] == 5, article_at_slot[i+1] == 3),
        And(article_at_slot[i] == 5, article_at_slot[i+1] == 4)
    )))))

# Constraint 3 (S before Q only if Q is third)
solver.add(Implies(ForAll([i, j], Implies(And(i >= 1, i <= 7, j >= 1, j <= 7, article_at_slot[i] == 5, article_at_slot[j] == 3), i < j)), article_at_slot[3] == 3))

# Constraint 4 (S before Y)
solver.add(ForAll([i, j], Implies(And(i >= 1, i <= 7, j >= 1, j <= 7, article_at_slot[i] == 5, article_at_slot[j] == 6), i < j)))

# Constraint 5 (J before G before R)
solver.add(ForAll([i, j, k], Implies(And(i >= 1, i <= 7, j >= 1, j <= 7, k >= 1, k <= 7, article_at_slot[i] == 2, article_at_slot[j] == 0, article_at_slot[k] == 4), And(i < j, j < k))))

# Constraint 6 (G is fourth)
solver.add(article_at_slot[4] == 0)

# Check answer choices
answer_choices = [
    article_at_slot[5] == 1,  # A: H is fifth
    article_at_slot[1] == 2,  # B: J is first
    article_at_slot[2] == 3,  # C: Q is second
    article_at_slot[5] == 5,  # D: S is fifth
    article_at_slot[6] == 6   # E: Y is sixth
]

for i in range(len(answer_choices)):
    solver.push()
    solver.add(answer_choices[i])
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()