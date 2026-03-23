from z3 import *

# Student indices: George, Helen, Irving, Kyle, Lenore, Nina, Olivia, Robert
(GEORGE, HELEN, IRVING, KYLE, LENORE, NINA, OLIVIA, ROBERT) = range(8)
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]

# Days: 0-Monday, 1-Tuesday, 2-Wednesday
# Slots: 0-morning, 1-afternoon
assigned = [[[Bool(f"assigned_{students[s]}_{['Mon','Tue','Wed'][d]}_{['morning','afternoon'][t]}") 
              for t in range(2)] for d in range(3)] for s in range(8)]

solver = Solver()

# Exactly six reporters
reporter_count = Sum([If(Or(assigned[s][0][0], assigned[s][0][1], 
                            assigned[s][1][0], assigned[s][1][1],
                            assigned[s][2][0], assigned[s][2][1]), 1, 0) 
                      for s in range(8)])
solver.add(reporter_count == 6)

# Two reports per day
for d in range(3):
    # Exactly one morning and one afternoon reporter each day
    morning_students = [assigned[s][d][0] for s in range(8)]
    afternoon_students = [assigned[s][d][1] for s in range(8)]
    
    # Exactly one morning reporter
    solver.add(Sum([If(m, 1, 0) for m in morning_students]) == 1)
    # Exactly one afternoon reporter
    solver.add(Sum([If(a, 1, 0) for a in afternoon_students]) == 1)
    
    # No student can give both morning and afternoon on same day
    for s in range(8):
        solver.add(Not(And(assigned[s][d][0], assigned[s][d][1])))

# George only on Tuesday
for d in [0, 2]:  # Monday and Wednesday
    for t in range(2):
        solver.add(Not(assigned[GEORGE][d][t]))

# Olivia and Robert cannot give afternoon reports
for d in range(3):
    solver.add(Not(assigned[OLIVIA][d][1]))
    solver.add(Not(assigned[ROBERT][d][1]))

# Nina constraint: if Nina gives report, then next day Helen and Irving must both give reports
# Nina cannot be on Wednesday (no following day)
solver.add(Not(Or([assigned[NINA][2][t] for t in range(2)])))

# If Nina on Monday, then Helen and Irving must both be assigned on Tuesday
nina_mon = Or(assigned[NINA][0][0], assigned[NINA][0][1])
helen_tue = Or(assigned[HELEN][1][0], assigned[HELEN][1][1])
irving_tue = Or(assigned[IRVING][1][0], assigned[IRVING][1][1])
solver.add(Implies(nina_mon, And(helen_tue, irving_tue)))

# If Nina on Tuesday, then Helen and Irving must both be assigned on Wednesday
nina_tue = Or(assigned[NINA][1][0], assigned[NINA][1][1])
helen_wed = Or(assigned[HELEN][2][0], assigned[HELEN][2][1])
irving_wed = Or(assigned[IRVING][2][0], assigned[IRVING][2][1])
solver.add(Implies(nina_tue, And(helen_wed, irving_wed)))

# Given assignments: Kyle gives afternoon report on Tuesday, Helen gives afternoon report on Wednesday
solver.add(assigned[KYLE][1][1])
solver.add(assigned[HELEN][2][1])

# Answer choices: list of (mon_morning, tue_morning, wed_morning)
answer_choices = [
    ("Irving", "Lenore", "Nina"),
    ("Lenore", "George", "Irving"),
    ("Nina", "Irving", "Lenore"),
    ("Robert", "George", "Irving"),
    ("Robert", "Irving", "Lenore")
]

# Map student names to indices
student_idx = {name: idx for idx, name in enumerate(students)}

# Check each answer choice
answer_index_list = []
for idx, (mon_mor, tue_mor, wed_mor) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraints for the morning reports
    mon_mor_idx = student_idx[mon_mor]
    tue_mor_idx = student_idx[tue_mor]
    wed_mor_idx = student_idx[wed_mor]
    
    # Ensure these students are assigned to the specified morning slots
    s_chk.add(assigned[mon_mor_idx][0][0])
    s_chk.add(assigned[tue_mor_idx][1][0])
    s_chk.add(assigned[wed_mor_idx][2][0])
    
    # Ensure no other student is assigned to these morning slots
    for s in range(8):
        if s != mon_mor_idx:
            s_chk.add(Not(assigned[s][0][0]))
        if s != tue_mor_idx:
            s_chk.add(Not(assigned[s][1][0]))
        if s != wed_mor_idx:
            s_chk.add(Not(assigned[s][2][0]))
    
    # Ensure Kyle and Helen are only in their specified slots
    s_chk.add(Not(assigned[KYLE][0][0]), Not(assigned[KYLE][0][1]))
    s_chk.add(Not(assigned[KYLE][2][0]), Not(assigned[KYLE][2][1]))
    s_chk.add(Not(assigned[HELEN][0][0]), Not(assigned[HELEN][0][1]))
    s_chk.add(Not(assigned[HELEN][1][0]), Not(assigned[HELEN][1][1]))
    
    # Ensure the three morning-report students are distinct
    s_chk.add(mon_mor_idx != tue_mor_idx)
    s_chk.add(tue_mor_idx != wed_mor_idx)
    s_chk.add(mon_mor_idx != wed_mor_idx)
    
    # Check if this configuration is possible
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)