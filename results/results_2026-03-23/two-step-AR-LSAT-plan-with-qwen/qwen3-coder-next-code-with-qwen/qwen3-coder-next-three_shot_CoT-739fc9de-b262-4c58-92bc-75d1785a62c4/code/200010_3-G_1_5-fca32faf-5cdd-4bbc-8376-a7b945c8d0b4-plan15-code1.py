from z3 import *

# Student indices: George=0, Helen=1, Irving=2, Kyle=3, Lenore=4, Nina=5, Olivia=6, Robert=7
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
num_students = 8

# Slot indices: 0=M_morn, 1=M_after, 2=T_morn, 3=T_after, 4=W_morn, 5=W_after
num_slots = 6

# Boolean variables: assigned[i][s] = True if student i is assigned to slot s
assigned = [[Bool(f"assigned_{i}_{s}") for s in range(num_slots)] for i in range(num_students)]

# Base solver
solver = Solver()

# Exactly six students are selected (sum of all assigned[i][*] = 6)
solver.add(Sum([If(assigned[i][s], 1, 0) for i in range(num_students) for s in range(num_slots)]) == 6)

# Each slot is assigned to exactly one student
for s in range(num_slots):
    solver.add(Sum([If(assigned[i][s], 1, 0) for i in range(num_students)]) == 1)

# Each selected student is assigned to exactly one slot
for i in range(num_students):
    solver.add(Sum([If(assigned[i][s], 1, 0) for s in range(num_slots)]) <= 1)

# Tuesday is the only day George can report (slots 2=T_morn, 3=T_after)
for s in [0, 1, 4, 5]:  # M_morn, M_after, W_morn, W_after
    solver.add(Not(assigned[0][s]))

# Neither Olivia nor Robert can give an afternoon report (slots 1, 3, 5 are afternoons)
for s in [1, 3, 5]:
    solver.add(Not(assigned[6][s]))  # Olivia
    solver.add(Not(assigned[7][s]))  # Robert

# Conditional constraint: If Nina gives a report, then Helen and Irving must both give reports the next day (unless Nina on Wednesday)
# Monday morning or afternoon -> Tuesday both Helen and Irving
solver.add(Implies(
    Or(assigned[5][0], assigned[5][1]),
    And(
        Or(assigned[1][2], assigned[1][3]),  # Helen on Tuesday
        Or(assigned[2][2], assigned[2][3])   # Irving on Tuesday
    )
))

# Tuesday morning or afternoon -> Wednesday both Helen and Irving
solver.add(Implies(
    Or(assigned[5][2], assigned[5][3]),
    And(
        Or(assigned[1][4], assigned[1][5]),  # Helen on Wednesday
        Or(assigned[2][4], assigned[2][5])   # Irving on Wednesday
    )
))

# Given scenario constraints:
# Kyle gives afternoon report on Tuesday (slot 3)
solver.add(assigned[3][3])

# Helen gives afternoon report on Wednesday (slot 5)
solver.add(assigned[1][5])

# Additional reasoning: Since Helen is assigned to W_after (slot 5), she cannot be elsewhere
for s in range(5):
    solver.add(Not(assigned[1][s]))

# Since Kyle is assigned to T_after (slot 3), he cannot be elsewhere
for s in range(4):
    solver.add(Not(assigned[3][s]))

# Now check each choice for morning slots (M_morn=0, T_morn=2, W_morn=4)
choices = [
    ("Irving", "Lenore", "Nina"),  # Choice 0: Irving (2), Lenore (4), Nina (5)
    ("Lenore", "George", "Irving"),  # Choice 1: Lenore (4), George (0), Irving (2)
    ("Nina", "Irving", "Lenore"),  # Choice 2: Nina (5), Irving (2), Lenore (4)
    ("Robert", "George", "Irving"),  # Choice 3: Robert (7), George (0), Irving (2)
    ("Robert", "Irving", "Lenore")   # Choice 4: Robert (7), Irving (2), Lenore (4)
]

answer_index_list = []
for idx, (m_morn_name, t_morn_name, w_morn_name) in enumerate(choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Map names to indices
    m_morn_idx = students.index(m_morn_name)
    t_morn_idx = students.index(t_morn_name)
    w_morn_idx = students.index(w_morn_name)
    
    # Assign morning slots
    s_chk.add(assigned[m_morn_idx][0])  # Monday morning
    s_chk.add(assigned[t_morn_idx][2])  # Tuesday morning
    s_chk.add(assigned[w_morn_idx][4])  # Wednesday morning
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)