from z3 import *

# Lab assistants indices: Julio=0, Kevin=1, Lan=2, Nessa=3, Olivia=4, Rebecca=5
assistants = ["Julio", "Kevin", "Lan", "Nessa", "Olivia", "Rebecca"]
assistant_indices = {name: idx for idx, name in enumerate(assistants)}

# Sessions: 0=W-morning, 1=W-afternoon, 2=Th-morning, 3=Th-afternoon, 4=F-morning, 5=F-afternoon
# day = session_index // 2, time = session_index % 2

assign = [Int(f"assign_{i}") for i in range(6)]

solver = Solver()

# Domain constraints: each session assigned to one of the 6 assistants
for i in range(6):
    solver.add(assign[i] >= 0, assign[i] <= 5)

# All-different constraint: each assistant leads exactly one session
solver.add(Distinct(assign))

# Kevin and Rebecca same day constraint
def get_day(session_idx):
    return session_idx // 2

# Find indices where Kevin and Rebecca are assigned
k_pos = [If(assign[i] == assistant_indices["Kevin"], i, -1) for i in range(6)]
r_pos = [If(assign[i] == assistant_indices["Rebecca"], i, -1) for i in range(6)]

# Kevin's session index is the one where assign[i] == Kevin_idx
k_session = Int("k_session")
r_session = Int("r_session")

# Add constraints to link k_session and r_session with assignments
solver.add(Or([And(assign[i] == assistant_indices["Kevin"], k_session == i) for i in range(6)]))
solver.add(Or([And(assign[i] == assistant_indices["Rebecca"], r_session == i) for i in range(6)]))

# Same day constraint: k_session // 2 == r_session // 2
solver.add(k_session / 2 == r_session / 2)

# Lan and Olivia not same day constraint
l_pos = Int("l_session")
o_pos = Int("o_session")

solver.add(Or([And(assign[i] == assistant_indices["Lan"], l_pos == i) for i in range(6)]))
solver.add(Or([And(assign[i] == assistant_indices["Olivia"], o_pos == i) for i in range(6)]))
solver.add(l_pos / 2 != o_pos / 2)

# Nessa must lead an afternoon session (session indices 1, 3, 5)
solver.add(Or(
    assign[1] == assistant_indices["Nessa"],
    assign[3] == assistant_indices["Nessa"],
    assign[5] == assistant_indices["Nessa"]
))

# Julio's session earlier than Olivia's
j_pos = Int("j_session")
solver.add(Or([And(assign[i] == assistant_indices["Julio"], j_pos == i) for i in range(6)]))
solver.add(j_pos < o_pos)

# Additional premise: Lan does not lead a Wednesday session (sessions 0,1)
solver.add(l_pos != 0)
solver.add(l_pos != 1)

# Answer choices: ['Rebecca', 'Olivia', 'Nessa', 'Kevin', 'Julio']
answer_choices = ["Rebecca", "Olivia", "Nessa", "Kevin", "Julio"]
answer_indices = [assistant_indices[name] for name in answer_choices]

# Check which assistants must lead a Thursday session (sessions 2,3)
answer_index_list = []
thursday_sessions = [2, 3]

for idx, assistant_idx in enumerate(answer_indices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint that this assistant does NOT lead any Thursday session
    for s in thursday_sessions:
        s_chk.add(assign[s] != assistant_idx)
    
    # If UNSAT, this assistant must lead a Thursday session
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)