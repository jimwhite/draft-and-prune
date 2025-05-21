from z3 import *

# Variables
article_at_slot = Array('article_at_slot', IntSort(), IntSort())
articles = ["G", "H", "J", "Q", "R", "S", "Y"]
article_mapping = {article: i for i, article in enumerate(articles)}

# Solver
solver = Solver()

# Constraint 0 (Domain)
i = Int('i') # Define i
solver.add(ForAll([i], Implies(And(i >= 1, i <= 7), And(article_at_slot[i] >= 0, article_at_slot[i] <= 6))))

# Constraint 1 (Distinctness)
solver.add(Distinct([article_at_slot[i] for i in range(1, 8)]))

# Constraint 2 (Consecutive Topics)
i = Int('i') # Define i again for the ForAll quantifier
solver.add(ForAll([i], Implies(And(i >= 1, i <= 6),
        Or(
            And(article_at_slot[i] < 3, Or(article_at_slot[i+1] == 6, And(article_at_slot[i+1] >= 3, article_at_slot[i+1] <= 5))),
            And(article_at_slot[i] >= 3, article_at_slot[i] <= 5, Or(article_at_slot[i+1] == 6, And(article_at_slot[i+1] < 3))),
            And(article_at_slot[i] == 6, Or(article_at_slot[i+1] < 3, And(article_at_slot[i+1] >= 3, article_at_slot[i+1] <= 5)))
        ))))

# Constraint 3 (S before Q condition)
i = Int('i') # Define i
j = Int('j') # Define j
solver.add(Implies(article_at_slot[3] != article_mapping["Q"], ForAll([i], Implies(article_at_slot[i] == article_mapping["S"], ForAll([j], Implies(article_at_slot[j] == article_mapping["Q"], i < j))))))

# Constraint 4 (S before Y)
i = Int('i') # Define i
j = Int('j') # Define j
solver.add(ForAll([i], Implies(article_at_slot[i] == article_mapping["S"], ForAll([j], Implies(article_at_slot[j] == article_mapping["Y"], i < j)))))

# Constraint 5 (J before G before R)
i = Int('i') # Define i
j = Int('j') # Define j
solver.add(ForAll([i], Implies(article_at_slot[i] == article_mapping["J"], ForAll([j], Implies(article_at_slot[j] == article_mapping["G"], i < j)))))
i = Int('i') # Define i
j = Int('j') # Define j
solver.add(ForAll([i], Implies(article_at_slot[i] == article_mapping["G"], ForAll([j], Implies(article_at_slot[j] == article_mapping["R"], i < j)))))

# Answer Choices
choices = [
  "H, S, J, Q, Y, G, R",
  "J, Q, G, H, S, Y, R",
  "Q, J, S, H, Y, G, R",
  "Q, J, Y, S, G, R, H",
  "S, G, Q, J, Y, R, H"
]

# Check each choice
for option_index, choice in enumerate(choices):
    solver.push()
    order = [article_mapping[article.strip()] for article in choice.split(',')]
    for i in range(7):
        solver.add(article_at_slot[i+1] == order[i])
    if solver.check() == sat:
        print(f"Option {chr(65 + option_index)} is correct")
        exit()
    solver.pop()
