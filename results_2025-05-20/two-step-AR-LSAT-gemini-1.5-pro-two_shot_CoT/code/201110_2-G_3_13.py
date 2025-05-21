from z3 import *

# Define constants for riders and bicycles
R, S, T, Y = 0, 1, 2, 3
F, G, H, J = 0, 1, 2, 3

# Define the assignment variable as a 2D array
assignment = [[Int(f"assignment[{d}][{b}]") for b in range(4)] for d in range(2)]

# Create the solver
solver = Solver()

# Constraint 1: Domain
for d in range(2):
    for b in range(4):
        solver.add(assignment[d][b] >= 0, assignment[d][b] < 4)

# Constraint 2: Bijection
for d in range(2):
    solver.add(Distinct(assignment[d][F], assignment[d][G], assignment[d][H], assignment[d][J]))

# Constraint 3: Reynaldo cannot test F
for d in range(2):
    solver.add(assignment[d][F] != R)

# Constraint 4: Yuki cannot test J
for d in range(2):
    solver.add(assignment[d][J] != Y)

# Constraint 5: Theresa must test H
solver.add(Or(assignment[0][H] == T, assignment[1][H] == T))

# Constraint 6: Yuki's first day bike is Seamus's second day bike
solver.add(Or(And(assignment[0][F] == Y, assignment[1][F] == S),
               And(assignment[0][G] == Y, assignment[1][G] == S),
               And(assignment[0][H] == Y, assignment[1][H] == S),
               And(assignment[0][J] == Y, assignment[1][J] == S)))

# Constraint 7: Each rider tests different bike on day 2
for r in range(4):
    solver.add(Or(And(assignment[0][F] == r, assignment[1][G] == r),
                   And(assignment[0][F] == r, assignment[1][H] == r),
                   And(assignment[0][F] == r, assignment[1][J] == r),
                   And(assignment[0][G] == r, assignment[1][F] == r),
                   And(assignment[0][G] == r, assignment[1][H] == r),
                   And(assignment[0][G] == r, assignment[1][J] == r),
                   And(assignment[0][H] == r, assignment[1][F] == r),
                   And(assignment[0][H] == r, assignment[1][G] == r),
                   And(assignment[0][H] == r, assignment[1][J] == r),
                   And(assignment[0][J] == r, assignment[1][F] == r),
                   And(assignment[0][J] == r, assignment[1][G] == r),
                   And(assignment[0][J] == r, assignment[1][H] == r)))


# Answer choices
options = [
    "F: Seamus, Reynaldo; G: Yuki, Seamus; H: Theresa, Yuki; J: Reynaldo, Theresa",
    "F: Seamus, Yuki; G: Reynaldo, Theresa; H: Yuki, Seamus; J: Theresa, Reynaldo",
    "F: Yuki, Seamus; G: Seamus, Reynaldo; H: Theresa, Yuki; J: Reynaldo, Theresa",
    "F: Yuki, Seamus; G: Theresa, Reynaldo; H: Reynaldo, Theresa; J: Seamus, Yuki",
    "F: Yuki, Theresa; G: Seamus, Yuki; H: Theresa, Reynaldo; J: Reynaldo, Seamus"
]

for i, option in enumerate(options):
    solver.push()
    for bike_assignment in option.split(';'):
        bike_str, riders_str = bike_assignment.strip().split(':')
        bike = {'F': F, 'G': G, 'H': H, 'J': J}[bike_str.strip()]
        rider1_str, rider2_str = riders_str.strip().split(',')
        rider1 = {'Reynaldo': R, 'Seamus': S, 'Theresa': T, 'Yuki': Y}[rider1_str.strip()]
        rider2 = {'Reynaldo': R, 'Seamus': S, 'Theresa': T, 'Yuki': Y}[rider2_str.strip()]
        solver.add(assignment[0][bike] == rider1)
        solver.add(assignment[1][bike] == rider2)

    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()

