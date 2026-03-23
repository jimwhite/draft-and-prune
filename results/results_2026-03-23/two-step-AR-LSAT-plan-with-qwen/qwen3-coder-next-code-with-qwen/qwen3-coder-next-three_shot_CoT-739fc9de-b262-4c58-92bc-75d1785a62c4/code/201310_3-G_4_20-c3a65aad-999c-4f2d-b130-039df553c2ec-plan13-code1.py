from z3 import *

# Bird indices: 0-OC, 1-P, 2-R, 3-S, 4-T
(OC, P, R, S, T) = range(5)

# Position variables: bird_pos[i] = position (1-5) where bird i is lectureed
bird_pos = [Int(f"bird_{i}") for i in range(5)]

# Hall variables: hall[j] = 0 (Gladwyn) or 1 (Howard) for position j+1
hall = [Int(f"hall_{j}") for j in range(5)]

# Base solver
solver = Solver()

# Permutation constraint: all bird positions distinct and cover 1-5
solver.add(Distinct(bird_pos))
for i in range(5):
    solver.add(bird_pos[i] >= 1, bird_pos[i] <= 5)

# Hall assignment: each hall position is 0 or 1
for j in range(5):
    solver.add(Or(hall[j] == 0, hall[j] == 1))

# Exactly three Gladwyn (hall=0), two Howard (hall=1)
solver.add(Sum([If(hall[j] == 0, 1, 0) for j in range(5)]) == 3)

# Fixed hall constraints
solver.add(hall[0] == 0)  # first lecture in Gladwyn
solver.add(hall[3] == 1)  # fourth lecture in Howard

# Sandpipers constraint: S in Howard, and earlier than OC
solver.add(hall[S] == 1)
solver.add(bird_pos[S] < bird_pos[OC])

# Terns/petrels/Gladwyn constraints
solver.add(bird_pos[T] < bird_pos[P])
solver.add(hall[P] == 0)  # petrels in Gladwyn

# Answer choices: convert to hall constraints
answer_choices = [
    (0, 1),  # first and second lectures in Gladwyn: hall[0]==0 and hall[1]==0
    (1, 2),  # second and third lectures in Howard: hall[1]==1 and hall[2]==1
    (0, 4),  # second and fifth lectures in Gladwyn: hall[1]==0 and hall[4]==0
    (2, 3),  # third and fourth lectures in Howard: hall[2]==1 and hall[3]==1
    (0, 4)   # third and fifth lectures in Gladwyn: hall[2]==0 and hall[4]==0
]

# Check each answer choice
answer_index_list = []
for idx, (pos1, pos2) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint for the answer choice
    s_chk.add(hall[pos1] == 0, hall[pos2] == 0)
    
    # If UNSAT, this choice must be false
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)