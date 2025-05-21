from z3 import *

P, Q, R, S, T, V, W = 0, 1, 2, 3, 4, 5, 6
options = [
    [Q, T, S, P, V, W, R],
    [Q, W, R, P, S, V, T],
    [V, W, Q, S, P, T, R],
    [V, W, S, P, Q, T, R],
    [V, W, S, P, R, T, Q]
]

for option_index, option in enumerate(options):
    solver = Solver()
    order = [Int("pos_%d" % i) for i in range(7)]
    for i in range(7):
        solver.add(order[i] >= 0, order[i] <= 6)

    solver.add(Distinct(order))

    # Peters recruited fourth
    solver.add(order[3] == P)

    # Villas immediately before White
    solver.add(Or([And(order[i] == V, order[i + 1] == W) for i in range(6)]))

    # Quinn recruited earlier than Rovero
    solver.add(order[option.index(Q)] < order[option.index(R)])

    # Stanton not immediately before/after Tao
    s_index = option.index(S)
    t_index = option.index(T)
    solver.add(Or(order[s_index] + 1 != order[t_index], order[s_index] -1 != order[t_index]))


    if solver.check() == sat:
        print(f"Option {chr(65 + option_index)} is correct")
        exit()