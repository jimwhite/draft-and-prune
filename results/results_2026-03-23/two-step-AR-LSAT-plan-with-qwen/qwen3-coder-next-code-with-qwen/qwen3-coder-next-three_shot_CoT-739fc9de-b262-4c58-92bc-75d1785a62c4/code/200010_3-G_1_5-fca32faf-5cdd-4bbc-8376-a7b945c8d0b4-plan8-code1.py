from z3 import *

# Student indices
(G, H, I, K, L, N, O, R) = range(8)
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]

# Days: 0-Monday, 1-Tuesday, 2-Wednesday
days = ["Monday", "Tuesday", "Wednesday"]
# Times: 0-morning, 1-afternoon
times = ["morning", "afternoon"]

# slot[student][day][time] = True if student gives report on that day and time
slot = [[[Bool(f"slot_{s}_{d}_{t}") for t in range(2)] for d in range(3)] for s in range(8)]

# Base solver
solver = Solver()

# Exactly six reports total
solver.add(Sum([If(slot[s][d][t], 1, 0) 
                for s in range(8) for d in range(3) for t in range(2)]) == 6)

# Two reports per day (one morning, one afternoon)
for d in range(3):
    # Exactly one morning reporter
    solver.add(Sum([If(slot[s][d][0], 1, 0) for s in range(8)]) == 1)
    # Exactly one afternoon reporter
    solver.add(Sum([If(slot[s][d][1], 1, 0) for s in range(8)]) == 1)

# Mutual exclusivity: each student gives at most one report
for s in range(8):
    # Sum of all slots for this student <= 1
    solver.add(Sum([If(slot[s][d][t], 1, 0) 
                    for d in range(3) for t in range(2)]) <= 1)

# George can only give report on Tuesday
for d in [0, 2]:  # Monday and Wednesday
    for t in range(2):
        solver.add(Not(slot[G][d][t]))

# Olivia and Robert cannot give afternoon reports
for s in [O, R]:
    for d in range(3):
        solver.add(Not(slot[s][d][1]))

# Conditional constraint for Nina
# If Nina gives a report on Monday, then Helen and Irving must give reports on Tuesday
solver.add(Implies(
    Or(slot[N][0][0], slot[N][0][1]),
    And(Or(slot[H][1][0], slot[H][1][1]), Or(slot[I][1][0], slot[I][1][1]))
))

# If Nina gives a report on Tuesday, then Helen and Irving must give reports on Wednesday
solver.add(Implies(
    Or(slot[N][1][0], slot[N][1][1]),
    And(Or(slot[H][2][0], slot[H][2][1]), Or(slot[I][2][0], slot[I][2][1]))
))

# Given conditions:
# Kyle gives afternoon report on Tuesday
solver.add(slot[K][1][1] == True)

# Helen gives afternoon report on Wednesday
solver.add(slot[H][2][1] == True)

# Answer choices: list of (morning_Monday, morning_Tuesday, morning_Wednesday)
answer_choices = [
    ("Irving", "Lenore", "Nina"),   # 0
    ("Lenore", "George", "Irving"), # 1
    ("Nina", "Irving", "Lenore"),   # 2
    ("Robert", "George", "Irving"), # 3
    ("Robert", "Irving", "Lenore")  # 4
]

# Map student names to indices
student_idx = {name: i for i, name in enumerate(students)}

# Check each answer choice
answer_index_list = []
for idx, (mon_morn, tue_morn, wed_morn) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraints for morning reporters
    mon_morn_idx = student_idx[mon_morn]
    tue_morn_idx = student_idx[tue_morn]
    wed_morn_idx = student_idx[wed_morn]
    
    # Set morning reporters
    s_chk.add(slot[mon_morn_idx][0][0] == True)
    s_chk.add(slot[tue_morn_idx][1][0] == True)
    s_chk.add(slot[wed_morn_idx][2][0] == True)
    
    # Ensure consistency: morning reporters must not conflict with afternoon reports already set
    # Kyle is afternoon on Tuesday, Helen is afternoon on Wednesday
    # So if tue_morn is Kyle or wed_morn is Helen, it would conflict (but Kyle and Helen are different people)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)