from z3 import *

# Target indices: 1=1 day, 2=2 days, 3=3 days
IW, IV, SW, SV, TW, TV = Ints('IW IV SW SV TW TV')

solver = Solver()

# Domain constraints: each target is 1, 2, or 3
solver.add(And(IW >= 1, IW <= 3))
solver.add(And(IV >= 1, IV <= 3))
solver.add(And(SW >= 1, SW <= 3))
solver.add(And(SV >= 1, SV <= 3))
solver.add(And(TW >= 1, TW <= 3))
solver.add(And(TV >= 1, TV <= 3))

# Base constraints
solver.add(IW <= IV)      # Image: website ≤ voicemail
solver.add(SW <= SV)      # Solide: website ≤ voicemail
solver.add(TW <= TV)      # Truvest: website ≤ voicemail
solver.add(IV < SV)       # Image's voicemail < Solide's voicemail
solver.add(IV < TV)       # Image's voicemail < Truvest's voicemail
solver.add(SW < TW)       # Solide's website < Truvest's website

# Given condition: Image's website target is 2 days
solver.add(IW == 2)

# Answer choices: [IV, SW, SV, TW, TV]
answer_targets = [IV, SW, SV, TW, TV]

# Check which target must be 2
answer_index_list = []
for idx, target in enumerate(answer_targets):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert target is not 2
    s_chk.add(target != 2)
    
    # If UNSAT, target must be 2
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)