from z3 import *

# Assistant indices: 0-Julio, 1-Kevin, 2-Lan, 3-Nessa, 4-Olivia, 5-Rebecca
# Session indices: 0-Wed AM, 1-Wed PM, 2-Thu AM, 3-Thu PM, 4-Fri AM, 5-Fri PM

assign = [Int(f"assign_{i}") for i in range(6)]

solver = Solver()

# Domain constraints: each assistant assigned to exactly one session (0-5)
for i in range(6):
    solver.add(assign[i] >= 0, assign[i] <= 5)

# All assistants assigned to distinct sessions
solver.add(Distinct(*assign))

# Helper function to get day from session index
def day(session_idx):
    # 0,1 -> Wednesday (day 0), 2,3 -> Thursday (day 1), 4,5 -> Friday (day 2)
    return If(session_idx <= 1, 0, If(session_idx <= 3, 1, 2))

# Kevin and Rebecca must lead sessions on the same day
solver.add(day(assign[1]) == day(assign[5]))

# Lan and Olivia cannot lead sessions on the same day
solver.add(day(assign[2]) != day(assign[4]))

# Nessa must lead an afternoon session (sessions 1, 3, or 5)
solver.add(Or(assign[3] == 1, assign[3] == 3, assign[3] == 5))

# Julio's session must be on an earlier day than Olivia's
solver.add(day(assign[0]) < day(assign[4]))

# Premise: Lan does NOT lead a Wednesday session (sessions 0 or 1)
solver.add(Or(assign[2] != 0, assign[2] != 1))

# Answer choices: [Rebecca(5), Olivia(4), Nessa(3), Kevin(1), Julio(0)]
answer_choices = [5, 4, 3, 1, 0]

# Check which assistants must lead a Thursday session (session index 2 or 3)
answer_index_list = []
for idx, assistant in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert assistant does NOT lead a Thursday session (not session 2 or 3)
    s_chk.add(And(assign[assistant] != 2, assign[assistant] != 3))
    
    # If UNSAT, then assistant must lead a Thursday session
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)