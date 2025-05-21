from z3 import *

# Define singers and slots
singers = ["Kammer", "Lugo", "Trillo", "Waite", "Yoshida", "Zinn"]
singer_ids = {s: i for i, s in enumerate(singers)}
num_slots = 6

# Define Z3 variables
audition_order = Array('audition_order', IntSort(), IntSort())
singer_slot = Array('singer_slot', IntSort(), IntSort())
recorded = Array('recorded', IntSort(), BoolSort())

solver = Solver()

# Permutation and Inverse Mapping Constraints
solver.add(Distinct([audition_order[i] for i in range(num_slots)]))
solver.add(And([And(audition_order[i] >= 0, audition_order[i] < num_slots) for i in range(num_slots)]))
solver.add(Distinct([singer_slot[i] for i in range(num_slots)]))
solver.add(And([And(singer_slot[i] >= 0, singer_slot[i] < num_slots) for i in range(num_slots)]))

for i in range(num_slots):
    solver.add(singer_slot[audition_order[i]] == i)
    solver.add(audition_order[singer_slot[i]] == i)

# Recorded Status Definition
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 0, i < num_slots), recorded[i] == Or(audition_order[i] == singer_ids["Kammer"], audition_order[i] == singer_ids["Lugo"]))))

# Specific Slot Constraints
solver.add(Not(recorded[3]))
solver.add(recorded[4])

# Relative Order Constraints
solver.add(singer_slot[singer_ids["Waite"]] < singer_slot[singer_ids["Kammer"]])
solver.add(singer_slot[singer_ids["Waite"]] < singer_slot[singer_ids["Lugo"]])
solver.add(singer_slot[singer_ids["Kammer"]] < singer_slot[singer_ids["Trillo"]])
solver.add(singer_slot[singer_ids["Zinn"]] < singer_slot[singer_ids["Yoshida"]])

# Answer Choices
choices = [
    "Kammer, Trillo, Zinn, Waite, Lugo, Yoshida",
    "Waite, Kammer, Yoshida, Zinn, Lugo, Trillo",
    "Waite, Lugo, Kammer, Trillo, Zinn, Yoshida",
    "Waite, Zinn, Kammer, Trillo, Lugo, Yoshida",
    "Zinn, Yoshida, Waite, Lugo, Kammer, Trillo"
]

for option_index, choice in enumerate(choices):
    solver.push()
    choice_singers = choice.split(', ')
    for slot_index, singer_name in enumerate(choice_singers):
        solver.add(audition_order[slot_index] == singer_ids[singer_name])
    if solver.check() == sat:
        print(f"Option {chr(65 + option_index)} is correct")
        exit()
    solver.pop()