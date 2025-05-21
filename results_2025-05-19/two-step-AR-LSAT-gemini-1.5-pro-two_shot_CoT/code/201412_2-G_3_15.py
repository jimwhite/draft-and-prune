from z3 import *

# Define variables
color_in_rug = Array('color_in_rug', IntSort(), IntSort())
F, O, P, T, W, Y = 0, 1, 2, 3, 4, 5
solver = Solver()

# Constraints
solver.add(PbEq([(color_in_rug[c] != -1, 1) for c in range(6)], 5))  # Constraint 0
solver.add(ForAll(c, Implies(color_in_rug[c] != -1, And(color_in_rug[c] >= 0, color_in_rug[c] <= 2)))) # Constraint 1, fixed quantifier syntax
solver.add(ForAll(r, Implies(color_in_rug[W] == r, PbEq([(color_in_rug[c] == r, 1) for c in range(6) if c != W], 2)))) # Constraint 2, fixed quantifier syntax
solver.add(Implies(color_in_rug[O] != -1, color_in_rug[P] == color_in_rug[O])) # Constraint 3
solver.add(color_in_rug[F] != color_in_rug[T]) # Constraint 4
solver.add(color_in_rug[P] != color_in_rug[T]) # Constraint 5
solver.add(color_in_rug[P] != color_in_rug[Y]) # Constraint 6
solver.add(color_in_rug[F] == color_in_rug[P]) # Constraint 7

# Constraint 8 (Distinct Rugs): Use c1 and c2 as variables in quantifier
c1 = Int('c1')
c2 = Int('c2')
solver.add(ForAll([c1, c2], Implies(And(c1 >=0, c1 < 6, c2 >= 0, c2 < 6, c1 != c2, color_in_rug[c1] != -1, color_in_rug[c2] != -1), color_in_rug[c1] != color_in_rug[c2])))


# Check answer choices
choices = [
    PbEq([(Sum([If(color_in_rug[c] == r, 1, 0) for c in range(6)]) == 1, 1) for r in range(3)], 1),  # Choice A
    color_in_rug[W] == -1,  # Choice B
    color_in_rug[Y] == -1,  # Choice C
    And(color_in_rug[T] == color_in_rug[W], color_in_rug[T] != -1),  # Choice D
    And(color_in_rug[T] == color_in_rug[Y], color_in_rug[T] != -1)  # Choice E
]

for i, choice in enumerate(choices):
    solver.push()
    solver.add(choice)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
