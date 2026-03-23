from z3 import *

# Student indices
(STUDENTS, idx_map) = (["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"], {})
for i, s in enumerate(STUDENTS):
    idx_map[s] = i

# Slot indices: 0=Mon morning, 1=Mon afternoon, 2=Tue morning, 3=Tue afternoon, 4=Wed morning, 5=Wed afternoon
SLOTS = range(6)

# Assignment variables: assign[student_index][slot] = True if student is assigned to slot
assign = [[Bool(f"assign_{s}_{slot}") for slot in SLOTS] for s in STUDENTS]

# Base solver
solver = Solver()

# Exactly six reports: each slot has exactly one student, and each student is assigned at most once
# One student per slot
for slot in SLOTS:
    solver.add(Sum([If(assign[i][slot], 1, 0) for i in range(len(STUDENTS))]) == 1)

# Each student assigned at most once
for i in range(len(STUDENTS)):
    solver.add(Sum([If(assign[i][slot], 1, 0) for slot in SLOTS]) <= 1)

# George only on Tuesday (slots 2 and 3)
george_idx = idx_map["George"]
for slot in SLOTS:
    if slot not in [2, 3]:
        solver.add(Not(assign[george_idx][slot]))

# Olivia and Robert cannot give afternoon reports (slots 1, 3, 5)
olivia_idx = idx_map["Olivia"]
robert_idx = idx_map["Robert"]
for slot in [1, 3, 5]:
    solver.add(Not(assign[olivia_idx][slot]))
    solver.add(Not(assign[robert_idx][slot]))

# Nina conditional constraint:
# If Nina is on Monday (0) or Tuesday (2), then Helen and Irving must both be assigned to some slot on the next day
# If Nina is on Wednesday (4 or 5), no constraint

nina_idx = idx_map["Nina"]
helen_idx = idx_map["Helen"]
irving_idx = idx_map["Irving"]

nina_mon = assign[nina_idx][0]
nina_tue_morn = assign[nina_idx][2]

# Monday Nina → Helen and Irving on Tuesday
solver.add(Implies(nina_mon, 
    And(
        Or(assign[helen_idx][2], assign[helen_idx][3]),
        Or(assign[irving_idx][2], assign[irving_idx][3])
    )
))

# Tuesday Nina → Helen and Irving on Wednesday
solver.add(Implies(nina_tue_morn, 
    And(
        Or(assign[helen_idx][4], assign[helen_idx][5]),
        Or(assign[irving_idx][4], assign[irving_idx][5])
    )
))

# Note: Nina could also be on Tue afternoon (slot 3), but that's covered by the same logic
# Let's add explicit constraint for Tue afternoon Nina as well
nina_tue_aft = assign[nina_idx][3]
solver.add(Implies(nina_tue_aft, 
    And(
        Or(assign[helen_idx][4], assign[helen_idx][5]),
        Or(assign[irving_idx][4], assign[irving_idx][5])
    )
))

# Answer choices
choices = [
    # 0
    {
        0: "Helen", 1: "Robert",
        2: "Olivia", 3: "Irving",
        4: "Lenore", 5: "Kyle"
    },
    # 1
    {
        0: "Irving", 1: "Olivia",
        2: "Helen", 3: "Kyle",
        4: "Nina", 5: "Lenore"
    },
    # 2
    {
        0: "Lenore", 1: "Helen",
        2: "George", 3: "Kyle",
        4: "Robert", 5: "Irving"
    },
    # 3
    {
        0: "Nina", 1: "Helen",
        2: "Robert", 3: "Irving",
        4: "Olivia", 5: "Lenore"
    },
    # 4
    {
        0: "Olivia", 1: "Nina",
        2: "Irving", 3: "Helen",
        4: "Kyle", 5: "George"
    }
]

# Check each choice
answer_index_list = []
for idx, assignment in enumerate(choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add concrete assignment for this choice
    for slot, student in assignment.items():
        s_chk.add(assign[idx_map[student]][slot])
    
    # Ensure all other students are not assigned to this slot
    for slot in SLOTS:
        assigned_student = assignment[slot]
        for s in STUDENTS:
            if s != assigned_student:
                s_chk.add(Not(assign[idx_map[s]][slot]))
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)