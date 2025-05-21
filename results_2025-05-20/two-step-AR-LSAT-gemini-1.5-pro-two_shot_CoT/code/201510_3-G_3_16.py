from z3 import *

# Define variables
schedule = Array('schedule', IntSort(), IntSort())
solver = Solver()

# Constraint 1: Each student works exactly two shifts
student = Int('student')
solver.add(ForAll([student], Implies(And(student >= 0, student <= 4), Sum([If(schedule[slot] == student, 1, 0) for slot in range(10)]) == 2)))

# Constraint 3: No student works both shifts of any day
day = Int('day')
solver.add(ForAll([day], Implies(And(day >= 0, day <= 4), schedule[day * 2] != schedule[day * 2 + 1])))

# Constraint 4: Louise works two consecutive second shifts
day = Int('day')
solver.add(Or([And(schedule[day * 2 + 1] == 4, schedule[(day + 1) * 2 + 1] == 4) for day in range(4)]))

# Constraint 5: Grecia works two non-consecutive first shifts
day1 = Int('day1')
day2 = Int('day2')
solver.add(Or([And(schedule[day1 * 2] == 0, schedule[day2 * 2] == 0, day1 != day2, day1 != day2 + 1, day1 != day2 - 1) for day1 in range(5) for day2 in range(5)]))


# Constraint 6: Katya works on Tuesday and Friday
solver.add(Or(schedule[1 * 2] == 3, schedule[1 * 2 + 1] == 3))
solver.add(Or(schedule[4 * 2] == 3, schedule[4 * 2 + 1] == 3))

# Constraint 7: Hakeem and Joe work on the same day at least once
day = Int('day')
solver.add(Or([And(Or(schedule[day * 2] == 1, schedule[day * 2 + 1] == 1), Or(schedule[day * 2] == 2, schedule[day * 2 + 1] == 2)) for day in range(5)]))

# Constraint 8: Grecia and Louise never work on the same day
day = Int('day')
solver.add(ForAll([day], Implies(And(day >= 0, day <= 4), Not(And(Or(schedule[day * 2] == 0, schedule[day * 2 + 1] == 0), Or(schedule[day * 2] == 4, schedule[day * 2 + 1] == 4))))))

# Premise: Hakeem works on Wednesday
solver.add(Or(schedule[2 * 2] == 1, schedule[2 * 2 + 1] == 1))

# Answer choices
options = [
    "Monday and Wednesday",
    "Monday and Thursday",
    "Tuesday and Wednesday",
    "Tuesday and Thursday",
    "Wednesday and Thursday"
]

for i, option in enumerate(options):
    days = []
    if "Monday" in option:
        days.append(0)
    if "Tuesday" in option:
        days.append(1)
    if "Wednesday" in option:
        days.append(2)
    if "Thursday" in option:
        days.append(3)
    if "Friday" in option:
        days.append(4)

    option_constraint = And([Or(schedule[day * 2] == 2, schedule[day * 2 + 1] == 2) for day in days])
    
    solver.push()
    solver.add(Not(option_constraint))
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()