from z3 import *

birds = ["oystercatchers", "petrels", "rails", "sandpipers", "terns"]
locations = ["Gladwyn Hall", "Howard Auditorium"]
slots = [i for i in range(5)]

bird_at_slot = Array('bird_at_slot', IntSort(), IntSort())
location_at_slot = Array('location_at_slot', IntSort(), IntSort())

solver = Solver()

# Constraint 1: Distinct Birds
solver.add(Distinct([bird_at_slot[i] for i in slots]))

# Constraint 2: Location Domain
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 0, i < 5), And(location_at_slot[i] >= 0, location_at_slot[i] <= 1))))


# Constraint 3: First Lecture Location
solver.add(location_at_slot[0] == 0)

# Constraint 4: Fourth Lecture Location
solver.add(location_at_slot[3] == 1)

# Constraint 5: Three Lectures in Gladwyn
solver.add(Sum([If(location_at_slot[i] == 0, 1, 0) for i in slots]) == 3)

# Constraint 6: Sandpipers Location
i = Int('i')
solver.add(Exists(i, Implies(And(i >= 0, i < 5),And(bird_at_slot[i] == 3, location_at_slot[i] == 1))))

# Constraint 7: Sandpipers before Oystercatchers
i = Int('i')
j = Int('j')
solver.add(Exists([i, j], Implies(And(i >= 0, i < 5, j >= 0, j < 5), And(bird_at_slot[i] == 3, bird_at_slot[j] == 0, i < j))))

# Constraint 8: Terns before Petrels
i = Int('i')
j = Int('j')
solver.add(Exists([i, j], Implies(And(i >= 0, i < 5, j >= 0, j < 5),And(bird_at_slot[i] == 4, bird_at_slot[j] == 1, i < j))))

# Constraint 9: Petrels Location
i = Int('i')
solver.add(Exists(i, Implies(And(i >= 0, i < 5),And(bird_at_slot[i] == 1, location_at_slot[i] == 0))))

answer_choices = [
    "oystercatchers, petrels, rails, sandpipers, terns",
    "petrels, sandpipers, oystercatchers, terns, rails",
    "rails, sandpipers, terns, petrels, oystercatchers",
    "sandpipers, terns, oystercatchers, rails, petrels",
    "terns, petrels, sandpipers, oystercatchers, rails"
]

for option_index, choice in enumerate(answer_choices):
    solver.push()
    choice_birds = choice.split(', ')
    for slot_index, bird_name in enumerate(choice_birds):
        bird_index = birds.index(bird_name)
        solver.add(bird_at_slot[slot_index] == bird_index)
    if solver.check() == sat:
        print(f"Option {chr(65 + option_index)} is correct")
        exit()
    solver.pop()