from z3 import *

# 1. Entities
R = 0
S = 1
T = 2
Y = 3
F = 0
G = 1
H = 2
J = 3

# 2. Variables
assignment = Array('assignment', IntSort(), IntSort(), IntSort())

# 3. Constraints
solver = Solver()
solver.add(ForAll([d, r], Implies(And(d >= 0, d <= 1, r >=0, r <= 3), And(assignment[d][r] >= 0, assignment[d][r] <= 3))))  # Constraint 1: Domain
solver.add(ForAll([d], Implies(And(d >= 0, d <= 1), Distinct([assignment[d][r] for r in range(4)]))))  # Constraint 2: Unique Bicycles per Day
solver.add(ForAll([r], Implies(And(r >= 0, r <= 3), assignment[0][r] != assignment[1][r])))  # Constraint 3: Different Bike Day 2 vs Day 1
solver.add(ForAll([d], Implies(And(d >= 0, d <= 1), assignment[d][R] != F)))  # Constraint 4: Reynaldo cannot test F
solver.add(ForAll([d], Implies(And(d >= 0, d <= 1), assignment[d][Y] != J)))  # Constraint 5: Yuki cannot test J
solver.add(Xor(assignment[0][T] == H, assignment[1][T] == H))  # Constraint 6: Theresa tests H exactly once
solver.add(assignment[0][Y] == assignment[1][S])  # Constraint 7: Yuki's Day 1 bike is Seamus's Day 2 bike

# 4. Answering the Question
answer_choices = [
    (0, R, J),  # "Reynaldo tests J on the first day."
    (1, R, J),  # "Reynaldo tests J on the second day."
    (0, S, H),  # "Seamus tests H on the first day."
    (0, Y, H),  # "Yuki tests H on the first day."
    (1, Y, H)   # "Yuki tests H on the second day."
]

for i, (day, rider, bike) in enumerate(answer_choices):
    solver.push()
    solver.add(assignment[day][rider] == bike)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
