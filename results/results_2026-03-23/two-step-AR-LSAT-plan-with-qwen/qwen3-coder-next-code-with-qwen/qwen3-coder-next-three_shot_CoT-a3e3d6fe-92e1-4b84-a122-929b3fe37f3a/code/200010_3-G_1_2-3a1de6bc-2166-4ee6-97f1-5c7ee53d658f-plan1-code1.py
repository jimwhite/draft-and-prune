from z3 import *

# Student indices: George=0, Helen=1, Irving=2, Kyle=3, Lenore=4, Nina=5, Olivia=6, Robert=7
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
student_idx = {name: i for i, name in enumerate(students)}

# report[s][d][t]: student s gives a report on day d (0=Mon, 1=Tue, 2=Wed) at time t (0=morning, 1=afternoon)
report = [[[Bool(f"report_{s}_{d}_{t}") for t in range(2)] for d in range(3)] for s in range(8)]

solver = Solver()

# Exactly 6 reports total
solver.add(Sum([If(report[s][d][t], 1, 0) for s in range(8) for d in range(3) for t in range(2)]) == 6)

# Exactly 2 reports per day
for d in range(3):
    solver.add(Sum([If(report[s][d][t], 1, 0) for s in range(8) for t in range(2)]) == 2)

# At most one report per time slot (morning and afternoon each day)
for d in range(3):
    for t in range(2):
        # Enforce exactly one reporter per slot (since each day has exactly 2 reports)
        solver.add(Sum([If(report[s][d][t], 1, 0) for s in range(8)]) == 1)

# Kyle and Lenore do not give reports
for s in [3, 4]:  # Kyle=3, Lenore=4
    for d in range(3):
        for t in range(2):
            solver.add(Not(report[s][d][t]))

# George can only report on Tuesday (day 1)
for d in [0, 2]:  # Monday and Wednesday
    for t in range(2):
        solver.add(Not(report[0][d][t]))  # George=0

# Olivia and Robert cannot give afternoon reports
for s in [6, 7]:  # Olivia=6, Robert=7
    for d in range(3):
        solver.add(Not(report[s][d][1]))

# Nina conditional constraint
# If Nina reports on Monday (d=0) or Tuesday (d=1), then Helen and Irving must both report the next day
for d in [0, 1]:
    for t in range(2):
        # If Nina reports on day d at time t, then Helen and Irving must both report on day d+1
        # Since exactly 2 reports per day, this means Helen and Irving are the only ones reporting on d+1
        nina_report = report[5][d][t]  # Nina=5
        
        # Helen must report on day d+1 (either morning or afternoon)
        helen_report = Or(report[1][d+1][0], report[1][d+1][1])
        # Irving must report on day d+1 (either morning or afternoon)
        irving_report = Or(report[2][d+1][0], report[2][d+1][1])
        
        # Implication: if Nina reports on day d, then Helen and Irving both report on day d+1
        solver.add(Implies(nina_report, And(helen_report, irving_report)))

# Answer choices: each is a triple (morning_Mon, morning_Tue, morning_Wed)
answer_choices = [
    ("Helen", "George", "Nina"),      # 0
    ("Irving", "Robert", "Helen"),   # 1
    ("Nina", "Helen", "Olivia"),     # 2
    ("Olivia", "Robert", "Irving"),  # 3
    ("Robert", "George", "Helen")    # 4
]

answer_index_list = []

for idx, (mon_morning, tue_morning, wed_morning) in enumerate(answer_choices):
    s_chk = Solver()
    # Add all base constraints
    for a in solver.assertions():
        s_chk.add(a)
    
    # Add fixed morning slot constraints
    # Monday morning: mon_morning
    mon_student = student_idx[mon_morning]
    s_chk.add(report[mon_student][0][0])
    # Ensure no other student reports Monday morning
    for s in range(8):
        if s != mon_student:
            s_chk.add(Not(report[s][0][0]))
    
    # Tuesday morning: tue_morning
    tue_student = student_idx[tue_morning]
    s_chk.add(report[tue_student][1][0])
    # Ensure no other student reports Tuesday morning
    for s in range(8):
        if s != tue_student:
            s_chk.add(Not(report[s][1][0]))
    
    # Wednesday morning: wed_morning
    wed_student = student_idx[wed_morning]
    s_chk.add(report[wed_student][2][0])
    # Ensure no other student reports Wednesday morning
    for s in range(8):
        if s != wed_student:
            s_chk.add(Not(report[s][2][0]))
    
    # Check if this configuration is possible
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)