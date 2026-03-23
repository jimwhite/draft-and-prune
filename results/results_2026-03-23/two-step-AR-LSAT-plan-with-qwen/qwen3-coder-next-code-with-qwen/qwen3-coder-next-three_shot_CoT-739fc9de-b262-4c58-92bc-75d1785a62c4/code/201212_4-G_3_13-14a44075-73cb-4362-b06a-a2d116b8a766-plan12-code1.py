from z3 import *

# Define variables for each target (1, 2, or 3 days)
IMG_web = Int("IMG_web")
IMG_voicemail = Int("IMG_voicemail")
SOL_web = Int("SOL_web")
SOL_voicemail = Int("SOL_voicemail")
TRU_web = Int("TRU_web")
TRU_voicemail = Int("TRU_voicemail")

solver = Solver()

# Domain constraints: each target is 1, 2, or 3
for var in [IMG_web, IMG_voicemail, SOL_web, SOL_voicemail, TRU_web, TRU_voicemail]:
    solver.add(Or(var == 1, var == 2, var == 3))

# No-longer-than constraint: website target ≤ voicemail target for each client
solver.add(IMG_web <= IMG_voicemail)
solver.add(SOL_web <= SOL_voicemail)
solver.add(TRU_web <= TRU_voicemail)

# Image's voicemail target must be shorter than the other clients' voicemail targets
solver.add(IMG_voicemail < SOL_voicemail)
solver.add(IMG_voicemail < TRU_voicemail)

# Solide's website target must be shorter than Truvest's website target
solver.add(SOL_web < TRU_web)

# Given condition: Image's website target is 2 days
solver.add(IMG_web == 2)

# Answer choices: indices correspond to variables in order:
# 0: IMG_voicemail, 1: SOL_web, 2: SOL_voicemail, 3: TRU_web, 4: TRU_voicemail
answer_vars = [IMG_voicemail, SOL_web, SOL_voicemail, TRU_web, TRU_voicemail]

answer_index_list = []
for idx, var in enumerate(answer_vars):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert this target is NOT 2 days
    s_chk.add(var != 2)
    
    # If UNSAT, then this target must be 2 days
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)