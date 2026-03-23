from z3 import *

# Lab assistants: Julio=0, Kevin=1, Lan=2, Nessa=3, Olivia=4, Rebecca=5
# Sessions: Wed AM=0, Wed PM=1, Thu AM=2, Thu PM=3, Fri AM=4, Fri PM=5

pos = [Int(f"pos_{i}") for i in range(6)]

solver = Solver()

# All positions distinct
solver.add(Distinct(pos))

# Each position between 0 and 5
for i in range(6):
    solver.add(pos[i] >= 0, pos[i] <= 5)

# Helper functions for day and time using Z3 constructs
def is_afternoon(session):
    return session % 2 == 1

def day_of(session):
    # Use Z3's IntDiv for division with integer constraints
    return IntVal(0) if False else (session - (session % 2)) // 2
    # Alternatively, use Z3's built-in division: (session - (session % 2)) / 2
    # But better to use explicit Z3 operations:
    # return (session - (session % 2)) // 2 works in Python but not for Z3 expressions
    # Correct approach: use (session // 2) is not valid, so we define it as:
    # day = session / 2 (integer division) is equivalent to floor(session/2)
    # In Z3, we can use: (session - (session % 2)) / 2
    # But since Z3 IntDiv is available, we can use:
    # return Int('tmp') but better to avoid helper functions for complex expressions
    # Instead, we'll inline the day calculation using Z3 operations

# Redefine without helper functions to avoid type issues
# For day_of: session // 2, but for Z3 Int expressions we use:
# day = (session - (session % 2)) / 2, but division in Z3 is tricky
# Actually, we can use: (session / 2) if session is even, but better to use:
# day = Int('d') and add constraints, but for simplicity we'll inline

# Fixed condition: Julio leads Thursday PM → pos[0] == 3
solver.add(pos[0] == 3)

# Kevin and Rebecca must lead sessions on the same day
# Day = session // 2, so we need: (pos[1] - pos[1]%2)/2 == (pos[5] - pos[5]%2)/2
# But modulo is expensive; instead, note that same day means:
# (pos[1] // 2) == (pos[5] // 2)
# In Z3, we can express this as: 
# pos[1] >= 2*d and pos[1] < 2*d+2 and same for pos[5], but simpler:
# Use: (pos[1] - pos[5]) % 2 == 0 and min(pos[1],pos[5]) >= max(pos[1],pos[5])//2*2 ... too complex
# Better: use the fact that day = (session - session%2)/2, but Z3 doesn't have // for IntRef
# Solution: define day variables explicitly

# Let's use a cleaner approach with explicit day variables
day = [Int(f"day_{i}") for i in range(6)]
for i in range(6):
    solver.add(day[i] == pos[i] / 2)  # Z3's Int division is floor division for non-negative

solver.add(day[1] == day[5])

# Lan and Olivia cannot lead sessions on the same day
solver.add(day[2] != day[4])

# Nessa must lead an afternoon session: pos[3] % 2 == 1
solver.add(pos[3] % 2 == 1)

# Julio's session earlier than Olivia's
solver.add(pos[0] < pos[4])

# Check consistency and extract assignments
if solver.check() == sat:
    m = solver.model()
    assignments = [m.evaluate(pos[i]).as_long() for i in range(6)]
    
    # Determine which assistants (excluding Julio) have uniquely determined sessions
    determined_count = 0
    
    # Check each assistant individually (1-5)
    for i in range(1, 6):
        s_alt = Solver()
        s_alt.add(solver.assertions())
        current_val = m.evaluate(pos[i]).as_long()
        s_alt.add(pos[i] != current_val)
        
        if s_alt.check() == unsat:
            determined_count += 1
    
    # Print the count
    print(determined_count)
else:
    print("No solution")