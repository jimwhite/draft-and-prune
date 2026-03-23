from z3 import *

# Student indices: George=0, Helen=1, Irving=2, Kyle=3, Lenore=4, Nina=5, Olivia=6, Robert=7
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
student_idx = {s: i for i, s in enumerate(students)}

# Days: Monday=0, Tuesday=1, Wednesday=2
# Slots: morning=0, afternoon=1

# report[student][day][slot] = True if student gives report on day in slot
report = [[[Bool(f"r_{s}_{d}_{sl}") for sl in range(2)] for d in range(3)] for s in range(8)]

solver = Solver()

# Exactly six reports total
solver.add(Sum([If(report[s][d][sl], 1, 0) 
                for s in range(8) for d in range(3) for sl in range(2)]) == 6)

# Two reports per day (one morning, one afternoon)
for d in range(3):
    solver.add(Sum([report[s][d][sl] for s in range(8) for sl in range(2)]) == 2)

# One report per student per day (at most one slot per day)
for s in range(8):
    for d in range(3):
        solver.add(AtMost(report[s][d][0], report[s][d][1]))

# Tuesday is the only day George can give a report
for d in [0, 2]:  # Monday and Wednesday
    for sl in range(2):
        solver.add(Not(report[student_idx["George"]][d][sl]))

# Olivia and Robert cannot give afternoon reports
for student in [student_idx["Olivia"], student_idx["Robert"]]:
    for d in range(3):
        solver.add(Not(report[student][d][1]))

# Nina conditional constraint
# If Nina reports on Monday, then Helen and Irving must both report on Tuesday
nina_mon_any = Or(report[student_idx["Nina"]][0][0], report[student_idx["Nina"]][0][1])
nina_tue_any = Or(report[student_idx["Nina"]][1][0], report[student_idx["Nina"]][1][1])

# If Nina reports Monday, then Helen and Irving must both report Tuesday (any slot)
solver.add(Implies(nina_mon_any, 
                   And(
                       Or(report[student_idx["Helen"]][1][0], report[student_idx["Helen"]][1][1]),
                       Or(report[student_idx["Irving"]][1][0], report[student_idx["Irving"]][1][1])
                   )))

# If Nina reports Tuesday, then Helen and Irving must both report Wednesday (any slot)
solver.add(Implies(nina_tue_any,
                   And(
                       Or(report[student_idx["Helen"]][2][0], report[student_idx["Helen"]][2][1]),
                       Or(report[student_idx["Irving"]][2][0], report[student_idx["Irving"]][2][1])
                   )))

# Kyle and Lenore do not give reports
for d in range(3):
    for sl in range(2):
        solver.add(Not(report[student_idx["Kyle"]][d][sl]))
        solver.add(Not(report[student_idx["Lenore"]][d][sl]))

# With Kyle and Lenore excluded, exactly 6 students remain: George, Helen, Irving, Nina, Olivia, Robert
# Since total reports = 6 and each day has exactly 2 reports (3 days), all remaining 6 must report exactly once

# Answer choices: each is a list of [Monday_morning, Tuesday_morning, Wednesday_morning]
answer_choices = [
    ["Helen", "George", "Nina"],
    ["Irving", "Robert", "Helen"],
    ["Nina", "Helen", "Olivia"],
    ["Olivia", "Robert", "Irving"],
    ["Robert", "George", "Helen"]
]

answer_index_list = []

for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraints for the morning reports as specified
    days = [0, 1, 2]  # Monday, Tuesday, Wednesday
    
    for d_idx, day in enumerate(days):
        student_name = choice[d_idx]
        s_chk.add(report[student_idx[student_name]][day][0])
        
        # Ensure no other report for this student on the same day
        s_chk.add(Not(report[student_idx[student_name]][day][1]))
    
    # Check if this configuration is satisfiable
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)