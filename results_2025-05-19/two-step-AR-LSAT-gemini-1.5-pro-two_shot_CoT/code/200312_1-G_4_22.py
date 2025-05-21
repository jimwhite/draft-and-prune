from z3 import *

# Variables
reviews = [[Bool(f'reviews[{i}][{j}]') for j in range(3)] for i in range(5)]

# Solver
solver = Solver()

# Constraint 1 (Review Counts)
kramer_count = Sum([If(reviews[1][i], 1, 0) for i in range(3)])
lopez_count = Sum([If(reviews[2][i], 1, 0) for i in range(3)])
megregian_count = Sum([If(reviews[3][i], 1, 0) for i in range(3)])
solver.add(And(kramer_count < megregian_count, lopez_count < megregian_count))

# Constraint 2 (Jiang Exclusion)
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 0, i < 3), Implies(reviews[0][i], Not(Or(reviews[2][i], reviews[3][i]))))))

# Constraint 3 (Kramer and O'Neill review Tamerlane)
solver.add(And(reviews[1][1], reviews[4][1]))

# Constraint 4 (Exactly two students review the same plays)
s1 = Int('s1')
s2 = Int('s2')
s3 = Int('s3')
p = Int('p')
solver.add(Exists([s1, s2], And(s1 != s2, s1 < 5, s2 < 5,
                                ForAll([p], Implies(And(p >= 0, p < 3), reviews[s1][p] == reviews[s2][p])),
                                ForAll([s3], Implies(And(s3 != s1, s3 != s2, s3 < 5),
                                                    Exists([p], And(p >= 0, p < 3, reviews[s3][p] != reviews[s1][p])))))))

# Constraint 5 (Each student reviews at least one play)
s = Int('s')
solver.add(ForAll([s], Implies(And(s >= 0, s < 5), Or(reviews[s][0], reviews[s][1], reviews[s][2]))))


# Answer choices
options = [
    [0, 1],  # Jiang, Kramer
    [1, 4],  # Kramer, O'Neill
    [1, 2, 4],  # Kramer, Lopez, O'Neill
    [1, 3, 4],  # Kramer, Megregian, O'Neill
    [2, 3, 4]  # Lopez, Megregian, O'Neill
]

option_labels = ['A', 'B', 'C', 'D', 'E']

for idx, option in enumerate(options):
    solver.push()
    # Add constraints for the current option
    for student_id in option:
        solver.add(reviews[student_id][1])
    for student_id in range(5):
        if student_id not in option:
            solver.add(Not(reviews[student_id][1]))

    if solver.check() == sat:
        print(f"Option {option_labels[idx]} is correct")
        exit()
    solver.pop()
