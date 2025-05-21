from z3 import *

# Define variables
audition_order = Array('audition_order', IntSort(), IntSort())
singers = {"K": 0, "L": 1, "T": 2, "W": 3, "Y": 4, "Z": 5}
solver = Solver()

# Constraint 0: Domain of audition_order
i = Int('i')
solver.add(ForAll(i, Implies(And(i >= 0, i < 6), And(audition_order[i] >= 0, audition_order[i] <= 5))))

# Constraint 1: Distinctness of audition_order
solver.add(Distinct([audition_order[i] for i in range(6)]))

# Constraint 2 (Kammer and Lugo are recorded, others are not, and one of the last two must be recorded)
solver.add(Or(audition_order[4] == singers["K"], audition_order[4] == singers["L"]))
solver.add(audition_order[5] != singers["T"])
solver.add(audition_order[5] != singers["W"])
solver.add(audition_order[5] != singers["Y"])
solver.add(audition_order[5] != singers["Z"])


# Constraint 3: Fourth audition not recorded
solver.add(audition_order[3] != singers["K"])
solver.add(audition_order[3] != singers["L"])

# Constraint 4: Fifth audition is recorded (already covered in Constraint 2)

# Helper function to find index
def find_index(arr, val):
    for i in range(6):
        if arr[i] == val:
            return i
    return -1  # Should not happen given the constraints

# Constraint 5: Waite before recorded
solver.add(ForAll(i, Implies(And(i >= 0, i < 6, audition_order[i] == singers["W"]),
                             And(i < find_index(audition_order, singers["K"]), i < find_index(audition_order, singers["L"])))))

# Constraint 6: Kammer before Trillo
solver.add(ForAll(i, Implies(And(i >= 0, i < 6, audition_order[i] == singers["K"]), i < find_index(audition_order, singers["T"]))))

# Constraint 7: Zinn before Yoshida
solver.add(ForAll(i, Implies(And(i >= 0, i < 6, audition_order[i] == singers["Z"]), i < find_index(audition_order, singers["Y"]))))

# Answer choices
options = [
    "Kammer, Trillo, Zinn, Waite, Lugo, Yoshida",
    "Waite, Kammer, Yoshida, Zinn, Lugo, Trillo",
    "Waite, Lugo, Kammer, Trillo, Zinn, Yoshida",
    "Waite, Zinn, Kammer, Trillo, Lugo, Yoshida",
    "Zinn, Yoshida, Waite, Lugo, Kammer, Trillo"
]

for opt_index, option in enumerate(options):
    solver.push()
    order = option.split(', ')
    for i in range(6):
        solver.add(audition_order[i] == singers[order[i][0]])
    if solver.check() == sat:
        print(f"Option {chr(65 + opt_index)} is correct")
        exit()
    solver.pop()