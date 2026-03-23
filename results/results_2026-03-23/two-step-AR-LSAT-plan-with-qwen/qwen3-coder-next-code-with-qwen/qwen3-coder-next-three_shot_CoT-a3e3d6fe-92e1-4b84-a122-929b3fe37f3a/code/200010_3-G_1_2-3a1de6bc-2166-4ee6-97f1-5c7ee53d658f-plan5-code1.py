from z3 import *

# Student indices: George, Helen, Irving, Kyle, Lenore, Nina, Olivia, Robert
(GEORGE, HELEN, IRVING, KYLE, LENORE, NINA, OLIVIA, ROBERT) = range(8)

# Days: Monday=0, Tuesday=1, Wednesday=2
# Times: morning=0, afternoon=1

# report[s][d][t] = True if student s gives a report on day d at time t
report = [[[Bool(f"report_{s}_{d}_{t}") for t in range(2)] for d in range(3)] for s in range(8)]

solver = Solver()

# Exactly six reports total
solver.add(Sum([If(report[s][d][t], 1, 0) 
                for s in range(8) 
                for d in range(3) 
                for t in range(2)]) == 6)

# Exactly two reports per day
for d in range(3):
    solver.add(Sum([If(report[s][d][t], 1, 0) 
                    for s in range(8) 
                    for t in range(2)]) == 2)

# George only on Tuesday
for d in [0, 2]:  # Monday and Wednesday
    for t in range(2):
        solver.add(Not(report[GEORGE][d][t]))

# Olivia and Robert cannot give afternoon reports
for s in [OLIVIA, ROBERT]:
    solver.add(Not(report[s][0][1]))
    solver.add(Not(report[s][1][1]))
    solver.add(Not(report[s][2][1]))

# Nina conditional constraint:
# If Nina gives a report on day d (d=0 or 1), then next day both Helen and Irving must give morning reports
for d in range(2):  # Monday (0) and Tuesday (1)
    for t in range(2):
        solver.add(
            Implies(report[NINA][d][t],
                    And(report[HELEN][d+1][0], report[IRVING][d+1][0]))
        )

# Kyle and Lenore do not give reports
for s in [KYLE, LENORE]:
    for d in range(3):
        for t in range(2):
            solver.add(Not(report[s][d][t]))

# Answer choices: list of (mon_morning, tue_morning, wed_morning)
answer_choices = [
    (HELEN, GEORGE, NINA),      # Choice 0
    (IRVING, ROBERT, HELEN),    # Choice 1
    (NINA, HELEN, OLIVIA),      # Choice 2
    (OLIVIA, ROBERT, IRVING),   # Choice 3
    (ROBERT, GEORGE, HELEN)     # Choice 4
]

# Check each answer choice
answer_index_list = []
for idx, (mon_morn, tue_morn, wed_morn) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assign the specified students to morning slots
    s_chk.add(report[mon_morn][0][0])
    s_chk.add(report[tue_morn][1][0])
    s_chk.add(report[wed_morn][2][0])
    
    # Ensure no other student is assigned to the same morning slot
    for s in range(8):
        if s != mon_morn:
            s_chk.add(Not(report[s][0][0]))
        if s != tue_morn:
            s_chk.add(Not(report[s][1][0]))
        if s != wed_morn:
            s_chk.add(Not(report[s][2][0]))
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)