from z3 import *

# Bird types: 0-oystercatchers, 1-petrels, 2-rails, 3-sandpipers, 4-terns
birds = ["oystercatchers", "petrels", "rails", "sandpipers", "terns"]
bird_indices = range(5)

# Position variables: position[bird] = lecture position (1-5)
position = {b: Int(f"pos_{b}") for b in birds}

# Venue variables: venue[bird] = True if Gladwyn Hall, False if Howard Auditorium
venue = {b: Bool(f"venue_{b}") for b in birds}

# Base solver
solver = Solver()

# Domain constraints: positions are distinct integers from 1 to 5
for b in birds:
    solver.add(position[b] >= 1, position[b] <= 5)
solver.add(Distinct(*[position[b] for b in birds]))

# Fixed venue constraints
# First lecture is in Gladwyn Hall (venue = True)
solver.add(Or([And(position[b] == 1, venue[b]) for b in birds]))

# Fourth lecture is in Howard Auditorium (venue = False)
solver.add(Or([And(position[b] == 4, Not(venue[b])) for b in birds]))

# Exactly three lectures in Gladwyn Hall
solver.add(Sum([If(venue[b], 1, 0) for b in birds]) == 3)

# Sandpipers constraints
solver.add(Not(venue["sandpipers"]))  # Howard Auditorium
solver.add(position["sandpipers"] < position["oystercatchers"])

# Terns and petrels constraints
solver.add(position["terns"] < position["petrels"])
solver.add(venue["petrels"])  # Gladwyn Hall

# Answer choices: each is a conjunction of venue constraints for specific positions
answer_choices = [
    # 0: first and second lectures both in Gladwyn Hall
    lambda pos, venue: And(
        Or([And(pos[b] == 1, venue[b]) for b in birds]),
        Or([And(pos[b] == 2, venue[b]) for b in birds])
    ),
    # 1: second and third lectures both in Howard Auditorium
    lambda pos, venue: And(
        Or([And(pos[b] == 2, Not(venue[b])) for b in birds]),
        Or([And(pos[b] == 3, Not(venue[b])) for b in birds])
    ),
    # 2: second and fifth lectures both in Gladwyn Hall
    lambda pos, venue: And(
        Or([And(pos[b] == 2, venue[b]) for b in birds]),
        Or([And(pos[b] == 5, venue[b]) for b in birds])
    ),
    # 3: third and fourth lectures both in Howard Auditorium
    lambda pos, venue: And(
        Or([And(pos[b] == 3, Not(venue[b])) for b in birds]),
        Or([And(pos[b] == 4, Not(venue[b])) for b in birds])
    ),
    # 4: third and fifth lectures both in Gladwyn Hall
    lambda pos, venue: And(
        Or([And(pos[b] == 3, venue[b]) for b in birds]),
        Or([And(pos[b] == 5, venue[b]) for b in birds])
    )
]

# Check each answer choice
answer_index_list = []
for idx, choice_func in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add the venue constraints for this choice
    s_chk.add(choice_func(position, venue))
    
    # If UNSAT, this choice must be false
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)