from z3 import *

# Lab assistants: 0=Julio, 1=Kevin, 2=Lan, 3=Nessa, 4=Olivia, 5=Rebecca
# Sessions: 0=Wed AM, 1=Wed PM, 2=Thu AM, 3=Thu PM, 4=Fri AM, 5=Fri PM

pos = [Int(f"pos_{i}") for i in range(6)]

solver = Solver()

# Domain constraints: each assistant assigned to exactly one session (0-5)
solver.add([And(pos[i] >= 0, pos[i] <= 5) for i in range(6)])
solver.add(Distinct(pos))

# Fixed constraint: Julio leads Thursday afternoon (session 3)
solver.add(pos[0] == 3)

# Same-day constraint for Kevin and Rebecca
def day(s):
    return s / 2

solver.add(day(pos[1]) == day(pos[5]))

# Different-day constraint for Lan and Olivia
solver.add(day(pos[2]) != day(pos[4]))

# Nessa afternoon constraint: session index must be odd (1, 3, or 5)
solver.add(Or(pos[3] == 1, pos[3] == 3, pos[3] == 5))

# Julio earlier than Olivia: pos[0] < pos[4]
solver.add(pos[0] < pos[4])

# Collect all models
models = []
while solver.check() == sat:
    m = solver.model()
    models.append(m)
    # Add constraint to exclude current model
    solver.add(Or([pos[i] != m[pos[i]] for i in range(6)]))

# Count how many assistants (excluding Julio) have fixed session across all models
count_fixed = 0
for j in range(1, 6):  # Kevin, Lan, Nessa, Olivia, Rebecca
    values = set()
    for m in models:
        values.add(m[pos[j]].as_long())
    if len(values) == 1:
        count_fixed += 1

# Map to answer choices
answers = ['one', 'two', 'three', 'four', 'five']
print(answers[count_fixed])