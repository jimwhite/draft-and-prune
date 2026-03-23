from z3 import *

# Student indices: George=0, Helen=1, Irving=2, Kyle=3, Lenore=4, Nina=5, Olivia=6, Robert=7
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
student_idx = {name: i for i, name in enumerate(students)}

# Slot indices: 0=Mon_morn, 1=Mon_aft, 2=Tue_morn, 3=Tue_aft, 4=Wed_morn, 5=Wed_aft
slot = [Int(f"slot_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: each slot assigned to one of 8 students
for s in range(6):
    solver.add(Or([slot[s] == i for i in range(8)]))

# Exactly six distinct students (all slots different)
solver.add(Distinct(slot))

# Fixed constraints from scenario
# Kyle gives afternoon report on Tuesday -> slot[3] = Kyle (index 3)
solver.add(slot[3] == student_idx["Kyle"])
# Helen gives afternoon report on Wednesday -> slot[5] = Helen (index 1)
solver.add(slot[5] == student_idx["Helen"])

# Tuesday is the only day George can give a report
# George (index 0) can only appear in slot[2] or slot[3]
# Since slot[3]=Kyle≠0, George can only be in slot[2] if used
for s in range(6):
    solver.add(Implies(slot[s] == student_idx["George"], s == 2))

# Neither Olivia nor Robert can give an afternoon report
# Afternoon slots: 1 (Mon_aft), 3 (Tue_aft), 5 (Wed_aft)
# slot[3]=Kyle and slot[5]=Helen already satisfy, enforce for slot[1] and slot[5]
solver.add(slot[1] != student_idx["Olivia"], slot[1] != student_idx["Robert"])
solver.add(slot[5] != student_idx["Olivia"], slot[5] != student_idx["Robert"])

# Nina conditional constraint
# If Nina (index 5) gives a report on Mon (slots 0,1), then Helen & Irving must both give reports on Tue
# But slot[3]=Kyle≠Helen,Irving, so Nina cannot be on Mon
solver.add(slot[0] != student_idx["Nina"])
solver.add(slot[1] != student_idx["Nina"])

# If Nina gives report on Tue_morn (slot[2]), then Helen & Irving must both give reports on Wed
# slot[5]=Helen (1) already satisfies Helen condition, so need slot[4] to be Helen or Irving
# Since Helen is already used in slot[5], slot[4] must be Irving (2)
# Formalize: if slot[2]==5, then slot[4] must be 1 or 2
solver.add(Implies(slot[2] == student_idx["Nina"], Or(slot[4] == student_idx["Helen"], slot[4] == student_idx["Irving"])))

# Answer choices: (Mon_morn, Tue_morn, Wed_morn) = (slot[0], slot[2], slot[4])
answer_choices = [
    ["Irving", "Lenore", "Nina"],      # 0: slot[0]=2, slot[2]=4, slot[4]=5
    ["Lenore", "George", "Irving"],   # 1: slot[0]=4, slot[2]=0, slot[4]=2
    ["Nina", "Irving", "Lenore"],     # 2: slot[0]=5, slot[2]=2, slot[4]=4
    ["Robert", "George", "Irving"],   # 3: slot[0]=7, slot[2]=0, slot[4]=2
    ["Robert", "Irving", "Lenore"]    # 4: slot[0]=7, slot[2]=2, slot[4]=4
]

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraints for morning reports
    s_chk.add(slot[0] == student_idx[choice[0]])
    s_chk.add(slot[2] == student_idx[choice[1]])
    s_chk.add(slot[4] == student_idx[choice[2]])
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)