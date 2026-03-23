from z3 import *

# Singer indices: Kammer=0, Lugo=1, Trillo=2, Waite=3, Yoshida=4, Zinn=5
singers = ["Kammer", "Lugo", "Trillo", "Waite", "Yoshida", "Zinn"]
pos = [Int(f"pos_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: positions 1-6, all distinct
for i in range(6):
    solver.add(pos[i] >= 1, pos[i] <= 6)
solver.add(Distinct(*pos))

# Recording constraints
# Recorded auditions: Kammer (0) and Lugo (1)
# Fourth audition cannot be recorded → pos_Kammer != 4, pos_Lugo != 4
solver.add(pos[0] != 4)
solver.add(pos[1] != 4)
# Fifth audition must be recorded → exactly one of Kammer or Lugo is in position 5
solver.add(Or(And(pos[0] == 5, pos[1] != 5), And(pos[0] != 5, pos[1] == 5)))

# Waite constraint: earlier than both recorded auditions
solver.add(pos[3] < pos[0])
solver.add(pos[3] < pos[1])

# Kammer–Trillo constraint: Kammer before Trillo
solver.add(pos[0] < pos[2])

# Zinn–Yoshida constraint: Zinn before Yoshida
solver.add(pos[5] < pos[4])

# Answer choices (each is a list of singers in order)
answer_choices = [
    ["Kammer", "Trillo", "Zinn", "Waite", "Lugo", "Yoshida"],
    ["Waite", "Kammer", "Yoshida", "Zinn", "Lugo", "Trillo"],
    ["Waite", "Lugo", "Kammer", "Trillo", "Zinn", "Yoshida"],
    ["Waite", "Zinn", "Kammer", "Trillo", "Lugo", "Yoshida"],
    ["Zinn", "Yoshida", "Waite", "Lugo", "Kammer", "Trillo"]
]

# Check each choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert exact positions from the choice
    for j, singer in enumerate(choice):
        singer_idx = singers.index(singer)
        s_chk.add(pos[singer_idx] == j + 1)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)