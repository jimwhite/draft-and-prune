from z3 import *

# Define variables
reviews = Array('reviews', IntSort(), IntSort())
reviews = [[Int(f'reviews[{i}][{j}]') for j in range(3)] for i in range(5)]

# Create solver
solver = Solver()

# Constraint 1: Review Domain
student = Int('student')
play = Int('play')
solver.add(ForAll([student, play], Implies(And(student >= 0, student < 5, play >= 0, play < 3), Or(reviews[student][play] == 0, reviews[student][play] == 1))))

# Constraint 2: Each student reviews at least one play
student = Int('student')
solver.add(ForAll([student], Implies(And(student >= 0, student < 5), Or([reviews[student][p] == 1 for p in range(3)]))))

# Constraint 3: Kramer and Lopez review fewer plays than Megregian
k_count = Int('k_count')
l_count = Int('l_count')
m_count = Int('m_count')
solver.add(k_count == Sum([reviews[1][p] for p in range(3)]))
solver.add(l_count == Sum([reviews[2][p] for p in range(3)]))
solver.add(m_count == Sum([reviews[3][p] for p in range(3)]))
solver.add(And(k_count < m_count, l_count < m_count))

# Constraint 4: Neither Lopez nor Megregian reviews any play Jiang reviews
play = Int('play')
solver.add(ForAll([play], Implies(And(play >= 0, play < 3), Implies(reviews[0][play] == 1, And(reviews[2][play] == 0, reviews[3][play] == 0)))))

# Constraint 5: Kramer and O'Neill review Tamerlane
solver.add(reviews[1][1] == 1)
solver.add(reviews[4][1] == 1)

# Constraint 6: Exactly two students review the same plays
s1 = Int('s1')
s2 = Int('s2')
s3 = Int('s3')
solver.add(Exists([s1, s2], And(s1 >= 0, s1 < 5, s2 >= 0, s2 < 5, s1 != s2,
                                ForAll([play], Implies(And(play >= 0, play < 3), reviews[s1][play] == reviews[s2][play])),
                                Not(Exists([s3], And(s3 >= 0, s3 < 5, s3 != s1, s3 != s2,
                                                    ForAll([play], Implies(And(play >= 0, play < 3), reviews[s1][play] == reviews[s3][play]))))))))


# Answer choices
options = [
    [0, 1],  # Jiang, Kramer
    [1, 4],  # Kramer, O'Neill
    [1, 2, 4],  # Kramer, Lopez, O'Neill
    [1, 3, 4],  # Kramer, Megregian, O'Neill
    [2, 3, 4]  # Lopez, Megregian, O'Neill
]

for i, option in enumerate(options):
    solver.push()
    for j in range(5):
        if j in option:
            solver.add(reviews[j][1] == 1)
        else:
            solver.add(reviews[j][1] == 0)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
