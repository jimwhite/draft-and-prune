from z3 import *

# Define variables
painting_info = Function('painting_info', IntSort(), IntSort(), IntSort(), IntSort())
solver = Solver()

# Domain constraints
solver.add(ForAll([s, w, p], Implies(And(0 <= s, s < 4, 0 <= w, w < 4, 0 <= p, p < 2), Or(painting_info(s, w, p) == -1, painting_info(s, w, p) == 0, painting_info(s, w, p) == 1))))

# Constraints
# Constraint 1 (Each student displays exactly two paintings)
solver.add(ForAll([s], Implies(And(0 <= s, s < 4), Sum([If(painting_info(s, w, p) != -1, 1, 0) for w in range(4) for p in range(2)]) == 2)))

# Constraint 2 (Exactly two paintings on each wall)
solver.add(ForAll([w], Implies(And(0 <= w, w < 4), Sum([If(painting_info(s, w, p) != -1, 1, 0) for s in range(4) for p in range(2)]) == 2)))

# Constraint 3 (Each student displays one oil and one watercolor)
solver.add(ForAll([s], Implies(And(0 <= s, s < 4), Sum([If(painting_info(s, w, p) == 0, 1, 0) for w in range(4) for p in range(2)]) == 1)))
solver.add(ForAll([s], Implies(And(0 <= s, s < 4), Sum([If(painting_info(s, w, p) == 1, 1, 0) for w in range(4) for p in range(2)]) == 1)))

# Constraint 4 (No wall has only watercolors)
solver.add(ForAll([w], Implies(And(0 <= w, w < 4), Exists([s, p], And(0 <= s, s < 4, 0 <= p, p < 2, painting_info(s, w, p) == 0)))))

# Constraint 5 (No wall has work of only one student)
solver.add(ForAll([w], Implies(And(0 <= w, w < 4), Exists([s1, s2, p1, p2], And(0 <= s1, s1 < 4, 0 <= s2, s2 < 4, s1 != s2, 0 <= p1, p1 < 2, 0 <= p2, p2 < 2, painting_info(s1, w, p1) != -1, painting_info(s2, w, p2) != -1)))))

# Constraint 6 (No wall has both Franz and Isaacs)
solver.add(ForAll([w], Implies(And(0 <= w, w < 4), Not(Exists([p1, p2], And(0 <= p1, p1 < 2, 0 <= p2, p2 < 2, painting_info(0, w, p1) != -1, painting_info(3, w, p2) != -1))))))

# Constraint 7 (Greene's watercolor is displayed in the upper position of the wall on which Franz's oil is displayed)
solver.add(ForAll([w, pf], Implies(And(0 <= w, w < 4, 0 <= pf, pf < 2, painting_info(0, w, pf) == 0), painting_info(1, w, 0) == 1)))


# Constraint 8 (Isaacs's oil is displayed in the lower position of wall 4)
solver.add(painting_info(3, 3, 1) == 0)

# Constraint 9 (Isaacs's watercolor is displayed on wall 2)
solver.add(Or(painting_info(3, 1, 0) == 1, painting_info(3, 1, 1) == 1))

# Constraint 10 (Franz's oil is displayed on wall 3)
solver.add(Or(painting_info(0, 2, 0) == 0, painting_info(0, 2, 1) == 0))

# Constraint 11 (Each slot has exactly one painting)
solver.add(ForAll([w, p], Implies(And(0 <= w, w < 4, 0 <= p, p < 2), Sum([If(painting_info(s, w, p) != -1, 1, 0) for s in range(4)]) == 1)))

# Answer choices
options = [
    Or(painting_info(0, 0, 0) == 1, painting_info(0, 0, 1) == 1),  # Franz's watercolor
    Or(painting_info(1, 0, 0) == 0, painting_info(1, 0, 1) == 0),  # Greene's oil
    Or(painting_info(1, 0, 0) == 1, painting_info(1, 0, 1) == 1),  # Greene's watercolor
    Or(painting_info(2, 0, 0) == 0, painting_info(2, 0, 1) == 0),  # Hidalgo's oil
    Or(painting_info(2, 0, 0) == 1, painting_info(2, 0, 1) == 1)   # Hidalgo's watercolor
]

for i, option in enumerate(options):
    solver.push()
    solver.add(Not(option))
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
