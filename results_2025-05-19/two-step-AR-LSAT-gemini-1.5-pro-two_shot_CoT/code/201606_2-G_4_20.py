from z3 import *

# Define constants for singer IDs
K = 0
L = 1
T = 2
W = 3
Y = 4
Z = 5

# Define variables
audition_schedule = Array('audition_schedule', IntSort(), IntSort())
recorded = Array('recorded', IntSort(), BoolSort())

# Create solver
solver = Solver()

# Constraint 1: Domain of audition_schedule
i = Int('i')
solver.add(ForAll(i, Implies(And(i >= 1, i <= 6), And(audition_schedule[i] >= 0, audition_schedule[i] <= 5))))

# Constraint 2: Distinctness of audition_schedule
solver.add(Distinct([audition_schedule[i] for i in range(1, 7)]))

# Constraint 3 & 4: Recorded auditions
s = Int('s')
solver.add(recorded[K] == True)
solver.add(recorded[L] == True)
solver.add(ForAll(s, Implies(And(s != K, s != L), recorded[s] == False)))


# Constraint 5 & 6: Fourth and Fifth auditions
solver.add(recorded[audition_schedule[4]] == False)
solver.add(recorded[audition_schedule[5]] == True)

# Constraint 7: Waite before recorded
i = Int('i')
j = Int('j')
solver.add(ForAll(i, Implies(And(i >= 1, i <= 6), Implies(recorded[audition_schedule[i]] == True,
                                                              ForAll(j, Implies(And(j >= 1, j <= 6),
                                                                                 Implies(audition_schedule[j] == W, j < i)))))))

# Constraint 8: Kammer before Trillo
i = Int('i')
j = Int('j')
solver.add(ForAll(i, Implies(And(i >= 1, i <= 6), Implies(audition_schedule[i] == K,
                                                              ForAll(j, Implies(And(j >= 1, j <= 6),
                                                                                 Implies(audition_schedule[j] == T, i < j)))))))

# Constraint 9: Zinn before Yoshida
i = Int('i')
j = Int('j')
solver.add(ForAll(i, Implies(And(i >= 1, i <= 6), Implies(audition_schedule[i] == Z,
                                                              ForAll(j, Implies(And(j >= 1, j <= 6),
                                                                                 Implies(audition_schedule[j] == Y, i < j)))))))


# Check answer choices
singer_options = [T, L, T, W, Z]  # Singer IDs corresponding to answer choices
option_letters = ['A', 'B', 'C', 'D', 'E']

for idx, singer_id in enumerate(singer_options):
    solver.push()
    solver.add(audition_schedule[6] == singer_id)
    if solver.check() == sat:
        print(f"Option {option_letters[idx]} is correct")
        exit()
    solver.pop()