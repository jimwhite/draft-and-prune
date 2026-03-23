from z3 import *

# Student indices: George, Helen, Irving, Kyle, Lenore, Nina, Olivia, Robert
(GEORGE, HELEN, IRVING, KYLE, LENORE, NINA, OLIVIA, ROBERT) = range(8)

# Days: Monday=0, Tuesday=1, Wednesday=2
# Slots: morning=0, afternoon=1

# assigned[s][d][slot] = True if student s gives report on day d in slot
assigned = [[[Bool(f"assigned_{s}_{d}_{slot}") for slot in range(2)] for d in range(3)] for s in range(8)]

solver = Solver()

# Exactly six reporters (Kyle and Lenore are excluded, so only 6 possible: George, Helen, Irving, Nina, Olivia, Robert)
# Constraint: each of the 6 active students can be assigned at most once
active_students = [GEORGE, HELEN, IRVING, NINA, OLIVIA, ROBERT]
for s in active_students:
    solver.add(Sum([If(assigned[s][d][slot], 1, 0) for d in range(3) for slot in range(2)]) <= 1)

# Exactly six total reports (i.e., exactly 6 students assigned, each once)
solver.add(Sum([If(
    Or(assigned[s][d][slot] for d in range(3) for slot in range(2)),
    1, 0
) for s in active_students]) == 6)

# Kyle and Lenore do not give reports
for d in range(3):
    for slot in range(2):
        solver.add(Not(assigned[KYLE][d][slot]))
        solver.add(Not(assigned[LENORE][d][slot]))

# Tuesday is the only day George can give a report
for d in [0, 2]:  # Monday and Wednesday
    for slot in range(2):
        solver.add(Not(assigned[GEORGE][d][slot]))

# Olivia and Robert cannot give afternoon reports
for d in range(3):
    solver.add(Not(assigned[OLIVIA][d][1]))
    solver.add(Not(assigned[ROBERT][d][1]))

# Nina conditional constraint:
# If Nina gives a report on Monday (d=0) or Tuesday (d=1), then Helen and Irving must both give reports on the next day
# If Nina gives a report on Wednesday (d=2), no constraint

# For Monday: if Nina reports Monday, then Helen and Irving must both report Tuesday (both slots)
for slot in range(2):
    solver.add(Implies(assigned[NINA][0][slot],
                       And(Or(assigned[HELEN][1][0], assigned[HELEN][1][1]),
                           Or(assigned[IRVING][1][0], assigned[IRVING][1][1]))))

# For Tuesday: if Nina reports Tuesday, then Helen and Irving must both report Wednesday
for slot in range(2):
    solver.add(Implies(assigned[NINA][1][slot],
                       And(Or(assigned[HELEN][2][0], assigned[HELEN][2][1]),
                           Or(assigned[IRVING][2][0], assigned[IRVING][2][1]))))

# Each day has exactly two reports (one morning, one afternoon)
for d in range(3):
    solver.add(Sum([If(assigned[s][d][slot], 1, 0) for s in active_students for slot in range(2)]) == 2)

# Answer choices: list of (mon_morning, tue_morning, wed_morning)
answer_choices = [
    (HELEN, GEORGE, NINA),      # 0
    (IRVING, ROBERT, HELEN),    # 1
    (NINA, HELEN, OLIVIA),      # 2
    (OLIVIA, ROBERT, IRVING),   # 3
    (ROBERT, GEORGE, HELEN)     # 4
]

answer_index_list = []

for idx, (mon_morn, tue_morn, wed_morn) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add fixed morning assignments
    # Monday morning: mon_morn
    s_chk.add(assigned[mon_morn][0][0])
    # Tuesday morning: tue_morn
    s_chk.add(assigned[tue_morn][1][0])
    # Wednesday morning: wed_morn
    s_chk.add(assigned[wed_morn][2][0])
    
    # Ensure no student appears twice in morning slots (already enforced by uniqueness constraint above)
    # But add explicit distinctness for safety
    s_chk.add(mon_morn != tue_morn, mon_morn != wed_morn, tue_morn != wed_morn)
    
    # Ensure each assigned student is among active students
    for s in [mon_morn, tue_morn, wed_morn]:
        if s not in active_students:
            s_chk.add(False)  # impossible
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)