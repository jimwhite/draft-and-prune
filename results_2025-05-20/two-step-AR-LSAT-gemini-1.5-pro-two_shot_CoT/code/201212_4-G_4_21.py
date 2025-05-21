from z3 import *

# Variables
article_at_slot = Array('article_at_slot', IntSort(), IntSort())
pos_G = Int('pos_G')
pos_H = Int('pos_H')
pos_J = Int('pos_J')
pos_Q = Int('pos_Q')
pos_R = Int('pos_R')
pos_S = Int('pos_S')
pos_Y = Int('pos_Y')
i = Int('i')

# Solver
solver = Solver()

# Constraints
solver.add(ForAll([i], Implies(And(i >= 1, i <= 7), And(article_at_slot[i] >= 0, article_at_slot[i] <= 6)))) # 0a
solver.add(And(pos_G >= 1, pos_G <= 7, pos_H >= 1, pos_H <= 7, pos_J >= 1, pos_J <= 7, pos_Q >= 1, pos_Q <= 7, pos_R >= 1, pos_R <= 7, pos_S >= 1, pos_S <= 7, pos_Y >= 1, pos_Y <= 7)) # 0b
solver.add(Distinct([pos_G, pos_H, pos_J, pos_Q, pos_R, pos_S, pos_Y])) # 1
solver.add(And(article_at_slot[pos_G] == 0, article_at_slot[pos_H] == 1, article_at_slot[pos_J] == 2, article_at_slot[pos_Q] == 3, article_at_slot[pos_R] == 4, article_at_slot[pos_S] == 5, article_at_slot[pos_Y] == 6)) # 1b
# Fixed: Closed the parenthesis for Or and added closing parenthesis for Not
solver.add(ForAll([i], Implies(And(i >= 1, i <= 6), Not(Or(
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
    And(article_at_slot[i] == 5, article_at_slot[i+1] == 4)))))) # 2
solver.add(Implies(pos_S < pos_Q, pos_Q == 3)) # 3
solver.add(pos_S < pos_Y) # 4
solver.add(And(pos_J < pos_G, pos_G < pos_R)) # 5
solver.add(pos_J == 3) # 6

# Check answer choices
options = [("G is fourth", pos_G == 4), ("H is sixth", pos_H == 6), ("Q is first", pos_Q == 1), ("S is second", pos_S == 2), ("Y is fifth", pos_Y == 5)]
for option_letter, constraint in zip("ABCDE", options):
    solver.push()
    solver.add(constraint[1])
    if solver.check() == sat:
        print(f"Option {option_letter} is correct")
        exit()
    solver.pop()

