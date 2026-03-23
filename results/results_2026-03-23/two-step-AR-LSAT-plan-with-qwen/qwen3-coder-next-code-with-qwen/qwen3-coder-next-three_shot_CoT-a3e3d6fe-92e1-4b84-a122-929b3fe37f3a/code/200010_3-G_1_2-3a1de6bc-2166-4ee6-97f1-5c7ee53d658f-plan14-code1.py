from z3 import *

# Student indices: George, Helen, Irving, Kyle, Lenore, Nina, Olivia, Robert
(GEORGE, HELEN, IRVING, KYLE, LENORE, NINA, OLIVIA, ROBERT) = range(8)
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]

# Days: 0=Monday, 1=Tuesday, 2=Wednesday
DAYS = 3

# Boolean variables: given[i][d] means student i gives a report on day d
given = [[Bool(f"given_{students[i]}_{d}") for d in range(DAYS)] for i in range(8)]

# Boolean variables: morning[i][d] and afternoon[i][d]
morning = [[Bool(f"morning_{students[i]}_{d}") for d in range(DAYS)] for i in range(8)]
afternoon = [[Bool(f"afternoon_{students[i]}_{d}") for d in range(DAYS)] for i in range(8)]

# Base solver
solver = Solver()

# Each student gives exactly one report (if they are among the six reporters)
# But first, we'll add general constraints and then enforce Kyle and Lenore don't report

# Constraint: given[i][d] iff (morning[i][d] or afternoon[i][d])
for i in range(8):
    for d in range(DAYS):
        solver.add(given[i][d] == Or(morning[i][d], afternoon[i][d]))

# A student cannot give both morning and afternoon on the same day
for i in range(8):
    for d in range(DAYS):
        solver.add(Not(And(morning[i][d], afternoon[i][d])))

# Each reporter gives exactly one report (total across days)
for i in range(8):
    solver.add(Sum([If(given[i][d], 1, 0) for d in range(DAYS)]) <= 1)

# Exactly six students report (exactly six have given[i][*] = true)
solver.add(Sum([If(given[i][d], 1, 0) for i in range(8) for d in range(DAYS)]) == 6)

# Exactly two reports per day (one morning, one afternoon)
for d in range(DAYS):
    solver.add(Sum([If(morning[i][d], 1, 0) for i in range(8)]) == 1)
    solver.add(Sum([If(afternoon[i][d], 1, 0) for i in range(8)]) == 1)

# George can only report on Tuesday
solver.add(given[GEORGE][0] == False)  # Monday
solver.add(given[GEORGE][2] == False)  # Wednesday

# Olivia and Robert cannot give afternoon reports
for d in range(DAYS):
    solver.add(afternoon[OLIVIA][d] == False)
    solver.add(afternoon[ROBERT][d] == False)

# Conditional: If Nina reports on Monday or Tuesday, then Helen and Irving must report the next day
for d in range(2):  # Monday (0) and Tuesday (1)
    solver.add(Implies(given[NINA][d], And(
        Or(morning[HELEN][d+1], afternoon[HELEN][d+1]),
        Or(morning[IRVING][d+1], afternoon[IRVING][d+1])
    )))

# Premise: Kyle and Lenore do NOT give reports
for d in range(DAYS):
    solver.add(given[KYLE][d] == False)
    solver.add(given[LENORE][d] == False)

# Since Kyle and Lenore don't report, the six reporters must be:
# George, Helen, Irving, Nina, Olivia, Robert
# So each of these six must give exactly one report (given[i][*] = True for exactly one day)
reporters = [GEORGE, HELEN, IRVING, NINA, OLIVIA, ROBERT]
for i in reporters:
    solver.add(Sum([If(given[i][d], 1, 0) for d in range(DAYS)]) == 1)

# Answer choices: each is a list of [Monday_morning, Tuesday_morning, Wednesday_morning]
answer_choices = [
    ["Helen", "George", "Nina"],      # Option 0
    ["Irving", "Robert", "Helen"],   # Option 1
    ["Nina", "Helen", "Olivia"],     # Option 2
    ["Olivia", "Robert", "Irving"],  # Option 3
    ["Robert", "George", "Helen"]    # Option 4
]

# Map student names to indices
student_idx = {name: idx for idx, name in enumerate(students)}

# Check each answer choice
answer_index_list = []
for idx, option in enumerate(answer_choices):
    s_chk = Solver()
    # Add all base constraints
    for a in solver.assertions():
        s_chk.add(a)
    
    # Add morning assignments from the option
    days = [0, 1, 2]  # Monday, Tuesday, Wednesday
    for d, student_name in zip(days, option):
        i = student_idx[student_name]
        s_chk.add(morning[i][d] == True)
    
    # Since each reporter gives exactly one report, and they're assigned morning on day d,
    # they cannot give afternoon on that day (already enforced by earlier constraints)
    
    # Check feasibility
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)