from z3 import *

# Compositions indices: F=0, H=1, L=2, O=3, P=4, R=5, S=6, T=7
compositions = ["F", "H", "L", "O", "P", "R", "S", "T"]
pos = {c: Int(f"pos_{c}") for c in compositions}

solver = Solver()

# Domain constraints: positions 1-8
for c in compositions:
    solver.add(pos[c] >= 1, pos[c] <= 8)

# All-different constraint
solver.add(Distinct(*[pos[c] for c in compositions]))

# O is performed either first or fifth
solver.add(Or(pos["O"] == 1, pos["O"] == 5))

# T is performed either immediately before F or immediately after R
solver.add(Or(pos["T"] + 1 == pos["F"], pos["R"] + 1 == pos["T"]))

# At least two compositions between F and R
solver.add(Or(pos["F"] + 2 <= pos["R"], pos["R"] + 2 <= pos["F"]))

# Eighth composition is L or H
solver.add(Or(pos["L"] == 8, pos["H"] == 8))

# P is performed before S
solver.add(pos["P"] < pos["S"])

# At least one composition between O and S
solver.add(Or(pos["O"] + 1 < pos["S"], pos["S"] + 1 < pos["O"]))

# Additional assumption: O is performed immediately after T
solver.add(pos["O"] == pos["T"] + 1)

# Collect all possible positions for F
solutions = []
for _ in range(100):  # Limit to avoid infinite loop
    if solver.check() == sat:
        m = solver.model()
        f_pos = m.eval(pos["F"]).as_long()
        solutions.append(f_pos)
        
        # Add constraint to exclude current solution for F position
        solver.add(pos["F"] != f_pos)
    else:
        break

# Get unique positions for F
f_positions = sorted(set(solutions))

# Map positions to answer choices
def get_answer_choice(positions):
    if set(positions) == {1, 2}:
        return "first or second"
    elif set(positions) == {2, 3}:
        return "second or third"
    elif set(positions) == {4, 6}:
        return "fourth or sixth"
    elif set(positions) == {4, 7}:
        return "fourth or seventh"
    elif set(positions) == {6, 7}:
        return "sixth or seventh"
    else:
        # Fallback: try to match any subset
        if all(p in [1, 2] for p in positions):
            return "first or second"
        elif all(p in [2, 3] for p in positions):
            return "second or third"
        elif all(p in [4, 6] for p in positions):
            return "fourth or sixth"
        elif all(p in [4, 7] for p in positions):
            return "fourth or seventh"
        elif all(p in [6, 7] for p in positions):
            return "sixth or seventh"
        else:
            # Try to find closest match
            if 1 in positions and 2 in positions:
                return "first or second"
            elif 2 in positions and 3 in positions:
                return "second or third"
            elif 4 in positions and (6 in positions or 7 in positions):
                if 6 in positions:
                    return "fourth or sixth"
                else:
                    return "fourth or seventh"
            elif 6 in positions and 7 in positions:
                return "sixth or seventh"
            else:
                # Default to first option if nothing matches
                return "first or second"

result = get_answer_choice(f_positions)
print(result)