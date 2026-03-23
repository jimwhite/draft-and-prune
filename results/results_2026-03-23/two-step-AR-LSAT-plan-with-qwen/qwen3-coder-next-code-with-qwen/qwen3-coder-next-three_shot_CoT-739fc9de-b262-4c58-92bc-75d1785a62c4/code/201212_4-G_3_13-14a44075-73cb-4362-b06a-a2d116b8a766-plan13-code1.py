from z3 import *

# Target values: 1 = 1 day, 2 = 2 days, 3 = 3 days
IW, IV, SW, SV, TW, TV = Ints('IW IV SW SV TW TV')

solver = Solver()

# Domain constraints: all targets in {1, 2, 3}
for var in [IW, IV, SW, SV, TW, TV]:
    solver.add(And(var >= 1, var <= 3))

# Per-client validity constraints: website target ≤ voicemail target
solver.add(IW <= IV)
solver.add(SW <= SV)
solver.add(TW <= TV)

# Image's voicemail target must be shorter than other clients' voicemail targets
solver.add(IV < SV)
solver.add(IV < TV)

# Solide's website target must be shorter than Truvest's website target
solver.add(SW < TW)

# Given condition: Image's website target is 2 days
solver.add(IW == 2)

# Check which targets must be 2 (excluding the given IW=2)
answer_choices = [
    "Image's voicemail target",  # IV
    "Solide's website target",   # SW
    "Solide's voicemail target", # SV
    "Truvest's website target",  # TW
    "Truvest's voicemail target" # TV
]

# Map answer choices to variables
choice_vars = [IV, SW, SV, TW, TV]

answer_index_list = []
for idx, var in enumerate(choice_vars):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert this target is NOT 2 days
    s_chk.add(var != 2)
    
    # If UNSAT, this target must be 2 days
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)