from z3 import *

# Student indices: George=0, Helen=1, Irving=2, Kyle=3, Lenore=4, Nina=5, Olivia=6, Robert=7
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
student_idx = {s: i for i, s in enumerate(students)}

# Slot indices: 0=Mon AM, 1=Mon PM, 2=Tue AM, 3=Tue PM, 4=Wed AM, 5=Wed PM
slot = [Int(f"slot_{i}") for i in range(8)]

# Base solver
solver = Solver()

# Domain constraints: each student either doesn't report (-1) or reports in one of 6 slots
for i in range(8):
    solver.add(Or(slot[i] == -1, And(slot[i] >= 0, slot[i] <= 5)))

# Exactly six students report
solver.add(Sum([If(slot[i] != -1, 1, 0) for i in range(8)]) == 6)

# Exactly two reports per day
## Monday (slots 0,1)
solver.add(Sum([If(slot[i] == 0, 1, 0) + If(slot[i] == 1, 1, 0) for i in range(8)]) == 2)
## Tuesday (slots 2,3)
solver.add(Sum([If(slot[i] == 2, 1, 0) + If(slot[i] == 3, 1, 0) for i in range(8)]) == 2)
## Wednesday (slots 4,5)
solver.add(Sum([If(slot[i] == 4, 1, 0) + If(slot[i] == 5, 1, 0) for i in range(8)]) == 2)

# Tuesday is the only day George can report
george_idx = student_idx["George"]
solver.add(Implies(slot[george_idx] != -1, Or(slot[george_idx] == 2, slot[george_idx] == 3)))

# Olivia and Robert cannot give afternoon reports
olivia_idx = student_idx["Olivia"]
robert_idx = student_idx["Robert"]
solver.add(Implies(slot[olivia_idx] != -1, Or(slot[olivia_idx] == 0, slot[olivia_idx] == 2, slot[olivia_idx] == 4)))
solver.add(Implies(slot[robert_idx] != -1, Or(slot[robert_idx] == 0, slot[robert_idx] == 2, slot[robert_idx] == 4)))

# Kyle gives afternoon report on Tuesday (slot=3)
kyle_idx = student_idx["Kyle"]
solver.add(slot[kyle_idx] == 3)

# Helen gives afternoon report on Wednesday (slot=5)
helen_idx = student_idx["Helen"]
solver.add(slot[helen_idx] == 5)

# Nina conditional constraint
nina_idx = student_idx["Nina"]
nina_slot = slot[nina_idx]

# If Nina reports on Monday (slot 0 or 1), then Helen and Irving must report Tuesday
solver.add(Implies(
    And(nina_slot != -1, Or(nina_slot == 0, nina_slot == 1)),
    And(slot[helen_idx] != -1, slot[student_idx["Irving"]] != -1,
        Or(slot[helen_idx] == 2, slot[helen_idx] == 3),
        Or(slot[student_idx["Irving"]] == 2, slot[student_idx["Irving"]] == 3))
))

# If Nina reports on Tuesday (slot 2), then Helen and Irving must report Wednesday
solver.add(Implies(
    And(nina_slot != -1, nina_slot == 2),
    And(slot[helen_idx] != -1, slot[student_idx["Irving"]] != -1,
        Or(slot[helen_idx] == 4, slot[helen_idx] == 5),
        Or(slot[student_idx["Irving"]] == 4, slot[student_idx["Irving"]] == 5))
))

# Slot uniqueness: no two students share the same slot
for i in range(8):
    for j in range(i + 1, 8):
        solver.add(Or(slot[i] == -1, slot[j] == -1, slot[i] != slot[j]))

# Answer choices: each is a list of [Mon AM reporter, Tue AM reporter, Wed AM reporter]
answer_choices = [
    ["Irving", "Lenore", "Nina"],      # 0
    ["Lenore", "George", "Irving"],   # 1
    ["Nina", "Irving", "Lenore"],     # 2
    ["Robert", "George", "Irving"],   # 3
    ["Robert", "Irving", "Lenore"]    # 4
]

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add fixed assignments from the answer choice
    # Monday morning (slot 0)
    mm_student = student_idx[choice[0]]
    s_chk.add(slot[mm_student] == 0)
    
    # Tuesday morning (slot 2)
    tm_student = student_idx[choice[1]]
    s_chk.add(slot[tm_student] == 2)
    
    # Wednesday morning (slot 4)
    wm_student = student_idx[choice[2]]
    s_chk.add(slot[wm_student] == 4)
    
    # Ensure Kyle and Helen are already assigned (they are in base constraints)
    # Also ensure the morning reporters are distinct and not Kyle or Helen
    s_chk.add(mm_student != kyle_idx, mm_student != helen_idx)
    s_chk.add(tm_student != kyle_idx, tm_student != helen_idx)
    s_chk.add(wm_student != kyle_idx, wm_student != helen_idx)
    
    # Ensure the three morning reporters are distinct
    s_chk.add(mm_student != tm_student, mm_student != wm_student, tm_student != wm_student)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)