from z3 import *

# Cargo types: fuel=0, grain=1, livestock=2, machinery=3, produce=4, textiles=5
bay = [Int(f"bay_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: each bay position is between 1 and 6, all distinct
for i in range(6):
    solver.add(bay[i] >= 1, bay[i] <= 6)
solver.add(Distinct(*bay))

# Ordering constraints
# grain > livestock: bay[1] > bay[2]
solver.add(bay[1] > bay[2])
# livestock > textiles: bay[2] > bay[5]
solver.add(bay[2] > bay[5])
# produce > fuel: bay[4] > bay[0]
solver.add(bay[4] > bay[0])
# textiles adjacent to produce: |bay[5] - bay[4]| = 1
solver.add(Or(bay[5] == bay[4] + 1, bay[5] == bay[4] - 1))

# Extra condition: exactly one bay between machinery and grain
# |bay[3] - bay[1]| = 2
solver.add(Or(bay[3] == bay[1] + 2, bay[3] == bay[1] - 2))

# Check which cargo types have uniquely determined positions
fixed_count = 0

for i in range(6):
    possible_positions = []
    for p in range(1, 7):
        s_chk = Solver()
        s_chk.add(solver.assertions())
        s_chk.add(bay[i] == p)
        
        if s_chk.check() == sat:
            possible_positions.append(p)
    
    # If exactly one position is possible, this cargo type is fixed
    if len(possible_positions) == 1:
        fixed_count += 1

# Map count to answer string
answer_map = {
    2: 'two',
    3: 'three',
    4: 'four',
    5: 'five',
    6: 'six'
}

print(answer_map[fixed_count])