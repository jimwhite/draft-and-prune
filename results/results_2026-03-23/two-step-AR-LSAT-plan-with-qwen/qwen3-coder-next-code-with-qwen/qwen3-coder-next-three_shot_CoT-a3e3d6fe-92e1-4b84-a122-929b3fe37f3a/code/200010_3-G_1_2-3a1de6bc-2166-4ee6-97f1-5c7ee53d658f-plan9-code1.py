from z3 import *

# Students: George, Helen, Irving, Kyle, Lenore, Nina, Olivia, Robert
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
student_to_idx = {s: i for i, s in enumerate(students)}

# Report slots: 0=Mon AM, 1=Mon PM, 2=Tue AM, 3=Tue PM, 4=Wed AM, 5=Wed PM
slots = [Int(f"slot_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: each slot assigned to one of the 8 students (represented as indices 0-7)
for i in range(6):
    solver.add(And(slots[i] >= 0, slots[i] <= 7))

# Exactly six distinct students report (Kyle and Lenore are excluded)
excluded = [student_to_idx["Kyle"], student_to_idx["Lenore"]]
# Enforce that Kyle and Lenore are not assigned to any slot
solver.add(And([slots[i] != excluded[0] for i in range(6)]))
solver.add(And([slots[i] != excluded[1] for i in range(6)]))

# Enforce exactly 6 distinct reporters (since Kyle and Lenore are excluded, we need 6 from remaining 6)
# We'll enforce that all 6 reporters are distinct and come from the allowed set
allowed_students = [i for i in range(8) if i not in excluded]
# Since there are exactly 6 slots and 6 allowed students, all must be used
for i in range(6):
    for j in range(i+1, 6):
        solver.add(slots[i] != slots[j])

# Tuesday-only constraint for George: if George reports, must be on Tue (slots 2 or 3)
george_idx = student_to_idx["George"]
solver.add(Implies(
    Or([slots[i] == george_idx for i in range(6)]),
    Or(slots[2] == george_idx, slots[3] == george_idx)
))

# Olivia and Robert cannot give afternoon reports (PM slots: 1, 3, 5)
olivia_idx = student_to_idx["Olivia"]
robert_idx = student_to_idx["Robert"]
for pm_slot in [1, 3, 5]:
    solver.add(slots[pm_slot] != olivia_idx)
    solver.add(slots[pm_slot] != robert_idx)

# Nina conditional constraint: if Nina reports on Mon or Tue, then next day both Helen and Irving must report
nina_idx = student_to_idx["Nina"]
helen_idx = student_to_idx["Helen"]
irving_idx = student_to_idx["Irving"]

# Nina on Monday (slot 0 or 1) -> Helen and Irving must both report on Tuesday
nina_mon = Or(slots[0] == nina_idx, slots[1] == nina_idx)
helen_tue = Or(slots[2] == helen_idx, slots[3] == helen_idx)
irving_tue = Or(slots[2] == irving_idx, slots[3] == irving_idx)
solver.add(Implies(nina_mon, And(helen_tue, irving_tue)))

# Nina on Tuesday (slot 2 or 3) -> Helen and Irving must both report on Wednesday
nina_tue = Or(slots[2] == nina_idx, slots[3] == nina_idx)
helen_wed = Or(slots[4] == helen_idx, slots[5] == helen_idx)
irving_wed = Or(slots[4] == irving_idx, slots[5] == irving_idx)
solver.add(Implies(nina_tue, And(helen_wed, irving_wed)))

# Answer choices: (Mon AM, Tue AM, Wed AM) = (slot[0], slot[2], slot[4])
answer_choices = [
    ("Helen", "George", "Nina"),
    ("Irving", "Robert", "Helen"),
    ("Nina", "Helen", "Olivia"),
    ("Olivia", "Robert", "Irving"),
    ("Robert", "George", "Helen")
]

# Convert answer choices to indices
answer_idx_list = []
for idx, (mon_am, tue_am, wed_am) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Fix the AM slots
    mon_am_idx = student_to_idx[mon_am]
    tue_am_idx = student_to_idx[tue_am]
    wed_am_idx = student_to_idx[wed_am]
    
    s_chk.add(slots[0] == mon_am_idx)
    s_chk.add(slots[2] == tue_am_idx)
    s_chk.add(slots[4] == wed_am_idx)
    
    if s_chk.check() == sat:
        answer_idx_list.append(idx)

print(answer_idx_list)