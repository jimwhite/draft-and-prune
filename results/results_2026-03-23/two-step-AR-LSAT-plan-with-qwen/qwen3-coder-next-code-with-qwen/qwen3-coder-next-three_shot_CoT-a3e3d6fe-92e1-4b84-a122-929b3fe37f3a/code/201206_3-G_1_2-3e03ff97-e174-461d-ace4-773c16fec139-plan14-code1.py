from z3 import *

# Lab assistants: Julio=0, Kevin=1, Lan=2, Nessa=3, Olivia=4, Rebecca=5
# Sessions: 0-Wed AM, 1-Wed PM, 2-Thu AM, 3-Thu PM, 4-Fri AM, 5-Fri PM

# session_of[a] = session index assigned to assistant a
session_of = [Int(f"session_{a}") for a in range(6)]

solver = Solver()

# Each assistant leads exactly one session (injective)
solver.add(Distinct(*session_of))
solver.add(And([And(session_of[a] >= 0, session_of[a] <= 5) for a in range(6)]))

# Helper functions
def day(s):
    return If(s == 0, 0, If(s == 1, 0, If(s == 2, 1, If(s == 3, 1, If(s == 4, 2, 2)))))

def is_afternoon(s):
    return Or(s == 1, s == 3, s == 5)

# Kevin and Rebecca must lead sessions on the same day
solver.add(day(session_of[1]) == day(session_of[5]))

# Lan and Olivia different days
solver.add(day(session_of[2]) != day(session_of[4]))

# Nessa afternoon session
solver.add(is_afternoon(session_of[3]))

# Julio earlier day than Olivia
solver.add(day(session_of[0]) < day(session_of[4]))

# Premise: Lan does NOT lead Wednesday session
solver.add(day(session_of[2]) != 0)

# Answer choices: Rebecca=5, Olivia=4, Nessa=3, Kevin=1, Julio=0
answer_choices = [5, 4, 3, 1, 0]  # indices for Rebecca, Olivia, Nessa, Kevin, Julio

answer_index_list = []

for idx, assistant in enumerate(answer_choices):
    s_chk = Solver()
    # Add all base constraints and premise
    for assertion in solver.assertions():
        s_chk.add(assertion)
    
    # Add assumption that assistant does NOT lead Thursday session
    s_chk.add(day(session_of[assistant]) != 1)
    
    # If UNSAT, then assistant MUST lead Thursday
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)