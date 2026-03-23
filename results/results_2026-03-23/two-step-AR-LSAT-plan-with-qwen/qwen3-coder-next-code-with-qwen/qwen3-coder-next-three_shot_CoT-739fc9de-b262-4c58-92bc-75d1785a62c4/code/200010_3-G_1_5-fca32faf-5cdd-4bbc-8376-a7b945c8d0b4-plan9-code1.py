from z3 import *

# Student indices: George=0, Helen=1, Irving=2, Kyle=3, Lenore=4, Nina=5, Olivia=6, Robert=7
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
student_idx = {name: i for i, name in enumerate(students)}

# Report slots: 0=Mon-morning, 1=Mon-afternoon, 2=Tue-morning, 3=Tue-afternoon, 4=Wed-morning, 5=Wed-afternoon
report = [Int(f"r_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: each report slot assigned to one of 8 students (0-7)
for i in range(6):
    solver.add(report[i] >= 0, report[i] <= 7)

# Injectivity constraint: exactly six distinct students report
solver.add(Distinct(*report))

# Fixed constraints from premise:
# Kyle gives afternoon report on Tuesday → slot 3 = Kyle (index 3)
solver.add(report[3] == student_idx["Kyle"])
# Helen gives afternoon report on Wednesday → slot 5 = Helen (index 1)
solver.add(report[5] == student_idx["Helen"])

# Tuesday is the only day George can report → George (0) can only be in slot 2 or 3
# Since slot 3 is Kyle, George can only possibly be in slot 2 (Tue-morning)
solver.add(Implies(report[0] == student_idx["George"], False))  # George not in Mon-morning
solver.add(Implies(report[1] == student_idx["George"], False))  # George not in Mon-afternoon
solver.add(Implies(report[4] == student_idx["George"], False))  # George not in Wed-morning
solver.add(Implies(report[5] == student_idx["George"], False))  # George not in Wed-afternoon (already Helen)
solver.add(Or(report[2] == student_idx["George"], report[2] != student_idx["George"]))  # George may be in slot 2

# Olivia (6) and Robert (7) cannot give afternoon reports → not in slots 1, 3, 5
for slot in [1, 3, 5]:
    solver.add(report[slot] != student_idx["Olivia"])
    solver.add(report[slot] != student_idx["Robert"])

# Nina conditional constraint:
# If Nina reports on Monday (slots 0 or 1), then Helen and Irving must both report on Tuesday (slots 2 and 3)
# But slot 3 is Kyle, so Helen and Irving cannot both be on Tuesday → Nina cannot report Monday
# If Nina reports on Tuesday (slots 2 or 3), then Helen and Irving must both report on Wednesday
# Slot 5 is Helen, so Irving must be in slot 4 (Wed-morning)
# If Nina reports on Wednesday (slots 4 or 5), no constraint. Slot 5 is Helen, so Nina only possible in slot 4.

# Encode Nina constraints:
nina_idx = student_idx["Nina"]
helen_idx = student_idx["Helen"]
irving_idx = student_idx["Irving"]

# Nina cannot be in Monday slots (0 or 1)
solver.add(report[0] != nina_idx)
solver.add(report[1] != nina_idx)

# If Nina is in slot 2 (Tue-morning), then slot 4 must be Irving
solver.add(Implies(report[2] == nina_idx, report[4] == irving_idx))

# If Nina is in slot 4 (Wed-morning), no additional constraint needed

# Answer choices: each choice is [Mon-morning, Tue-morning, Wed-morning] = [slot0, slot2, slot4]
answer_choices = [
    ["Irving", "Lenore", "Nina"],   # 0
    ["Lenore", "George", "Irving"], # 1
    ["Nina", "Irving", "Lenore"],   # 2
    ["Robert", "George", "Irving"], # 3
    ["Robert", "Irving", "Lenore"]  # 4
]

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add the three morning report assignments
    s_chk.add(report[0] == student_idx[choice[0]])  # Mon-morning
    s_chk.add(report[2] == student_idx[choice[1]])  # Tue-morning
    s_chk.add(report[4] == student_idx[choice[2]])  # Wed-morning
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)