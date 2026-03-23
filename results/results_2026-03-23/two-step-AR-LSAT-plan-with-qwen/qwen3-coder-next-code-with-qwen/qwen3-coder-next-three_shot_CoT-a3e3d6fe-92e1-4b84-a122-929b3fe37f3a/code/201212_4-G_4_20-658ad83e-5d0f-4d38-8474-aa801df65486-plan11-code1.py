from z3 import *

# Article indices: G=0, H=1, J=2, Q=3, R=4, S=5, Y=6
articles = ["G", "H", "J", "Q", "R", "S", "Y"]
pos = [Int(f"pos_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: positions 1-7, all distinct
for i in range(7):
    solver.add(pos[i] >= 1, pos[i] <= 7)
solver.add(Distinct(pos))

# Topic mapping: finance={0,1,2}, nutrition={3,4,5}, wildlife={6}
def topic(i):
    if i <= 2:  # G, H, J
        return 0  # finance
    elif i <= 5:  # Q, R, S
        return 1  # nutrition
    else:  # Y
        return 2  # wildlife

# No consecutive same topic constraint
for i in range(7):
    for j in range(7):
        if i != j:
            # If articles i and j are consecutive, their topics must differ
            solver.add(Implies(Abs(pos[i] - pos[j]) == 1, topic(i) != topic(j)))

# S can be earlier than Q only if Q is third: (pos[S] < pos[Q]) → (pos[Q] == 3)
solver.add(Implies(pos[5] < pos[3], pos[3] == 3))

# S must be earlier than Y: pos[S] < pos[Y]
solver.add(pos[5] < pos[6])

# J must be earlier than G, and G must be earlier than R: pos[J] < pos[G] < pos[R]
solver.add(pos[2] < pos[0], pos[0] < pos[4])

# Answer choices: G is second (i=0), H is second (i=1), S is second (i=5), R is third (i=4), Y is third (i=6)
# Note: The question asks "which one could be true", and the choices are phrased as "X is [position]"
# We check for each choice whether it's possible (SAT)
answer_index_list = []
choice_articles = [0, 1, 5, 4, 6]  # G, H, S, R, Y
positions = [2, 2, 2, 3, 3]  # second for first three, third for last two

for idx in range(5):
    i = choice_articles[idx]
    p = positions[idx]
    
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(pos[i] == p)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)