from z3 import *

# Cargo types: fuel=0, grain=1, livestock=2, machinery=3, produce=4, textiles=5
cargo_types = ["fuel", "grain", "livestock", "machinery", "produce", "textiles"]

# bay[i] = bay number (1-6) where cargo type i is stored
bay = [Int(f"bay_{c}") for c in cargo_types]

solver = Solver()

# Domain constraints: each bay number between 1 and 6
for b in bay:
    solver.add(b >= 1, b <= 6)

# All bays distinct
solver.add(Distinct(bay))

# Relative ordering constraints
# grain > livestock
solver.add(bay[1] > bay[2])
# livestock > textiles
solver.add(bay[2] > bay[5])
# produce > fuel
solver.add(bay[4] > bay[0])
# textiles adjacent to produce: |bay[textiles] - bay[produce]| == 1
solver.add(Or(bay[5] == bay[4] + 1, bay[5] == bay[4] - 1))

# Exactly one bay between machinery and grain: |bay[machinery] - bay[grain]| == 2
solver.add(Or(bay[3] == bay[1] + 2, bay[3] == bay[1] - 2))

# Enumerate all satisfying assignments and collect values for each cargo type
def get_all_solutions():
    solutions = []
    while solver.check() == sat:
        m = solver.model()
        solution = [m.eval(b).as_long() for b in bay]
        solutions.append(solution)
        
        # Block this solution
        solver.add(Or(*[bay[i] != solution[i] for i in range(6)]))
    return solutions

solutions = get_all_solutions()

# For each cargo type, collect all possible bay positions across solutions
possible_bays = [[] for _ in range(6)]
for sol in solutions:
    for i in range(6):
        possible_bays[i].append(sol[i])

# Count how many cargo types have exactly one possible bay position
fixed_count = sum(1 for bays in possible_bays if len(set(bays)) == 1)

# Map count to answer choice
answer_map = {2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six'}
print(answer_map[fixed_count])