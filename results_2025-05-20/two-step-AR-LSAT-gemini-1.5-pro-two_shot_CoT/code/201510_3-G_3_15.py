from z3 import *

# Variables
schedule = Array('schedule', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraint 1 (Domain)
for d in range(5):
    for s in range(2):
        solver.add(And(schedule[d * 2 + s] >= 0, schedule[d * 2 + s] < 5))

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
solver.add(Or([And(schedule[day1 * 2] == 0, schedule[day2 * 2] == 0) for day1 in range(5) for day2 in range(5) if day1 != day2 and day1 + 1 != day2 and day2 + 1 != day1]))

# Constraint 7 (Katya works on Tuesday and Friday)
solver.add(Or(schedule[1*2] == 3, schedule[1*2+1] == 3))
solver.add(Or(schedule[4*2] == 3, schedule[4*2+1] == 3))


# Constraint 8 (Hakeem and Joe work on the same day as each other at least once)
solver.add(Or([And(Or(schedule[day*2] == 1, schedule[day*2+1] == 1), Or(schedule[day*2] == 2, schedule[day*2+1] == 2)) for day in range(5)]))

# Constraint 9 (Grecia and Louise never work on the same day)
for day in range(5):
    solver.add(Not(And(Or(schedule[day*2] == 0, schedule[day*2+1] == 0), Or(schedule[day*2] == 4, schedule[day*2+1] == 4))))


# Answer choices
answer_choices = [
    Or(schedule[1 * 2] == 0, schedule[1 * 2 + 1] == 0),  # A
    Or(schedule[2 * 2] == 1, schedule[2 * 2 + 1] == 1),  # B
    Or(schedule[1 * 2] == 2, schedule[1 * 2 + 1] == 2),  # C
    Or(schedule[3 * 2] == 2, schedule[3 * 2 + 1] == 2),  # D
    Or(schedule[1 * 2] == 4, schedule[1 * 2 + 1] == 4)   # E
]

for i, choice in enumerate(answer_choices):
    solver.push()
    solver.add(choice)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()