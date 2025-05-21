from z3 import *

# Entities
R = 0
S = 1
T = 2
Y = 3
F = 0
G = 1
H = 2
J = 3

# Variables
assignment = Function('assignment', IntSort(), IntSort(), IntSort()) # Changed to Function

# Solver
solver = Solver()

# Constraints
d = Int('d')
b = Int('b')
solver.add(ForAll([d, b], Implies(And(d >= 0, d < 2, b >= 0, b < 4), And(assignment(d, b) >= 0, assignment(d, b) < 4)))) # Added domain constraints

r1 = Int('r1')
r2 = Int('r2')
solver.add(ForAll([d, r1, r2], Implies(And(d >= 0, d < 2, r1 != r2, r1 >=0, r1 < 4, r2 >= 0, r2 < 4), assignment(d, r1) != assignment(d, r2)))) # Added domain constraints and used != directly


d = Int('d')
solver.add(ForAll([d], Implies(d >= 0, d < 2, Distinct([assignment(d, b) for b in range(4)])))) # Added domain constraint

d = Int('d')
solver.add(ForAll([d], Implies(d >= 0, d < 2, assignment(d, F) != R))) # Added domain constraint

d = Int('d')
solver.add(ForAll([d], Implies(d >= 0, d < 2, assignment(d, J) != Y))) # Added domain constraint

solver.add(Or(assignment(0, H) == T, assignment(1, H) == T))

b = Int('b')
solver.add(ForAll([b], Implies(And(b >= 0, b < 4), Implies(assignment(0, b) == Y, assignment(1, b) == S)))) # Added domain constraint

solver.add(Distinct([assignment(1, b) for b in range(4)]))

r = Int('r')
b1 = Int('b1')
b2 = Int('b2')
b3 = Int('b3')

solver.add(ForAll([r], Implies(And(r >= 0, r < 4), Exists([b1, b2], And(Distinct(b1, b2), b1 >= 0, b1 < 4, b2 >= 0, b2 < 4, assignment(0, b1) == r, assignment(1, b2) == r, ForAll([b3], Implies(And(b3 != b1, b3 != b2, b3 >= 0, b3 < 4), Or(assignment(0, b3) != r, assignment(1, b3) != r)))))))) # Added domain constraint


# Answer Choices
options = [
    [[(0, F, S), (1, F, R), (0, G, Y), (1, G, S), (0, H, T), (1, H, Y), (0, J, R), (1, J, T)], "A"],
    [[(0, F, S), (1, F, Y), (0, G, R), (1, G, T), (0, H, Y), (1, H, S), (0, J, T), (1, J, R)], "B"],
    [[(0, F, Y), (1, F, S), (0, G, S), (1, G, R), (0, H, T), (1, H, Y), (0, J, R), (1, J, T)], "C"],
    [[(0, F, Y), (1, F, S), (0, G, T), (1, G, R), (0, H, R), (1, H, T), (0, J, S), (1, J, Y)], "D"],
    [[(0, F, Y), (1, F, T), (0, G, S), (1, G, Y), (0, H, T), (1, H, R), (0, J, R), (1, J, S)], "E"]
]

for option, letter in options:
    solver.push()
    for day, bike, rider in option:
        solver.add(assignment(day, bike) == rider) # Changed to function call
    if solver.check() == sat:
        print(f"Option {letter} is correct")
        exit()
    solver.pop()
