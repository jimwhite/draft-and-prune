from z3 import *

# Define variables
schedule = Array('schedule', IntSort(), IntSort())
solver = Solver()

# Constraint 1 (Domain)
d = Int('d')
s = Int('s')
solver.add(ForAll([d], And(d >= 0, d < 5)))
solver.add(ForAll([s], And(s >= 0, s < 2)))
solver.add(ForAll([d, s], And(schedule[d * 2 + s] >= 0, schedule[d * 2 + s] < 5)))

# Constraint 2 (Each student works exactly two shifts)
student = Int('student')
solver.add(ForAll([student], Sum([If(schedule[slot] == student, 1, 0) for slot in range(10)]) == 2))

# Constraint 3 (Each shift is worked by exactly one student)
slot = Int('slot')
solver.add(ForAll([slot], Sum([If(schedule[slot] == student, 1, 0) for student in range(5)]) == 1))

# Constraint 4 (No student works both shifts of any day)
solver.add(ForAll([d], schedule[d * 2] != schedule[d * 2 + 1]))

# Constraint 5 (Louise works two consecutive second shifts)
solver.add(Or([And(schedule[d * 2 + 1] == 4, schedule[(d + 1) * 2 + 1] == 4) for d in range(4)]))

# Constraint 6 (Grecia works two non-consecutive first shifts)
d1 = Int('d1')
d2 = Int('d2')
solver.add(Or([And(schedule[d1 * 2] == 0, schedule[d2 * 2] == 0, Not(d1 == d2), Not(Abs(d1 - d2) == 1)) for d1 in range(5) for d2 in range(5)]))

# Constraint 7 (Katya works on Tuesday and Friday)
solver.add(And(Or(schedule[1 * 2] == 3, schedule[1 * 2 + 1] == 3), Or(schedule[4 * 2] == 3, schedule[4 * 2 + 1] == 3)))

# Constraint 8 (Hakeem and Joe work on the same day at least once)
solver.add(Or([Or(And(schedule[d * 2] == 1, schedule[d * 2 + 1] == 2), And(schedule[d * 2] == 2, schedule[d * 2 + 1] == 1)) for d in range(5)]))

# Constraint 9 (Grecia and Louise never work on the same day)
solver.add(ForAll([d], Not(And(Or(schedule[d*2] == 0, schedule[d*2+1] == 0), Or(schedule[d*2] == 4, schedule[d*2+1] == 4)))))


# Check answer choices
answer_choices = [
    Or(schedule[1 * 2] == 0, schedule[1 * 2 + 1] == 0),  # Grecia works on Tuesday
    Or(schedule[2 * 2] == 1, schedule[2 * 2 + 1] == 1),  # Hakeem works on Wednesday
    Or(schedule[1 * 2] == 2, schedule[1 * 2 + 1] == 2),  # Joe works on Tuesday
    Or(schedule[3 * 2] == 2, schedule[3 * 2 + 1] == 2),  # Joe works on Thursday
    Or(schedule[1 * 2] == 4, schedule[1 * 2 + 1] == 4)   # Louise works on Tuesday
]

for i in range(len(answer_choices)):
    solver.push()
    solver.add(answer_choices[i])
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()