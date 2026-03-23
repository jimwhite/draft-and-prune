from z3 import *

# Variables: IW, IV, SW, SV, TW, TV (Image Website, Image Voicemail, etc.)
IW, IV, SW, SV, TW, TV = Ints('IW IV SW SV TW TV')

solver = Solver()

# Domain constraints: all targets in {1, 2, 3}
for var in [IW, IV, SW, SV, TW, TV]:
    solver.add(Or(var == 1, var == 2, var == 3))

# No website target longer than voicemail for each client
solver.add(IW <= IV)
solver.add(SW <= SV)
solver.add(TW <= TV)

# Image's voicemail target must be shorter than the other clients' voicemail targets
solver.add(IV < SV)
solver.add(IV < TV)

# Solide's website target must be shorter than Truvest's website target
solver.add(SW < TW)

# Given condition: Image's website target is 2 days
solver.add(IW == 2)

# Check which targets must be 2 using proof by contradiction
answer_choices = [
    IV,  # Image's voicemail target
    SW,  # Solide's website target
    SV,  # Solide's voicemail target
    TW,  # Truvest's website target
    TV   # Truvest's voicemail target
]

answer_index_list = []
for idx, target in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert target is NOT 2
    s_chk.add(target != 2)
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)