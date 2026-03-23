from z3 import *

# Lab assistants indices: Julio=0, Kevin=1, Lan=2, Nessa=3, Olivia=4, Rebecca=5
assistants = ["Julio", "Kevin", "Lan", "Nessa", "Olivia", "Rebecca"]

# Session positions: 0=WM, 1=WA, 2=TM, 3=TA, 4=FM, 5=FA
pos = [Int(f"pos_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: all positions distinct and in [0,5]
solver.add(Distinct(pos))
for i in range(6):
    solver.add(pos[i] >= 0, pos[i] <= 5)

# Fixed assignment: Julio leads Thursday afternoon (position 3)
solver.add(pos[0] == 3)

# Same-day constraint for Kevin and Rebecca
def day(p):
    return IntVal(p // 2) if isinstance(p, int) else p / 2

solver.add(day(pos[1]) == day(pos[5]))

# Different-day constraint for Lan and Olivia
solver.add(day(pos[2]) != day(pos[4]))

# Nessa must lead an afternoon session (odd positions: 1,3,5)
solver.add(pos[3] % 2 == 1)

# Julio's session must be earlier than Olivia's
solver.add(pos[0] < pos[4])

# Check uniqueness for each of the other assistants (Kevin, Lan, Nessa, Olivia, Rebecca)
determined_count = 0

for i in [1, 2, 3, 4, 5]:  # Kevin, Lan, Nessa, Olivia, Rebecca
    s = Solver()
    s.add(solver.assertions())
    
    # Collect all possible values for pos[i]
    solutions = []
    while s.check() == sat:
        m = s.model()
        val = m.eval(pos[i]).as_long()
        solutions.append(val)
        # Add constraint to exclude this value for next iteration
        s.add(pos[i] != val)
    
    # If only one possible value, then it's determined
    if len(solutions) == 1:
        determined_count += 1

# Map count to answer string
answers = ['one', 'two', 'three', 'four', 'five']
print(answers[determined_count])