from z3 import *

# Variables
schedule = Array('schedule', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
i = Int('i')
d = Int('d')
s = Int('s')
d1 = Int('d1')
d2 = Int('d2')

# Constraint 0 (Domain) - Explicitly enforce the domain
solver.add(ForAll([i], Implies(And(i >= 0, i < 10), And(schedule[i] >= 0, schedule[i] < 5))))


# Constraint 2 (Each Student Works Two Shifts)
solver.add(ForAll([s], Implies(And(s >= 0, s < 5), Sum([If(schedule[i] == s, 1, 0) for i in range(10)]) == 2)))

# Constraint 3 (No Student Works Both Shifts on the Same Day)
solver.add(ForAll([d], Implies(And(d >= 0, d < 5), schedule[d * 2] != schedule[d * 2 + 1])))

# Constraint 4 (Louise Works Two Consecutive Second Shifts)
solver.add(Or([And(schedule[d * 2 + 1] == 4, schedule[(d + 1) * 2 + 1] == 4) for d in range(4)]))

# Constraint 5 (Grecia Works Two Non-Consecutive First Shifts)
solver.add(Or([And(schedule[d1 * 2] == 0, schedule[d2 * 2] == 0, Not(Or(d1 == d2, d1 == d2 + 1, d1 == d2 - 1))) for d1 in range(5) for d2 in range(5)]))

# Constraint 6 (Katya Works Tuesday and Friday)
solver.add(Or(schedule[1 * 2] == 3, schedule[1 * 2 + 1] == 3))
solver.add(Or(schedule[4 * 2] == 3, schedule[4 * 2 + 1] == 3))

# Constraint 7 (Hakeem and Joe Work on the Same Day at least once)
solver.add(Or([Or(And(schedule[d * 2] == 1, schedule[d * 2 + 1] == 2), And(schedule[d * 2] == 2, schedule[d * 2 + 1] == 1)) for d in range(5)]))

# Constraint 8 (Grecia and Louise Never Work on the Same Day)
solver.add(ForAll([d], Implies(And(d >= 0, d < 5), Not(Or(And(schedule[d * 2] == 0, schedule[d * 2 + 1] == 4), And(schedule[d * 2] == 4, schedule[d * 2 + 1] == 0))))))


if solver.check() == sat:
    model = solver.model()
    for day in range(5):
        for shift in range(2):
            student_id = model.evaluate(schedule[day * 2 + shift]).as_long() # Use evaluate() and access the array element correctly
            print(f"Day {day}, Shift {shift}: Student {student_id}")
else:
    print("No solution found.")

