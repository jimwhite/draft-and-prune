from z3 import *

# Student indices: Juana=0, Kelly=1, Lateefah=2, Mei=3, Olga=4
green = [Bool(f"green_{i}") for i in range(5)]
facilitator = [Bool(f"facilitator_{i}") for i in range(5)]

solver = Solver()

# Team size constraints: exactly 3 on green (since Lateefah and Mei are on green)
solver.add(green[2] == True)  # Lateefah on green
solver.add(green[3] == True)  # Mei on green (premise)
solver.add(Sum([If(green[i], 1, 0) for i in range(5)]) == 3)

# Juana and Olga on different teams
solver.add(green[0] != green[4])

# Olga is a facilitator
solver.add(facilitator[4] == True)

# Kelly is not a facilitator
solver.add(facilitator[1] == False)

# Exactly one facilitator per team
# Green team facilitator: sum of facilitator[i] for green members == 1
green_facilitators = [And(green[i], facilitator[i]) for i in range(5)]
solver.add(Sum([If(f, 1, 0) for f in green_facilitators]) == 1)

# Red team facilitator: sum of facilitator[i] for red members == 1
red_facilitators = [And(Not(green[i]), facilitator[i]) for i in range(5)]
solver.add(Sum([If(f, 1, 0) for f in red_facilitators]) == 1)

# Check each answer choice
answer_choices = [
    "Juana is assigned to the green team.",  # index 0
    "Kelly is assigned to the red team.",   # index 1
    "Olga is assigned to the green team.",  # index 2
    "Lateefah is a facilitator.",           # index 3
    "Mei is a facilitator."                 # index 4
]

answer_index_list = []

# Case A: Juana on green (green[0] == True), Olga on red
solver_A = Solver()
solver_A.add(solver.assertions())
solver_A.add(green[0] == True)

# Case B: Juana on red (green[0] == False), Olga on green
solver_B = Solver()
solver_B.add(solver.assertions())
solver_B.add(green[0] == False)

# Check each answer choice in both cases
for idx, ans in enumerate(answer_choices):
    # Option 0: Juana on green
    if idx == 0:
        cond_A = True
        cond_B = False
    # Option 1: Kelly on red (i.e., not green)
    elif idx == 1:
        cond_A = False
        cond_B = False
    # Option 2: Olga on green
    elif idx == 2:
        cond_A = False
        cond_B = True
    # Option 3: Lateefah is facilitator
    elif idx == 3:
        s_chk_A = Solver()
        s_chk_A.add(solver_A.assertions())
        s_chk_A.add(facilitator[2] == False)
        res_A = s_chk_A.check() == unsat
        
        s_chk_B = Solver()
        s_chk_B.add(solver_B.assertions())
        s_chk_B.add(facilitator[2] == False)
        res_B = s_chk_B.check() == unsat
        
        cond_A = res_A
        cond_B = res_B
    # Option 4: Mei is facilitator
    elif idx == 4:
        s_chk_A = Solver()
        s_chk_A.add(solver_A.assertions())
        s_chk_A.add(facilitator[3] == False)
        res_A = s_chk_A.check() == unsat
        
        s_chk_B = Solver()
        s_chk_B.add(solver_B.assertions())
        s_chk_B.add(facilitator[3] == False)
        res_B = s_chk_B.check() == unsat
        
        cond_A = res_A
        cond_B = res_B
    
    # For options 0,1,2: evaluate directly in both cases
    if idx <= 2:
        # Case A model check
        s_A = Solver()
        s_A.add(solver_A.assertions())
        if idx == 0:
            s_A.add(green[0] == True)
        elif idx == 1:
            s_A.add(Not(green[1]))
        elif idx == 2:
            s_A.add(green[4] == True)
        
        sat_A = s_A.check() == sat
        
        # Case B model check
        s_B = Solver()
        s_B.add(solver_B.assertions())
        if idx == 0:
            s_B.add(green[0] == True)
        elif idx == 1:
            s_B.add(Not(green[1]))
        elif idx == 2:
            s_B.add(green[4] == True)
        
        sat_B = s_B.check() == sat
        
        cond_A = sat_A
        cond_B = sat_B
    
    # Must be true in both cases
    if cond_A and cond_B:
        answer_index_list.append(idx)

print(answer_index_list)