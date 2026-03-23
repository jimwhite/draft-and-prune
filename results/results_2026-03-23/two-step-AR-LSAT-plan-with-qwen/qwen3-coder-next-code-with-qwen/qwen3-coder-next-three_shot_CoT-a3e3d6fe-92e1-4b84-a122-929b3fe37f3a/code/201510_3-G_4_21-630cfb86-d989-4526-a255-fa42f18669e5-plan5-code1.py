from z3 import *

# Cookbook indices: K=0, L=1, M=2, N=3, O=4, P=5
season = [Bool(f"season_{i}") for i in range(6)]

solver = Solver()

# Given: N is published in the fall → season[3] = True
solver.add(season[3])

# M and P cannot be in the same season → season[2] != season[5]
solver.add(season[2] != season[5])

# K and N must be in the same season → season[0] == season[3]
solver.add(season[0] == season[3])

# If K is in fall, O must be in fall → Since K=fall (from above), this forces O=fall
# But we can express it as: season[0] → season[4]
solver.add(Implies(season[0], season[4]))

# If M is in fall, N must be in spring → season[2] → Not(season[3])
# Since season[3] is True, this becomes: Not(season[2]) (M must be spring)
solver.add(Implies(season[2], Not(season[3])))

# Check consistency and extract forced values
if solver.check() == sat:
    m = solver.model()
    
    # Based on reasoning, we know:
    # season[3] (N) = True
    # season[0] (K) = True (same as N)
    # season[4] (O) = True (K implies O, and K=True)
    # season[2] (M) = False (since N=True, M cannot be True)
    # season[5] (P) = True (since M=False and they must differ)
    
    # L (index 1) is unconstrained
    
    # Now check each choice
    choices = [
        "K is published in the spring.",  # season[0] == False
        "L is published in the fall.",    # season[1] == True
        "M is published in the fall.",    # season[2] == True
        "O is published in the spring.",  # season[4] == False
        "P is published in the spring."   # season[5] == False
    ]
    
    answer_index_list = []
    
    for idx, choice in enumerate(choices):
        s_chk = Solver()
        s_chk.add(solver.assertions())
        
        if idx == 0:  # K in spring
            s_chk.add(Not(season[0]))
        elif idx == 1:  # L in fall
            s_chk.add(season[1])
        elif idx == 2:  # M in fall
            s_chk.add(season[2])
        elif idx == 3:  # O in spring
            s_chk.add(Not(season[4]))
        elif idx == 4:  # P in spring
            s_chk.add(Not(season[5]))
        
        if s_chk.check() == sat:
            answer_index_list.append(idx)
    
    print(answer_index_list)
else:
    # If base constraints are inconsistent (shouldn't happen), output empty list
    print([])