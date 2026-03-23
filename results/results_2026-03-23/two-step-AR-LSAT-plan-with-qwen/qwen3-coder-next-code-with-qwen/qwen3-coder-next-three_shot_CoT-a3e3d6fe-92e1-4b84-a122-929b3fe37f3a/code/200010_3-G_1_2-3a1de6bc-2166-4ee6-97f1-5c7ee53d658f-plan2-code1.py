from z3 import *

# Student indices: George, Helen, Irving, Kyle, Lenore, Nina, Olivia, Robert
(GEORGE, HELEN, IRVING, KYLE, LENORE, NINA, OLIVIA, ROBERT) = range(8)
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]

# Days: 0=Monday, 1=Tuesday, 2=Wednesday
# Sessions: 0=morning, 1=afternoon
report = [[[Bool(f"report_{students[i]}_{d}_{s}") for s in range(2)] for d in range(3)] for i in range(8)]

solver = Solver()

# Exactly six reporters total
solver.add(Sum([If(report[i][d][s], 1, 0) for i in range(8) for d in range(3) for s in range(2)]) == 6)

# Exactly two reports per day
for d in range(3):
    solver.add(Sum([If(report[i][d][s], 1, 0) for i in range(8) for s in range(2)]) == 2)

# George can only report on Tuesday
for d in [0, 2]:  # Monday and Wednesday
    for s in range(2):
        solver.add(Not(report[GEORGE][d][s]))

# Olivia and Robert cannot give afternoon reports
for d in range(3):
    solver.add(Not(report[OLIVIA][d][1]))
    solver.add(Not(report[ROBERT][d][1]))

# Nina conditional constraint
# If Nina reports on Monday, then Helen and Irving must both report on Tuesday
nina_mon = Or(report[NINA][0][0], report[NINA][0][1])
helen_tue = Or(report[HELEN][1][0], report[HELEN][1][1])
irving_tue = Or(report[IRVING][1][0], report[IRVING][1][1])
solver.add(Implies(nina_mon, And(helen_tue, irving_tue)))

# If Nina reports on Tuesday, then Helen and Irving must both report on Wednesday
nina_tue = Or(report[NINA][1][0], report[NINA][1][1])
helen_wed = Or(report[HELEN][2][0], report[HELEN][2][1])
irving_wed = Or(report[IRVING][2][0], report[IRVING][2][1])
solver.add(Implies(nina_tue, And(helen_wed, irving_wed)))

# Kyle and Lenore do not give reports
for d in range(3):
    for s in range(2):
        solver.add(Not(report[KYLE][d][s]))
        solver.add(Not(report[LENORE][d][s]))

# Each reporter gives exactly one report (since six reporters and six reports)
for i in range(8):
    solver.add(Sum([If(report[i][d][s], 1, 0) for d in range(3) for s in range(2)]) <= 1)

# Answer choices: each is a triple [Mon_morning, Tue_morning, Wed_morning]
answer_choices = [
    ("Helen", "George", "Nina"),      # index 0
    ("Irving", "Robert", "Helen"),    # index 1
    ("Nina", "Helen", "Olivia"),      # index 2
    ("Olivia", "Robert", "Irving"),   # index 3
    ("Robert", "George", "Helen")     # index 4
]

# Map student names to indices
student_idx = {name: idx for idx, name in enumerate(students)}

# Check each answer choice
answer_index_list = []
for idx, (mon_mor, tue_mor, wed_mor) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraints for morning reports as specified
    mon_mor_idx = student_idx[mon_mor]
    tue_mor_idx = student_idx[tue_mor]
    wed_mor_idx = student_idx[wed_mor]
    
    s_chk.add(report[mon_mor_idx][0][0])
    s_chk.add(report[tue_mor_idx][1][0])
    s_chk.add(report[wed_mor_idx][2][0])
    
    # Check feasibility
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)