from z3 import *

# Variables: IW, IV, SW, SV, TW, TV ∈ {1, 2, 3}
IW, IV, SW, SV, TW, TV = Ints('IW IV SW SV TW TV')

solver = Solver()

# Domain constraints
for var in [IW, IV, SW, SV, TW, TV]:
    solver.add(Or(var == 1, var == 2, var == 3))

# Website ≤ voicemail constraints
solver.add(IW <= IV)
solver.add(SW <= SV)
solver.add(TW <= TV)

# Image's voicemail target must be shorter than the other clients' voicemail targets
solver.add(IV < SV, IV < TV)

# Solide's website target must be shorter than Truvest's website target
solver.add(SW < TW)

# Given condition: Image's website target is 2 days
solver.add(IW == 2)

# Answer choices: [IV, SW, SV, TW, TV]
answer_choices = [
    IV,
    SW,
    SV,
    TW,
    TV
]

# Check each answer choice using proof by contradiction
answer_index_list = []
for idx, target in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert that the candidate target is NOT 2
    s_chk.add(target != 2)
    
    # If UNSAT, this target must be 2
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)