from z3 import *

# Target indices: 0-IW, 1-IV, 2-SW, 3-SV, 4-TW, 5-TV
IW, IV, SW, SV, TW, TV = range(6)

# Create variables
targets = [Int(f"t_{i}") for i in range(6)]

solver = Solver()

# Domain constraints: each target ∈ {1, 2, 3}
for t in targets:
    solver.add(Or(t == 1, t == 2, t == 3))

# Website ≤ voicemail constraints
solver.add(targets[IW] <= targets[IV])
solver.add(targets[SW] <= targets[SV])
solver.add(targets[TW] <= targets[TV])

# Image voicemail must be strictly shorter than both other clients' voicemail targets
solver.add(targets[IV] < targets[SV])
solver.add(targets[IV] < targets[TV])

# Solide website must be strictly shorter than Truvest website
solver.add(targets[SW] < targets[TW])

# Given condition: Image's website target is 2 days
solver.add(targets[IW] == 2)

# Answer choices indices: [IV, SW, SV, TW, TV]
answer_choices = [IV, SW, SV, TW, TV]

# Find which targets must be 2 (i.e., cannot be ≠2)
answer_index_list = []
for idx, target_idx in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert target ≠ 2 (i.e., =1 or =3)
    s_chk.add(Or(targets[target_idx] == 1, targets[target_idx] == 3))
    
    # If UNSAT, then target must be 2
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)