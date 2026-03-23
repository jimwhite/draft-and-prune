from z3 import *

# Cargo types: 0-fuel, 1-grain, 2-livestock, 3-machinery, 4-produce, 5-textiles
cargo_types = ["fuel", "grain", "livestock", "machinery", "produce", "textiles"]

# bay[i] = bay number (1-6) for cargo type i
bay = [Int(f"bay_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: each bay number between 1 and 6, all distinct
for i in range(6):
    solver.add(bay[i] >= 1, bay[i] <= 6)
solver.add(Distinct(*bay))

# Ordering constraints
# grain > livestock (bay[1] > bay[2])
solver.add(bay[1] > bay[2])
# livestock > textiles (bay[2] > bay[5])
solver.add(bay[2] > bay[5])
# produce > fuel (bay[4] > bay[0])
solver.add(bay[4] > bay[0])
# textiles and produce are adjacent: |bay[5] - bay[4]| = 1
solver.add(Or(bay[5] == bay[4] + 1, bay[5] == bay[4] - 1))

# Conditional constraint: exactly one bay between machinery and grain
# |bay[3] - bay[1]| = 2
solver.add(Or(bay[3] == bay[1] + 2, bay[3] == bay[1] - 2))

# Collect all satisfying assignments
models = []
while solver.check() == sat:
    model = solver.model()
    models.append([model[bay[i]].as_long() for i in range(6)])
    
    # Add constraint to exclude current model
    solver.add(Or(*[bay[i] != models[-1][i] for i in range(6)]))

# Count how many cargo types have fixed bay positions across all models
fixed_count = 0
for i in range(6):
    values = set(model[i] for model in models)
    if len(values) == 1:
        fixed_count += 1

print(fixed_count)