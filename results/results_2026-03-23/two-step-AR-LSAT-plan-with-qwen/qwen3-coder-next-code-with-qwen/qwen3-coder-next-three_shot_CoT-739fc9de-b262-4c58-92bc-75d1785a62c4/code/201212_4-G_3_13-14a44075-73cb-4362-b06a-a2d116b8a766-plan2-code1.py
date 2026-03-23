from z3 import *

# Variables: IW, IV, SW, SV, TW, TV (Image Website, Image Voicemail, etc.)
IW, IV, SW, SV, TW, TV = Ints('IW IV SW SV TW TV')

solver = Solver()

# Domain constraints: all targets in {1, 2, 3}
for var in [IW, IV, SW, SV, TW, TV]:
    solver.add(Or(var == 1, var == 2, var == 3))

# Client-level ordering: website ≤ voicemail for each client
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

# Answer choices indices:
# 0: Image's voicemail target (IV)
# 1: Solide's website target (SW)
# 2: Solide's voicemail target (SV)
# 3: Truvest's website target (TW)
# 4: Truvest's voicemail target (TV)

answer_choices = [IV, SW, SV, TW, TV]
answer_index_list = []

for idx, target in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert this target is NOT 2 days
    s_chk.add(target != 2)
    
    # If UNSAT, then this target must be 2 days
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)