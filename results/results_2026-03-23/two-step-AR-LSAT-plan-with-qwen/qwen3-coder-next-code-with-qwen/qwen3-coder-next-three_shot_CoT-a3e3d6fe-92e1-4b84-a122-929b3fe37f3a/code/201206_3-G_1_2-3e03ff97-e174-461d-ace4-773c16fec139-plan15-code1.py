from z3 import *

# Lab assistants: Julio=0, Kevin=1, Lan=2, Nessa=3, Olivia=4, Rebecca=5
# Sessions: 0-Wed morning, 1-Wed afternoon, 2-Thu morning, 3-Thu afternoon, 4-Fri morning, 5-Fri afternoon
# day[i] = i // 2 (0=Wed, 1=Thu, 2=Fri)

# Create position variables for each assistant
pos = [Int(f"pos_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: each position between 0 and 5, all distinct
for i in range(6):
    solver.add(pos[i] >= 0, pos[i] <= 5)
solver.add(Distinct(*pos))

# Helper: day of session i is i // 2 (Z3-compatible version)
def get_day(session_idx):
    return If(Or(session_idx == 0, session_idx == 1), 0,
              If(Or(session_idx == 2, session_idx == 3), 1, 2))

# Kevin and Rebecca must lead sessions on the same day
solver.add(get_day(pos[1]) == get_day(pos[5]))

# Lan and Olivia cannot lead sessions on the same day
solver.add(get_day(pos[2]) != get_day(pos[4]))

# Nessa must lead an afternoon session (sessions 1, 3, 5)
solver.add(Or(pos[3] == 1, pos[3] == 3, pos[3] == 5))

# Julio's session must be earlier than Olivia's (chronological order)
solver.add(pos[0] < pos[4])

# Additional constraint: Lan does NOT lead a Wednesday session (days 0)
solver.add(get_day(pos[2]) != 0)

# Answer choices: Rebecca=5, Olivia=4, Nessa=3, Kevin=1, Julio=0
answer_choices = [5, 4, 3, 1, 0]

# Check which assistants must lead a Thursday session
must_thu_list = []
for idx, assistant in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint: assistant does NOT lead any Thursday session (sessions 2 and 3)
    s_chk.add(pos[assistant] != 2, pos[assistant] != 3)
    
    # If UNSAT, this assistant must lead a Thursday session
    if s_chk.check() == unsat:
        must_thu_list.append(assistant)

# Output the assistant name corresponding to the index
# Map indices back to names: 0=Julio, 1=Kevin, 2=Lan, 3=Nessa, 4=Olivia, 5=Rebecca
assistant_names = ["Julio", "Kevin", "Lan", "Nessa", "Olivia", "Rebecca"]
print(assistant_names[must_thu_list[0]] if must_thu_list else "")