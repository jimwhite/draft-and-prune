from z3 import *

# Define variables
composition_at_slot = Array('composition_at_slot', IntSort(), IntSort())
solver = Solver()

# Define compositions and slots
compositions = {"F": 0, "H": 1, "L": 2, "O": 3, "P": 4, "R": 5, "S": 6, "T": 7}
slots = list(range(8))

# Helper function for IndexOf
def IndexOf(array, element):
    for i in range(8):
        if array[i] == element:
            return i
    return -1  # Should not happen in this problem


# Constraint 0 (Domain)
for i in range(8):  # Fixed: Iterate and add constraints individually
    solver.add(And(composition_at_slot[i] >= 0, composition_at_slot[i] < 8))

# Constraint 1 (Distinctness)
solver.add(Distinct([composition_at_slot[i] for i in range(8)]))

# Constraint 2 (T before F or after R)
solver.add(Or(IndexOf(composition_at_slot, compositions["T"]) == IndexOf(composition_at_slot, compositions["F"]) - 1,
             IndexOf(composition_at_slot, compositions["T"]) == IndexOf(composition_at_slot, compositions["R"]) + 1))

# Constraint 3 (Two between F and R)
solver.add(Or(Sum([If(And(i > IndexOf(composition_at_slot, compositions["F"]), i < IndexOf(composition_at_slot, compositions["R"])), 1, 0) for i in range(8)]) >= 2,
             Sum([If(And(i > IndexOf(composition_at_slot, compositions["R"]), i < IndexOf(composition_at_slot, compositions["F"])), 1, 0) for i in range(8)]) >= 2))

# Constraint 4 (O is first or fifth)
solver.add(Or(composition_at_slot[0] == compositions["O"], composition_at_slot[4] == compositions["O"]))

# Constraint 5 (Eighth is L or H)
solver.add(Or(composition_at_slot[7] == compositions["L"], composition_at_slot[7] == compositions["H"]))

# Constraint 6 (P before S)
solver.add(IndexOf(composition_at_slot, compositions["P"]) < IndexOf(composition_at_slot, compositions["S"]))

# Constraint 7 (One between O and S)
solver.add(Or(Sum([If(And(i > IndexOf(composition_at_slot, compositions["O"]), i < IndexOf(composition_at_slot, compositions["S"])), 1, 0) for i in range(8)]) >= 1,
             Sum([If(And(i > IndexOf(composition_at_slot, compositions["S"]), i < IndexOf(composition_at_slot, compositions["O"])), 1, 0) for i in range(8)]) >= 1))

# Constraint 8 (T is fifth, F is sixth)
solver.add(And(composition_at_slot[4] == compositions["T"], composition_at_slot[5] == compositions["F"]))

# Check answer choices
answer_choices = ["fourth or seventh", "third or sixth", "third or fourth", "second or seventh", "first or fourth"]
for i, choice in enumerate(answer_choices):
    solver.push()
    if choice == "fourth or seventh":
        solver.add(Or(composition_at_slot[3] == compositions["S"], composition_at_slot[6] == compositions["S"]))
    elif choice == "third or sixth":
        solver.add(Or(composition_at_slot[2] == compositions["S"], composition_at_slot[5] == compositions["S"]))
    elif choice == "third or fourth":
        solver.add(Or(composition_at_slot[2] == compositions["S"], composition_at_slot[3] == compositions["S"]))
    elif choice == "second or seventh":
        solver.add(Or(composition_at_slot[1] == compositions["S"], composition_at_slot[6] == compositions["S"]))
    elif choice == "first or fourth":
        solver.add(Or(composition_at_slot[0] == compositions["S"], composition_at_slot[3] == compositions["S"]))

    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
