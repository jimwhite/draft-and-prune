from z3 import *

# Define variables
schedule = Array('schedule', IntSort(), IntSort())
solver = Solver()

# Constraint 0 (Domain)
d = Int('d')
s = Int('s')
solver.add(ForAll([d], And(d >= 0, d < 5)))
solver.add(ForAll([s], And(s >= 0, s < 2)))
solver.add(ForAll([d, s], And(schedule[d * 2 + s] >= 0, schedule[d * 2 + s] < 5)))

# Constraint 1 (Each student works exactly two shifts)
student = Int('student')
solver.add(ForAll([student], Sum([If(schedule[slot] == student, 1, 0) for slot in range(10)]) == 2))

# Constraint 2 (Each shift is worked by exactly one student)
slot = Int('slot')
solver.add(ForAll([slot], Sum([If(schedule[slot] == student, 1, 0) for student in range(5)]) == 1))

# Constraint 3 (No student works both shifts of any day)
day = Int('day')
solver.add(ForAll([day], schedule[day * 2] != schedule[day * 2 + 1]))

# Constraint 4 (Louise works two consecutive second shifts)
day = Int('day')
solver.add(Exists([day], And(day >= 0, day < 4, schedule[day * 2 + 1] == 4, schedule[(day + 1) * 2 + 1] == 4)))

# Constraint 5 (Grecia works two non-consecutive first shifts)
day1 = Int('day1')
day2 = Int('day2')
solver.add(Exists([day1, day2], And(day1 >= 0, day1 < 5, day2 >= 0, day2 < 5, day1 != day2, Not(Or(day1 == day2 + 1, day2 == day1 + 1)), schedule[day1 * 2] == 0, schedule[day2 * 2] == 0)))

# Constraint 6 (Katya works on Tuesday and Friday)
solver.add(Or(schedule[1 * 2] == 3, schedule[1 * 2 + 1] == 3))
solver.add(Or(schedule[4 * 2] == 3, schedule[4 * 2 + 1] == 3))

# Constraint 7 (Hakeem and Joe work on the same day at least once)
day = Int('day')
solver.add(Exists([day], And(Or(schedule[day * 2] == 1, schedule[day * 2 + 1] == 1), Or(schedule[day * 2] == 2, schedule[day * 2 + 1] == 2))))

# Constraint 8 (Grecia and Louise never work on the same day)
day = Int('day')
solver.add(ForAll([day], Not(And(Or(schedule[day * 2] == 0, schedule[day * 2 + 1] == 0), Or(schedule[day * 2] == 4, schedule[day * 2 + 1] == 4)))))


# Premise: Grecia and Joe work on the same day at least once
day = Int('day')
solver.add(Exists([day], And(Or(schedule[day * 2] == 0, schedule[day * 2 + 1] == 0), Or(schedule[day * 2] == 2, schedule[day * 2 + 1] == 2))))

# Check answer choices
options = [
    (schedule[1 * 2] == 0),  # Grecia works the first shift on Tuesday
    (schedule[0 * 2 + 1] == 1),  # Hakeem works the second shift on Monday
    (schedule[2 * 2 + 1] == 1),  # Hakeem works the second shift on Wednesday
    (schedule[2 * 2] == 2),  # Joe works the first shift on Wednesday
    (schedule[3 * 2] == 2)  # Joe works the first shift on Thursday
]

for i, option in enumerate(options):
    solver.push()
    solver.add(option)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()