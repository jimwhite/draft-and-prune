from z3 import *

# Variables
house_at_slot = Array('house_at_slot', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 0, i < 7), And(house_at_slot[i] >= 0, house_at_slot[i] < 7))))
solver.add(Distinct([house_at_slot[i] for i in range(7)]))
solver.add(Or(house_at_slot[5] == 0, house_at_slot[6] == 0))
solver.add(And(house_at_slot[0] != 1, house_at_slot[1] != 1))

k = Int('k')
l = Int('l')
m = Int('m')
solver.add(ForAll([k, l, m], Implies(And(k >= 0, k < 7, l >= 0, l < 7, m >= 0, m < 7, house_at_slot[k] == 1, house_at_slot[l] == 2, house_at_slot[m] == 3), And(k < l, l < m))))

# Answer choices
choices = [
    [1, 5, 2, 3, 4, 0, 6],
    [4, 2, 6, 1, 3, 5, 0],
    [5, 6, 1, 2, 4, 3, 0],
    [5, 6, 3, 4, 1, 2, 0],
    [6, 5, 1, 0, 2, 4, 3]
]

# Check each choice
for choice_index, choice in enumerate(choices):
    solver.push()
    for slot, house in enumerate(choice):
        solver.add(house_at_slot[slot] == house)
    if solver.check() == sat:
        print(f"Option {chr(65 + choice_index)} is correct")
        exit()
    solver.pop()