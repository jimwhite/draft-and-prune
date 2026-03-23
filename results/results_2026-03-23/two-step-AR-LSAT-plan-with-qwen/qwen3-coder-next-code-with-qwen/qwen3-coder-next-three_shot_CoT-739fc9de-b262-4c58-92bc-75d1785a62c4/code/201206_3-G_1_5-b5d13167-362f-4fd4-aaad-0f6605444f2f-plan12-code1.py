from z3 import *

# Lab assistants: Julio=0, Kevin=1, Lan=2, Nessa=3, Olivia=4, Rebecca=5
# Sessions: 0=Wed AM, 1=Wed PM, 2=Thu AM, 3=Thu PM, 4=Fri AM, 5=Fri PM

assistant = [Int(f"asst_{i}") for i in range(6)]  # assistant[i] = which assistant leads session i
session_of = [Int(f"sof_{j}") for j in range(6)]  # session_of[j] = which session assistant j leads

solver = Solver()

# Domain constraints
for i in range(6):
    solver.add(assistant[i] >= 0, assistant[i] <= 5)
for j in range(6):
    solver.add(session_of[j] >= 0, session_of[j] <= 5)

# Permutation constraints
solver.add(Distinct(assistant))
solver.add(Distinct(session_of))

# Inverse relationship: assistant[i] == j iff session_of[j] == i
for i in range(6):
    for j in range(6):
        solver.add(Implies(assistant[i] == j, session_of[j] == i))
        solver.add(Implies(session_of[j] == i, assistant[i] == j))

# Fixed constraint: Julio leads Thursday afternoon (session 3)
solver.add(session_of[0] == 3)

# Kevin and Rebecca must lead sessions on the same day
solver.add(If(session_of[1] <= 1, 0, If(session_of[1] <= 3, 1, 2)) == 
           If(session_of[5] <= 1, 0, If(session_of[5] <= 3, 1, 2)))

# Lan and Olivia cannot lead sessions on the same day
solver.add(If(session_of[2] <= 1, 0, If(session_of[2] <= 3, 1, 2)) != 
           If(session_of[4] <= 1, 0, If(session_of[4] <= 3, 1, 2)))

# Nessa must lead an afternoon session
solver.add(session_of[3] % 2 == 1)

# Julio's session must be earlier day than Olivia's
solver.add(If(session_of[0] <= 1, 0, If(session_of[0] <= 3, 1, 2)) < 
           If(session_of[4] <= 1, 0, If(session_of[4] <= 3, 1, 2)))

# Check how many assistants (excluding Julio) have uniquely determined sessions
count = 0

for j in range(1, 6):  # assistants Kevin (1) through Rebecca (5)
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Try to find two different models where session_of[j] differs
    s1 = Solver()
    s1.add(solver.assertions())
    
    # Get a model
    if s1.check() == sat:
        m = s1.model()
        val1 = m.eval(session_of[j]).as_long()
        
        # Try to find another model with different value
        s2 = Solver()
        s2.add(solver.assertions())
        s2.add(session_of[j] != val1)
        
        if s2.check() == unsat:
            count += 1

print(count)