from z3 import *

# Variables
article_at_slot = Array('article_at_slot', IntSort(), IntSort())

# Article IDs
G = 0
H = 1
J = 2
Q = 3
R = 4
S = 5
Y = 6

# Solver
solver = Solver()

# Constraint 0 (Domain)
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 1, i <= 7), And(article_at_slot[i] >= 0, article_at_slot[i] <= 6))))

# Constraint 1 (Distinctness)
solver.add(Distinct([article_at_slot[i] for i in range(1, 8)]))

# Topic Predicates
def IsFinance(a):
    return Or(a == G, a == H, a == J)

def IsNutrition(a):
    return Or(a == Q, a == R, a == S)

def IsWildlife(a):
    return (a == Y)

# Constraint 2 (Consecutive Topics)
solver.add(ForAll([i], Implies(And(i >= 1, i <= 6), Not(Or(
    And(IsFinance(article_at_slot[i]), IsFinance(article_at_slot[i+1])),
    And(IsNutrition(article_at_slot[i]), IsNutrition(article_at_slot[i+1])),
    And(IsWildlife(article_at_slot[i]), IsWildlife(article_at_slot[i+1]))
)))))

# Constraint 3 (S before Q conditional)
i = Int('i')
j = Int('j')
solver.add(Implies(Exists([i, j], And(i >= 1, i <= 7, j >= 1, j <= 7, i < j, article_at_slot[i] == S, article_at_slot[j] == Q)), article_at_slot[3] == Q))

# Constraint 4 (S before Y)
i = Int('i')
j = Int('j')
solver.add(Exists([i, j], And(i >= 1, i <= 7, j >= 1, j <= 7, i < j, article_at_slot[i] == S, article_at_slot[j] == Y)))

# Constraint 5 (J before G before R)
i = Int('i')
j = Int('j')
k = Int('k')
solver.add(Exists([i, j, k], And(i >= 1, i <= 7, j >= 1, j <= 7, k >= 1, k <= 7, i < j, j < k, article_at_slot[i] == J, article_at_slot[j] == G, article_at_slot[k] == R)))

# Answer Choices
options = [
    "H, S, J, Q, Y, G, R",
    "J, Q, G, H, S, Y, R",
    "Q, J, S, H, Y, G, R",
    "Q, J, Y, S, G, R, H",
    "S, G, Q, J, Y, R, H"
]

option_mapping = {
    "G": G, "H": H, "J": J, "Q": Q, "R": R, "S": S, "Y": Y
}


for option_index, option in enumerate(options):
    solver.push()
    articles = [option_mapping[article.strip()] for article in option.split(',')]
    for i in range(7):
        solver.add(article_at_slot[i+1] == articles[i])
    if solver.check() == sat:
        print(f"Option {chr(65 + option_index)} is correct")
        exit()
    solver.pop()