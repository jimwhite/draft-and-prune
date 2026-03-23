from z3 import *

# Lab assistants: 0=Julio, 1=Kevin, 2=Lan, 3=Nessa, 4=Olivia, 5=Rebecca
# Sessions: 0=WM, 1=WA, 2=TM, 3=TA, 4=FM, 5=FA

assign = [Int(f"assign_{i}") for i in range(6)]

solver = Solver()

# Domain constraints
for i in range(6):
    solver.add(assign[i] >= 0, assign[i] <= 5)

# Bijection constraint
solver.add(Distinct(*assign))

# Fixed assignment: Julio leads Thursday afternoon (session index 3)
solver.add(assign[0] == 3)

# Same-day constraint for Kevin and Rebecca
def day(s):
    return s / 2

solver.add(day(assign[1]) == day(assign[5]))

# Cannot-same-day constraint for Lan and Olivia
solver.add(day(assign[2]) != day(assign[4]))

# Nessa afternoon constraint (odd session indices: 1,3,5)
solver.add(assign[3] % 2 == 1)

# Julio earlier than Olivia: assign[0] < assign[4]
solver.add(assign[0] < assign[4])

# Collect all satisfying assignments and determine which assistants have fixed sessions
solutions = []
while solver.check() == sat:
    m = solver.model()
    solutions.append([m[assign[i]].as_long() for i in range(6)])
    # Block this solution
    solver.add(Or(*[assign[i] != solutions[-1][i] for i in range(6)]))

# For each assistant (excluding Julio), count distinct session assignments across all solutions
determined_count = 0
for i in range(1, 6):  # assistants 1-5 (Kevin, Lan, Nessa, Olivia, Rebecca)
    values = set(sol[i] for sol in solutions)
    if len(values) == 1:
        determined_count += 1

# Map count to answer string
answer_map = {0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five'}
print(answer_map[determined_count])