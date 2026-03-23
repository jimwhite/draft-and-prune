from z3 import *

# Target indices: 0-IW, 1-IV, 2-SW, 3-SV, 4-TW, 5-TV
IW, IV, SW, SV, TW, TV = range(6)

# Create variables for each target's value (1, 2, or 3 days)
targets = [Int(f"t_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: each target is 1, 2, or 3
for t in targets:
    solver.add(Or(t == 1, t == 2, t == 3))

# Website ≤ voicemail constraints per client
solver.add(targets[IW] <= targets[IV])  # Image: IW ≤ IV
solver.add(targets[SW] <= targets[SV])  # Solide: SW ≤ SV
solver.add(targets[TW] <= targets[TV])  # Truvest: TW ≤ TV

# Image's voicemail target must be shorter than the other clients' voicemail targets
solver.add(targets[IV] < targets[SV])
solver.add(targets[IV] < targets[TV])

# Solide's website target must be shorter than Truvest's website target
solver.add(targets[SW] < targets[TW])

# Given condition: Image's website target is 2 days
solver.add(targets[IW] == 2)

# Answer choices: [IV, SW, SV, TW, TV]
answer_choices = [IV, SW, SV, TW, TV]

# Check each answer choice using proof by contradiction
answer_index_list = []
for idx, target_idx in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert this target is NOT 2 days
    s_chk.add(targets[target_idx] != 2)
    
    # If UNSAT, this target must be 2 days
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)