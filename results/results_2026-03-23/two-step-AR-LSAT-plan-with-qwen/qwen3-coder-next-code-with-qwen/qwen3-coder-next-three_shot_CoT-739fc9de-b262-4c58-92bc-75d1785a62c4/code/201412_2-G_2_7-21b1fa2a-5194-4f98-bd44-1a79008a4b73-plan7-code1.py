from z3 import *

# Art historians: Farley=0, Garcia=1, Holden=2, Jiang=3
# Topics: lithographs=0, oil_paintings=1, sculptures=2, watercolors=3

# Decision variables
h_topic = [[Bool(f"h_topic_{h}_{t}") for t in range(4)] for h in range(4)]
topic_pos = [Int(f"topic_pos_{t}") for t in range(4)]

solver = Solver()

# Each historian gives exactly one topic
for h in range(4):
    solver.add(Sum([If(h_topic[h][t], 1, 0) for t in range(4)]) == 1)

# Each topic is given by exactly one historian
for t in range(4):
    solver.add(Sum([If(h_topic[h][t], 1, 0) for h in range(4)]) == 1)

# Topic positions are distinct and between 1 and 4
solver.add(Distinct(*topic_pos))
for t in range(4):
    solver.add(topic_pos[t] >= 1, topic_pos[t] <= 4)

# Define historian positions: historian_pos[h] = position of the topic given by historian h
historian_pos = [Int(f"historian_pos_{h}") for h in range(4)]
for h in range(4):
    # historian_pos[h] = sum over t of (topic_pos[t] * h_topic[h][t])
    # Since exactly one topic per historian, we can use:
    constraints = []
    for t in range(4):
        # If h_topic[h][t] is true, then historian_pos[h] == topic_pos[t]
        constraints.append(Implies(h_topic[h][t], historian_pos[h] == topic_pos[t]))
    solver.add(And(*constraints))

# Topic ordering constraints
# oil paintings < lithographs and watercolors < lithographs
solver.add(topic_pos[1] < topic_pos[0])  # oil < litho
solver.add(topic_pos[3] < topic_pos[0])  # water < litho

# Farley's lecture earlier than oil paintings
solver.add(historian_pos[0] < topic_pos[1])  # Farley < oil

# Holden's lecture earlier than both Garcia's and Jiang's
solver.add(historian_pos[2] < historian_pos[1])  # Holden < Garcia
solver.add(historian_pos[2] < historian_pos[3])  # Holden < Jiang

# Answer choices (negations to test for "must be true")
answer_choices = [
    # A. Farley < sculptures
    lambda: historian_pos[0] >= topic_pos[2],
    # B. Holden < lithographs
    lambda: historian_pos[2] >= topic_pos[0],
    # C. sculptures < Garcia
    lambda: topic_pos[2] >= historian_pos[1],
    # D. sculptures < Jiang
    lambda: topic_pos[2] >= historian_pos[3],
    # E. watercolors < Garcia
    lambda: topic_pos[3] >= historian_pos[1]
]

answer_index_list = []
for idx, negation in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add negation of the statement
    s_chk.add(negation())
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)