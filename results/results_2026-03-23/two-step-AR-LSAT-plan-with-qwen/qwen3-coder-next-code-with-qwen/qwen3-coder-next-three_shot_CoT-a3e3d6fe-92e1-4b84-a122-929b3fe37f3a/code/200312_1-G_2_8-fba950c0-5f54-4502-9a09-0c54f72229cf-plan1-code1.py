from z3 import *

# Cargo types: fuel=0, grain=1, livestock=2, machinery=3, produce=4, textiles=5
bay = [Int(f"bay_{c}") for c in range(6)]

# Base solver
solver = Solver()

# Domain constraints: each bay position between 1 and 6, all distinct
solver.add([And(bay[c] >= 1, bay[c] <= 6) for c in range(6)])
solver.add(Distinct(bay))

# Ordering constraints
# grain > livestock ⇒ bay[1] > bay[2]
solver.add(bay[1] > bay[2])
# livestock > textiles ⇒ bay[2] > bay[5]
solver.add(bay[2] > bay[5])
# produce > fuel ⇒ bay[4] > bay[0]
solver.add(bay[4] > bay[0])
# textiles adjacent to produce ⇒ |bay[5] - bay[4]| = 1
solver.add(Or(bay[5] == bay[4] + 1, bay[5] == bay[4] - 1))

# Hypothesis: exactly one bay between machinery and grain ⇒ |bay[3] - bay[1]| = 2
solver.add(Or(bay[3] == bay[1] + 2, bay[3] == bay[1] - 2))

# Collect possible cargo types for each bay position
determined_bays = 0

for p in range(1, 7):  # bay positions 1 through 6
    forced_cargo = None
    all_sat = True
    
    for c in range(6):
        s_chk = Solver()
        s_chk.add(solver.assertions())
        
        # Check if cargo c can be in bay p
        s_chk.add(bay[c] == p)
        
        if s_chk.check() == unsat:
            continue  # cargo c cannot be in bay p
        
        # Now check if cargo c is forced into bay p
        s_chk_forced = Solver()
        s_chk_forced.add(solver.assertions())
        # Assert that cargo c is NOT in bay p
        s_chk_forced.add(bay[c] != p)
        
        if s_chk_forced.check() == unsat:
            # If removing cargo c from bay p makes it UNSAT, then cargo c must be in bay p
            if forced_cargo is None:
                forced_cargo = c
            else:
                # Two different cargos forced into same bay - impossible
                all_sat = False
                break
    
    if forced_cargo is not None and all_sat:
        determined_bays += 1

# Map to answer choices
mapping = {2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six'}
print(mapping[determined_bays])