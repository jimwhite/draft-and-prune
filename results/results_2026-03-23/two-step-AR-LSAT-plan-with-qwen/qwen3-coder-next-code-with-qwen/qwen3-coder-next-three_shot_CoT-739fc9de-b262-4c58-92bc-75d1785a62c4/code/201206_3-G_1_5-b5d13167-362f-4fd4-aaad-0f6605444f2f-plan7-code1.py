from z3 import *

# Lab assistants: 0=Julio, 1=Kevin, 2=Lan, 3=Nessa, 4=Olivia, 5=Rebecca
# Sessions: 0-5 representing (Day, Time): Day in {0=Wed,1=Thu,2=Fri}, Time in {0=Morn,1=After}
# Session index = Day*2 + Time

assign = [Int(f"assign_{i}") for i in range(6)]

solver = Solver()

# Injectivity: all assignments distinct
solver.add(Distinct(*assign))

# Domain constraints: each assignment between 0 and 5
for i in range(6):
    solver.add(assign[i] >= 0, assign[i] <= 5)

# Fixed constraint: Julio leads Thursday afternoon (session index 3)
solver.add(assign[0] == 3)

# Kevin and Rebecca same day: Day(s) = s // 2
solver.add(assign[1]//2 == assign[5]//2)

# Lan and Olivia different day
solver.add(assign[2]//2 != assign[4]//2)

# Nessa afternoon: session index % 2 == 1
solver.add(assign[3]%2 == 1)

# Julio earlier day than Olivia: Day(3) = 1, so Day(assign[4]) > 1 → assign[4] >= 4
solver.add(assign[4] >= 4)

# Count how many of the other assistants (1-5) have uniquely determined sessions
determined_count = 0

for j in range(1, 6):
    # Get all possible values for assign[j]
    s = Solver()
    s.add(solver.assertions())
    
    # Collect all possible values for assign[j]
    values = set()
    while s.check() == sat:
        m = s.model()
        val = m[assign[j]].as_long()
        values.add(val)
        
        # Block this assignment for assign[j] to find other possibilities
        s.add(assign[j] != val)
    
    # If only one possible value, then determined
    if len(values) == 1:
        determined_count += 1

# Map count to answer string
answers = ['one', 'two', 'three', 'four', 'five']
print(answers[determined_count])