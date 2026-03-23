from z3 import *

# Lab assistants indices: 0=Julio, 1=Kevin, 2=Lan, 3=Nessa, 4=Olivia, 5=Rebecca
# Sessions indices: 0=WM, 1=WA, 2=TM, 3=TA, 4=FM, 5=FA
# day(session): 0 for Wed (sessions 0,1), 1 for Thu (2,3), 2 for Fri (4,5)
# time(session): 0 for morning (0,2,4), 1 for afternoon (1,3,5)

pos = [Int(f"pos_{i}") for i in range(6)]

solver = Solver()

# Domain constraints: each assistant assigned to exactly one session (0-5)
solver.add([And(pos[i] >= 0, pos[i] <= 5) for i in range(6)])
solver.add(Distinct(pos))

# Fixed constraint: Julio leads Thursday afternoon (session index 3)
solver.add(pos[0] == 3)

# Kevin and Rebecca same day constraint
def day(s):
    return If(Or(s == 0, s == 1), 0, If(Or(s == 2, s == 3), 1, 2))

def time(s):
    return If(Or(s == 0, s == 2, s == 4), 0, 1)

solver.add(day(pos[1]) == day(pos[5]))  # Kevin and Rebecca same day

# Lan and Olivia not same day constraint
solver.add(day(pos[2]) != day(pos[4]))

# Nessa afternoon constraint
solver.add(time(pos[3]) == 1)

# Julio earlier than Olivia (pos[0] < pos[4])
solver.add(pos[0] < pos[4])

# Collect possible sessions for each assistant (except Julio)
other_assistants = [1, 2, 3, 4, 5]  # Kevin, Lan, Nessa, Olivia, Rebecca
uniquely_determined_count = 0

for assistant in other_assistants:
    possible_sessions = []
    for session_idx in range(6):
        s_check = Solver()
        s_check.add(solver.assertions())
        s_check.add(pos[assistant] == session_idx)
        
        if s_check.check() == sat:
            possible_sessions.append(session_idx)
    
    if len(possible_sessions) == 1:
        uniquely_determined_count += 1

print(uniquely_determined_count)