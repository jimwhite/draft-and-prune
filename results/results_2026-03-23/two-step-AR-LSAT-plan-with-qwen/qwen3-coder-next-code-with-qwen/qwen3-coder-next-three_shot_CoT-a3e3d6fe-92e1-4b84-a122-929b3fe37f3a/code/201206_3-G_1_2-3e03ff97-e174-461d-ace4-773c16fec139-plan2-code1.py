from z3 import *

# Assistant indices: Julio=0, Kevin=1, Lan=2, Nessa=3, Olivia=4, Rebecca=5
ASSISTANTS = ["Julio", "Kevin", "Lan", "Nessa", "Olivia", "Rebecca"]
(JULIO, KEVIN, LAN, NESSA, OLIVIA, REBECCA) = range(6)

# Session indices: 0-5 (Wed AM=0, Wed PM=1, Thu AM=2, Thu PM=3, Fri AM=4, Fri PM=5)
SESSIONS = 6

# Create assignment variables: assign[i] = session index for assistant i
assign = [Int(f"assign_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Distinctness constraint: each session led by exactly one assistant
solver.add(Distinct(*assign))

# Day and period helpers using Z3 expressions (not Python integer division)
def day(session_var):
    return If(session_var == 0, IntVal(0), (session_var - (session_var % 2)) / 2)

def period(session_var):
    return session_var % 2

# Add constraints
## Kevin and Rebecca must be on the same day
solver.add(day(assign[KEVIN]) == day(assign[REBECCA]))

## Lan and Olivia cannot be on the same day
solver.add(day(assign[LAN]) != day(assign[OLIVIA]))

## Nessa must lead an afternoon session
solver.add(period(assign[NESSA]) == 1)

## Julio's session must be on an earlier day than Olivia's
solver.add(day(assign[JULIO]) < day(assign[OLIVIA]))

## Conditional premise: Lan does NOT lead a Wednesday session
solver.add(day(assign[LAN]) != 0)

# Answer choices indices: Rebecca=5, Olivia=4, Nessa=3, Kevin=1, Julio=0
answer_choices = [REBECCA, OLIVIA, NESSA, KEVIN, JULIO]

# Check each answer choice
answer_index_list = []
for idx, assistant in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert this assistant leads NO Thursday session (day != 1)
    s_chk.add(day(assign[assistant]) != 1)
    
    # If UNSAT, this assistant MUST lead a Thursday session
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)