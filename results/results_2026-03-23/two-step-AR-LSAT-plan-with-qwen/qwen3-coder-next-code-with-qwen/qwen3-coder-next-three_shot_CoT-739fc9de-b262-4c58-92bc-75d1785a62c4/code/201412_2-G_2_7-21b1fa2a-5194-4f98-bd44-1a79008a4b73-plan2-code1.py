from z3 import *

# Art historians: 0=Farley, 1=Garcia, 2=Holden, 3=Jiang
# Topics: 0=lithographs, 1=oil paintings, 2=sculptures, 3=watercolors

# Variables: pos[i] = position (1-4) of historian i's lecture
pos = [Int(f"pos_{i}") for i in range(4)]

# Variables: topic_of[i] = topic given by historian i (0-3)
topic_of = [Int(f"topic_of_{i}") for i in range(4)]

# Variables: historian_of[j] = historian who gives topic j (0-3)
historian_of = [Int(f"historian_of_{j}") for j in range(4)]

# Base solver
solver = Solver()

# Domain constraints: positions 1-4, topics 0-3, historians 0-3
for i in range(4):
    solver.add(pos[i] >= 1, pos[i] <= 4)
    solver.add(topic_of[i] >= 0, topic_of[i] <= 3)

for j in range(4):
    solver.add(historian_of[j] >= 0, historian_of[j] <= 3)

# All positions distinct
solver.add(Distinct(pos))

# All topics assigned to historians (topic_of is a permutation)
solver.add(Distinct(topic_of))

# All historians assigned to topics (historian_of is a permutation)
solver.add(Distinct(historian_of))

# Link topic_of and historian_of: they are inverses
for i in range(4):
    for j in range(4):
        solver.add(Implies(topic_of[i] == j, historian_of[j] == i))
        solver.add(Implies(historian_of[j] == i, topic_of[i] == j))

# Ordering constraints
# Oil paintings (topic 1) and watercolors (topic 3) both earlier than lithographs (topic 0)
solver.add(Select(pos, Select(historian_of, IntVal(1))) < Select(pos, Select(historian_of, IntVal(0))))
solver.add(Select(pos, Select(historian_of, IntVal(3))) < Select(pos, Select(historian_of, IntVal(0))))

# Farley's lecture earlier than oil paintings
solver.add(pos[0] < Select(pos, Select(historian_of, IntVal(1))))

# Holden's lecture earlier than Garcia's and Jiang's
solver.add(pos[2] < pos[1])
solver.add(pos[2] < pos[3])

# Answer choices: check which must be true
answer_choices = [
    "Farley earlier than sculptures",  # A: pos[0] < pos[historian_of[2]]
    "Holden earlier than lithographs", # B: pos[2] < pos[historian_of[0]]
    "sculptures earlier than Garcia",  # C: pos[historian_of[2]] < pos[1]
    "sculptures earlier than Jiang",   # D: pos[historian_of[2]] < pos[3]
    "watercolors earlier than Garcia"  # E: pos[historian_of[3]] < pos[1]
]

answer_index_list = []

for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add negation of the statement
    if choice == "Farley earlier than sculptures":
        s_chk.add(pos[0] >= Select(pos, Select(historian_of, IntVal(2))))
    elif choice == "Holden earlier than lithographs":
        s_chk.add(pos[2] >= Select(pos, Select(historian_of, IntVal(0))))
    elif choice == "sculptures earlier than Garcia":
        s_chk.add(Select(pos, Select(historian_of, IntVal(2))) >= pos[1])
    elif choice == "sculptures earlier than Jiang":
        s_chk.add(Select(pos, Select(historian_of, IntVal(2))) >= pos[3])
    elif choice == "watercolors earlier than Garcia":
        s_chk.add(Select(pos, Select(historian_of, IntVal(3))) >= pos[1])
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)