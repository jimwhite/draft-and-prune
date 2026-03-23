from z3 import *

# Student indices: George=0, Helen=1, Irving=2, Kyle=3, Lenore=4, Nina=5, Olivia=6, Robert=7
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]

# Slot variables: slot[s][d][t] = True if student s gives report on day d, time t
# Days: Monday=0, Tuesday=1, Wednesday=2
# Times: morning=0, afternoon=1
slot = [[[Bool(f"slot_{s}_{d}_{t}") for t in range(2)] for d in range(3)] for s in range(8)]

solver = Solver()

# Exactly six reports total
solver.add(Sum([If(slot[s][d][t], 1, 0) 
                for s in range(8) 
                for d in range(3) 
                for t in range(2)]) == 6)

# One report per slot (at most one student per time slot)
for d in range(3):
    for t in range(2):
        # At most one student per slot
        solver.add(Sum([If(slot[s][d][t], 1, 0) for s in range(8)]) <= 1)

# Two reports per day
for d in range(3):
    solver.add(Sum([If(slot[s][d][t], 1, 0) 
                    for s in range(8) 
                    for t in range(2)]) == 2)

# Tuesday is the only day George can give a report
for d in range(3):
    for t in range(2):
        if d != 1:  # Not Tuesday
            solver.add(Not(slot[0][d][t]))  # George cannot report on Mon/Wed

# Olivia (6) and Robert (7) cannot give afternoon reports
for d in range(3):
    solver.add(Not(slot[6][d][1]))  # Olivia not afternoon
    solver.add(Not(slot[7][d][1]))  # Robert not afternoon

# Kyle (3) and Lenore (4) do NOT give reports
for d in range(3):
    for t in range(2):
        solver.add(Not(slot[3][d][t]))
        solver.add(Not(slot[4][d][t]))

# Nina conditional constraint
# If Nina gives a report on Monday (d=0), then Helen and Irving must both give reports on Tuesday
# If Nina gives a report on Tuesday (d=1), then Helen and Irving must both give reports on Wednesday
# If Nina gives a report on Wednesday (d=2), no further constraint

nina_mon = slot[5][0][0] | slot[5][0][1]
nina_tue = slot[5][1][0] | slot[5][1][1]
nina_wed = slot[5][2][0] | slot[5][2][1]

# Nina on Monday → Helen and Irving both report on Tuesday
solver.add(Implies(nina_mon, 
                   (slot[1][1][0] | slot[1][1][1]) & 
                   (slot[2][1][0] | slot[2][1][1])))

# Nina on Tuesday → Helen and Irving both report on Wednesday
solver.add(Implies(nina_tue, 
                   (slot[1][2][0] | slot[1][2][1]) & 
                   (slot[2][2][0] | slot[2][2][1])))

# Answer choices: morning reporters for Mon, Tue, Wed
answer_choices = [
    ("Helen", "George", "Nina"),      # 0
    ("Irving", "Robert", "Helen"),    # 1
    ("Nina", "Helen", "Olivia"),      # 2
    ("Olivia", "Robert", "Irving"),   # 3
    ("Robert", "George", "Helen")     # 4
]

# Map student names to indices
student_idx = {name: i for i, name in enumerate(students)}

# Check each answer choice
answer_index_list = []
for idx, (mon_morn, tue_morn, wed_morn) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Enforce morning slots as per choice
    mon_stud = student_idx[mon_morn]
    tue_stud = student_idx[tue_morn]
    wed_stud = student_idx[wed_morn]
    
    s_chk.add(slot[mon_stud][0][0] == True)
    s_chk.add(slot[tue_stud][1][0] == True)
    s_chk.add(slot[wed_stud][2][0] == True)
    
    # Check satisfiability
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)