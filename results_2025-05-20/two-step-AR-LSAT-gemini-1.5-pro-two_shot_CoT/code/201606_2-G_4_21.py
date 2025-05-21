from z3 import *

# Define constants for singers
K = 0
L = 1
T = 2
W = 3
Y = 4
Z = 5

# Define variables
audition_schedule = Array('audition_schedule', IntSort(), IntSort())
recorded_singer = Array('recorded_singer', IntSort(), BoolSort())
i = Int('i')
j = Int('j')

# Create solver and add constraints
solver = Solver()

# Constraint 1: Domain of audition_schedule
solver.add(ForAll(i, Implies(And(i >= 1, i <= 6), And(audition_schedule[i] >= 0, audition_schedule[i] <= 5))))

# Constraint 2: Distinctness of audition_schedule
solver.add(Distinct([audition_schedule[i] for i in range(1, 7)]))

# Constraint 3 & 4: Recorded singers
solver.add(recorded_singer[K] == True)
solver.add(recorded_singer[L] == True)
solver.add(recorded_singer[T] == False)
solver.add(recorded_singer[W] == False)
solver.add(recorded_singer[Y] == False)
solver.add(recorded_singer[Z] == False)

# Constraint 5: Fourth audition not recorded
solver.add(recorded_singer[audition_schedule[4]] == False)

# Constraint 6: Fifth audition is recorded
solver.add(recorded_singer[audition_schedule[5]] == True)

# Constraint 7: Waite before recorded
solver.add(ForAll([i, j], Implies(And(i >= 1, i <= 6, j >= 1, j <= 6, audition_schedule[i] == W, recorded_singer[audition_schedule[j]] == True), i < j)))

# Constraint 8: Kammer before Trillo
solver.add(ForAll([i, j], Implies(And(i >= 1, i <= 6, j >= 1, j <= 6, audition_schedule[i] == K, audition_schedule[j] == T), i < j)))

# Constraint 9: Zinn before Yoshida
solver.add(ForAll([i, j], Implies(And(i >= 1, i <= 6, j >= 1, j <= 6, audition_schedule[i] == Z, audition_schedule[j] == Y), i < j)))

# Constraint 10: Kammer immediately before Yoshida
solver.add(ForAll(i, Implies(And(i >= 1, i <= 5, audition_schedule[i] == K), audition_schedule[i+1] == Y)))

# Check answer choices
answer_choices = [
    (2, K),  # Kammer's audition is second.
    (4, T),  # Trillo's audition is fourth.
    (3, W),  # Waite's audition is third.
    (6, Y),  # Yoshida's audition is sixth.
    (2, Z)   # Zinn's audition is second.
]
option_letter = 'A'
for slot, singer in answer_choices:
    solver.push()
    solver.add(audition_schedule[slot] == singer)
    if solver.check() == sat:
        print(f"Option {option_letter} is correct")
        exit()
    solver.pop()
    option_letter = chr(ord(option_letter) + 1)