from z3 import *

# Define variables
audition_slot = Array('audition_slot', IntSort(), IntSort())
singers = ["K", "L", "T", "W", "Y", "Z"]
solver = Solver()

# Constraint 1: Domain of audition_slot
i = Int('i')
solver.add(ForAll(i, Implies(And(i >= 0, i < 6), And(audition_slot[i] >= 0, audition_slot[i] < 6))))

# Constraint 2: Distinctness of audition_slot
solver.add(Distinct([audition_slot[i] for i in range(6)]))

# Constraint 3: 4th not recorded
solver.add(Or(audition_slot[2] == 3, audition_slot[3] == 3, audition_slot[4] == 3, audition_slot[5] == 3))

# Constraint 4: 5th is recorded
solver.add(Or(audition_slot[0] == 4, audition_slot[1] == 4))

# Constraint 5: Waite before recorded
solver.add(And(audition_slot[3] < audition_slot[0], audition_slot[3] < audition_slot[1]))

# Constraint 6: Kammer before Trillo
solver.add(audition_slot[0] < audition_slot[2])

# Constraint 7: Zinn before Yoshida
solver.add(audition_slot[5] < audition_slot[4])

# Check answer choices
answers = ["fifth", "fourth", "third", "second", "first"]
for idx, ans in enumerate(answers):
    solver.push()
    if ans == "fifth":
        solver.add(audition_slot[4] == 4)
    elif ans == "fourth":
        solver.add(audition_slot[4] == 3)
    elif ans == "third":
        solver.add(audition_slot[4] == 2)
    elif ans == "second":
        solver.add(audition_slot[4] == 1)
    elif ans == "first":
        solver.add(audition_slot[4] == 0)

    if solver.check() == sat:
        print(f"Option {chr(65 + idx)} is correct")
        exit()
    solver.pop()