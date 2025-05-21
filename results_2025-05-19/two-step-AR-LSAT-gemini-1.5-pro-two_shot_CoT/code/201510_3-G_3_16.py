from z3 import *

# Define variables
schedule = Array('schedule', IntSort(), IntSort())
solver = Solver()

# Constraint 0 (Domain)
slot = Int('slot')
solver.add(ForAll([slot], Implies(And(slot >= 0, slot <= 9), And(schedule[slot] >= 0, schedule[slot] <= 4))))

# Constraint 1 (Each student works exactly two shifts)
student = Int('student')
solver.add(ForAll([student], Implies(And(student >= 0, student <= 4), Sum([If(schedule[s] == student, 1, 0) for s in range(10)]) == 2)))

# Constraint 2 (Each shift is worked by exactly one student)
day = Int('day')
solver.add(ForAll([day], Implies(And(day >= 0, day <= 4), Distinct([schedule[day * 2], schedule[day * 2 + 1]]))))

# Constraint 3 (Louise works two consecutive second shifts)
solver.add(Or([And(schedule[day * 2 + 1] == 4, schedule[(day + 1) * 2 + 1] == 4) for day in range(4)]))

# Constraint 4 (Grecia works two non-consecutive first shifts)
g_day1 = Int('g_day1')
g_day2 = Int('g_day2')
solver.add(Exists([g_day1, g_day2], And(g_day1 >= 0, g_day1 <= 4, g_day2 >= 0, g_day2 <= 4, Not(Or(g_day2 == g_day1 + 1, g_day2 == g_day1 - 1)), schedule[g_day1 * 2] == 0, schedule[g_day2 * 2] == 0, Distinct([g_day1, g_day2]))))

# Constraint 5 (Katya works Tuesday and Friday)
solver.add(Or(schedule[1 * 2] == 3, schedule[1 * 2 + 1] == 3))
solver.add(Or(schedule[4 * 2] == 3, schedule[4 * 2 + 1] == 3))

# Constraint 6 (Hakeem and Joe work on the same day at least once)
solver.add(Or([Or(And(schedule[day * 2] == 1, schedule[day * 2 + 1] == 2), And(schedule[day * 2] == 2, schedule[day * 2 + 1] == 1)) for day in range(5)]))

# Constraint 7 (Grecia and Louise never work on the same day)
day = Int('day')
solver.add(ForAll([day], Implies(And(day >= 0, day <= 4), Not(Or(And(schedule[day * 2] == 0, schedule[day * 2 + 1] == 4), And(schedule[day * 2] == 4, schedule[day * 2 + 1] == 0))))))

# Hakeem works on Wednesday
solver.add(Or(schedule[2 * 2] == 1, schedule[2 * 2 + 1] == 1))

# Check answer choices
options = [
    [(0, 2), (2, 2)],  # Monday and Wednesday
    [(0, 2), (3, 2)],  # Monday and Thursday
    [(1, 2), (2, 2)],  # Tuesday and Wednesday
    [(1, 2), (3, 2)],  # Tuesday and Thursday
    [(2, 2), (3, 2)]   # Wednesday and Thursday
]
option_labels = ['A', 'B', 'C', 'D', 'E']

for i, option in enumerate(options):
    solver.push()
    for day in option:
        solver.add(Or(schedule[day[0] * 2] == 2, schedule[day[0] * 2 + 1] == 2))
    if solver.check() == sat:
        print(f"Option {option_labels[i]} is correct")
        exit()
    solver.pop()