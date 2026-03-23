from z3 import *

# Lab assistant indices: 0-Julio, 1-Kevin, 2-Lan, 3-Nessa, 4-Olivia, 5-Rebecca
(JUL, KEV, LAN, NES, OLI, REB) = range(6)

# Session positions: 0-5 (WM=0, WA=1, TM=2, TA=3, FM=4, FA=5)
pos = [Int(f"pos_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: each position between 0 and 5, all distinct
for i in range(6):
    solver.add(pos[i] >= 0, pos[i] <= 5)
solver.add(Distinct(*pos))

# Helper functions for day and time using Z3 constructs
def get_day(p):
    return p / 2

def get_time(p):
    return p % 2

# Constraint: Kevin and Rebecca same day
solver.add(get_day(pos[KEV]) == get_day(pos[REB]))

# Constraint: Lan and Olivia different days
solver.add(get_day(pos[LAN]) != get_day(pos[OLI]))

# Constraint: Nessa afternoon session (time = 1)
solver.add(get_time(pos[NES]) == 1)

# Constraint: Julio earlier day than Olivia
solver.add(get_day(pos[JUL]) < get_day(pos[OLI]))

# Given condition: Lan does NOT lead a Wednesday session (day 0)
solver.add(get_day(pos[LAN]) != 0)

# Answer choices indices
answer_choices = [REB, OLI, NES, KEV, JUL]

# Check each answer choice
answer_index_list = []
for idx, assistant in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert this assistant does NOT lead any Thursday session (day 1)
    s_chk.add(get_day(pos[assistant]) != 1)
    
    # If UNSAT, this assistant must lead a Thursday session
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)