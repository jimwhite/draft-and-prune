from z3 import *

# Define singers and audition slots
K, L, T, W, Y, Z = 0, 1, 2, 3, 4, 5
singers = [K, L, T, W, Y, Z]

# Define Z3 variables
audition_schedule = Array('audition_schedule', IntSort(), IntSort())
i, j, k = Ints('i j k')

# Create solver and add constraints
solver = Solver()

# Constraint 1: Domain
solver.add(ForAll([i], Implies(And(i >= 1, i <= 6), And(audition_schedule[i] >= 0, audition_schedule[i] <= 5))))

# Constraint 2: Distinctness
solver.add(Distinct([audition_schedule[i] for i in range(1, 7)]))

# Constraint 3: Recorded Auditions
solver.add(Or(audition_schedule[5] == K, audition_schedule[5] == L))

# Constraint 4: Fourth Audition Not Recorded
solver.add(And(audition_schedule[4] != K, audition_schedule[4] != L))

# Constraint 5: Waite Before Recorded
solver.add(ForAll([i, j, k], Implies(And(audition_schedule[i] == W, audition_schedule[j] == K, audition_schedule[k] == L), And(i < j, i < k))))

# Constraint 6: Kammer Before Trillo
solver.add(ForAll([i, j], Implies(And(audition_schedule[i] == K, audition_schedule[j] == T), i < j)))

# Constraint 7: Zinn Before Yoshida
solver.add(ForAll([i, j], Implies(And(audition_schedule[i] == Z, audition_schedule[j] == Y), i < j)))


# Check answer choices
options = [K, L, T, W, Z]
option_labels = ["A", "B", "C", "D", "E"]

for idx, singer in enumerate(options):
    solver.push()
    solver.add(audition_schedule[2] == singer)
    if solver.check() == unsat:
        print(f"Option {option_labels[idx]} is correct")
        exit()
    solver.pop()