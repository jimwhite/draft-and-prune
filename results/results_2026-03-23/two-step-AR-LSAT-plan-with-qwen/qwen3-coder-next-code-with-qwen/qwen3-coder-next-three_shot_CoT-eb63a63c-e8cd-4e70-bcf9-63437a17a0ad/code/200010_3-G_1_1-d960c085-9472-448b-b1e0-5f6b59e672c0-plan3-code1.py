from z3 import *

# Student indices: George=0, Helen=1, Irving=2, Kyle=3, Lenore=4, Nina=5, Olivia=6, Robert=7
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
student_idx = {s: i for i, s in enumerate(students)}

# Time slots: 0=Mon-morning, 1=Mon-afternoon, 2=Tue-morning, 3=Tue-afternoon, 4=Wed-morning, 5=Wed-afternoon
# -1 means the student does not give a report

slot = [Int(f"slot_{s}") for s in students]

solver = Solver()

# Domain constraints: each slot is either -1 or 0-5
for i in range(8):
    solver.add(Or([slot[i] == j for j in range(-1, 6)]))

# Exactly six reports: exactly six students have slot[i] != -1
report_count = Sum([If(slot[i] == -1, 0, 1) for i in range(8)])
solver.add(report_count == 6)

# One student per slot: for each time slot s in 0..5, at most one student has slot[i] = s
for s in range(6):
    # For each pair of students, they cannot both be assigned to slot s
    for i in range(8):
        for j in range(i + 1, 8):
            solver.add(Or(slot[i] != s, slot[j] != s))

# Tuesday-only-for-George: if George reports, then slot[0] must be 2 or 3
solver.add(Implies(slot[student_idx["George"]] != -1, 
                   Or(slot[student_idx["George"]] == 2, slot[student_idx["George"]] == 3)))

# No afternoon for Olivia or Robert: if they report, slot must be morning (0, 2, or 4)
olivia_morning = Or(slot[student_idx["Olivia"]] == -1, 
                    slot[student_idx["Olivia"]] == 0,
                    slot[student_idx["Olivia"]] == 2,
                    slot[student_idx["Olivia"]] == 4)
robert_morning = Or(slot[student_idx["Robert"]] == -1,
                    slot[student_idx["Robert"]] == 0,
                    slot[student_idx["Robert"]] == 2,
                    slot[student_idx["Robert"]] == 4)
solver.add(olivia_morning, robert_morning)

# Nina conditional constraint
nina_slot = slot[student_idx["Nina"]]
helen_slot = slot[student_idx["Helen"]]
irving_slot = slot[student_idx["Irving"]]

# If Nina reports on Monday (slot=0), then Helen and Irving must report on Tuesday
nina_monday_cond = Implies(And(nina_slot == 0, nina_slot != -1),
                           And(helen_slot == 2, irving_slot == 2))

# If Nina reports on Tuesday (slot=2), then Helen and Irving must report on Wednesday
nina_tuesday_cond = Implies(And(nina_slot == 2, nina_slot != -1),
                            And(helen_slot == 4, irving_slot == 4))

# If Nina reports on Wednesday (slot=4 or 5), no constraint needed
solver.add(nina_monday_cond, nina_tuesday_cond)

# Answer choices (schedules)
answer_choices = [
    # 0: 'Mon. morning: Helen; Mon. afternoon: Robert Tues. morning: Olivia; Tues. afternoon: Irving Wed. morning: Lenore; Wed. afternoon: Kyle'
    {
        "Helen": 0, "Robert": 1, "Olivia": 2, "Irving": 3, "Lenore": 4, "Kyle": 5,
        "George": -1, "Nina": -1
    },
    # 1: 'Mon. morning: Irving; Mon. afternoon: Olivia Tues. morning: Helen; Tues. afternoon: Kyle Wed. morning: Nina; Wed. afternoon: Lenore'
    {
        "Irving": 0, "Olivia": 1, "Helen": 2, "Kyle": 3, "Nina": 4, "Lenore": 5,
        "George": -1, "Robert": -1
    },
    # 2: 'Mon. morning: Lenore; Mon. afternoon: Helen Tues. morning: George; Tues. afternoon: Kyle Wed. morning: Robert; Wed. afternoon: Irving'
    {
        "Lenore": 0, "Helen": 1, "George": 2, "Kyle": 3, "Robert": 4, "Irving": 5,
        "Olivia": -1, "Nina": -1
    },
    # 3: 'Mon. morning: Nina; Mon. afternoon: Helen Tues. morning: Robert; Tues. afternoon: Irving Wed. morning: Olivia; Wed. afternoon: Lenore'
    {
        "Nina": 0, "Helen": 1, "Robert": 2, "Irving": 3, "Olivia": 4, "Lenore": 5,
        "George": -1, "Kyle": -1
    },
    # 4: 'Mon. morning: Olivia; Mon. afternoon: Nina Tues. morning: Irving; Tues. afternoon: Helen Wed. morning: Kyle; Wed. afternoon: George'
    {
        "Olivia": 0, "Nina": 1, "Irving": 2, "Helen": 3, "Kyle": 4, "George": 5,
        "Robert": -1, "Lenore": -1
    }
]

answer_index_list = []
for idx, schedule in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add the specific assignment constraints
    for student, assigned_slot in schedule.items():
        s_chk.add(slot[student_idx[student]] == assigned_slot)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)