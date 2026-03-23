from z3 import *

# Lab assistants: 0=Julio, 1=Kevin, 2=Lan, 3=Nessa, 4=Olivia, 5=Rebecca
# Sessions: 0=Wed AM, 1=Wed PM, 2=Thu AM, 3=Thu PM, 4=Fri AM, 5=Fri PM

pos = [Int(f"pos_{i}") for i in range(6)]

solver = Solver()

# Domain constraints: each assistant assigned to exactly one session (0-5)
solver.add([And(pos[i] >= 0, pos[i] <= 5) for i in range(6)])
solver.add(Distinct(pos))

# Fixed constraint: Julio leads Thursday afternoon session (session index 3)
solver.add(pos[0] == 3)

# Kevin and Rebecca must lead sessions on the same day
solver.add(pos[1] // 2 == pos[5] // 2)

# Lan and Olivia cannot lead sessions on the same day
solver.add(pos[2] // 2 != pos[4] // 2)

# Nessa must lead an afternoon session (session indices 1, 3, 5)
solver.add(Or(pos[3] == 1, pos[3] == 3, pos[3] == 5))

# Julio's session must be on an earlier day than Olivia's
# Since pos[0] = 3 (day index 1), we need day of Olivia > 1 → session index in {4,5}
solver.add(pos[0] // 2 < pos[4] // 2)

# Collect possible sessions for each assistant (excluding Julio)
assistant_indices = [1, 2, 3, 4, 5]  # Kevin, Lan, Nessa, Olivia, Rebecca
forced_count = 0

for i in assistant_indices:
    possible_sessions = []
    for s in range(6):
        if s == 3:  # session 3 is already taken by Julio
            continue
        s_chk = Solver()
        s_chk.add(solver.assertions())
        s_chk.add(pos[i] == s)
        if s_chk.check() == sat:
            possible_sessions.append(s)
    
    if len(possible_sessions) == 1:
        forced_count += 1

# Map count to answer choice
answers = ['one', 'two', 'three', 'four', 'five']
print(answers[forced_count])