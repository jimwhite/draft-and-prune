from z3 import *

# Define companies and buildings
RP = 0
SC = 1
TC = 2
GT = 0
YH = 1
ZH = 2
FT = 3
LB = 4
KB = 5
MB = 6
OB = 7
buildings = [Int("building_%d" % i) for i in range(8)]

def solve_and_check(target_ownership):
    solver = Solver()
    for b in buildings:
        solver.add(Or(b == RP, b == SC, b == TC))

    # Initial ownership
    solver.add(buildings[GT] == RP)
    solver.add(buildings[YH] == RP)
    solver.add(buildings[ZH] == RP)
    solver.add(buildings[FT] == SC)
    solver.add(buildings[LB] == SC)
    solver.add(buildings[KB] == TC)
    solver.add(buildings[MB] == TC)
    solver.add(buildings[OB] == TC)

    # Target ownership constraints
    # Corrected: Use building constants instead of string literals
    for building, owner in target_ownership.items():
        solver.add(buildings[eval(building)] == owner)  # eval() converts string keys to their corresponding integer values

    return solver.check()


# Check each answer choice
options = [
    ({"LB": RP, "MB": RP, "OB": RP}, "A"),
    ({"GT": SC, "MB": SC}, "B"),
    ({"KB": SC, "MB": SC, "OB": SC}, "C"),
    ({"FT": TC, "YH": TC}, "D"),
    ({"GT": TC, "LB": TC}, "E"),
]

for ownership, option_letter in options:
    if solve_and_check(ownership) == sat:
        continue
    else:
        print(f"Option {option_letter} is correct")
        exit()

print("No option is impossible.")

