from z3 import *

# Entities (as IDs)
George, Helen, Irving, Kyle, Lenore, Nina, Olivia, Robert = 0, 1, 2, 3, 4, 5, 6, 7
Monday, Tuesday, Wednesday = 0, 1, 2
Morning, Afternoon = 0, 1

# Variables
schedule = Array('schedule', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
# C1: Domain - Corrected quantifier syntax
i = Int('i') # Declare i as an Int
solver.add(ForAll(i, Implies(And(i >= 0, i < 6), And(schedule[i] >= 0, schedule[i] < 8))))

# C2: Distinctness
solver.add(Distinct([schedule[i] for i in range(6)]))

# C3: Two reports per day
day = Int('day') # Declare day as an Int
solver.add(ForAll(day, Implies(And(day >= 0, day < 3), Distinct([schedule[day * 2], schedule[day * 2 + 1]]))))

# C4: George's schedule
solver.add(Or(schedule[2] == George, schedule[3] == George))

# C5: No Olivia/Robert in afternoon
solver.add(ForAll(day, Implies(And(day >= 0, day < 3), And(schedule[day * 2 + 1] != Olivia, schedule[day * 2 + 1] != Robert))))

# C6: Nina's implication
solver.add(ForAll(day, Implies(And(day >= 0, day < 2), Implies(Or(schedule[day * 2] == Nina, schedule[day * 2 + 1] == Nina), And(Or(schedule[(day + 1) * 2] == Helen, schedule[(day + 1) * 2 + 1] == Helen), Or(schedule[(day + 1) * 2] == Irving, schedule[(day + 1) * 2 + 1] == Irving))))))


# Helper function for same day check
def SameDay(day, s1, s2):
    return Or(And(schedule[day * 2] == s1, schedule[day * 2 + 1] == s2), And(schedule[day * 2] == s2, schedule[day * 2 + 1] == s1))

# Answer choices
pairs = [(George, Lenore), (Helen, Nina), (Irving, Robert), (Kyle, Nina), (Olivia, Kyle)]
options = ["A", "B", "C", "D", "E"]

# Check each pair
for i, (s1, s2) in enumerate(pairs):
    solver.push()
    solver.add(Or(SameDay(Monday, s1, s2), SameDay(Tuesday, s1, s2)))
    if solver.check() == unsat:
        print(f"Option {options[i]} is correct")
        exit()
    solver.pop()
