from z3 import *

# Define variables
schedule = Array('schedule', IntSort(), IntSort())
solver = Solver()

# Constraint 1 (Domain)
for d in range(5):
    for s in range(2):
        solver.add(And(schedule[d * 2 + s] >= 0, schedule[d * 2 + s] < 5))

# Constraint 2 (Each student works exactly two shifts)
for student in range(5):
    solver.add(Sum([If(schedule[d * 2 + s] == student, 1, 0) for d in range(5) for s in range(2)]) == 2)

# Constraint 3 (Each shift is worked by exactly one student)
for d in range(5):
    solver.add(Distinct([schedule[d * 2 + 0], schedule[d * 2 + 1]]))

# Constraint 5 (Louise works two consecutive second shifts)
solver.add(Or([And(schedule[d * 2 + 1] == 4, schedule[(d + 1) * 2 + 1] == 4) for d in range(4)]))

# Constraint 6 (Grecia works two non-consecutive first shifts)
solver.add(Or([And(schedule[d1 * 2 + 0] == 0, schedule[d2 * 2 + 0] == 0) for d1 in range(5) for d2 in range(5) if (d1 != d2 and abs(d1 - d2) != 1)]))

# Constraint 7 (Katya works on Tuesday and Friday)
solver.add(Or(schedule[1 * 2 + 0] == 3, schedule[1 * 2 + 1] == 3))
solver.add(Or(schedule[4 * 2 + 0] == 3, schedule[4 * 2 + 1] == 3))

# Constraint 8 (Hakeem and Joe work on the same day at least once)
solver.add(Or([Or(And(schedule[d * 2 + 0] == 1, schedule[d * 2 + 1] == 2), And(schedule[d * 2 + 0] == 2, schedule[d * 2 + 1] == 1)) for d in range(5)]))

# Constraint 9 (Grecia and Louise never work on the same day)
for d in range(5):
    solver.add(Not(Or(And(schedule[d * 2 + 0] == 0, schedule[d * 2 + 1] == 4), And(schedule[d * 2 + 1] == 0, schedule[d * 2 + 0] == 4))))

# Constraint 10 (Grecia and Joe work on the same day at least once)
solver.add(Or([Or(And(schedule[d * 2 + 0] == 0, schedule[d * 2 + 1] == 2), And(schedule[d * 2 + 0] == 2, schedule[d * 2 + 1] == 0)) for d in range(5)]))

# Check answer choices
answer_choices = [
    (1, 0, 0),  # Grecia works the first shift on Tuesday
    (0, 1, 1),  # Hakeem works the second shift on Monday
    (2, 1, 1),  # Hakeem works the second shift on Wednesday
    (2, 0, 2),  # Joe works the first shift on Wednesday
    (3, 0, 2)   # Joe works the first shift on Thursday
]

for i, (day, shift, student) in enumerate(answer_choices):
    solver.push()
    solver.add(schedule[day * 2 + shift] == student)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()