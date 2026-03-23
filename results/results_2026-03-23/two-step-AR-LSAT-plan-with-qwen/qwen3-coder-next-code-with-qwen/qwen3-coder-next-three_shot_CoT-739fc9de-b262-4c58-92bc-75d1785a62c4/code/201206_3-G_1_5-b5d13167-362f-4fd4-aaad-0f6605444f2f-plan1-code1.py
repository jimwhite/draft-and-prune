from z3 import *

# Lab assistants: Julio, Kevin, Lan, Nessa, Olivia, Rebecca
assistants = ["Julio", "Kevin", "Lan", "Nessa", "Olivia", "Rebecca"]
n = len(assistants)

# Session indices: 0=WM, 1=WA, 2=TM, 3=TA, 4=FM, 5=FA
pos = [Int(f"pos_{a}") for a in assistants]

# Base solver
solver = Solver()

# Domain constraints: each assistant assigned to exactly one session (0-5)
for i in range(n):
    solver.add(pos[i] >= 0, pos[i] <= 5)

# All positions distinct
solver.add(Distinct(pos))

# Fixed constraint: Julio leads Thursday afternoon → session index 3
solver.add(pos[0] == 3)  # Julio is at index 0

# Helper functions for day and time
def get_day(session_idx):
    # 0=Wed (sessions 0,1), 1=Thu (2,3), 2=Fri (4,5)
    if session_idx in [0, 1]:
        return 0
    elif session_idx in [2, 3]:
        return 1
    else:
        return 2

def get_time(session_idx):
    # morning: even indices (0,2,4), afternoon: odd indices (1,3,5)
    return session_idx % 2

# Kevin and Rebecca must lead sessions on the same day
solver.add(get_day(pos[1]) == get_day(pos[5]))  # Kevin=1, Rebecca=5

# Lan and Olivia cannot lead sessions on the same day
solver.add(get_day(pos[2]) != get_day(pos[4]))  # Lan=2, Olivia=4

# Nessa must lead an afternoon session
solver.add(get_time(pos[3]) == 1)  # Nessa=3

# Julio's session must be earlier than Olivia's
solver.add(pos[0] < pos[4])  # Julio=0, Olivia=4

# Collect all satisfying assignments
models = []
while solver.check() == sat:
    m = solver.model()
    models.append(m)
    # Add constraint to exclude current model
    solver.add(Or([pos[i] != m[pos[i]] for i in range(n)]))

# Count how many assistants (excluding Julio) have uniquely determined sessions
determined_count = 0

# For each assistant except Julio (indices 1-5)
for i in range(1, n):
    # Collect all possible sessions for this assistant across models
    possible_sessions = set()
    for m in models:
        possible_sessions.add(m[pos[i]].as_long())
    
    # If only one possible session, this assistant's assignment is determined
    if len(possible_sessions) == 1:
        determined_count += 1

# Map count to answer string
answer_map = {
    0: 'zero',
    1: 'one',
    2: 'two',
    3: 'three',
    4: 'four',
    5: 'five'
}

print(answer_map[determined_count])