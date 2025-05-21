from z3 import *

# Variables
article_at_slot = Array('article_at_slot', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
# 1. Domain
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 1, i <= 7), And(article_at_slot[i] >= 0, article_at_slot[i] <= 6))))

# 2. Distinctness
solver.add(Distinct([article_at_slot[i] for i in range(1, 8)]))

# 3. No Consecutive Same Topic
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


# 4. S before Q condition
solver.add(Implies(article_at_slot[3] != 3, article_at_slot[5] < article_at_slot[3]))

# 5. S before Y
solver.add(article_at_slot[5] < article_at_slot[6])

# 6. J before G before R  -- Fix: Chain comparison is not supported, use separate comparisons
solver.add(article_at_slot[2] < article_at_slot[0])
solver.add(article_at_slot[0] < article_at_slot[4])

# 7. G is fourth
solver.add(article_at_slot[4] == 0) #G

# Check answer choices
options = [
    article_at_slot[5] == 1,  # H is fifth
    article_at_slot[1] == 2,  # J is first
    article_at_slot[2] == 3,  # Q is second
    article_at_slot[5] == 5,  # S is fifth
    article_at_slot[6] == 6   # Y is sixth
]

for i, option in enumerate(options):
    solver.push()
    solver.add(option)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
