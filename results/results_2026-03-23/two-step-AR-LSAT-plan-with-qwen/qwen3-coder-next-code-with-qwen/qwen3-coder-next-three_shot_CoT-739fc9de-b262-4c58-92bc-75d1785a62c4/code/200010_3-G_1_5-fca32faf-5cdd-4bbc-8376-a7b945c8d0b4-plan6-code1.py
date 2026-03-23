from z3 import *

# Student indices
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
student_idx = {s: i for i, s in enumerate(students)}

# Days: 0=Monday, 1=Tuesday, 2=Wednesday
# Slots: 0=morning, 1=afternoon
report = [[[Bool(f"report_{s}_{d}_{t}") for t in range(2)] for d in range(3)] for s in range(8)]

# Base solver
solver = Solver()

# Exactly six reports total
solver.add(Sum([If(report[s][d][t], 1, 0) 
                for s in range(8) for d in range(3) for t in range(2)]) == 6)

# Two reports per day
for d in range(3):
    solver.add(Sum([If(report[s][d][t], 1, 0) 
                    for s in range(8) for t in range(2)]) == 2)

# Each student gives at most one report
for s in range(8):
    solver.add(Sum([If(report[s][d][t], 1, 0) 
                    for d in range(3) for t in range(2)]) <= 1)

# George only on Tuesday
for d in [0, 2]:  # Monday and Wednesday
    for t in range(2):
        solver.add(Not(report[student_idx["George"]][d][t]))

# Olivia and Robert cannot give afternoon reports
for s in [student_idx["Olivia"], student_idx["Robert"]]:
    for d in range(3):
        solver.add(Not(report[s][d][1]))

# Nina conditional constraint
# If Nina reports on Monday, then Helen and Irving must both report on Tuesday (both slots)
nina_mon = Or(report[student_idx["Nina"]][0][0], report[student_idx["Nina"]][0][1])
helen_tue_both = And(report[student_idx["Helen"]][1][0], report[student_idx["Helen"]][1][1])
irving_tue_both = And(report[student_idx["Irving"]][1][0], report[student_idx["Irving"]][1][1])
solver.add(Implies(nina_mon, And(helen_tue_both, irving_tue_both)))

# If Nina reports on Tuesday, then Helen and Irving must both report on Wednesday (both slots)
nina_tue = Or(report[student_idx["Nina"]][1][0], report[student_idx["Nina"]][1][1])
helen_wed_both = And(report[student_idx["Helen"]][2][0], report[student_idx["Helen"]][2][1])
irving_wed_both = And(report[student_idx["Irving"]][2][0], report[student_idx["Irving"]][2][1])
solver.add(Implies(nina_tue, And(helen_wed_both, irving_wed_both)))

# Fixed assignments from question
solver.add(report[student_idx["Kyle"]][1][1] == True)  # Kyle afternoon Tuesday
solver.add(report[student_idx["Helen"]][2][1] == True)  # Helen afternoon Wednesday

# Answer choices: (Monday morning, Tuesday morning, Wednesday morning)
answer_choices = [
    ("Irving", "Lenore", "Nina"),
    ("Lenore", "George", "Irving"),
    ("Nina", "Irving", "Lenore"),
    ("Robert", "George", "Irving"),
    ("Robert", "Irving", "Lenore")
]

# Check each answer choice
answer_index_list = []
for idx, (mon_mor, tue_mor, wed_mor) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assign morning slots
    s_chk.add(report[student_idx[mon_mor]][0][0] == True)
    s_chk.add(report[student_idx[tue_mor]][1][0] == True)
    s_chk.add(report[student_idx[wed_mor]][2][0] == True)
    
    # Ensure no student is assigned to multiple slots (already handled by per-student ≤1 constraint)
    # Check satisfiability
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)