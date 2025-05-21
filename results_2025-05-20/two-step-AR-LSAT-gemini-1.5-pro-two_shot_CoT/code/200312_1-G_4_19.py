from z3 import *

# Define variables
reviews = [[Bool(f"reviews[{s}][{p}]") for p in range(3)] for s in range(5)]
num_plays_reviewed = [Int(f"num_plays_reviewed[{s}]") for s in range(5)]

solver = Solver()

# Constraint 1: Each student reviews at least one play
for s in range(5):
    solver.add(Or(reviews[s][0], reviews[s][1], reviews[s][2]))

# Constraint 2: Kramer and Lopez review fewer plays than Megregian
solver.add(And(num_plays_reviewed[1] < num_plays_reviewed[3], num_plays_reviewed[2] < num_plays_reviewed[3]))

# Constraint 3: Neither Lopez nor Megregian reviews any play Jiang reviews
for p in range(3):
    solver.add(Implies(reviews[0][p], And(Not(reviews[2][p]), Not(reviews[3][p]))))

# Constraint 4: Kramer and O'Neill both review Tamerlane
solver.add(And(reviews[1][1], reviews[4][1]))

# Constraint 5: Exactly two students review the same plays
solver.add(Exists([k, l], And(k >= 0, k < 5, l >= 0, l < 5, k != l,
                             And([reviews[k][p] == reviews[l][p] for p in range(3)]),
                             ForAll([m], Implies(And(m >= 0, m < 5, m != k, m != l),
                                                Not(And([reviews[k][p] == reviews[l][p] for p in range(3)]))))))
k = Int('k') # Define k and l outside the Exists scope
l = Int('l')
m = Int('m')


# Constraint 6: Calculate number of plays reviewed
for s in range(5):
    solver.add(num_plays_reviewed[s] == Sum([If(reviews[s][p], 1, 0) for p in range(3)]))

# Answer choices
options = [
    [2],  # Lopez
    [4],  # O'Neill
    [0, 2],  # Jiang, Lopez
    [1, 4],  # Kramer, O'Neill
    [2, 3]  # Lopez, Megregian
]

option_labels = ['A', 'B', 'C', 'D', 'E']

for i, option in enumerate(options):
    solver.push()
    for student in option:
        solver.add(reviews[student][0])  # Reviews Sunset
        solver.add(Not(reviews[student][1]))  # Doesn't review Tamerlane
        solver.add(Not(reviews[student][2]))  # Doesn't review Undulation

    other_students = [s for s in range(5) if s not in option]
    for student in other_students:
        solver.add(Or(Not(reviews[student][0]), reviews[student][1], reviews[student][2])) # Doesn't review only Sunset

    if solver.check() == sat:
        print(f"Option {option_labels[i]} is correct")
        exit()
    solver.pop()

