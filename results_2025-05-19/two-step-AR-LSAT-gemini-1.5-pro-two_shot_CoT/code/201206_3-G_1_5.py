from z3 import *

# Entities
J = 0
K = 1
L = 2
N = 3
O = 4
R = 5
W = 0
T = 1
F = 2
M = 0
A = 1

# Variables
assignment = Array('assignment', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
i = Int('i')
solver.add(ForAll([i], And(assignment[i] >= 0, assignment[i] < 6)))  # Domain

solver.add(Distinct([assignment[i] for i in range(6)]))  # Distinctness

solver.add(Or(And(assignment[0] == K, assignment[1] == R), And(assignment[1] == K, assignment[0] == R),
            And(assignment[2] == K, assignment[3] == R), And(assignment[3] == K, assignment[2] == R),
            And(assignment[4] == K, assignment[5] == R), And(assignment[5] == K, assignment[4] == R)))  # Kevin & Rebecca

solver.add(Or(
    And(assignment[0] == L, Or(assignment[2] == O, assignment[3] == O, assignment[4] == O, assignment[5] == O)),
    And(assignment[1] == L, Or(assignment[2] == O, assignment[3] == O, assignment[4] == O, assignment[5] == O)),
    And(assignment[2] == L, Or(assignment[0] == O, assignment[1] == O, assignment[4] == O, assignment[5] == O)),
    And(assignment[3] == L, Or(assignment[0] == O, assignment[1] == O, assignment[4] == O, assignment[5] == O)),
    And(assignment[4] == L, Or(assignment[0] == O, assignment[1] == O, assignment[2] == O, assignment[3] == O)),
    And(assignment[5] == L, Or(assignment[0] == O, assignment[1] == O, assignment[2] == O, assignment[3] == O)),
    And(assignment[0] == O, Or(assignment[2] == L, assignment[3] == L, assignment[4] == L, assignment[5] == L)),
    And(assignment[1] == O, Or(assignment[2] == L, assignment[3] == L, assignment[4] == L, assignment[5] == L)),
    And(assignment[2] == O, Or(assignment[0] == L, assignment[1] == L, assignment[4] == L, assignment[5] == L)),
    And(assignment[3] == O, Or(assignment[0] == L, assignment[1] == L, assignment[4] == L, assignment[5] == L)),
    And(assignment[4] == O, Or(assignment[0] == L, assignment[1] == L, assignment[2] == L, assignment[3] == L)),
    And(assignment[5] == O, Or(assignment[0] == L, assignment[1] == L, assignment[2] == L, assignment[3] == L))
))  # Lan & Olivia


solver.add(Or(assignment[1] == N, assignment[3] == N, assignment[5] == N))  # Nessa

i = Int('i')
j = Int('j')
solver.add(ForAll([i, j], Implies(And(assignment[i] == J, assignment[j] == O), i < j)))  # Julio before Olivia

# Julio leads Thursday afternoon
solver.add(assignment[3] == J)

# Count determined assistants
determined_count = 0
for assistant_id in [K, L, N, O, R]:
    possible_slots = [s for s in range(6) if s != 3]
    while possible_slots:
        s = possible_slots.pop()
        solver.push()
        solver.add(assignment[s] == assistant_id)
        if solver.check() == unsat:
            solver.pop()
        else:
            solver.push()
            solver.add(assignment[s] != assistant_id)
            if solver.check() == unsat:
                determined_count += 1
                solver.pop()
                break
            solver.pop()

if determined_count == 1:
    print("Option A is correct")
elif determined_count == 2:
    print("Option B is correct")
elif determined_count == 3:
    print("Option C is correct")
elif determined_count == 4:
    print("Option D is correct")
elif determined_count == 5:
    print("Option E is correct")