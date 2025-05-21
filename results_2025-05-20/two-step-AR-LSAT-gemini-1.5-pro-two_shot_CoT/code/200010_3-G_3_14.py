from z3 import *

# Define variables
performance_order = Array('performance_order', IntSort(), IntSort())

# Define solver
solver = Solver()

# Constraint 0 (Domain)
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 0, i <= 7), And(performance_order[i] >= 0, performance_order[i] <= 7))))

# Constraint 1 (Distinctness)
solver.add(Distinct([performance_order[i] for i in range(8)]))

# Helper function for IndexOf
def IndexOf(array, value):
    for i in range(8):
        if array[i] == value:
            return i
    return -1


# Constraint 2 (T before F or after R)
solver.add(Or(IndexOf(performance_order, 7) == IndexOf(performance_order, 0) - 1, IndexOf(performance_order, 7) == IndexOf(performance_order, 5) + 1))

# Constraint 3 (Two between F and R)
solver.add(Abs(IndexOf(performance_order, 0) - IndexOf(performance_order, 5)) >= 3)

# Constraint 4 (O is first or fifth)
solver.add(Or(IndexOf(performance_order, 3) == 0, IndexOf(performance_order, 3) == 4))

# Constraint 5 (Eighth is L or H)
solver.add(Or(performance_order[7] == 2, performance_order[7] == 1))

# Constraint 6 (P before S)
solver.add(IndexOf(performance_order, 4) < IndexOf(performance_order, 6))

# Constraint 7 (One between O and S)
solver.add(Abs(IndexOf(performance_order, 3) - IndexOf(performance_order, 6)) >= 2)

# Constraint 8 (T is fifth)
solver.add(IndexOf(performance_order, 7) == 4)

# Constraint 9 (F is sixth)
solver.add(IndexOf(performance_order, 0) == 5)

# Answer choices
options = [
    {3, 6},  # fourth or seventh
    {2, 5},  # third or sixth
    {2, 3},  # third or fourth
    {1, 6},  # second or seventh
    {0, 3}   # first or fourth
]

# Check each option
for i, option in enumerate(options):
    possible_s_positions = set()
    for j in range(8):
        solver.push()
        solver.add(IndexOf(performance_order, 6) == j)
        if solver.check() == sat:
            possible_s_positions.add(j)
        solver.pop()
    if possible_s_positions == option:
        print(f"Option {chr(65 + i)} is correct")
        exit()