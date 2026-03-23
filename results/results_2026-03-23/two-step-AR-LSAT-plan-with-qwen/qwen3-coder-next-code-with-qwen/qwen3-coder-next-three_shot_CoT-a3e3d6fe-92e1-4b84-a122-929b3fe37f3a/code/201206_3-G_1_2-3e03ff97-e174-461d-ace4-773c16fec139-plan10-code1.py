from z3 import *

# Lab assistants indices: Julio=0, Kevin=1, Lan=2, Nessa=3, Olivia=4, Rebecca=5
assistants = ["Julio", "Kevin", "Lan", "Nessa", "Olivia", "Rebecca"]
assistant_indices = {name: idx for idx, name in enumerate(assistants)}

# Sessions: 0=WedAM, 1=WedPM, 2=ThuAM, 3=ThuPM, 4=FriAM, 5=FriPM
# Session to day mapping: day[i] = i//2 (0=Wed, 1=Thu, 2=Fri)
session_to_day = [i//2 for i in range(6)]

# Create assignment variables: assign[i] = assistant index assigned to session i
assign = [Int(f"assign_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Each session gets exactly one assistant, all assistants used exactly once
solver.add(Distinct(*assign))
for i in range(6):
    solver.add(And(assign[i] >= 0, assign[i] <= 5))

# Nessa must lead an afternoon session (sessions 1, 3, 5)
solver.add(Or(*[assign[i] == assistant_indices["Nessa"] for i in [1, 3, 5]]))

# Kevin and Rebecca must lead sessions on the same day
# Create helper variables for session indices of each assistant
session_of = [Int(f"session_of_{a}") for a in range(6)]
for i in range(6):
    solver.add(ForAll([Int("a")], Implies(assign[i] == IntVal(i), False)))  # placeholder, will fix below
for a in range(6):
    solver.add(session_of[a] >= 0, session_of[a] <= 5)

# Enforce session_of relationship: session_of[a] = i iff assign[i] = a
for i in range(6):
    for a in range(6):
        solver.add(Implies(assign[i] == a, session_of[a] == i))
        solver.add(Implies(session_of[a] == i, assign[i] == a))

# Kevin and Rebecca same day constraint
solver.add(session_to_day[session_of[assistant_indices["Kevin"]]] == 
           session_to_day[session_of[assistant_indices["Rebecca"]]])

# Lan and Olivia cannot lead sessions on the same day
solver.add(session_to_day[session_of[assistant_indices["Lan"]]] != 
           session_to_day[session_of[assistant_indices["Olivia"]]])

# Nessa afternoon constraint (redundant with above but explicit)
solver.add(Or(*[session_of[assistant_indices["Nessa"]] == i for i in [1, 3, 5]]))

# Julio's session day < Olivia's session day
solver.add(session_to_day[session_of[assistant_indices["Julio"]]] < 
           session_to_day[session_of[assistant_indices["Olivia"]]])

# Lan does NOT lead a Wednesday session (sessions 0,1)
solver.add(And(*[assign[i] != assistant_indices["Lan"] for i in [0, 1]]))

# Answer choices: ['Rebecca', 'Olivia', 'Nessa', 'Kevin', 'Julio']
answer_choices = ["Rebecca", "Olivia", "Nessa", "Kevin", "Julio"]
answer_indices = [assistant_indices[name] for name in answer_choices]

# Check which assistants MUST be in Thursday (sessions 2 or 3)
answer_index_list = []

for idx, a_idx in enumerate(answer_indices):
    # Check if assistant a_idx can be assigned to Wed (0,1) or Fri (4,5)
    # If all non-Thursday positions are UNSAT, then a_idx must be in Thursday
    
    can_be_wed = False
    can_be_fri = False
    
    # Check Wed positions (0,1)
    for pos in [0, 1]:
        s_chk = Solver()
        s_chk.add(solver.assertions())
        s_chk.add(session_of[a_idx] == pos)
        if s_chk.check() == sat:
            can_be_wed = True
            break
    
    # Check Fri positions (4,5)
    for pos in [4, 5]:
        s_chk = Solver()
        s_chk.add(solver.assertions())
        s_chk.add(session_of[a_idx] == pos)
        if s_chk.check() == sat:
            can_be_fri = True
            break
    
    # If cannot be in Wed or Fri, must be in Thu
    if not can_be_wed and not can_be_fri:
        answer_index_list.append(idx)

print(answer_index_list)