from z3 import *

# Student indices
(STUDENTS, idx_map) = (["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"], {})
for i, s in enumerate(STUDENTS):
    idx_map[s] = i

# Days: 0-Monday, 1-Tuesday, 2-Wednesday
DAYS = 3
# Times: 0-morning, 1-afternoon
TIMES = 2

# slot[s][d][t] = True if student s gives report on day d at time t
slot = [[[Bool(f"slot_{s}_{d}_{t}") for t in range(TIMES)] for d in range(DAYS)] for s in range(len(STUDENTS))]

# Base solver
solver = Solver()

# Total reports constraint: exactly six students give reports (each gives exactly one report)
total_reports = []
for s in range(len(STUDENTS)):
    reports_for_s = Or([slot[s][d][t] for d in range(DAYS) for t in range(TIMES)])
    total_reports.append(reports_for_s)
solver.add(Sum([If(r, 1, 0) for r in total_reports]) == 6)

# Each slot can have at most one student
for d in range(DAYS):
    for t in range(TIMES):
        # Exactly one student per slot
        students_in_slot = []
        for s in range(len(STUDENTS)):
            students_in_slot.append(slot[s][d][t])
        # At least one student per slot (since exactly 2 reports per day, and 3 days => 6 slots filled)
        solver.add(Or(*students_in_slot))
        # At most one student per slot
        for i in range(len(STUDENTS)):
            for j in range(i + 1, len(STUDENTS)):
                solver.add(Not(And(students_in_slot[i], students_in_slot[j])))

# George only on Tuesday
for t in range(TIMES):
    solver.add(Not(slot[idx_map["George"]][0][t]))  # Monday
    solver.add(Not(slot[idx_map["George"]][2][t]))  # Wednesday

# Olivia and Robert cannot give afternoon reports
for d in range(DAYS):
    solver.add(Not(slot[idx_map["Olivia"]][d][1]))
    solver.add(Not(slot[idx_map["Robert"]][d][1]))

# Nina conditional constraint
# If Nina reports on Monday, then Helen and Irving must report on Tuesday
nina_monday = Or(slot[idx_map["Nina"]][0][0], slot[idx_map["Nina"]][0][1])
helen_tue = Or(slot[idx_map["Helen"]][1][0], slot[idx_map["Helen"]][1][1])
irving_tue = Or(slot[idx_map["Irving"]][1][0], slot[idx_map["Irving"]][1][1])
solver.add(Implies(nina_monday, And(helen_tue, irving_tue)))

# If Nina reports on Tuesday, then Helen and Irving must report on Wednesday
nina_tue = Or(slot[idx_map["Nina"]][1][0], slot[idx_map["Nina"]][1][1])
helen_wed = Or(slot[idx_map["Helen"]][2][0], slot[idx_map["Helen"]][2][1])
irving_wed = Or(slot[idx_map["Irving"]][2][0], slot[idx_map["Irving"]][2][1])
solver.add(Implies(nina_tue, And(helen_wed, irving_wed)))

# Given scenario constraints
# Kyle gives afternoon report on Tuesday
solver.add(slot[idx_map["Kyle"]][1][1] == True)
# Helen gives afternoon report on Wednesday
solver.add(slot[idx_map["Helen"]][2][1] == True)

# Answer choices: each is a list of [Monday_morning, Tuesday_morning, Wednesday_morning]
answer_choices = [
    ["Irving", "Lenore", "Nina"],
    ["Lenore", "George", "Irving"],
    ["Nina", "Irving", "Lenore"],
    ["Robert", "George", "Irving"],
    ["Robert", "Irving", "Lenore"]
]

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add fixed morning reports
    # Monday morning: choice[0]
    s_chk.add(slot[idx_map[choice[0]]][0][0] == True)
    # Tuesday morning: choice[1]
    s_chk.add(slot[idx_map[choice[1]]][1][0] == True)
    # Wednesday morning: choice[2]
    s_chk.add(slot[idx_map[choice[2]]][2][0] == True)
    
    # Ensure no student is assigned to both morning and afternoon on same day
    for s in range(len(STUDENTS)):
        for d in range(DAYS):
            s_chk.add(Not(And(slot[s][d][0], slot[s][d][1])))
    
    # Ensure Kyle is only assigned to Tuesday afternoon (not morning) and Helen only Wednesday afternoon
    s_chk.add(Not(slot[idx_map["Kyle"]][1][0]))  # Kyle not Tuesday morning
    s_chk.add(Not(slot[idx_map["Helen"]][2][0]))  # Helen not Wednesday morning
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)