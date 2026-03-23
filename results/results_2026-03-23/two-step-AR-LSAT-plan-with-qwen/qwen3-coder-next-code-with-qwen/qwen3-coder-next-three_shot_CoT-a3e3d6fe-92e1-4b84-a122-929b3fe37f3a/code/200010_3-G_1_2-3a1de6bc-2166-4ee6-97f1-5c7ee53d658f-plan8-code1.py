from z3 import *

# Students: George, Helen, Irving, Kyle, Lenore, Nina, Olivia, Robert
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
student_idx = {s: i for i, s in enumerate(students)}

# Boolean variables indicating if a student speaks
speaks = [Bool(f"speaks_{s}") for s in students]

# Integer variables for slot positions (0-5)
slot = [Int(f"slot_{s}") for s in students]

# Base solver
solver = Solver()

# Exactly 6 students speak (Kyle and Lenore do not speak, so exactly the other 6 must speak)
solver.add(And(
    Not(speaks[student_idx["Kyle"]]),
    Not(speaks[student_idx["Lenore"]])
))
solver.add(Sum([If(s, 1, 0) for s in speaks]) == 6)

# Each speaker is assigned a distinct slot (0-5)
for i, s in enumerate(students):
    solver.add(Implies(speaks[i], And(slot[i] >= 0, slot[i] <= 5)))
    solver.add(Implies(Not(speaks[i]), slot[i] == -1))

# All speakers have distinct slots
for i in range(len(students)):
    for j in range(i + 1, len(students)):
        solver.add(Or(
            Not(speaks[i]),
            Not(speaks[j]),
            slot[i] != slot[j]
        ))

# Tuesday is the only day George can give a report
# Slots: 0=Mon AM, 1=Mon PM, 2=Tue AM, 3=Tue PM, 4=Wed AM, 5=Wed PM
# Tuesday slots are 2 and 3
solver.add(Implies(speaks[student_idx["George"]], Or(slot[student_idx["George"]] == 2, slot[student_idx["George"]] == 3)))

# Olivia and Robert cannot give afternoon reports
# Afternoon slots: 1, 3, 5
solver.add(Implies(speaks[student_idx["Olivia"]], Or(slot[student_idx["Olivia"]] == 0, slot[student_idx["Olivia"]] == 2, slot[student_idx["Olivia"]] == 4)))
solver.add(Implies(speaks[student_idx["Robert"]], Or(slot[student_idx["Robert"]] == 0, slot[student_idx["Robert"]] == 2, slot[student_idx["Robert"]] == 4)))

# Conditional: If Nina gives a report on Monday (slots 0 or 1), then Helen and Irving must both give reports on Tuesday (slots 2,3)
nina_mon = And(speaks[student_idx["Nina"]], Or(slot[student_idx["Nina"]] == 0, slot[student_idx["Nina"]] == 1))
solver.add(Implies(nina_mon, And(
    speaks[student_idx["Helen"]],
    speaks[student_idx["Irving"]],
    Or(slot[student_idx["Helen"]] == 2, slot[student_idx["Helen"]] == 3),
    Or(slot[student_idx["Irving"]] == 2, slot[student_idx["Irving"]] == 3)
)))

# If Nina gives a report on Tuesday (slots 2 or 3), then Helen and Irving must both give reports on Wednesday (slots 4,5)
nina_tue = And(speaks[student_idx["Nina"]], Or(slot[student_idx["Nina"]] == 2, slot[student_idx["Nina"]] == 3))
solver.add(Implies(nina_tue, And(
    speaks[student_idx["Helen"]],
    speaks[student_idx["Irving"]],
    Or(slot[student_idx["Helen"]] == 4, slot[student_idx["Helen"]] == 5),
    Or(slot[student_idx["Irving"]] == 4, slot[student_idx["Irving"]] == 5)
)))

# Answer choices: (Mon AM, Tue AM, Wed AM) = slots 0, 2, 4
answer_choices = [
    ("Helen", "George", "Nina"),
    ("Irving", "Robert", "Helen"),
    ("Nina", "Helen", "Olivia"),
    ("Olivia", "Robert", "Irving"),
    ("Robert", "George", "Helen")
]

answer_index_list = []
for idx, (mon_am, tue_am, wed_am) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraints for morning slots
    s_chk.add(slot[student_idx[mon_am]] == 0)
    s_chk.add(slot[student_idx[tue_am]] == 2)
    s_chk.add(slot[student_idx[wed_am]] == 4)
    
    # Ensure these three students actually speak
    s_chk.add(speaks[student_idx[mon_am]])
    s_chk.add(speaks[student_idx[tue_am]])
    s_chk.add(speaks[student_idx[wed_am]])
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)