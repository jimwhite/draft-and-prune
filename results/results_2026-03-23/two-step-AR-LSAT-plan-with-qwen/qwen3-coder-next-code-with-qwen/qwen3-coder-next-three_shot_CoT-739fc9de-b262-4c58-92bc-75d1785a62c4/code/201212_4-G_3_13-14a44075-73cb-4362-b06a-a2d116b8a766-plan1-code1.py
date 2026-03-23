from z3 import *

# Target variables: 1=1 day, 2=2 days, 3=3 days
IW = Int("IW")
IV = Int("IV")
SW = Int("SW")
SV = Int("SV")
TW = Int("TW")
TV = Int("TV")

solver = Solver()

# Domain constraints
for var in [IW, IV, SW, SV, TW, TV]:
    solver.add(var >= 1, var <= 3)

# Website ≤ Voicemail per client
solver.add(IW <= IV)
solver.add(SW <= SV)
solver.add(TW <= TV)

# Image's voicemail is strictly shorter than others' voicemail targets
solver.add(IV < SV, IV < TV)

# Solide's website is shorter than Truvest's website
solver.add(SW < TW)

# Given condition: Image's website target is 2 days
solver.add(IW == 2)

# Check which targets must be 2 days using proof by contradiction
target_names = [
    "Image's voicemail target",
    "Solide's website target",
    "Solide's voicemail target",
    "Truvest's website target",
    "Truvest's voicemail target"
]

target_vars = [IV, SW, SV, TW, TV]
answer_index_list = []

for idx, var in enumerate(target_vars):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert this target is NOT 2 days
    s_chk.add(var != 2)
    
    # If UNSAT, this target must be 2 days
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)