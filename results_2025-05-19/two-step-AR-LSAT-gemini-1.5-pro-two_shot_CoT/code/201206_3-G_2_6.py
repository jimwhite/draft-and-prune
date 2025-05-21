from z3 import *

# Encoding
P = 0
O = 1
R1 = 2
R2 = 3
S = 4
T = 5
V = 6

arrangement = Array('arrangement', IntSort(), IntSort())
solver = Solver()
x = Int('x')

# Constraint 1 (Domain)
solver.add(ForAll([x], Implies(And(x >= 1, x <= 7), And(arrangement[x] >= 0, arrangement[x] <= 6))))

# Constraint 2 (Distinctness)
solver.add(Distinct([arrangement[i] for i in range(1, 8)]))

# Constraint 3 (Pharmacy at End)
solver.add(Or(arrangement[1] == P, arrangement[7] == P))

# Constraint 4 (Restaurant at Other End)
solver.add(Or(arrangement[1] == R1, arrangement[1] == R2, arrangement[7] == R1, arrangement[7] == R2))

# Constraint 5 (Restaurants Separated)
solver.add(ForAll([x], Implies(Or(arrangement[x] == R1, arrangement[x] == R2),
                              And(Implies(x + 1 <= 7, Not(Or(arrangement[x + 1] == R1, arrangement[x + 1] == R2))),
                                  Implies(x + 2 <= 7, Not(Or(arrangement[x + 2] == R1, arrangement[x + 2] == R2)))))))

# Constraint 6 (Pharmacy Next to O or V)
solver.add(Implies(arrangement[1] == P, Or(arrangement[2] == O, arrangement[2] == V)))
solver.add(Implies(arrangement[7] == P, Or(arrangement[6] == O, arrangement[6] == V)))

# Constraint 7 (Toy Store Not Next to V)
solver.add(ForAll([x], Implies(arrangement[x] == T,
                              And(Implies(x + 1 <= 7, arrangement[x + 1] != V),
                                  Implies(x - 1 >= 1, arrangement[x - 1] != V)))))

# Answer Choices
options = [
    [P, O, S, R1, V, T, R2],
    [P, V, O, S, R1, T, R2],
    [R1, S, V, P, O, T, R2],
    [R1, T, O, R2, V, S, P],
    [R1, O, T, R2, S, V, P]
]

for option_index, option in enumerate(options):
    for r1_r2_swap in [False, True]:
        solver.push()
        if r1_r2_swap:
            option = [R2 if val == R1 else (R1 if val == R2 else val) for val in option]
        for i in range(7):
            solver.add(arrangement[i + 1] == option[i])
        if solver.check() == sat:
            print(f"Option {chr(65 + option_index)} is correct")
            exit()
        solver.pop()