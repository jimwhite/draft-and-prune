from z3 import *

# Lab assistants: 0=Julio, 1=Kevin, 2=Lan, 3=Nessa, 4=Olivia, 5=Rebecca
# Sessions: 0=Wed AM, 1=Wed PM, 2=Thu AM, 3=Thu PM, 4=Fri AM, 5=Fri PM

slot = [Int(f"slot_{i}") for i in range(6)]

solver = Solver()

# Each assistant assigned to exactly one session (all distinct)
solver.add(Distinct(slot))

# Domain constraints: sessions are 0-5
for i in range(6):
    solver.add(slot[i] >= 0, slot[i] <= 5)

# Fixed constraint: Julio leads Thursday afternoon (slot index 3)
solver.add(slot[0] == 3)

# Helper functions using Z3 expressions
def day(s):
    # 0 for Wed (slots 0,1), 1 for Thu (slots 2,3), 2 for Fri (slots 4,5)
    return If(s < 2, 0, If(s < 4, 1, 2))

def period(s):
    # 0 for AM (even slots), 1 for PM (odd slots)
    return If(s % 2 == 0, 0, 1)

# Kevin and Rebecca must lead sessions on the same day
solver.add(day(slot[1]) == day(slot[5]))

# Lan and Olivia cannot lead sessions on the same day
solver.add(day(slot[2]) != day(slot[4]))

# Nessa must lead an afternoon session (period = 1)
solver.add(period(slot[3]) == 1)

# Julio's session must be earlier than Olivia's
solver.add(slot[0] < slot[4])

# Collect all satisfying models and check which slots are fixed
solver.add(slot[0] == 3)  # Redundant but explicit

# Get all solutions
models = []
while solver.check() == sat:
    m = solver.model()
    models.append([m[slot[i]].as_long() for i in range(6)])
    
    # Add constraint to exclude current model
    solver.add(Or(*[slot[i] != models[-1][i] for i in range(6)]))

# Count how many assistants (excluding Julio) have fixed slots across all models
fixed_count = 0
for j in range(1, 6):
    values = set(m[j] for m in models)
    if len(values) == 1:
        fixed_count += 1

# Map count to answer choice
answers = ['one', 'two', 'three', 'four', 'five']
print(answers[fixed_count])