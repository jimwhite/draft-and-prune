from z3 import *

# Variables
schedule = Array('schedule', IntSort(), IntSort())
i = Int('i')
s = Int('s')
d = Int('d')
g1 = Int('g1')
g2 = Int('g2')

# Solver
solver = Solver()

# Constraints
# Constraint 0 (Domain)
solver.add(ForAll([i], And(schedule[i] >= 0, schedule[i] < 5)))

# Constraint 1 (Each Student Works Two Shifts)
for s in range(5):
    solver.add(Sum([If(schedule[i] == s, 1, 0) for i in range(10)]) == 2)

# Constraint 2 (No Student Works Both Shifts)
solver.add(ForAll([d], Not(schedule[d * 2] == schedule[d * 2 + 1])))

# Constraint 3 (Louise Works Two Consecutive Second Shifts)
solver.add(Or([And(schedule[d * 2 + 1] == 4, schedule[(d + 1) * 2 + 1] == 4) for d in range(4)]))

# Constraint 4 (Grecia Works Two Non-Consecutive First Shifts)
solver.add(Exists([g1, g2], And(g1 >= 0, g1 < 5, g2 >= 0, g2 < 5, g1 != g2, Not(Or(g1 == g2 + 1, g2 == g1 + 1)), schedule[g1 * 2] == 0, schedule[g2 * 2] == 0)))

# Constraint 5 (Katya Works Tuesday and Friday Second Shift)
solver.add(schedule[3] == 3)
solver.add(schedule[9] == 3)

# Constraint 6 (Hakeem and Joe Work on the Same Day at least once)
solver.add(Or([Or(And(schedule[d * 2] == 1, schedule[d * 2 + 1] == 2), And(schedule[d * 2] == 2, schedule[d * 2 + 1] == 1)) for d in range(5)]))

# Constraint 7 (Grecia and Louise Never Work on the Same Day)
solver.add(ForAll([d], Not(Or(
    And(schedule[d*2] == 0, schedule[d*2+1] == 4),
    And(schedule[d*2] == 4, schedule[d*2+1] == 0),
    And(schedule[d*2] == 0, Or([schedule[d*2+1] == s for s in range(5) if s != 4])),
    And(schedule[d*2] == 4, Or([schedule[d*2+1] == s for s in range(5) if s != 0])),
    And(Or([schedule[d*2] == s for s in range(5) if s != 4 and s != 0]), schedule[d*2+1] == 0),
    And(Or([schedule[d*2] == s for s in range(5) if s != 0 and s != 4]), schedule[d*2+1] == 4)
))))


# Answer Choices
options = [
    [1, 4, 4, 1, 3],
    [2, 1, 0, 4, 4],
    [2, 3, 1, 4, 3],
    [4, 3, 2, 4, 3],
    [4, 4, 1, 2, 2]
]

# Check each option
for option_index, option in enumerate(options):
    solver.push()
    for day in range(5):
        solver.add(schedule[day * 2 + 1] == option[day])
    if solver.check() == sat:
        print(f"Option {chr(65 + option_index)} is correct")
        exit()
    solver.pop()