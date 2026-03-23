from z3 import *

# Cargo type indices: 0=fuel, 1=grain, 2=livestock, 3=machinery, 4=produce, 5=textiles
(fuel, grain, livestock, machinery, produce, textiles) = range(6)

# bay[type_idx] = bay number (1-6) holding that cargo type
bay = [Int(f"bay_{t}") for t in range(6)]

# Base solver
solver = Solver()

# Domain constraints: each bay number between 1 and 6, all distinct
solver.add([And(bay[t] >= 1, bay[t] <= 6) for t in range(6)])
solver.add(Distinct(bay))

# Ordering constraints
solver.add(bay[grain] > bay[livestock])
solver.add(bay[livestock] > bay[textiles])
solver.add(bay[produce] > bay[fuel])

# Textiles and produce are adjacent
solver.add(Or(bay[textiles] == bay[produce] + 1, bay[textiles] == bay[produce] - 1))

# Hypothesis: exactly one bay between machinery and grain
solver.add(Or(bay[machinery] == bay[grain] + 2, bay[machinery] == bay[grain] - 2))

# Collect all satisfying assignments
solutions = []
while solver.check() == sat:
    model = solver.model()
    # Extract bay assignments
    sol = [model.eval(bay[t]).as_long() for t in range(6)]
    solutions.append(sol)
    
    # Add constraint to exclude this exact assignment
    solver.add(Or(*[bay[t] != sol[t] for t in range(6)]))

# Check which cargo types have fixed bay numbers across all solutions
determined = [True] * 6
if len(solutions) > 0:
    for t in range(6):
        first_val = solutions[0][t]
        for sol in solutions[1:]:
            if sol[t] != first_val:
                determined[t] = False
                break

# Count determined cargo types
count_determined = sum(determined)

# Map count to answer string
answer_map = {
    2: 'two',
    3: 'three',
    4: 'four',
    5: 'five',
    6: 'six'
}

print(answer_map.get(count_determined, 'unknown'))