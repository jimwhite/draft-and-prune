from z3 import *

# Accomplice indices
(PETERS, QUINN, ROVERO, STANTON, TAO, VILLAS, WHITE) = range(7)

# Create order variables: order[i] = accomplice index at position i (0-indexed)
order = [Int(f"pos_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: each position has an accomplice index from 0 to 6
for i in range(7):
    solver.add(order[i] >= 0, order[i] <= 6)

# All different constraint: each accomplice appears exactly once
solver.add(Distinct(order))

# Fixed constraint: Peters is recruited fourth → position 3 (0-indexed)
solver.add(order[3] == PETERS)

# Villas-White adjacency constraint: Villas immediately before White
solver.add(And(
    0 <= order.index(VILLAS),
    order.index(VILLAS) < 6,
    order[order.index(VILLAS)] == VILLAS,
    order[order.index(VILLAS) + 1] == WHITE
))

# Quinn-Rovero precedence constraint: Quinn recruited earlier than Rovero
solver.add(And(
    0 <= order.index(QUINN),
    order.index(QUINN) < 7,
    0 <= order.index(ROVERO),
    order.index(ROVERO) < 7,
    order[order.index(QUINN)] == QUINN,
    order[order.index(ROVERO)] == ROVERO,
    order.index(QUINN) < order.index(ROVERO)
))

# Stanton-Tao non-adjacency constraint: not immediately before or after
solver.add(Not(Or(
    And(order.index(STANTON) >= 0, order.index(STANTON) < 6, order[order.index(STANTON)] == STANTON, order[order.index(STANTON) + 1] == TAO),
    And(order.index(TAO) >= 0, order.index(TAO) < 6, order[order.index(TAO)] == TAO, order[order.index(TAO) + 1] == STANTON)
)))

# Answer choices as lists of names in order
answer_choices = [
    ["Quinn", "Tao", "Stanton", "Peters", "Villas", "White", "Rovero"],
    ["Quinn", "White", "Rovero", "Peters", "Stanton", "Villas", "Tao"],
    ["Villas", "White", "Quinn", "Stanton", "Peters", "Tao", "Rovero"],
    ["Villas", "White", "Stanton", "Peters", "Quinn", "Tao", "Rovero"],
    ["Villas", "White", "Stanton", "Peters", "Rovero", "Tao", "Quinn"]
]

# Map names to indices
name_to_index = {
    "Peters": PETERS,
    "Quinn": QUINN,
    "Rovero": ROVERO,
    "Stanton": STANTON,
    "Tao": TAO,
    "Villas": VILLAS,
    "White": WHITE
}

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    # Add all base constraints
    s_chk.add(solver.assertions())
    
    # Assert the specific order for this choice
    for i, name in enumerate(choice):
        s_chk.add(order[i] == name_to_index[name])
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)