from z3 import *

# Target variables: each in {1, 2, 3}
iw = Int('iw')
iv = Int('iv')
sw = Int('sw')
sv = Int('sv')
tw = Int('tw')
tv = Int('tv')

solver = Solver()

# Domain constraints
for var in [iw, iv, sw, sv, tw, tv]:
    solver.add(Or(var == 1, var == 2, var == 3))

# Constraint: no client's website target exceeds its voicemail target
solver.add(iw <= iv)
solver.add(sw <= sv)
solver.add(tw <= tv)

# Constraint: Image's voicemail target is shorter than the other clients' voicemail targets
solver.add(iv < sv)
solver.add(iv < tv)

# Constraint: Solide's website target is shorter than Truvest's website target
solver.add(sw < tw)

# Given condition: Image's website target is 2 days
solver.add(iw == 2)

# Check each answer choice using proof by contradiction
answer_choices = [
    "Image's voicemail target",
    "Solide's website target",
    "Solide's voicemail target",
    "Truvest's website target",
    "Truvest's voicemail target"
]

# Map answer choices to variables
var_map = {
    "Image's voicemail target": iv,
    "Solide's website target": sw,
    "Solide's voicemail target": sv,
    "Truvest's website target": tw,
    "Truvest's voicemail target": tv
}

answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert this target is NOT 2 days
    s_chk.add(var_map[choice] != 2)
    
    # If UNSAT, this target must be 2 days
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)