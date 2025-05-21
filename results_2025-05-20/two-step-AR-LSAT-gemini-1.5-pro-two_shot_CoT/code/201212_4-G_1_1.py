from z3 import *

# Define variables
house_at_slot = Array('house_at_slot', IntSort(), IntSort())
solver = Solver()

# House IDs: J=0, K=1, L=2, M=3, N=4, O=5, P=6
# Slot IDs: Morning1=0, Morning2=1, Afternoon1=2, Afternoon2=3, Afternoon3=4, Evening1=5, Evening2=6

# Constraint 0 (Domain)
i = Int('i')
solver.add(ForAll(i, Implies(And(i >= 0, i < 7), And(house_at_slot[i] >= 0, house_at_slot[i] < 7))))

# Constraint 1 (Distinctness)
solver.add(Distinct([house_at_slot[i] for i in range(7)]))

# Constraint 2 (J in Evening)
solver.add(Or(house_at_slot[5] == 0, house_at_slot[6] == 0))

# Constraint 3 (K not in Morning)
solver.add(And(house_at_slot[0] != 1, house_at_slot[1] != 1))

# Constraint 4 (L before M)
i = Int('i')
j = Int('j')
solver.add(ForAll([i, j], Implies(And(i >= 0, i < 7, j >= 0, j < 7, house_at_slot[i] == 2, house_at_slot[j] == 3), i < j)))

# Constraint 5 (L after K)
i = Int('i')
j = Int('j')
solver.add(ForAll([i, j], Implies(And(i >= 0, i < 7, j >= 0, j < 7, house_at_slot[i] == 1, house_at_slot[j] == 2), i < j)))


# Answer choices
options = [
    "K, 0, L, M, N, J, P",
    "N, L, P, K, M, 0, J",
    "0, P, K, L, N, M, J",
    "0, P, M, N, K, L, J",
    "P, 0, K, J, L, N, M"
]
house_mapping = {'J': 0, 'K': 1, 'L': 2, 'M': 3, 'N': 4, 'O': 5, 'P': 6, '0': 0}

for option_index, option in enumerate(options):
    solver.push()
    houses = option.split(',')
    for slot_index, house_str in enumerate(houses):
        house_str = house_str.strip()
        house_id = house_mapping[house_str]
        solver.add(house_at_slot[slot_index] == house_id)

    if solver.check() == sat:
        print(f"Option {chr(65 + option_index)} is correct")
        exit()
    solver.pop()
