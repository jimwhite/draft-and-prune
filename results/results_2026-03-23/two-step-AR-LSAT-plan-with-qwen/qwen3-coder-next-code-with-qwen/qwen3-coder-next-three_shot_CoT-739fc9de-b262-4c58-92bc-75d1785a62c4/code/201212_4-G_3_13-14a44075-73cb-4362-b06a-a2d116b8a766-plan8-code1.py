from z3 import *

# Target indices: 0-IW, 1-IV, 2-SW, 3-SV, 4-TW, 5-TV
IW, IV, SW, SV, TW, TV = range(6)

# Create variables
targets = [Int(f"t_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: each target is 1, 2, or 3
for t in targets:
    solver.add(Or(t == 1, t == 2, t == 3))

# Website ≤ voicemail constraints
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

# Answer choices indices: ["Image's voicemail target", "Solide's website target", "Solide's voicemail target", "Truvest's website target", "Truvest's voicemail target"]
answer_indices = [IV, SW, SV, TW, TV]

# Check which targets must be 2
answer_index_list = []
for idx in answer_indices:
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert this target is NOT 2
    s_chk.add(targets[idx] != 2)
    
    # If UNSAT, then target must be 2
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)