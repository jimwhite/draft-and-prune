from z3 import *

# Variables
day = [[Int("day_%s_%s" % (i, j)) for j in range(3)] for i in range(3)]

# Solver
solver = Solver()

# Constraints
for i in range(3):
    for j in range(3):
        solver.add(day[i][j] >= 0, day[i][j] <= 4)

for i in range(3):
    for j1 in range(3):
        for j2 in range(3):
            if j1 != j2:
                solver.add(day[i][j1] != day[i][j2])

for i1 in range(3):
    for i2 in range(3):
        for j in range(3):
            if i1 != i2:
                solver.add(day[i1][j] != day[i2][j])

solver.add(Or([Or([day[i][j] == 0 for j in range(3)]) for i in range(3)]))
solver.add(day[0][1] == day[1][0])
solver.add(day[2][1] == 3)


# Answering the question
daily_batch_counts = [Sum([If(day[i][j] == d, 1, 0) for i in range(3) for j in range(3)]) for d in range(5)]
count = 0

for d in range(5):
    solver.push()
    solver.add(daily_batch_counts[d] <= 2)
    if solver.check() == sat:
        count += 1
    solver.pop()

if count == 1:
    print("Option A is correct")
elif count == 2:
    print("Option B is correct")
elif count == 3:
    print("Option C is correct")
elif count == 4:
    print("Option D is correct")
elif count == 5:
    print("Option E is correct")

```