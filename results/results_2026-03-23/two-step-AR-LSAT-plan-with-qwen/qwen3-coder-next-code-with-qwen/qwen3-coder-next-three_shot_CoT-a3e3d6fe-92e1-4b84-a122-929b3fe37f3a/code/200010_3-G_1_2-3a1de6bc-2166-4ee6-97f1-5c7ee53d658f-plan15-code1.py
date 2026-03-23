from z3 import *

# Student indices: George, Helen, Irving, Kyle, Lenore, Nina, Olivia, Robert
(GEORGE, HELEN, IRVING, KYLE, LENORE, NINA, OLIVIA, ROBERT) = range(8)
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]

# Days: 0=Monday, 1=Tuesday, 2=Wednesday
# Slots: 0=morning, 1=afternoon

# Create assignment variables: assigned[s][d][slot] = True if student s reports on day d, slot
assigned = [[[Bool(f"assigned_{students[s]}_d{d}_slot{slot}") for slot in range(2)] for d in range(3)] for s in range(8)]

solver = Solver()

# Exactly six reporters (exactly 6 students give exactly one report each)
reporter_count = [Or(*[assigned[s][d][slot] for d in range(3) for slot in range(2)]) for s in range(8)]
solver.add(Sum([If(r, 1, 0) for r in reporter_count]) == 6)

# Exactly two reports per day
for d in range(3):
    solver.add(Sum([If(assigned[s][d][slot], 1, 0) for s in range(8) for slot in range(2)]) == 2)

# Each student gives at most one report
for s in range(8):
    solver.add(Sum([If(assigned[s][d][slot], 1, 0) for d in range(3) for slot in range(2)]) <= 1)

# George only on Tuesday
for d in [0, 2]:  # Monday and Wednesday
    for slot in range(2):
        solver.add(Not(assigned[GEORGE][d][slot]))

# Olivia and Robert cannot give afternoon reports
for d in range(3):
    solver.add(Not(assigned[OLIVIA][d][1]))
    solver.add(Not(assigned[ROBERT][d][1]))

# Nina constraint: If Nina reports on day d, then:
#   if d=0 (Mon): Helen and Irving must both report on Tuesday
#   if d=1 (Tue): Helen and Irving must both report on Wednesday
#   if d=2 (Wed): no requirement

# Create helper variables for Nina's day
nina_mon = Or(assigned[NINA][0][0], assigned[NINA][0][1])
nina_tue = Or(assigned[NINA][1][0], assigned[NINA][1][1])
nina_wed = Or(assigned[NINA][2][0], assigned[NINA][2][1])

# Nina on Monday implies Helen and Irving both report on Tuesday
solver.add(Implies(nina_mon, 
    And(
        Or(assigned[HELEN][1][0], assigned[HELEN][1][1]),
        Or(assigned[IRVING][1][0], assigned[IRVING][1][1])
    )))

# Nina on Tuesday implies Helen and Irving both report on Wednesday
solver.add(Implies(nina_tue,
    And(
        Or(assigned[HELEN][2][0], assigned[HELEN][2][1]),
        Or(assigned[IRVING][2][0], assigned[IRVING][2][1])
    )))

# Premise: Kyle and Lenore do not give reports
for s in [KYLE, LENORE]:
    for d in range(3):
        for slot in range(2):
            solver.add(Not(assigned[s][d][slot]))

# Answer choices: morning reports (slot=0) for Mon, Tue, Wed respectively
answer_choices = [
    ("Helen", "George", "Nina"),      # 0
    ("Irving", "Robert", "Helen"),    # 1
    ("Nina", "Helen", "Olivia"),      # 2
    ("Olivia", "Robert", "Irving"),   # 3
    ("Robert", "George", "Helen")     # 4
]

# Map student names to indices
student_name_to_idx = {
    "George": GEORGE, "Helen": HELEN, "Irving": IRVING,
    "Kyle": KYLE, "Lenore": LENORE, "Nina": NINA,
    "Olivia": OLIVIA, "Robert": ROBERT
}

answer_index_list = []
for idx, (mon_morning, tue_morning, wed_morning) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Enforce morning slots for the specified students
    mon_student = student_name_to_idx[mon_morning]
    tue_student = student_name_to_idx[tue_morning]
    wed_student = student_name_to_idx[wed_morning]
    
    # Monday morning must be mon_student
    s_chk.add(assigned[mon_student][0][0])
    # No other student on Monday morning
    for s in range(8):
        if s != mon_student:
            s_chk.add(Not(assigned[s][0][0]))
    
    # Tuesday morning must be tue_student
    s_chk.add(assigned[tue_student][1][0])
    # No other student on Tuesday morning
    for s in range(8):
        if s != tue_student:
            s_chk.add(Not(assigned[s][1][0]))
    
    # Wednesday morning must be wed_student
    s_chk.add(assigned[wed_student][2][0])
    # No other student on Wednesday morning
    for s in range(8):
        if s != wed_student:
            s_chk.add(Not(assigned[s][2][0]))
    
    # Check if this configuration is possible
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)