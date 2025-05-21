from z3 import *

# Define position variables
pos_O, pos_P, pos_R1, pos_R2, pos_S, pos_T, pos_V = Ints('pos_O pos_P pos_R1 pos_R2 pos_S pos_T pos_V')

solver = Solver()

# Base constraints
solver.add(Distinct(pos_O, pos_P, pos_R1, pos_R2, pos_S, pos_T, pos_V))
for pos in [pos_O, pos_P, pos_R1, pos_R2, pos_S, pos_T, pos_V]:
    solver.add(And(pos >= 1, pos <= 7))
solver.add(Or(pos_P == 1, pos_P == 7))
solver.add(Or(pos_R1 == 1, pos_R1 == 7, pos_R2 == 1, pos_R2 == 7))
solver.add(If(pos_R1 > pos_R2, pos_R1 - pos_R2, pos_R2 - pos_R1) > 2)
solver.add(Or(If(pos_P > pos_O, pos_P - pos_O, pos_O - pos_P) == 1, If(pos_P > pos_V, pos_P - pos_V, pos_V - pos_P) == 1))
solver.add(If(pos_T > pos_V, pos_T - pos_V, pos_V - pos_T) != 1)


# Premise: Optometrist next to Shoe store
solver.add(If(pos_O > pos_S, pos_O - pos_S, pos_S - pos_O) == 1)
# Ensure both pos_O and pos_S are within (1, 7). This is already implied by the base constraints.


# Define positions on either side of O-S pair. Define p1 and p2 before using them.
p1 = Int('p1')
p2 = Int('p2')
solver.add(If(pos_O < pos_S, p1 == pos_O - 1, p1 == pos_S - 1))
solver.add(If(pos_O < pos_S, p2 == pos_S + 1, p2 == pos_O + 1))




# Answer choices
options = [
    Or(And(pos_P == p1, Or(pos_R1 == p2, pos_R2 == p2)), And(Or(pos_R1 == p1, pos_R2 == p1), pos_P == p2)),  # A
    Or(And(pos_P == p1, pos_T == p2), And(pos_T == p1, pos_P == p2)),  # B
    Or(And(pos_R1 == p1, pos_R2 == p2), And(pos_R2 == p1, pos_R1 == p2)),  # C
    Or(And(Or(pos_R1 == p1, pos_R2 == p1), pos_T == p2), And(pos_T == p1, Or(pos_R1 == p2, pos_R2 == p2))),  # D
    Or(And(Or(pos_R1 == p1, pos_R2 == p1), pos_V == p2), And(pos_V == p1, Or(pos_R1 == p2, pos_R2 == p2)))   # E
]

for i, option in enumerate(options):
    solver.push()
    solver.add(Not(option))
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
