from z3 import *

# Define variables
schedule = Array('schedule', IntSort(), Array(IntSort(), IntSort()))
solver = Solver()

# Constraint 1: Domain
d = Int('d')
s = Int('s')
solver.add(ForAll([d, s], Implies(And(d >= 0, d < 5, s >= 0, s < 2), And(schedule[d][s] >= 0, schedule[d][s] < 5))))

# Constraint 2: Each student works exactly two shifts
student = Int('student')
solver.add(ForAll([student], Implies(And(student >= 0, student < 5), Sum([If(schedule[d][s] == student, 1, 0) for d in range(5) for s in range(2)]) == 2)))

# Constraint 3: No student works both shifts of any day
solver.add(ForAll([d], Implies(And(d >= 0, d < 5), schedule[d][0] != schedule[d][1])))

# Constraint 4: Louise works second shift on two consecutive days
d = Int('d')
solver.add(Exists([d], And(d >= 0, d < 4, schedule[d][1] == 4, schedule[d+1][1] == 4)))

# Constraint 5: Grecia works first shift on two non-consecutive days
d1 = Int('d1')
d2 = Int('d2')
solver.add(Exists([d1, d2], And(d1 >= 0, d1 < 5, d2 >= 0, d2 < 5, schedule[d1][0] == 0, schedule[d2][0] == 0, d1 != d2, Or(d1 > d2 + 1, d2 > d1 + 1))))

# Constraint 6: Katya works on Tuesday and Friday
solver.add(Or(schedule[1][0] == 3, schedule[1][1] == 3))
solver.add(Or(schedule[4][0] == 3, schedule[4][1] == 3))

# Constraint 7: Hakeem and Joe work on the same day at least once
d = Int('d')
solver.add(Exists([d], And(d >= 0, d < 5, Or(schedule[d][0] == 1, schedule[d][1] == 1), Or(schedule[d][0] == 2, schedule[d][1] == 2))))

# Constraint 8: Grecia and Louise never work on the same day
d = Int('d')
solver.add(ForAll([d], Implies(And(d >= 0, d < 5), Not(Or(And(schedule[d][0] == 0, schedule[d][1] == 4), And(schedule[d][1] == 0, schedule[d][0] == 4), And(schedule[d][0] == 0, schedule[d][0] == 4), And(schedule[d][1] == 0, schedule[d][1] == 4)))))) # Corrected the logic here


# Check answer choices
choices = [
    [1, 4, 4, 1, 3],
    [2, 1, 0, 4, 4],
    [2, 3, 1, 4, 3],
    [4, 3, 2, 4, 3],
    [4, 4, 1, 2, 2]
]

for i, choice in enumerate(choices):
    solver.push()
    for day in range(5):
        solver.add(schedule[day][1] == choice[day])
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
