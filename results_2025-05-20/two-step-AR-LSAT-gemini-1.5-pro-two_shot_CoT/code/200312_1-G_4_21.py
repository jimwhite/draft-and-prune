from z3 import *

# Define variables
reviews = Array('reviews', IntSort(), IntSort())

# Create solver
solver = Solver()

# Constraint 1: Each student reviews at least one play
s = Int('s')
solver.add(ForAll([s], Implies(And(s >= 0, s < 5), Or([Select(reviews, s * 3 + p) == 1 for p in range(3)]))))

# Constraint 2: Kramer and Lopez review fewer plays than Megregian
solver.add(Sum([Select(reviews, 1 * 3 + p) for p in range(3)]) < Sum([Select(reviews, 3 * 3 + p) for p in range(3)]))
solver.add(Sum([Select(reviews, 2 * 3 + p) for p in range(3)]) < Sum([Select(reviews, 3 * 3 + p) for p in range(3)]))

# Constraint 3: Neither Lopez nor Megregian reviews any play Jiang reviews
p = Int('p')
solver.add(ForAll([p], Implies(And(p >= 0, p < 3, Select(reviews, 0 * 3 + p) == 1), And(Select(reviews, 2 * 3 + p) == 0, Select(reviews, 3 * 3 + p) == 0))))

# Constraint 4: Kramer and O'Neill both review Tamerlane
solver.add(Select(reviews, 1 * 3 + 1) == 1)
solver.add(Select(reviews, 4 * 3 + 1) == 1)

# Constraint 5: Exactly two students review the same plays
s1 = Int('s1')
s2 = Int('s2')
s3 = Int('s3')
solver.add(Exists([s1, s2], And(s1 >= 0, s1 < 5, s2 >= 0, s2 < 5, s1 != s2,
                                ForAll([p], Implies(And(p >= 0, p < 3), Select(reviews, s1 * 3 + p) == Select(reviews, s2 * 3 + p))),
                                ForAll([s3], Implies(And(s3 >= 0, s3 < 5, s3 != s1, s3 != s2),
                                                   Not(ForAll([p], Implies(And(p >= 0, p < 3), Select(reviews, s3 * 3 + p) == Select(reviews, s1 * 3 + p)))))))))

# Constraint 6: Exactly three students review Undulation
solver.add(Sum([Select(reviews, s * 3 + 2) for s in range(5)]) == 3)

# Check answer choices
for i, option in enumerate(['A', 'B', 'C', 'D', 'E']):
    solver.push()
    if option == 'A':
        solver.add(Select(reviews, 3 * 3 + 2) == 0)
    elif option == 'B':
        solver.add(Select(reviews, 4 * 3 + 2) == 0)
    elif option == 'C':
        solver.add(Select(reviews, 0 * 3 + 2) == 1)
    elif option == 'D':
        solver.add(Select(reviews, 2 * 3 + 1) == 1)
    elif option == 'E':
        solver.add(Select(reviews, 4 * 3 + 0) == 1)

    if solver.check() == sat:
        print(f"Option {option} is correct")
        exit()
    solver.pop()

