from z3 import *

# Lab assistants: Julio=0, Kevin=1, Lan=2, Nessa=3, Olivia=4, Rebecca=5
# Sessions: 0-WM, 1-WA, 2-TM, 3-TA (fixed for Julio), 4-FM, 5-FA

assistant = [Int(f"asst_{i}") for i in range(6)]

solver = Solver()

# All assistants distinct
solver.add(Distinct(*assistant))

# Fixed: Julio leads Thursday afternoon (session 3)
solver.add(assistant[3] == 0)

# Helper: session_to_day(session_index) -> 0=Wed, 1=Thu, 2=Fri
# session_to_time(session_index) -> 0=morning, 1=afternoon

def day(s):
    return s // 2

def time(s):
    return s % 2

# Use binary assignment variables instead of inverse mapping
# x[a][s] = 1 if assistant a leads session s, 0 otherwise
x = [[Bool(f"x_{a}_{s}") for s in range(6)] for a in range(6)]

# Each assistant leads exactly one session
for a in range(6):
    solver.add(Sum([If(x[a][s], 1, 0) for s in range(6)]) == 1)

# Each session has exactly one assistant
for s in range(6):
    solver.add(Sum([If(x[a][s], 1, 0) for a in range(6)]) == 1)

# Julio leads Thursday afternoon (session 3)
solver.add(x[0][3] == True)

# Kevin and Rebecca same day
for s1 in range(6):
    for s2 in range(6):
        if day(s1) == day(s2):
            solver.add(Implies(x[1][s1], x[5][s2]))
            solver.add(Implies(x[5][s2], x[1][s1]))

# Actually better: directly express same day constraint
solver.add(Or(*[And(x[1][s1], x[5][s2]) for s1 in range(6) for s2 in range(6) if day(s1) == day(s2)]))

# Lan and Olivia different days
solver.add(Or(*[And(x[2][s1], x[4][s2]) for s1 in range(6) for s2 in range(6) if day(s1) != day(s2)]))

# Nessa afternoon session
solver.add(Or(x[3][1], x[3][3], x[3][5]))

# Julio before Olivia (session index)
solver.add(Or(*[And(x[0][s1], x[4][s2]) for s1 in range(6) for s2 in range(6) if s1 < s2]))

# Now check for each other assistant (Kevin, Lan, Nessa, Olivia, Rebecca)
# how many sessions they can possibly lead under the constraint assistant[3]==0

other_assistants = [1, 2, 3, 4, 5]  # Kevin, Lan, Nessa, Olivia, Rebecca
unique_count = 0

for a in other_assistants:
    feasible_sessions = []
    for s in range(6):
        if s == 3:  # skip Thursday afternoon (already taken by Julio)
            continue
        s_chk = Solver()
        for assertion in solver.assertions():
            s_chk.add(assertion)
        s_chk.add(x[a][s] == True)
        if s_chk.check() == sat:
            feasible_sessions.append(s)
    if len(feasible_sessions) == 1:
        unique_count += 1

print(unique_count)