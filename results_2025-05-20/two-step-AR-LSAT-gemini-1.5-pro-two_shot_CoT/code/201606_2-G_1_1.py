from z3 import *

# Define variables
member = Array('member', IntSort(), BoolSort())
leader = Int('leader')

# Define solver and add constraints
solver = Solver()

# Constraint 1: Exactly 3 members
solver.add(Sum([If(member[i], 1, 0) for i in range(7)]) == 3)

# Constraint 2: Leader is a member
solver.add(And([Implies(leader == i, member[i]) for i in range(7)]))

# Constraint 3: Quinn/Ruiz leader constraint
solver.add(And([Implies(member[i], leader == i) for i in [0, 1]]))

# Constraint 4: Smith/Taylor constraint
solver.add(Implies(member[2], member[3]))

# Constraint 5: Wells/Ruiz/Verma constraint
solver.add(Implies(member[5], Not(Or(member[1], member[4]))))

# Answer choices
choices = [
    [1, 3, 5],  # Ruiz (leader), Taylor, Wells
    [4, 0, 3],  # Verma (leader), Quinn, Taylor
    [4, 2, 3],  # Verma (leader), Smith, Taylor
    [4, 2, 6],  # Verma (leader), Smith, Xue
    [6, 4, 5]   # Xue (leader), Verma, Wells
]

for i, choice in enumerate(choices):
    solver.push()
    solver.add(leader == choice[0])
    for j in range(7):
        if j in choice:
            solver.add(member[j] == True)
        else:
            solver.add(member[j] == False)

    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()