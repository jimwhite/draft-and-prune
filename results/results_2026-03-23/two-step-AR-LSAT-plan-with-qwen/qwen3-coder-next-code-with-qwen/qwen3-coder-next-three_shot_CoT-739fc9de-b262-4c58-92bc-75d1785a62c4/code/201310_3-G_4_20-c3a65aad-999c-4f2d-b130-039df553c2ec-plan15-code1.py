from z3 import *

# Bird types: 0-oystercatchers, 1-petrels, 2-rails, 3-sandpipers, 4-terns
birds = ["oystercatchers", "petrels", "rails", "sandpipers", "terns"]

# Hall assignment variables: hall[i] = True if lecture i (1-indexed) is in Gladwyn Hall
hall = [Bool(f"hall_{i}") for i in range(1, 6)]

# Position variables: pos_bird = lecture position (1-5) for each bird type
pos = {bird: Int(f"pos_{bird}") for bird in birds}

# Helper function to get hall variable at position p (1-indexed)
def hall_at(p):
    return If(p == 1, hall[0],
           If(p == 2, hall[1],
           If(p == 3, hall[2],
           If(p == 4, hall[3],
           If(p == 5, hall[4], BoolVal(False))))))

# Base solver
solver = Solver()

# Global constraints
## First lecture is in Gladwyn Hall (position 1)
solver.add(hall[0] == True)
## Fourth lecture is in Howard Auditorium (position 4)
solver.add(hall[3] == False)
## Exactly three lectures are in Gladwyn Hall
solver.add(Sum([If(hall[i], 1, 0) for i in range(5)]) == 3)

# Position constraints
## Each bird position between 1 and 5
for bird in birds:
    solver.add(pos[bird] >= 1, pos[bird] <= 5)
## All positions distinct
solver.add(Distinct(*[pos[bird] for bird in birds]))

# Location ordering constraints
## Sandpipers lecture is in Howard Auditorium and earlier than oystercatchers
solver.add(hall_at(pos["sandpipers"]) == False)
solver.add(pos["sandpipers"] < pos["oystercatchers"])

## Terns lecture is earlier than petrels, and petrels lecture is in Gladwyn Hall
solver.add(pos["terns"] < pos["petrels"])
solver.add(hall_at(pos["petrels"]) == True)

# Answer choices (0-indexed)
answer_choices = [
    # Choice 0: First and second lectures are both in Gladwyn Hall
    And(hall[0] == True, hall[1] == True),
    # Choice 1: Second and third lectures are both in Howard Auditorium
    And(hall[1] == False, hall[2] == False),
    # Choice 2: Second and fifth lectures are both in Gladwyn Hall
    And(hall[1] == True, hall[4] == True),
    # Choice 3: Third and fourth lectures are both in Howard Auditorium
    And(hall[2] == False, hall[3] == False),
    # Choice 4: Third and fifth lectures are both in Gladwyn Hall
    And(hall[2] == True, hall[4] == True)
]

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add the choice condition
    s_chk.add(choice)
    
    # If UNSAT, this choice must be false
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)