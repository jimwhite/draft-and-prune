from z3 import *

# Target values: 1 -> "1 day", 2 -> "2 days", 3 -> "3 days"
IW, IV, SW, SV, TW, TV = Ints('IW IV SW SV TW TV')

solver = Solver()

# Domain constraints: each variable in {1, 2, 3}
for var in [IW, IV, SW, SV, TW, TV]:
    solver.add(Or(var == 1, var == 2, var == 3))

# Website <= voicemail for each client
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

# Answer choices: indices correspond to the list below
answer_choices = [
    IV,  # Image's voicemail target
    SW,  # Solide's website target
    SV,  # Solide's voicemail target
    TW,  # Truvest's website target
    TV   # Truvest's voicemail target
]

answer_index_list = []

for idx, var in enumerate(answer_choices):
    # Check if var must be 2
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Try var != 2 (i.e., var == 1 or var == 3)
    s_chk.add(Or(var == 1, var == 3))
    
    if s_chk.check() == unsat:
        # If UNSAT when var != 2, then var must be 2
        answer_index_list.append(idx)

print(answer_index_list)