from z3 import *

# Variables
schedule = Array('schedule', IntSort(), IntSort())
F, G, H, I, J = 0, 1, 2, 3, 4
M, T, W = 0, 1, 2
w = Int('w')

# Solver and base constraints
solver = Solver()
solver.add(ForAll([w], And(schedule[w] >= 0, schedule[w] <= 2)))
solver.add(Distinct([schedule[w] for w in range(5)]))
solver.add(schedule[F] != schedule[G])
solver.add(schedule[I] == W)
solver.add(Sum([If(schedule[w] == T, 1, 0) for w in range(5)]) == 2)
solver.add(schedule[H] != M)
solver.add(schedule[J] == M)


# Check answer choices
answer_choices = [
    (schedule[F] == W),  # A
    (schedule[H] == T),  # B
    (schedule[G] == T),  # C
    (schedule[F] == schedule[H]),  # D
    (schedule[G] == schedule[H])   # E
]

for i, choice in enumerate(answer_choices):
    solver.push()
    solver.add(Not(choice))
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()