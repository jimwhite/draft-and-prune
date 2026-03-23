from z3 import *

# Student indices
(STUDENTS, idx_map) = (["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"], {})
for i, s in enumerate(STUDENTS):
    idx_map[s] = i

# Days: 0=Monday, 1=Tuesday, 2=Wednesday
# Slots: 0=morning, 1=afternoon

# report[s][d][t] = True if student s gives a report on day d at slot t
report = [[[Bool(f"report_{s}_{d}_{t}") for t in range(2)] for d in range(3)] for s in range(8)]

# Base solver
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

# At most one report per slot (one morning, one afternoon per day)
for d in range(3):
    for t in range(2):
        # Exactly one student per slot (since exactly two reports per day and each slot holds one report)
        solver.add(Sum([If(report[s][d][t], 1, 0) for s in range(8)]) == 1)

# George only on Tuesday (day=1)
for d in [0, 2]:
    for t in range(2):
        solver.add(Not(report[idx_map["George"]][d][t]))

# Olivia and Robert cannot give afternoon reports
for d in range(3):
    solver.add(Not(report[idx_map["Olivia"]][d][1]))
    solver.add(Not(report[idx_map["Robert"]][d][1]))

# Nina conditional constraint
# If Nina reports on Monday (day 0), then Helen and Irving must both report on Tuesday
nina_mon = Or(report[idx_map["Nina"]][0][0], report[idx_map["Nina"]][0][1])
helen_tue = Or(report[idx_map["Helen"]][1][0], report[idx_map["Helen"]][1][1])
irving_tue = Or(report[idx_map["Irving"]][1][0], report[idx_map["Irving"]][1][1])
solver.add(Implies(nina_mon, And(helen_tue, irving_tue)))

# If Nina reports on Tuesday (day 1), then Helen and Irving must both report on Wednesday
nina_tue = Or(report[idx_map["Nina"]][1][0], report[idx_map["Nina"]][1][1])
helen_wed = Or(report[idx_map["Helen"]][2][0], report[idx_map["Helen"]][2][1])
irving_wed = Or(report[idx_map["Irving"]][2][0], report[idx_map["Irving"]][2][1])
solver.add(Implies(nina_tue, And(helen_wed, irving_wed)))

# Answer choices
answer_choices = [
    # 0: 'Mon. morning: Helen; Mon. afternoon: Robert Tues. morning: Olivia; Tues. afternoon: Irving Wed. morning: Lenore; Wed. afternoon: Kyle'
    [("Helen", 0, 0), ("Robert", 0, 1), ("Olivia", 1, 0), ("Irving", 1, 1), ("Lenore", 2, 0), ("Kyle", 2, 1)],
    # 1: 'Mon. morning: Irving; Mon. afternoon: Olivia Tues. morning: Helen; Tues. afternoon: Kyle Wed. morning: Nina; Wed. afternoon: Lenore'
    [("Irving", 0, 0), ("Olivia", 0, 1), ("Helen", 1, 0), ("Kyle", 1, 1), ("Nina", 2, 0), ("Lenore", 2, 1)],
    # 2: 'Mon. morning: Lenore; Mon. afternoon: Helen Tues. morning: George; Tues. afternoon: Kyle Wed. morning: Robert; Wed. afternoon: Irving'
    [("Lenore", 0, 0), ("Helen", 0, 1), ("George", 1, 0), ("Kyle", 1, 1), ("Robert", 2, 0), ("Irving", 2, 1)],
    # 3: 'Mon. morning: Nina; Mon. afternoon: Helen Tues. morning: Robert; Tues. afternoon: Irving Wed. morning: Olivia; Wed. afternoon: Lenore'
    [("Nina", 0, 0), ("Helen", 0, 1), ("Robert", 1, 0), ("Irving", 1, 1), ("Olivia", 2, 0), ("Lenore", 2, 1)],
    # 4: 'Mon. morning: Olivia; Mon. afternoon: Nina Tues. morning: Irving; Tues. afternoon: Helen Wed. morning: Kyle; Wed. afternoon: George'
    [("Olivia", 0, 0), ("Nina", 0, 1), ("Irving", 1, 0), ("Helen", 1, 1), ("Kyle", 2, 0), ("George", 2, 1)]
]

# Check each answer choice
answer_index_list = []
for idx, schedule in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Set assignments for the schedule
    assigned_students = set()
    for (student, day, slot) in schedule:
        s_chk.add(report[idx_map[student]][day][slot])
        assigned_students.add(student)
    
    # Ensure exactly these 6 students are reporting (others must be false for all slots)
    for s in range(8):
        if STUDENTS[s] not in assigned_students:
            for d in range(3):
                for t in range(2):
                    s_chk.add(Not(report[s][d][t]))
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)