from z3 import *

# Student indices
(GEORGE, HELEN, IRVING, KYLE, LENORE, NINA, OLIVIA, ROBERT) = range(8)

# Slot indices: 0-MM, 1-MA, 2-TM, 3-TA, 4-WM, 5-WA
slot_student = [Int(f"slot_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: each slot assigned one of the 8 students
for i in range(6):
    solver.add(Or(
        slot_student[i] == GEORGE,
        slot_student[i] == HELEN,
        slot_student[i] == IRVING,
        slot_student[i] == KYLE,
        slot_student[i] == LENORE,
        slot_student[i] == NINA,
        slot_student[i] == OLIVIA,
        slot_student[i] == ROBERT
    ))

# Exactly six distinct students are used (no repeats)
solver.add(Distinct(*slot_student))

# Tuesday-only constraint: George can only give reports on Tuesday (slots 2 or 3)
for i in range(6):
    solver.add(Implies(slot_student[i] == GEORGE, Or(i == 2, i == 3)))

# Afternoon-restriction: Olivia and Robert cannot give afternoon reports
# Afternoon slots are 1 (MA), 3 (TA), 5 (WA)
for i in [1, 3, 5]:
    solver.add(slot_student[i] != OLIVIA)
    solver.add(slot_student[i] != ROBERT)

# Nina conditional constraint
# Define helper expressions for Nina's position
nina_slot = Int('nina_slot')
solver.add(nina_slot == If(slot_student[0] == NINA, 0,
              If(slot_student[1] == NINA, 1,
              If(slot_student[2] == NINA, 2,
              If(slot_student[3] == NINA, 3,
              If(slot_student[4] == NINA, 4,
              If(slot_student[5] == NINA, 5, -1))))))

# Nina on Monday (slot 0 or 1) → Helen and Irving must be on Tuesday (slots 2,3)
solver.add(Implies(
    Or(slot_student[0] == NINA, slot_student[1] == NINA),
    And(
        Or(slot_student[2] == HELEN, slot_student[3] == HELEN),
        Or(slot_student[2] == IRVING, slot_student[3] == IRVING)
    )
))

# Nina on Tuesday (slot 2 or 3) → Helen and Irving must be on Wednesday (slots 4,5)
solver.add(Implies(
    Or(slot_student[2] == NINA, slot_student[3] == NINA),
    And(
        Or(slot_student[4] == HELEN, slot_student[5] == HELEN),
        Or(slot_student[4] == IRVING, slot_student[5] == IRVING)
    )
))

# Nina on Wednesday (slot 4 or 5) → no additional constraint needed

# Define the answer choices
choices = [
    # Choice 0: 'Mon. morning: Helen; Mon. afternoon: Robert Tues. morning: Olivia; Tues. afternoon: Irving Wed. morning: Lenore; Wed. afternoon: Kyle'
    [HELEN, ROBERT, OLIVIA, IRVING, LENORE, KYLE],
    # Choice 1: 'Mon. morning: Irving; Mon. afternoon: Olivia Tues. morning: Helen; Tues. afternoon: Kyle Wed. morning: Nina; Wed. afternoon: Lenore'
    [IRVING, OLIVIA, HELEN, KYLE, NINA, LENORE],
    # Choice 2: 'Mon. morning: Lenore; Mon. afternoon: Helen Tues. morning: George; Tues. afternoon: Kyle Wed. morning: Robert; Wed. afternoon: Irving'
    [LENORE, HELEN, GEORGE, KYLE, ROBERT, IRVING],
    # Choice 3: 'Mon. morning: Nina; Mon. afternoon: Helen Tues. morning: Robert; Tues. afternoon: Irving Wed. morning: Olivia; Wed. afternoon: Lenore'
    [NINA, HELEN, ROBERT, IRVING, OLIVIA, LENORE],
    # Choice 4: 'Mon. morning: Olivia; Mon. afternoon: Nina Tues. morning: Irving; Tues. afternoon: Helen Wed. morning: Kyle; Wed. afternoon: George'
    [OLIVIA, NINA, IRVING, HELEN, KYLE, GEORGE]
]

# Check each choice
answer_index_list = []
for idx, schedule in enumerate(choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the exact assignments from the choice
    for i in range(6):
        s_chk.add(slot_student[i] == schedule[i])
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

# Output the index of the valid schedule (only one should be SAT)
print(answer_index_list[0] if answer_index_list else -1)