from z3 import *

# Lab assistants: 0=Julio, 1=Kevin, 2=Lan, 3=Nessa, 4=Olivia, 5=Rebecca
# Sessions: 0=WM, 1=WA, 2=TM, 3=TA, 4=FM, 5=FA

pos = [Int(f"pos_{i}") for i in range(6)]

solver = Solver()

# Domain constraints: all positions distinct and in [0,5]
solver.add(Distinct(pos))
for i in range(6):
    solver.add(pos[i] >= 0, pos[i] <= 5)

# Fixed constraint: Julio leads Thursday afternoon (session index 3)
solver.add(pos[0] == 3)

# Helper: day of session s is s // 2 (Z3-compatible version)
def day(s):
    return If(s % 2 == 0, s / 2, s / 2)

# Kevin and Rebecca must be on same day
solver.add(day(pos[1]) == day(pos[5]))

# Lan and Olivia cannot be on same day
solver.add(day(pos[2]) != day(pos[4]))

# Nessa must lead an afternoon session (odd indices: 1,3,5)
solver.add(Or(pos[3] == 1, pos[3] == 3, pos[3] == 5))

# Julio's session day < Olivia's session day
solver.add(day(pos[0]) < day(pos[4]))

# Additional deduction: Since Julio is on day 1 (Thursday), Olivia must be on day 2
solver.add(day(pos[4]) == 2)

# Check how many assistants (excluding Julio) have uniquely determined positions
count_fixed = 0

for assistant in range(1, 6):  # Kevin (1), Lan (2), Nessa (3), Olivia (4), Rebecca (5)
    possible_positions = []
    
    for session in range(6):
        if session == 3:  # Thursday afternoon is taken by Julio
            continue
            
        s_chk = Solver()
        s_chk.add(solver.assertions())
        s_chk.add(pos[assistant] == session)
        
        if s_chk.check() == sat:
            possible_positions.append(session)
    
    # If exactly one possible position, this assistant's session is determined
    if len(possible_positions) == 1:
        count_fixed += 1

# Map count to answer choice
answers = ['one', 'two', 'three', 'four', 'five']
print(answers[count_fixed])