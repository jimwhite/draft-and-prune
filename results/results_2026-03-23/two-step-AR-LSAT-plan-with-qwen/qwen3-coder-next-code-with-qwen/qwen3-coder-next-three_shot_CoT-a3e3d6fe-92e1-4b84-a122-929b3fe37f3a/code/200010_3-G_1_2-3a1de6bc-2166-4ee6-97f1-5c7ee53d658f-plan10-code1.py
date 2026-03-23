from z3 import *

# Student indices
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
student_idx = {s: i for i, s in enumerate(students)}

# Days: 0=Monday, 1=Tuesday, 2=Wednesday
# Slots: 0=morning, 1=afternoon
report = [[[Bool(f"report_{s}_{d}_{slot}") for slot in range(2)] for d in range(3)] for s in range(8)]

solver = Solver()

# Exactly six reports total
total_reports = Sum([If(report[s][d][slot], 1, 0) 
                     for s in range(8) for d in range(3) for slot in range(2)])
solver.add(total_reports == 6)

# Two reports per day
for d in range(3):
    daily_reports = Sum([If(report[s][d][slot], 1, 0) 
                         for s in range(8) for slot in range(2)])
    solver.add(daily_reports == 2)

# George only on Tuesday
for d in [0, 2]:  # Monday and Wednesday
    for slot in range(2):
        solver.add(Not(report[student_idx["George"]][d][slot]))

# Olivia and Robert cannot give afternoon reports
for s in [student_idx["Olivia"], student_idx["Robert"]]:
    for d in range(3):
        solver.add(Not(report[s][d][1]))

# Nina implication constraints
# If Nina reports on Monday, then Helen and Irving must both report on Tuesday
nina_mon = Or(report[student_idx["Nina"]][0][0], report[student_idx["Nina"]][0][1])
helen_tue = Or(report[student_idx["Helen"]][1][0], report[student_idx["Helen"]][1][1])
irving_tue = Or(report[student_idx["Irving"]][1][0], report[student_idx["Irving"]][1][1])
solver.add(Implies(nina_mon, And(helen_tue, irving_tue)))

# If Nina reports on Tuesday, then Helen and Irving must both report on Wednesday
nina_tue = Or(report[student_idx["Nina"]][1][0], report[student_idx["Nina"]][1][1])
helen_wed = Or(report[student_idx["Helen"]][2][0], report[student_idx["Helen"]][2][1])
irving_wed = Or(report[student_idx["Irving"]][2][0], report[student_idx["Irving"]][2][1])
solver.add(Implies(nina_tue, And(helen_wed, irving_wed)))

# Kyle and Lenore do not give reports
for s in [student_idx["Kyle"], student_idx["Lenore"]]:
    for d in range(3):
        for slot in range(2):
            solver.add(Not(report[s][d][slot]))

# Each student can give at most one report
for s in range(8):
    solver.add(Sum([If(report[s][d][slot], 1, 0) 
                    for d in range(3) for slot in range(2)]) <= 1)

# Each slot per day can have at most one reporter
for d in range(3):
    for slot in range(2):
        for i in range(8):
            for j in range(i + 1, 8):
                solver.add(Or(Not(report[i][d][slot]), Not(report[j][d][slot])))

# Answer choices
answer_choices = [
    ("Helen", "George", "Nina"),   # choice 0
    ("Irving", "Robert", "Helen"), # choice 1
    ("Nina", "Helen", "Olivia"),   # choice 2
    ("Olivia", "Robert", "Irving"),# choice 3
    ("Robert", "George", "Helen")  # choice 4
]

answer_index_list = []
for idx, (mon_morn, tue_morn, wed_morn) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add morning report assignments
    s_chk.add(report[student_idx[mon_morn]][0][0])
    s_chk.add(report[student_idx[tue_morn]][1][0])
    s_chk.add(report[student_idx[wed_morn]][2][0])
    
    # Ensure no student is assigned to more than one slot (already handled by per-student constraint)
    # But also ensure the three students are distinct
    if len({mon_morn, tue_morn, wed_morn}) != 3:
        # Skip if same student appears multiple times (invalid)
        continue
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)