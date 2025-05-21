from z3 import *

# Define variables
member = Array('member', IntSort(), BoolSort())
leader = Int('leader')

# Define solver and add constraints
solver = Solver()
solver.add(Sum([If(member[i], 1, 0) for i in range(7)]) == 3)  # Constraint 1
solver.add(member[leader])  # Constraint 2
solver.add(And([Implies(member[i], leader == i) for i in [0, 1]]))  # Constraint 3
solver.add(Implies(member[2], member[3]))  # Constraint 4
solver.add(Implies(member[5], Not(Or(member[1], member[4]))))  # Constraint 5

# Answer choices
choices = [
    [1, 3, 5],  # Ruiz (leader), Taylor, Wells
    [4, 0, 3],  # Verma (leader), Quinn, Taylor
    [4, 2, 3],  # Verma (leader), Smith, Taylor
    [4, 2, 6],  # Verma (leader), Smith, Xue
    [6, 4, 5]   # Xue (leader), Verma, Wells
]

# Check each answer choice
for i, choice in enumerate(choices):
    solver.push()
    solver.add(leader == choice[0])
    for j in choice:
        solver.add(member[j])
    for j in range(7):
        if j not in choice:
            solver.add(Not(member[j]))
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()