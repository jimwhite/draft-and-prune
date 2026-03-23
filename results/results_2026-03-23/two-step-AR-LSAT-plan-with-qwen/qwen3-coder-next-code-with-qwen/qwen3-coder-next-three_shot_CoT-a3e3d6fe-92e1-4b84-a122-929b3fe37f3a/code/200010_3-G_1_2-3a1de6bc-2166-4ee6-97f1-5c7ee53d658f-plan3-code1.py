from z3 import *

# Student indices: George, Helen, Irving, Kyle, Lenore, Nina, Olivia, Robert
(GEORGE, HELEN, IRVING, KYLE, LENORE, NINA, OLIVIA, ROBERT) = range(8)
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]

# Days: Monday=0, Tuesday=1, Wednesday=2
# Periods: morning=0, afternoon=1

# Create assignment variables: assigned[s][d][p] = True if student s reports on day d, period p
assigned = [[[Bool(f"assigned_{s}_{d}_{p}") for p in range(2)] for d in range(3)] for s in range(8)]

solver = Solver()

# Constraint 4: Exactly six reports total
reports_count = Sum([If(assigned[s][d][p], 1, 0) 
                     for s in range(8) for d in range(3) for p in range(2)])
solver.add(reports_count == 6)

# Constraint 5: At most one report per slot
for d in range(3):
    for p in range(2):
        solver.add(Sum([If(assigned[s][d][p], 1, 0) for s in range(8)]) <= 1)

# Constraint 6: Exactly six students used (each report is by a different student)
student_used = [Or([assigned[s][d][p] for d in range(3) for p in range(2)]) for s in range(8)]
solver.add(Sum([If(student_used[s], 1, 0) for s in range(8)]) == 6)

# Constraint 7: Kyle and Lenore do not give reports
for d in range(3):
    for p in range(2):
        solver.add(Not(assigned[KYLE][d][p]))
        solver.add(Not(assigned[LENORE][d][p]))

# Constraint 8: Tuesday is the only day George can give a report
for d in range(3):
    if d != 1:  # Monday and Wednesday
        for p in range(2):
            solver.add(Not(assigned[GEORGE][d][p]))

# Constraint 9: Olivia and Robert cannot give afternoon reports
for d in range(3):
    solver.add(Not(assigned[OLIVIA][d][1]))
    solver.add(Not(assigned[ROBERT][d][1]))

# Constraint 10: Nina conditional constraint
nina_mon = Or(assigned[NINA][0][0], assigned[NINA][0][1])
nina_tue = Or(assigned[NINA][1][0], assigned[NINA][1][1])
nina_wed = Or(assigned[NINA][2][0], assigned[NINA][2][1])

helen_tue = Or(assigned[HELEN][1][0], assigned[HELEN][1][1])
irving_tue = Or(assigned[IRVING][1][0], assigned[IRVING][1][1])
helen_wed = Or(assigned[HELEN][2][0], assigned[HELEN][2][1])
irving_wed = Or(assigned[IRVING][2][0], assigned[IRVING][2][1])

# If Nina on Monday, then Helen and Irving on Tuesday
solver.add(Implies(nina_mon, And(helen_tue, irving_tue)))
# If Nina on Tuesday, then Helen and Irving on Wednesday
solver.add(Implies(nina_tue, And(helen_wed, irving_wed)))
# No constraint if Nina on Wednesday

# Answer choices: each is a list of [Monday_morning, Tuesday_morning, Wednesday_morning]
answer_choices = [
    ["Helen", "George", "Nina"],      # index 0
    ["Irving", "Robert", "Helen"],   # index 1
    ["Nina", "Helen", "Olivia"],     # index 2
    ["Olivia", "Robert", "Irving"],  # index 3
    ["Robert", "George", "Helen"]    # index 4
]

# Map student names to indices
student_idx = {
    "George": GEORGE, "Helen": HELEN, "Irving": IRVING,
    "Kyle": KYLE, "Lenore": LENORE, "Nina": NINA,
    "Olivia": OLIVIA, "Robert": ROBERT
}

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add fixed assignments for morning slots
    # Monday morning (day=0, period=0)
    s_chk.add(assigned[student_idx[choice[0]]][0][0])
    # Tuesday morning (day=1, period=0)
    s_chk.add(assigned[student_idx[choice[1]]][1][0])
    # Wednesday morning (day=2, period=0)
    s_chk.add(assigned[student_idx[choice[2]]][2][0])
    
    # Check feasibility
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)