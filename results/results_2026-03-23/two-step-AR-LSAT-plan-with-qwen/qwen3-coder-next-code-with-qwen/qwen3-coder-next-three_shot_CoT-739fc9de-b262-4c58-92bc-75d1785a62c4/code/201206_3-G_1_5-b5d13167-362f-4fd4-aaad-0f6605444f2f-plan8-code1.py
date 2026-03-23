from z3 import *

# Lab assistants indices: 0=Julio, 1=Kevin, 2=Lan, 3=Nessa, 4=Olivia, 5=Rebecca
# Sessions: 0=Wed AM, 1=Wed PM, 2=Thu AM, 3=Thu PM, 4=Fri AM, 5=Fri PM

assign = [Int(f"assign_{i}") for i in range(6)]

solver = Solver()

# Domain constraints: each assistant assigned to exactly one session (0-5)
for i in range(6):
    solver.add(assign[i] >= 0, assign[i] <= 5)

# All assignments distinct
solver.add(Distinct(assign))

# Fixed constraint: Julio leads Thursday afternoon (session 3)
JULIO, KEVIN, LAN, NESSA, OLIVIA, REBECCA = 0, 1, 2, 3, 4, 5
solver.add(assign[JULIO] == 3)

# Kevin and Rebecca same day constraint: session//2 gives day index (0=Wed, 1=Thu, 2=Fri)
solver.add(assign[KEVIN] // 2 == assign[REBECCA] // 2)

# Lan and Olivia different day constraint
solver.add(assign[LAN] // 2 != assign[OLIVIA] // 2)

# Nessa afternoon constraint: session index is odd (1,3,5)
solver.add(assign[NESSA] % 2 == 1)

# Julio earlier than Olivia: assign[JULIO] < assign[OLIVIA]
solver.add(assign[JULIO] < assign[OLIVIA])

# Collect all models
models = []
while solver.check() == sat:
    model = solver.model()
    models.append(model)
    # Add constraint to exclude current model
    solver.add(Or(*[assign[i] != model[assign[i]].as_long() for i in range(6)]))

# For each assistant (excluding Julio), check if their session is fixed across all models
fixed_count = 0
for i in range(6):
    if i == JULIO:  # Skip Julio since fixed by condition
        continue
    
    values = set()
    for model in models:
        val = model[assign[i]].as_long()
        values.add(val)
    
    if len(values) == 1:
        fixed_count += 1

# Map count to answer
answers = ['one', 'two', 'three', 'four', 'five']
print(answers[fixed_count])