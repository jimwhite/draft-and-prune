from z3 import *

# Art historians: 0=Farley, 1=Garcia, 2=Holden, 3=Jiang
# Topics: 0=lithographs, 1=oil paintings, 2=sculptures, 3=watercolors

# Position variables (1-4)
hist_pos = [Int(f"hist_pos_{i}") for i in range(4)]
topic_pos = [Int(f"topic_pos_{t}") for t in range(4)]

# Mapping: historian i gives topic h2t[i]
h2t = [Int(f"h2t_{i}") for i in range(4)]

solver = Solver()

# Each historian gives exactly one topic (h2t is a permutation)
solver.add(Distinct(h2t))

# Each historian's position equals the topic they give
for i in range(4):
    # Use Select to index into topic_pos with h2t[i]
    solver.add(hist_pos[i] == Select(topic_pos, h2t[i]))

# Positions are permutations of 1..4
solver.add(Distinct(hist_pos))
solver.add(Distinct(topic_pos))

# Domain constraints: positions between 1 and 4
for i in range(4):
    solver.add(hist_pos[i] >= 1, hist_pos[i] <= 4)
for t in range(4):
    solver.add(topic_pos[t] >= 1, topic_pos[t] <= 4)

# Ordering constraints
# oil paintings and watercolors before lithographs
solver.add(topic_pos[1] < topic_pos[0])  # oil paintings before lithographs
solver.add(topic_pos[3] < topic_pos[0])  # watercolors before lithographs

# Farley's lecture earlier than oil paintings
solver.add(hist_pos[0] < topic_pos[1])  # Farley before oil paintings

# Holden earlier than Garcia and Jiang
solver.add(hist_pos[2] < hist_pos[1])  # Holden before Garcia
solver.add(hist_pos[2] < hist_pos[3])  # Holden before Jiang

# Answer choices (as formulas that must be true)
answer_choices = [
    hist_pos[0] < topic_pos[2],  # Farley before sculptures
    hist_pos[2] < topic_pos[0],  # Holden before lithographs
    topic_pos[2] < hist_pos[1],  # sculptures before Garcia
    topic_pos[2] < hist_pos[3],  # sculptures before Jiang
    topic_pos[3] < hist_pos[1]   # watercolors before Garcia
]

answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    # Add negation of the choice
    s_chk.add(Not(choice))
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)