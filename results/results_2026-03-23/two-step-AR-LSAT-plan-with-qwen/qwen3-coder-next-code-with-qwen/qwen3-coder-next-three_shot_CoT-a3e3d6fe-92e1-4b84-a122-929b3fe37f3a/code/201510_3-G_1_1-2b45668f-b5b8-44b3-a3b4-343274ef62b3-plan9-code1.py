from z3 import *

# Accomplice indices: 0-Peters, 1-Quinn, 2-Rovero, 3-Stanton, 4-Tao, 5-Villas, 6-White
names = ["Peters", "Quinn", "Rovero", "Stanton", "Tao", "Villas", "White"]
pos = [Int(f"pos_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: positions 1-7, all distinct
for i in range(7):
    solver.add(pos[i] >= 1, pos[i] <= 7)
solver.add(Distinct(*pos))

# Fixed constraint: Peters is recruited fourth
solver.add(pos[0] == 4)

# Relative ordering: Quinn earlier than Rovero
solver.add(pos[1] < pos[2])

# Adjacency: Villas immediately before White
solver.add(pos[5] + 1 == pos[6])

# Separation: Stanton not adjacent to Tao
solver.add(Abs(pos[3] - pos[4]) != 1)

# Answer choices (each is a list of names in order from first to last)
choices = [
    ["Quinn", "Tao", "Stanton", "Peters", "Villas", "White", "Rovero"],
    ["Quinn", "White", "Rovero", "Peters", "Stanton", "Villas", "Tao"],
    ["Villas", "White", "Quinn", "Stanton", "Peters", "Tao", "Rovero"],
    ["Villas", "White", "Stanton", "Peters", "Quinn", "Tao", "Rovero"],
    ["Villas", "White", "Stanton", "Peters", "Rovero", "Tao", "Quinn"]
]

# Check each choice
answer_index_list = []
for idx, choice in enumerate(choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraints that match the candidate ordering
    for position, name in enumerate(choice, start=1):
        if name == "Peters":
            s_chk.add(pos[0] == position)
        elif name == "Quinn":
            s_chk.add(pos[1] == position)
        elif name == "Rovero":
            s_chk.add(pos[2] == position)
        elif name == "Stanton":
            s_chk.add(pos[3] == position)
        elif name == "Tao":
            s_chk.add(pos[4] == position)
        elif name == "Villas":
            s_chk.add(pos[5] == position)
        elif name == "White":
            s_chk.add(pos[6] == position)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)