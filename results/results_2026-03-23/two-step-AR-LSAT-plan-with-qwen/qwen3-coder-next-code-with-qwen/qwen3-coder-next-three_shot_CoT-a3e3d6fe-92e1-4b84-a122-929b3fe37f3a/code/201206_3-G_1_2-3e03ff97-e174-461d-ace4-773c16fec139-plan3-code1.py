from z3 import *

# Lab assistants indices: Julio=0, Kevin=1, Nessa=2, Olivia=3, Rebecca=4, Lan=5
assistants = ["Julio", "Kevin", "Nessa", "Olivia", "Rebecca", "Lan"]
assistant_indices = {name: i for i, name in enumerate(assistants)}

# Session positions: 0-5 (Wed morning=0, Wed afternoon=1, Thu morning=2, Thu afternoon=3, Fri morning=4, Fri afternoon=5)
pos = [Int(f"pos_{name}") for name in assistants]

# Base solver
solver = Solver()

# Domain constraints: all positions distinct and in [0,5]
solver.add(Distinct(pos))
for i in range(6):
    solver.add(pos[i] >= 0, pos[i] <= 5)

# Helper function for day: Wed=0 (positions 0,1), Thu=1 (positions 2,3), Fri=2 (positions 4,5)
def day(p):
    return If(p <= 1, 0, If(p <= 3, 1, 2))

# Constraint 1: Kevin and Rebecca must lead sessions on the same day
solver.add(day(pos[assistant_indices["Kevin"]]) == day(pos[assistant_indices["Rebecca"]]))

# Constraint 2: Lan and Olivia cannot lead sessions on the same day
solver.add(day(pos[assistant_indices["Lan"]]) != day(pos[assistant_indices["Olivia"]]))

# Constraint 3: Nessa must lead an afternoon session (positions 1, 3, or 5)
solver.add(Or(pos[assistant_indices["Nessa"]] == 1,
              pos[assistant_indices["Nessa"]] == 3,
              pos[assistant_indices["Nessa"]] == 5))

# Constraint 4: Julio's session must be earlier than Olivia's
solver.add(pos[assistant_indices["Julio"]] < pos[assistant_indices["Olivia"]])

# Assumed condition: Lan does NOT lead a Wednesday session (day != 0)
solver.add(day(pos[assistant_indices["Lan"]]) != 0)

# Answer choices indices: Rebecca=4, Olivia=3, Nessa=2, Kevin=1, Julio=0
answer_choices = [4, 3, 2, 1, 0]  # Rebecca, Olivia, Nessa, Kevin, Julio

# Check each answer choice
must_thursday_list = []
for idx in answer_choices:
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assume assistant idx does NOT lead any Thursday session (positions 2 or 3)
    s_chk.add(And(pos[idx] != 2, pos[idx] != 3))
    
    # If UNSAT, then assistant idx MUST lead a Thursday session
    if s_chk.check() == unsat:
        must_thursday_list.append(idx)

print(must_thursday_list)