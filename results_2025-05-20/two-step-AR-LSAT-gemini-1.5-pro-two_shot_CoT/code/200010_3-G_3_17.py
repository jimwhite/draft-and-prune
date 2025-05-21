from z3 import *

# Define variables
performance_order = Array('performance_order', IntSort(), IntSort())

# Define a helper function to get the index of a composition
def IndexOf(comp_id):
    for i in range(8):
        if performance_order[i] == comp_id:
            return i
    return -1  # Should never reach here if constraints are satisfied

solver = Solver()

# Constraint 0 (Domain)
for i in range(8):
    solver.add(And(performance_order[i] >= 0, performance_order[i] <= 7))

# Constraint 1 (Distinctness)
solver.add(Distinct([performance_order[i] for i in range(8)]))

# Constraint 2 (T before F or after R)
solver.add(Or(IndexOf(7) + 1 == IndexOf(0), IndexOf(7) - 1 == IndexOf(5)))

# Constraint 3 (Two between F and R)
solver.add(Or(Sum([If(And(i > IndexOf(0), i < IndexOf(5)), 1, 0) for i in range(8)]) >= 2,
               Sum([If(And(i > IndexOf(5), i < IndexOf(0)), 1, 0) for i in range(8)]) >= 2))

# Constraint 4 (O is first or fifth)
solver.add(Or(performance_order[0] == 3, performance_order[4] == 3))

# Constraint 5 (Eighth is L or H)
solver.add(Or(performance_order[7] == 2, performance_order[7] == 1))

# Constraint 6 (P before S)
solver.add(IndexOf(4) < IndexOf(6))

# Constraint 7 (One between O and S)
solver.add(Or(Sum([If(And(i > IndexOf(3), i < IndexOf(6)), 1, 0) for i in range(8)]) >= 1,
               Sum([If(And(i > IndexOf(6), i < IndexOf(3)), 1, 0) for i in range(8)]) >= 1))

# Constraint 8 (P is third)
solver.add(performance_order[2] == 4)

# Constraint 9 (S is sixth)
solver.add(performance_order[5] == 6)


# Check answer choices
answer_choices = [
    (0, 1),  # F or H
    (0, 3),  # F or O
    (0, 7),  # F or T
    (1, 2),  # H or L
    (3, 5)   # O or R
]

for i, (comp1, comp2) in enumerate(answer_choices):
    solver.push()
    solver.add(And(performance_order[4] != comp1, performance_order[4] != comp2))
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()