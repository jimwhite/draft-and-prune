from z3 import *

# Lab assistant indices: 0=Julio, 1=Kevin, 2=Lan, 3=Nessa, 4=Olivia, 5=Rebecca
# Session indices: 0=WM, 1=WA, 2=TM, 3=TA, 4=FM, 5=FA

assign = [Int(f"assign_{i}") for i in range(6)]

solver = Solver()

# Injectivity constraint
solver.add(Distinct(assign))

# Session-to-day/period helper (encoded using Z3 expressions)
def day(s):
    return s / 2

def period(s):
    return s % 2

# Fixed constraint: Julio leads Thursday afternoon (session index 3)
solver.add(assign[0] == 3)

# Kevin and Rebecca same day
solver.add(day(assign[1]) == day(assign[5]))

# Lan and Olivia different days
solver.add(day(assign[2]) != day(assign[4]))

# Nessa afternoon session
solver.add(period(assign[3]) == 1)

# Julio earlier day than Olivia
solver.add(day(assign[0]) < day(assign[4]))

# Check model and extract assignments
result = solver.check()
if result == sat:
    m = solver.model()
    # Extract assignments
    assignments = [m.eval(assign[i]).as_long() for i in range(6)]
    
    # Count how many of the other 5 assistants (excluding Julio) have determined sessions
    count = 0
    for i in range(1, 6):  # Kevin, Lan, Nessa, Olivia, Rebecca
        val = assignments[i]
        count += 1
    
    # But we need to verify which ones are uniquely determined
    # Let's check uniqueness by testing each assistant individually
    
    assistants = ["Julio", "Kevin", "Lan", "Nessa", "Olivia", "Rebecca"]
    other_assistants = [1, 2, 3, 4, 5]  # excluding Julio (index 0)
    
    determined_count = 0
    for i in other_assistants:
        s_chk = Solver()
        s_chk.add(solver.assertions())
        
        # Get the assignment for assistant i from original model
        s_chk.add(assign[i] == assignments[i])
        
        # Check if this assignment is forced (only one possibility)
        s_chk2 = Solver()
        s_chk2.add(solver.assertions())
        s_chk2.add(assign[i] != assignments[i])
        
        if s_chk2.check() == unsat:
            determined_count += 1
    
    print(determined_count)
else:
    print(0)