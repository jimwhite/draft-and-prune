from z3 import *

# Bird types: Oystercatchers (O), Petrels (P), Rails (R), Sandpipers (S), Terns (T)
birds = ["O", "P", "R", "S", "T"]

# Slot variables: slot[bird] = position (1-5) of the lecture for that bird
slot = {b: Int(f"slot_{b}") for b in birds}

# Venue variables: venue[i] = True means Gladwyn Hall, False means Howard Auditorium (for slot i+1)
venue = [Bool(f"venue_{i}") for i in range(5)]

# Helper function to get venue at slot position (1-indexed)
def get_venue_at_slot(bird):
    s = slot[bird]
    return If(And(s >= 1, s <= 5), 
              If(s == 1, venue[0],
                 If(s == 2, venue[1],
                    If(s == 3, venue[2],
                       If(s == 4, venue[3], venue[4])))),
              False)

# Base solver
solver = Solver()

# Domain constraints: each slot is between 1 and 5, all distinct
for b in birds:
    solver.add(slot[b] >= 1, slot[b] <= 5)
solver.add(Distinct(*[slot[b] for b in birds]))

# Fixed venue constraints
solver.add(venue[0] == True)  # First lecture in Gladwyn Hall (slot 1)
solver.add(venue[3] == False) # Fourth lecture in Howard Auditorium (slot 4)

# Exactly three Gladwyn Hall lectures
solver.add(Sum([If(venue[i], 1, 0) for i in range(5)]) == 3)

# Sandpiper constraints
solver.add(get_venue_at_slot("S") == False)  # S in Howard Auditorium
solver.add(slot["S"] < slot["O"])          # S earlier than O

# Tern/petrel constraints
solver.add(slot["T"] < slot["P"])          # T earlier than P
solver.add(get_venue_at_slot("P") == True)   # P in Gladwyn Hall

# Answer choices (as conditions on venue slots)
answer_conditions = [
    And(venue[0], venue[1]),               # A: 1st and 2nd in Gladwyn
    And(Not(venue[1]), Not(venue[2])),     # B: 2nd and 3rd in Howard
    And(venue[1], venue[4]),               # C: 2nd and 5th in Gladwyn
    And(Not(venue[2]), Not(venue[3])),     # D: 3rd and 4th in Howard
    And(venue[2], venue[4])                # E: 3rd and 5th in Gladwyn
]

# Check each answer choice to see if it must be false
must_be_false_index_list = []
for idx, cond in enumerate(answer_conditions):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(cond)
    
    if s_chk.check() == unsat:
        must_be_false_index_list.append(idx)

print(must_be_false_index_list)