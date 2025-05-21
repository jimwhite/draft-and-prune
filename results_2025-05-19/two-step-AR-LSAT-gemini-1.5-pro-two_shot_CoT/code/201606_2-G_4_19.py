from z3 import *

# Define constants for singers
K = 0
L = 1
T = 2
W = 3
Y = 4
Z = 5

# Define the audition schedule array
audition_schedule = Array('audition_schedule', IntSort(), IntSort())

# Create the solver
solver = Solver()

# Constraint 1: Domain of audition_schedule
i = Int('i')
solver.add(ForAll(i, Implies(And(i >= 1, i <= 6), And(audition_schedule[i] >= 0, audition_schedule[i] <= 5))))

# Constraint 2: Distinctness of audition_schedule
solver.add(Distinct([audition_schedule[i] for i in range(1, 7)]))

# Constraint 3: Kammer and Lugo recordings
solver.add(Sum([If(Or(audition_schedule[i] == K, audition_schedule[i] == L), 1, 0) for i in range(1, 7)]) == 2)


def indexof(arr, val, n):
    for i in range(1, n + 1):
        if arr[i] == val:
            return i
    return n


# Constraint 4: Exactly two recordings and 5th must be recorded, 4th not recorded
K_slot = indexof(audition_schedule, K, 6)
L_slot = indexof(audition_schedule, L, 6)
solver.add(Or(K_slot == 5, L_slot == 5))
solver.add(And(K_slot != 4, L_slot != 4))
solver.add(And(K_slot > 0, K_slot < 7, L_slot > 0, L_slot < 7))
solver.add(K_slot != L_slot)


# Constraint 5: Waite before recorded
solver.add(And(indexof(audition_schedule, W, 6) < indexof(audition_schedule, K, 6),
               indexof(audition_schedule, W, 6) < indexof(audition_schedule, L, 6)))

# Constraint 6: Kammer before Trillo
solver.add(indexof(audition_schedule, K, 6) < indexof(audition_schedule, T, 6))

# Constraint 7: Zinn before Yoshida
solver.add(indexof(audition_schedule, Z, 6) < indexof(audition_schedule, Y, 6))

# Check answer choices
singers = [K, L, T, W, Z]
singer_names = ["Kammer's audition", "Lugo's audition", "Trillo's audition", "Waite's audition", "Zinn's audition"]

for idx, singer_id in enumerate(singers):
    solver.push()
    solver.add(audition_schedule[2] == singer_id)
    if solver.check() == unsat:
        print(f"Option {chr(65 + idx)} is correct")
        exit()
    solver.pop()