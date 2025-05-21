from z3 import *

# Define buildings and companies
RP, SC, TC = 0, 1, 2
GT, YH, ZH, FT, LB, KB, MB, OB = 0, 1, 2, 3, 4, 5, 6, 7
buildings = [Int("b%d" % i) for i in range(8)]

solver = Solver()

# Initial ownership constraints
solver.add(buildings[GT] == RP)
solver.add(buildings[YH] == RP)
solver.add(buildings[ZH] == RP)
solver.add(buildings[FT] == SC)
solver.add(buildings[LB] == SC)
solver.add(buildings[KB] == TC)
solver.add(buildings[MB] == TC)
solver.add(buildings[OB] == TC)

# Possible trades
possible_trades = []

# Type 1 trades (same class swap)
possible_trades.append(And(buildings[GT] == SC, buildings[FT] == RP))
possible_trades.append(And(buildings[LB] == TC, buildings[KB] == SC))
possible_trades.append(And(buildings[LB] == TC, buildings[MB] == SC))
possible_trades.append(And(buildings[LB] == TC, buildings[OB] == SC))
possible_trades.append(And(buildings[YH] == RP, buildings[ZH] == RP)) # No effective change

# Type 2 trades (C1 for two C2) - Skipping as it requires more complex constraints
# Type 3 trades (C2 for two C3)
possible_trades.append(And(buildings[LB] == RP, buildings[YH] == SC, buildings[ZH] == SC))
possible_trades.append(And(buildings[KB] == RP, buildings[YH] == TC, buildings[ZH] == TC))
possible_trades.append(And(buildings[MB] == RP, buildings[YH] == TC, buildings[ZH] == TC))
possible_trades.append(And(buildings[OB] == RP, buildings[YH] == TC, buildings[ZH] == TC))


options = [
    [ # Option A
        And(buildings[FT] == RP, buildings[GT] == RP,
            buildings[YH] == SC, buildings[ZH] == SC, buildings[LB] == SC,
            buildings[KB] == TC, buildings[MB] == TC, buildings[OB] == TC)
    ],
    [ # Option B
        And(buildings[GT] == RP, buildings[KB] == RP, buildings[OB] == RP,
            buildings[FT] == SC, buildings[LB] == SC,
            buildings[MB] == TC, buildings[YH] == TC, buildings[ZH] == TC)
    ],
    [ # Option C
        And(buildings[GT] == RP, buildings[LB] == RP,
            buildings[FT] == SC, buildings[YH] == SC, buildings[ZH] == SC,
            buildings[KB] == TC, buildings[MB] == TC, buildings[OB] == TC)
    ],
    [ # Option D
        And(buildings[GT] == RP, buildings[MB] == RP, buildings[YH] == RP,
            buildings[FT] == SC, buildings[LB] == SC,
            buildings[KB] == TC, buildings[OB] == TC, buildings[ZH] == TC)
    ],
    [ # Option E
        And(buildings[GT] == RP, buildings[YH] == RP, buildings[ZH] == RP,
            buildings[LB] == SC, buildings[OB] == SC,
            buildings[FT] == TC, buildings[KB] == TC, buildings[MB] == TC)
    ]
]

for i, option in enumerate(options):
    solver.push()
    solver.add(Or(possible_trades))
    solver.add(option)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()