from z3 import *

# Define singers and slots
K, L, T, W, Y, Z = 0, 1, 2, 3, 4, 5
singers = [K, L, T, W, Y, Z]
slots = list(range(1, 7))

# Define the audition schedule variable (Z3 array)
audition_schedule = Array('audition_schedule', IntSort(), IntSort())

# Create the solver
solver = Solver()

# Constraint 1: Domain of audition_schedule
i = Int('i')
solver.add(ForAll(i, Implies(And(i >= 1, i <= 6), And(audition_schedule[i] >= 0, audition_schedule[i] <= 5))))

# Constraint 2: Distinctness of audition_schedule
solver.add(Distinct([audition_schedule[i] for i in range(1, 7)]))

# Constraint 4: Fourth audition not recorded
solver.add(And(audition_schedule[4] != K, audition_schedule[4] != L))

# Constraint 7: Kammer before Trillo
j = Int('j')  # Define j for use in quantifier
solver.add(ForAll(i, Implies(audition_schedule[i] == K, ForAll(j, Implies(audition_schedule[j] == T, i < j)))))

# Constraint 8: Zinn before Yoshida
k = Int('k')  # Define k for use in quantifier (distinct from i and j)
solver.add(ForAll(i, Implies(audition_schedule[i] == Z, ForAll(k, Implies(audition_schedule[k] == Y, i < k)))))

# Constraint 9: Kammer immediately before Yoshida
solver.add(ForAll(i, Implies(And(i >= 1, i <= 5, audition_schedule[i] == K), audition_schedule[i + 1] == Y)))


# Iterate through possible second recorded slots (1, 2, 3, 6)
for j in [1, 2, 3, 6]:
    solver.push()

    # Constraint 3: Kammer and Lugo are recorded (using current j)
    solver.add(Or(And(audition_schedule[5] == K, audition_schedule[j] == L), And(audition_schedule[5] == L, audition_schedule[j] == K)))

    # Constraint 6: Waite before recorded (using current j)
    solver.add(ForAll(i, Implies(audition_schedule[i] == W, And(i < 5, i < j))))

    # Check answer choices
    answer_choices = [
        (lambda: audition_schedule[2] == K, "A"),  # Kammer's audition is second.
        (lambda: audition_schedule[4] == T, "B"),  # Trillo's audition is fourth.
        (lambda: audition_schedule[3] == W, "C"),  # Waite's audition is third.
        (lambda: audition_schedule[6] == Y, "D"),  # Yoshida's audition is sixth.
        (lambda: audition_schedule[2] == Z, "E")   # Zinn's audition is second.
    ]
    for constraint, option in answer_choices:
        solver.push()
        solver.add(constraint())
        if solver.check() == sat:
            print(f"Option {option} is correct")
            exit()
        solver.pop()

    solver.pop()

