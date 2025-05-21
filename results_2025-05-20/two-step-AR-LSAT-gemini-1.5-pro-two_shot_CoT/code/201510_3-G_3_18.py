from z3 import *

# Define variables
schedule = Array('schedule', IntSort(), IntSort())
solver = Solver()

# Constraint 1 (Domain - implicit in array usage and constraints below)

# Constraint 2 (Each student works exactly two shifts)
for student in range(5):
    solver.add(Sum([If(schedule[slot] == student, 1, 0) for slot in range(10)]) == 2)

# Constraint 3 (Each shift is worked by exactly one student)
for slot in range(10):
    solver.add(Sum([If(schedule[slot] == student, 1, 0) for student in range(5)]) == 1)

# Constraint 4 (No student works both shifts of any day)
for day in range(5):
    solver.add(schedule[day * 2] != schedule[day * 2 + 1])

# Constraint 5 (Louise works two consecutive second shifts)
solver.add(Or([And(schedule[day * 2 + 1] == 4, schedule[(day + 1) * 2 + 1] == 4) for day in range(4)]))

# Constraint 6 (Grecia works two non-consecutive first shifts)
solver.add(Or([And(schedule[day1 * 2] == 0, schedule[day2 * 2] == 0) for day1 in range(5) for day2 in range(5) if day1 + 1 != day2 and day1 != day2]))


# Constraint 7 (Katya works on Tuesday and Friday)
solver.add(Or(schedule[1 * 2] == 3, schedule[1 * 2 + 1] == 3))
solver.add(Or(schedule[4 * 2] == 3, schedule[4 * 2 + 1] == 3))

# Constraint 8 (Hakeem and Joe work on the same day at least once)
solver.add(Or([And(Or(schedule[day * 2] == 1, schedule[day * 2 + 1] == 1), Or(schedule[day * 2] == 2, schedule[day * 2 + 1] == 2)) for day in range(5)]))

# Constraint 9 (Grecia and Louise never work on the same day)
for day in range(5):
    solver.add(Not(And(Or(schedule[day * 2] == 0, schedule[day * 2 + 1] == 0), Or(schedule[day * 2] == 4, schedule[day * 2 + 1] == 4))))

# Premise: Katya works the second shift on Tuesday
solver.add(schedule[1 * 2 + 1] == 3)

# Check answer choices
answer_choices = [
    (0, 0 * 2),  # A: Grecia works the first shift on Monday
    (1, 0 * 2),  # B: Hakeem works the first shift on Monday
    (1, 2 * 2 + 1),  # C: Hakeem works the second shift on Wednesday
    (2, 3 * 2 + 1),  # D: Joe works the second shift on Thursday
    (4, 0 * 2 + 1)   # E: Louise works the second shift on Monday
]

for i, (student, slot) in enumerate(answer_choices):
    solver.push()
    solver.add(schedule[slot] == student)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()