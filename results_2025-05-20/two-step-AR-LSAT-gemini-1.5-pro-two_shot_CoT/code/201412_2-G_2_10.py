from z3 import *

# 1. Define Entities and Mappings
Farley, Garcia, Holden, Jiang = 0, 1, 2, 3
Lithographs, Oil, Sculptures, Watercolors = 0, 1, 2, 3

# 2. Declare Z3 Variables
slot_to_historian = Array('slot_to_historian', IntSort(), IntSort())
slot_to_topic = Array('slot_to_topic', IntSort(), IntSort())
historian_to_topic = Array('historian_to_topic', IntSort(), IntSort())
slot_L, slot_O, slot_S, slot_W = Ints('slot_L slot_O slot_S slot_W')
slot_F, slot_G, slot_H, slot_J = Ints('slot_F slot_G slot_H slot_J')
i = Int('i')

# 3. Formulate Base Constraints
solver = Solver()

# Permutation Constraints
solver.add(Distinct([slot_to_historian[i] for i in range(4)]))
solver.add(Distinct([slot_to_topic[i] for i in range(4)]))
solver.add(Distinct([historian_to_topic[i] for i in range(4)]))

# Consistency Constraint
solver.add(ForAll(i, Implies(And(i >= 0, i <= 3), historian_to_topic[slot_to_historian[i]] == slot_to_topic[i])))

# Define slot variables
solver.add(slot_to_topic[slot_L] == Lithographs)
solver.add(slot_to_topic[slot_O] == Oil)
solver.add(slot_to_topic[slot_S] == Sculptures)
solver.add(slot_to_topic[slot_W] == Watercolors)
solver.add(slot_to_historian[slot_F] == Farley)
solver.add(slot_to_historian[slot_G] == Garcia)
solver.add(slot_to_historian[slot_H] == Holden)
solver.add(slot_to_historian[slot_J] == Jiang)

solver.add(And([And(x >= 0, x <= 3) for x in [slot_L, slot_O, slot_S, slot_W, slot_F, slot_G, slot_H, slot_J]]))


# Problem Constraints
solver.add(And(slot_O < slot_L, slot_W < slot_L))
solver.add(slot_F < slot_O)
solver.add(And(slot_H < slot_G, slot_H < slot_J))
solver.add(historian_to_topic[Garcia] == Sculptures)

# 4. Test Answer Choices
options = [
    (slot_L == 2, "A"),
    (slot_O == 2, "B"),
    (slot_S == 0, "C"),
    (slot_S == 1, "D"),
    (slot_W == 1, "E"),
]

for option, option_letter in options:
    solver.push()
    solver.add(option)
    if solver.check() == sat:
        print(f"Option {option_letter} is correct")
        exit()
    solver.pop()