from z3 import *

# Constants
Franz, Greene, Hidalgo, Isaacs = 0, 1, 2, 3
Oil, Watercolor = 0, 1
Wall1, Wall2, Wall3, Wall4 = 0, 1, 2, 3
Upper, Lower = 0, 1

# Z3 variables
wall_upper = Array('wall_upper', IntSort(), IntSort())
wall_lower = Array('wall_lower', IntSort(), IntSort())

solver = Solver()

# Constraints
solver.add(Distinct([wall_upper[w] for w in range(4)] + [wall_lower[w] for w in range(4)]))
# Fixed: Iterate and add constraints individually
for w in range(4):
    solver.add(And(wall_upper[w] >= 0, wall_upper[w] <= 7, wall_lower[w] >= 0, wall_lower[w] <= 7))
for w in range(4):
    solver.add(Or(wall_upper[w] % 2 == 0, wall_lower[w] % 2 == 0))
# Fixed: Use integer division correctly
for w in range(4):
    solver.add(wall_upper[w] / 2 != wall_lower[w] / 2)
for w in range(4):
    solver.add(Not(Or(And(wall_upper[w] / 2 == Franz, wall_lower[w] / 2 == Isaacs), And(wall_upper[w] / 2 == Isaacs, wall_lower[w] / 2 == Franz))))
# Greene's watercolor above Franz's oil
for w in range(4):
    solver.add(Implies(And(wall_upper[w] == 3, wall_lower[w] == 0), w == Wall1)) # Greene's watercolor (index 3) above Franz's oil (index 0)
# Isaacs's oil on wall 4 lower
solver.add(wall_lower[Wall4] == 6)  # Isaacs's oil (index 6)

# Premise: Hidalgo's oil on wall 2
solver.add(Or(wall_upper[Wall2] == 4, wall_lower[Wall2] == 4))

# Answer choices
options = [0, 3, 2, 5, 7]  # Painting indices for each option
option_letters = ['A', 'B', 'C', 'D', 'E']

for i, p_opt in enumerate(options):
    solver.push()
    solver.add(Or(And(wall_upper[Wall2] == 4, wall_lower[Wall2] == p_opt), And(wall_lower[Wall2] == 4, wall_upper[Wall2] == p_opt)))
    if solver.check() == sat:
        print(f"Option {option_letters[i]} is correct")
        exit()
    solver.pop()
