from z3 import *

# Lab assistants indices: Julio=0, Kevin=1, Lan=2, Nessa=3, Olivia=4, Rebecca=5
# Sessions: 0-Wed AM, 1-Wed PM, 2-Thurs AM, 3-Thurs PM (fixed for Julio), 4-Fri AM, 5-Fri PM

# Create session variables for each assistant
session = [Int(f"session_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Distinctness constraint: each session assigned to exactly one assistant
solver.add(Distinct(*session))

# Fixed constraint: Julio leads Thursday afternoon (session 3)
solver.add(session[0] == 3)

# Helper functions for day and time using Z3 constructs
def day(s):
    return s / 2  # Integer division in Z3

def time(s):
    return s % 2

# Kevin and Rebecca must be on the same day
solver.add(day(session[1]) == day(session[5]))

# Lan and Olivia cannot be on the same day
solver.add(day(session[2]) != day(session[4]))

# Nessa must lead an afternoon session (time = 1)
solver.add(time(session[3]) == 1)

# Julio's session day < Olivia's session day
solver.add(day(session[0]) < day(session[4]))

# Check feasibility
if solver.check() != sat:
    print("Error: No solution exists")
else:
    # Collect all assistants except Julio
    other_assistants = [1, 2, 3, 4, 5]  # Kevin, Lan, Nessa, Olivia, Rebecca
    
    determined_count = 0
    for assistant in other_assistants:
        possible_sessions = []
        # Try each session except Julio's (session 3)
        for s in range(6):
            if s == 3:
                continue
            s_chk = Solver()
            s_chk.add(solver.assertions())
            s_chk.add(session[assistant] == s)
            
            if s_chk.check() == sat:
                possible_sessions.append(s)
        
        # If exactly one session is possible, assistant's session is determined
        if len(possible_sessions) == 1:
            determined_count += 1
    
    # Map count to answer choice index
    if determined_count == 1:
        print(0)  # 'one'
    elif determined_count == 2:
        print(1)  # 'two'
    elif determined_count == 3:
        print(2)  # 'three'
    elif determined_count == 4:
        print(3)  # 'four'
    elif determined_count == 5:
        print(4)  # 'five'