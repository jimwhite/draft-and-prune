from z3 import *

# Lab assistants indices: Julio=0, Kevin=1, Lan=2, Nessa=3, Olivia=4, Rebecca=5
# Sessions: 0=(Wed,M), 1=(Wed,A), 2=(Thu,M), 3=(Thu,A), 4=(Fri,M), 5=(Fri,A)

# Session to (day, period) mapping using Z3 expressions
def get_day(session):
    return IntVal(0) if session < 2 else (IntVal(1) if session < 4 else IntVal(2))

def get_period(session):
    return If(session % 2 == 0, IntVal(0), IntVal(1))

# Create assignment variables: assign[i] = session index assigned to assistant i
assign = [Int(f"assign_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Injectivity constraint: each assistant leads exactly one session (permutation)
solver.add(Distinct(*assign))

# Domain constraints: each assistant assigned to a session 0-5
for i in range(6):
    solver.add(assign[i] >= 0, assign[i] <= 5)

# Kevin and Rebecca must lead sessions on the same day
solver.add(If(assign[1] < 2, IntVal(0), If(assign[1] < 4, IntVal(1), IntVal(2))) == 
           If(assign[5] < 2, IntVal(0), If(assign[5] < 4, IntVal(1), IntVal(2))))

# Lan and Olivia cannot lead sessions on the same day
solver.add(If(assign[2] < 2, IntVal(0), If(assign[2] < 4, IntVal(1), IntVal(2))) != 
           If(assign[4] < 2, IntVal(0), If(assign[4] < 4, IntVal(1), IntVal(2))))

# Nessa must lead an afternoon session (period = 1)
solver.add(assign[3] % 2 == 1)

# Julio's session must be on an earlier day than Olivia's
solver.add(If(assign[0] < 2, IntVal(0), If(assign[0] < 4, IntVal(1), IntVal(2))) < 
           If(assign[4] < 2, IntVal(0), If(assign[4] < 4, IntVal(1), IntVal(2))))

# Extra assumption: Lan does NOT lead a Wednesday session
solver.add(If(assign[2] < 2, IntVal(0), If(assign[2] < 4, IntVal(1), IntVal(2))) != 0)

# Answer choices indices: Rebecca=5, Olivia=4, Nessa=3, Kevin=1, Julio=0
answer_choices = [5, 4, 3, 1, 0]  # Rebecca, Olivia, Nessa, Kevin, Julio

# Check each answer choice
answer_index_list = []
for idx, assistant in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert that this assistant does NOT lead any Thursday session (day != 1)
    s_chk.add(If(assign[assistant] < 2, IntVal(0), If(assign[assistant] < 4, IntVal(1), IntVal(2))) != 1)
    
    # If UNSAT, this assistant must lead a Thursday session
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)