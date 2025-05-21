from z3 import *

# Variables
schedule = Array('schedule', IntSort(), IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints

# Constraint 1 (Domain)
c = Int('c')
b = Int('b')
domain_c = And(c >= 0, c < 3)
domain_b = And(b >= 0, b < 3)
# Fixed: Accessing 2D array requires two indices
Constraint1 = ForAll([c, b], Implies(And(domain_c, domain_b), And(schedule[c, b] >= 0, schedule[c, b] < 5)))
solver.add(Constraint1)

# Constraint 2 (No two batches of the same kind on the same day)
b1 = Int('b1')
b2 = Int('b2')
domain_b1 = And(b1 >= 0, b1 < 3)
domain_b2 = And(b2 >= 0, b2 < 3)
# Fixed: Accessing 2D array requires two indices
Constraint2 = ForAll([c, b1, b2], Implies(And(domain_c, domain_b1, domain_b2, b1 != b2), schedule[c, b1] != schedule[c, b2]))
solver.add(Constraint2)

# Constraint 3 (At least one batch on Monday)
Constraint3 = Exists([c, b], And(domain_c, domain_b, schedule[c, b] == 0))
solver.add(Constraint3)

# Constraint 4 (Oatmeal 2nd batch and Peanut Butter 1st batch on same day)
# Fixed: Accessing 2D array requires two indices
Constraint4 = schedule[0, 1] == schedule[1, 0]
solver.add(Constraint4)

# Constraint 5 (Sugar 2nd batch on Thursday)
# Fixed: Accessing 2D array requires two indices
Constraint5 = schedule[2, 1] == 3
solver.add(Constraint5)

# Constraint 6 (No batches on Wednesday)
# Fixed: Accessing 2D array requires two indices
Constraint6 = ForAll([c, b], Implies(And(domain_c, domain_b), schedule[c, b] != 2))
solver.add(Constraint6)

# Helper function
def count_on_day(d):
    # Fixed: Accessing 2D array requires two indices
    return Sum([If(schedule[c, b] == d, 1, 0) for c in range(3) for b in range(3)])

# Answer choices
ChoiceA = (count_on_day(1) == 3)
ChoiceB = (count_on_day(4) == 3)
ChoiceC = (count_on_day(0) >= 2)
ChoiceD = (count_on_day(3) >= 2)
ChoiceE = (count_on_day(0) < count_on_day(1))

choices = [ChoiceA, ChoiceB, ChoiceC, ChoiceD, ChoiceE]
choice_names = ['A', 'B', 'C', 'D', 'E']

for i in range(len(choices)):
    choice = choices[i]
    choice_name = choice_names[i]
    solver.push()
    solver.add(Not(choice))
    if solver.check() == unsat:
        print(f"Option {choice_name} is correct")
        exit()
    solver.pop()
