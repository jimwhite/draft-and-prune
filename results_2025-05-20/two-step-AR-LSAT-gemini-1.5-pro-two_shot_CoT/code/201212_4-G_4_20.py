from z3 import *

# Variables
pos = Array('pos', IntSort(), IntSort())
article_at_slot = Array('article_at_slot', IntSort(), IntSort())
i = Int('i')
j = Int('j')

# Solver
solver = Solver()

# Article IDs: G=0, H=1, J=2, Q=3, R=4, S=5, Y=6
# Topics by ID: Finance={0,1,2}, Nutrition={3,4,5}, Wildlife={6}

# Constraints
solver.add(ForAll([j], Implies(And(j >= 0, j <= 6), And(pos[j] >= 1, pos[j] <= 7))))
solver.add(Distinct([pos[j] for j in range(0, 7)]))

solver.add(ForAll([i], Implies(And(i >= 1, i <= 7), And(article_at_slot[i] >= 0, article_at_slot[i] <= 6))))
solver.add(Distinct([article_at_slot[i] for i in range(1, 8)]))

solver.add(ForAll([i], Implies(And(i >= 1, i <= 7), pos[article_at_slot[i]] == i)))

def IsFinance(a):
    return Or(a == 0, a == 1, a == 2)

def IsNutrition(a):
    return Or(a == 3, a == 4, a == 5)

def IsWildlife(a):
    return (a == 6)

solver.add(ForAll([i], Implies(And(i >= 1, i <= 6), 
                               And(Not(And(IsFinance(article_at_slot[i]), IsFinance(article_at_slot[i+1]))),
                                   Not(And(IsNutrition(article_at_slot[i]), IsNutrition(article_at_slot[i+1]))),
                                   Not(And(IsWildlife(article_at_slot[i]), IsWildlife(article_at_slot[i+1])))))))

solver.add(Implies(pos[5] < pos[3], pos[3] == 3))
solver.add(pos[5] < pos[6])
solver.add(pos[2] < pos[0])
solver.add(pos[0] < pos[4])

# Answer choices
options = [
    pos[0] == 2,  # G is second
    pos[1] == 2,  # H is second
    pos[5] == 2,  # S is second
    pos[4] == 3,  # R is third
    pos[6] == 3   # Y is third
]

for idx, option in enumerate(options):
    solver.push()
    solver.add(option)
    if solver.check() == sat:
        print(f"Option {chr(65 + idx)} is correct")
        exit()
    solver.pop()