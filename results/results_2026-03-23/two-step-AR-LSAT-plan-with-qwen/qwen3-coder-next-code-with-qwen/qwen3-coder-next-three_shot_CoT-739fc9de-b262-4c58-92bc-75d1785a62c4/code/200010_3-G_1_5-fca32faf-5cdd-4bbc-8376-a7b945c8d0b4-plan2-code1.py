from z3 import *

# Student indices: George=0, Helen=1, Irving=2, Kyle=3, Lenore=4, Nina=5, Olivia=6, Robert=7
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
num_students = 8

# Slot indices: MonMorning=0, MonAfternoon=1, TueMorning=2, TueAfternoon=3, WedMorning=4, WedAfternoon=5
num_slots = 6

# assigned[i] = slot index if student i is selected, -1 otherwise
assigned = [Int(f"assigned_{i}") for i in range(num_students)]

# Base solver
solver = Solver()

# Selection constraint: exactly six students are selected
selected_count = Sum([If(assigned[i] != -1, 1, 0) for i in range(num_students)])
solver.add(selected_count == 6)

# Slot uniqueness constraint: no two students share the same slot
slot_constraints = []
for i in range(num_students):
    for j in range(i + 1, num_students):
        slot_constraints.append(Or(assigned[i] == -1, assigned[j] == -1, assigned[i] != assigned[j]))
solver.add(slot_constraints)

# Domain constraints: each assigned slot must be between 0 and 5
for i in range(num_students):
    solver.add(Or(assigned[i] == -1, And(assigned[i] >= 0, assigned[i] <= 5)))

# Fixed assignments from prompt
solver.add(assigned[3] == 3)  # Kyle: TueAfternoon = slot 3
solver.add(assigned[1] == 5)  # Helen: WedAfternoon = slot 5

# George can only report on Tuesday (slots 2 or 3)
solver.add(Implies(assigned[0] != -1, Or(assigned[0] == 2, assigned[0] == 3)))

# Olivia and Robert cannot give afternoon reports (slots 1, 3, 5 are afternoon)
solver.add(Implies(assigned[6] != -1, Or(assigned[6] == 0, assigned[6] == 2, assigned[6] == 4)))
solver.add(Implies(assigned[7] != -1, Or(assigned[7] == 0, assigned[7] == 2, assigned[7] == 4)))

# Nina conditional constraint
# If Nina reports (assigned[5] != -1) and her slot is not Wed (i.e., slot < 4), then Helen and Irving must both report the next day
# Note: Helen is already assigned to slot 5 (WedAfternoon), so we only need to check Irving's assignment
# For Nina on MonMorning (0) or MonAfternoon (1): next day is Tue → slots 2,3
# For Nina on TueMorning (2) or TueAfternoon (3): next day is Wed → slots 4,5
# Since Helen is already on slot 5 (WedAfternoon), we only need Irving to be on WedMorning (4) if Nina is on Tue
# But the constraint says "Helen and Irving must both give reports" on next day, so we need to check if Helen is assigned to a slot on the next day
# Since Helen is fixed to slot 5 (WedAfternoon), she only satisfies the constraint if Nina reports on Tue (so next day is Wed)
# For Nina on Mon: Helen must be on Tue, but she's fixed to Wed → impossible. So Nina cannot report on Mon.
# For Nina on Tue: Helen must be on Wed (she is), and Irving must be on Wed → slot 4 or 5, but Helen takes 5, so Irving must take 4
# For Nina on Wed: no constraint

nina_slot = assigned[5]
irving_slot = assigned[2]

# If Nina reports on Mon (slot 0 or 1), then Helen must be on Tue (slots 2,3) and Irving on Tue
# But Helen is fixed to slot 5 (Wed), so this is impossible → Nina cannot be on Mon
solver.add(Implies(nina_slot == 0, False))
solver.add(Implies(nina_slot == 1, False))

# If Nina reports on Tue (slot 2 or 3), then Helen must be on Wed and Irving must be on Wed
# Helen is fixed to slot 5 (Wed), so we just need Irving to be on Wed (slot 4 or 5)
# But slot 5 is taken by Helen, so Irving must be on slot 4 (WedMorning)
solver.add(Implies(Or(nina_slot == 2, nina_slot == 3), irving_slot == 4))

# If Nina reports on Wed (slot 4 or 5), no constraint
solver.add(Implies(nina_slot == 4, True))
solver.add(Implies(nina_slot == 5, True))

# Helper function to get day from slot
def day_of_slot(slot_val):
    return slot_val // 2

# Answer choices: morning reporters for Mon, Tue, Wed → slots 0, 2, 4
answer_choices = [
    ("Irving", "Lenore", "Nina"),   # Choice 0: Irving=0, Lenore=2, Nina=4
    ("Lenore", "George", "Irving"), # Choice 1: Lenore=0, George=2, Irving=4
    ("Nina", "Irving", "Lenore"),   # Choice 2: Nina=0, Irving=2, Lenore=4
    ("Robert", "George", "Irving"), # Choice 3: Robert=0, George=2, Irving=4
    ("Robert", "Irving", "Lenore")  # Choice 4: Robert=0, Irving=2, Lenore=4
]

# Map student names to indices
student_idx = {name: i for i, name in enumerate(students)}

# Check each answer choice
answer_index_list = []
for idx, (mon_morn, tue_morn, wed_morn) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraints for morning slots
    s_chk.add(assigned[student_idx[mon_morn]] == 0)   # Monday morning = slot 0
    s_chk.add(assigned[student_idx[tue_morn]] == 2)   # Tuesday morning = slot 2
    s_chk.add(assigned[student_idx[wed_morn]] == 4)   # Wednesday morning = slot 4
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)