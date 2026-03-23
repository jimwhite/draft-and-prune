from z3 import *

# Assistant indices: 0=Julio, 1=Kevin, 2=Lan, 3=Nessa, 4=Olivia, 5=Rebecca
(JULIO, KEVIN, LAN, NESSA, OLIVIA, REBECCA) = range(6)

# Session indices: 0=W_morning, 1=W_afternoon, 2=Th_morning, 3=Th_afternoon, 4=F_morning, 5=F_afternoon
# Day mapping: 0->Wed, 1->Wed, 2->Thu, 3->Thu, 4->Fri, 5->Fri
def day(session_idx):
    return If(session_idx < 2, 0,
              If(session_idx < 4, 1, 2))

# Assignment variables: assign[i] = session index for assistant i
assign = [Int(f"assign_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: each assistant assigned to exactly one session (0-5)
for i in range(6):
    solver.add(assign[i] >= 0, assign[i] <= 5)

# All assignments distinct (bijection)
solver.add(Distinct(*assign))

# Kevin and Rebecca same day constraint
solver.add(day(assign[KEVIN]) == day(assign[REBECCA]))

# Lan and Olivia different day constraint
solver.add(day(assign[LAN]) != day(assign[OLIVIA]))

# Nessa afternoon constraint: sessions 1, 3, or 5
solver.add(Or(assign[NESSA] == 1, assign[NESSA] == 3, assign[NESSA] == 5))

# Julio earlier day than Olivia
solver.add(day(assign[JULIO]) < day(assign[OLIVIA]))

# Premise: Lan does NOT lead a Wednesday session (not sessions 0 or 1)
solver.add(And(assign[LAN] != 0, assign[LAN] != 1))

# Answer choices: ['Rebecca', 'Olivia', 'Nessa', 'Kevin', 'Julio']
answer_choices = [REBECCA, OLIVIA, NESSA, KEVIN, JULIO]

# Check each answer choice
answer_index_list = []
for idx, assistant in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint that assistant does NOT lead any Thursday session (sessions 2 or 3)
    s_chk.add(And(assign[assistant] != 2, assign[assistant] != 3))
    
    # If UNSAT, then assistant MUST lead a Thursday session
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)