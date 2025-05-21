from z3 import *

# Variables
article_at_slot = Array('article_at_slot', IntSort(), IntSort())
articles = [Int('article_%i' % i) for i in range(7)]  # Not used directly, but helpful for readability

# Solver
solver = Solver()

# Constraint 0 (Domain)
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 1, i <= 7), And(article_at_slot[i] >= 0, article_at_slot[i] <= 6))))

# Constraint 1 (Distinctness)
solver.add(Distinct([article_at_slot[i] for i in range(1, 8)]))

# Constraint 2 (Consecutive Topics)
def IsFinance(a):
    return Or(a == 0, a == 1, a == 2)

def IsNutrition(a):
    return Or(a == 3, a == 4, a == 5)

def IsWildlife(a):
    return (a == 6)

solver.add(ForAll([i], Implies(And(i >= 1, i <= 6),
                               And(Implies(IsFinance(article_at_slot[i]), Not(IsFinance(article_at_slot[i + 1]))),
                                   Implies(IsNutrition(article_at_slot[i]), Not(IsNutrition(article_at_slot[i + 1]))),
                                   Implies(IsWildlife(article_at_slot[i]), Not(IsWildlife(article_at_slot[i + 1])))))))


# Constraint 3 (S before Q only if Q is third)
i, j = Ints('i j')
solver.add(Or(Exists([i, j], And(i >= 1, i <= 7, j >= 1, j <= 7, i >= j, article_at_slot[i] == 5, article_at_slot[j] == 3)),
             article_at_slot[3] == 3))

# Constraint 4 (S before Y)
i, j = Ints('i j')
solver.add(Exists([i, j], And(i >= 1, i <= 7, j >= 1, j <= 7, i < j, article_at_slot[i] == 5, article_at_slot[j] == 6)))

# Constraint 5 (J before G before R)
i, j, k = Ints('i j k')
solver.add(Exists([i, j, k], And(i >= 1, i <= 7, j >= 1, j <= 7, k >= 1, k <= 7,
                                 article_at_slot[i] == 2, article_at_slot[j] == 0, article_at_slot[k] == 4,
                                 i < j, j < k)))

# Check answer choices
options = ["H is fourth.", "H is sixth.", "R is fourth.", "R is seventh.", "Y is fifth."]
constraints = [article_at_slot[4] == 1, article_at_slot[6] == 1, article_at_slot[4] == 4,
               article_at_slot[7] == 4, article_at_slot[5] == 6]

for idx, (option_text, constraint) in enumerate(zip(options, constraints)):
    solver.push()
    solver.add(constraint)
    if solver.check() == sat:
        m = solver.model()
        solver.push()
        solver.add(Not(And([article_at_slot[i] == m.eval(article_at_slot[i], model_completion=True) for i in range(1, 8)])))
        if solver.check() == unsat:
            print(f"Option {chr(65 + idx)} is correct")
            exit()
        solver.pop()
    solver.pop()