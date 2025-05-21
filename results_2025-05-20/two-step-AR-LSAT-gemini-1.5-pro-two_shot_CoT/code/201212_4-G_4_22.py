from z3 import *

# Variables
article_at_slot = Array('article_at_slot', IntSort(), IntSort())
i = Int('i')

# Solver
solver = Solver()

# Constraints
# Constraint 0 (Domain)
solver.add(ForAll([i], Implies(And(i >= 1, i <= 7), And(article_at_slot[i] >= 0, article_at_slot[i] <= 6))))

# Constraint 1 (Distinctness)
solver.add(Distinct([article_at_slot[i] for i in range(1, 8)]))

# Constraint 2 (Consecutive Topics)
solver.add(ForAll([i], Implies(And(i >= 1, i <= 6), Not(Or(
    And(article_at_slot[i] <= 2, article_at_slot[i+1] <=2),
    And(article_at_slot[i] >= 3, article_at_slot[i] <= 5, article_at_slot[i+1] >= 3, article_at_slot[i+1] <= 5)
)))))

# Helper function for IndexOf
def IndexOf(arr, val):
    for i in range(1, 8):
        if solver.check(arr[i] == val) == sat:
            return i
    return -1  # Should not reach here in this problem

# Constraint 3 (S before Q condition)
solver.add(Implies(IndexOf(article_at_slot, 5) < IndexOf(article_at_slot, 3), article_at_slot[3] == 3))

# Constraint 4 (S before Y)
solver.add(IndexOf(article_at_slot, 5) < IndexOf(article_at_slot, 6))

# Constraint 5 (J before G before R)
solver.add(IndexOf(article_at_slot, 2) < IndexOf(article_at_slot, 0))
solver.add(IndexOf(article_at_slot, 0) < IndexOf(article_at_slot, 4))


# Check answer choices
positions = [1, 3, 4, 5, 6]
options = ["A", "B", "C", "D", "E"]

for idx, pos in enumerate(positions):
    solver.push()
    solver.add(article_at_slot[pos] == 5)
    if solver.check() == unsat:
        print(f"Option {options[idx]} is correct")
        exit()
    solver.pop()