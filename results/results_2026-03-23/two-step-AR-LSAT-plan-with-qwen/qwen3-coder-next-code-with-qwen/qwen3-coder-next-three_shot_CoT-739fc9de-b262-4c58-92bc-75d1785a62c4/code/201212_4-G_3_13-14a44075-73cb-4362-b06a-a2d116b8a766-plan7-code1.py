from z3 import *

# Variables for targets: 1=1 day, 2=2 days, 3=3 days
I_web, I_voic = Ints('I_web I_voic')
S_web, S_voic = Ints('S_web S_voic')
T_web, T_voic = Ints('T_web T_voic')

solver = Solver()

# Domain constraints: each target in {1, 2, 3}
for var in [I_web, I_voic, S_web, S_voic, T_web, T_voic]:
    solver.add(Or(var == 1, var == 2, var == 3))

# Ordering constraint for each client: website target <= voicemail target
solver.add(I_web <= I_voic)
solver.add(S_web <= S_voic)
solver.add(T_web <= T_voic)

# Image's voicemail target must be shorter than the other clients' voicemail targets
solver.add(I_voic < S_voic)
solver.add(I_voic < T_voic)

# Solide's website target must be shorter than Truvest's website target
solver.add(S_web < T_web)

# Given condition: Image's website target is 2 days
solver.add(I_web == 2)

# Check which answer choice must be 2 days using proof by contradiction
answer_choices = [
    I_voic,   # Image's voicemail target (index 0)
    S_web,    # Solide's website target (index 1)
    S_voic,   # Solide's voicemail target (index 2)
    T_web,    # Truvest's website target (index 3)
    T_voic    # Truvest's voicemail target (index 4)
]

answer_index_list = []
for idx, var in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert this target is NOT 2 days
    s_chk.add(var != 2)
    
    # If UNSAT, then this target must be 2 days
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)