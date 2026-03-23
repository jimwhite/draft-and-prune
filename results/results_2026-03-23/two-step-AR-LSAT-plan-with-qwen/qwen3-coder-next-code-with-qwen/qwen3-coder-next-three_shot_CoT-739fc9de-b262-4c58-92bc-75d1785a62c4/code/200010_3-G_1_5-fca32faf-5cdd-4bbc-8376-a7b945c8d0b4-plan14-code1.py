from z3 import *

# Student indices
(G, H, I, K, L, N, O, R) = range(8)
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]

# Day-slot variables: assigned[student][day_slot] where day_slot: 0=Mon_mor, 1=Mon_aft, 2=Tue_mor, 3=Tue_aft, 4=Wed_mor, 5=Wed_aft
assigned = [[Bool(f"assigned_{students[s]}_{ds}") for ds in range(6)] for s in range(8)]

# Base solver
solver = Solver()

# Exactly six students report (each report is one student in one slot)
solver.add(Sum([If(assigned[s][ds], 1, 0) for s in range(8) for ds in range(6)]) == 6)

# Exactly two reports per day
for day in range(3):
    morning_slot = day * 2
    afternoon_slot = day * 2 + 1
    solver.add(Sum([If(assigned[s][morning_slot], 1, 0) + If(assigned[s][afternoon_slot], 1, 0) for s in range(8)]) == 2)

# One report per slot per day (at most one student per slot)
for ds in range(6):
    # At most one student assigned to this slot
    for s1 in range(8):
        for s2 in range(s1 + 1, 8):
            solver.add(Not(And(assigned[s1][ds], assigned[s2][ds])))

# Tuesday is the only day George can report
for ds in range(6):
    if ds != 2 and ds != 3:  # Only Tuesday slots (morning=2, afternoon=3)
        solver.add(Not(assigned[G][ds]))

# Neither Olivia nor Robert can give an afternoon report
for s in [O, R]:
    for day in range(3):
        afternoon_slot = day * 2 + 1
        solver.add(Not(assigned[s][afternoon_slot]))

# Given assumptions: Kyle gives afternoon report on Tuesday, Helen gives afternoon report on Wednesday
solver.add(assigned[K][3] == True)  # Kyle, Tue_aft (slot 3)
solver.add(assigned[H][5] == True)  # Helen, Wed_aft (slot 5)

# Nina conditional constraint
# If Nina reports on Monday (slots 0 or 1), then Helen and Irving must both report on Tuesday (both slots)
nina_mon = Or(assigned[N][0], assigned[N][1])
solver.add(Implies(nina_mon, And(
    assigned[H][2], assigned[H][3],  # Helen both Tuesday slots
    assigned[I][2], assigned[I][3]   # Irving both Tuesday slots
)))

# If Nina reports on Tuesday (slots 2 or 3), then Helen and Irving must both report on Wednesday (both slots)
nina_tue = Or(assigned[N][2], assigned[N][3])
solver.add(Implies(nina_tue, And(
    assigned[H][4], assigned[H][5],  # Helen both Wednesday slots
    assigned[I][4], assigned[I][5]   # Irving both Wednesday slots
)))

# Answer choices: (Mon_mor, Tue_mor, Wed_mor)
answer_choices = [
    ("Irving", "Lenore", "Nina"),      # 0
    ("Lenore", "George", "Irving"),    # 1
    ("Nina", "Irving", "Lenore"),      # 2
    ("Robert", "George", "Irving"),    # 3
    ("Robert", "Irving", "Lenore")     # 4
]

# Map student names to indices
student_idx = {name: idx for idx, name in enumerate(students)}

# Check each answer choice
answer_index_list = []
for idx, (mon_mor_name, tue_mor_name, wed_mor_name) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add fixed morning assignments
    mon_mor_idx = student_idx[mon_mor_name]
    tue_mor_idx = student_idx[tue_mor_name]
    wed_mor_idx = student_idx[wed_mor_name]
    
    s_chk.add(assigned[mon_mor_idx][0] == True)  # Monday morning
    s_chk.add(assigned[tue_mor_idx][2] == True)  # Tuesday morning
    s_chk.add(assigned[wed_mor_idx][4] == True)  # Wednesday morning
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)