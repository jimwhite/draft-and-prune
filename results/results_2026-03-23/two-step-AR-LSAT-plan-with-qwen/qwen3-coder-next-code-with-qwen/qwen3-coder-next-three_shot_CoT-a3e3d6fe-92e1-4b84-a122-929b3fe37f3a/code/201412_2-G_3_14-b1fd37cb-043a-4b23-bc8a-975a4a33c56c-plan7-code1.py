from z3 import *

# Color indices: forest=0, olive=1, peach=2, turquoise=3, white=4, yellow=5
colors = ["forest", "olive", "peach", "turquoise", "white", "yellow"]

# Answer choices: pairs of solid rug colors
answer_choices = [
    ("forest", "peach"),
    ("forest", "yellow"),
    ("peach", "turquoise"),
    ("peach", "yellow"),
    ("turquoise", "yellow")
]

# Result list for impossible pairs
impossible_indices = []

for idx, (s1, s2) in enumerate(answer_choices):
    solver = Solver()
    
    # Represent rug assignments with boolean variables
    # For each color c and rug r (0,1,2), use variable in_rug[c][r] meaning color c is in rug r
    # Rugs 0 and 1 are the solid rugs (s1 and s2), rug 2 is multicolored
    in_rug = [[Bool(f"in_{c}_{r}") for r in range(3)] for c in range(6)]
    
    # Map color names to indices
    color_idx = {c: i for i, c in enumerate(colors)}
    
    # Each color used appears in exactly one rug
    for c in range(6):
        solver.add(Sum([If(in_rug[c][r], 1, 0) for r in range(3)]) == 1)
    
    # Exactly five colors are used (one color is excluded)
    used = [Bool(f"used_{c}") for c in range(6)]
    for c in range(6):
        solver.add(used[c] == Or([in_rug[c][r] for r in range(3)]))
    solver.add(Sum([If(used[c], 1, 0) for c in range(6)]) == 5)
    
    # Solid rugs: s1 and s2 each appear alone in their rug
    idx_s1 = color_idx[s1]
    idx_s2 = color_idx[s2]
    
    # s1 is in exactly one rug and that rug has only s1
    solver.add(Or([And(in_rug[idx_s1][r], 
                       And([Not(in_rug[c][r]) for c in range(6) if c != idx_s1])) 
                  for r in range(3)]))
    
    # s2 is in exactly one rug and that rug has only s2
    solver.add(Or([And(in_rug[idx_s2][r], 
                       And([Not(in_rug[c][r]) for c in range(6) if c != idx_s2])) 
                  for r in range(3)]))
    
    # s1 and s2 are in different rugs
    solver.add(Or([And(in_rug[idx_s1][r1], in_rug[idx_s2][r2]) for r1 in range(3) for r2 in range(3) if r1 != r2]))
    
    # The third rug (multicolored) must contain exactly 3 colors
    # Determine which rug is multicolored (not s1's rug, not s2's rug)
    # We'll enforce that exactly 3 colors are in the remaining rug
    for r in range(3):
        # Count how many colors are in rug r
        count_r = Sum([If(in_rug[c][r], 1, 0) for c in range(6)])
        # If rug r is not s1's rug and not s2's rug, it must have exactly 3 colors
        # But we don't know which rug is which, so instead enforce:
        # Exactly one rug has 1 color (s1), exactly one rug has 1 color (s2), and one rug has 3 colors
        # Actually, since s1 and s2 are fixed to be solid, we can directly enforce:
        # The multicolored rug has exactly 3 colors
        pass
    
    # Instead, enforce the structure directly:
    # There are exactly two rugs with exactly 1 color (s1 and s2), and one rug with exactly 3 colors
    # But since we know which colors are solid, enforce:
    
    # For each rug r, count colors
    counts = [Sum([If(in_rug[c][r], 1, 0) for c in range(6)]) for r in range(3)]
    
    # Exactly two rugs have count 1, one rug has count 3
    solver.add(Or(
        And(counts[0] == 1, counts[1] == 1, counts[2] == 3),
        And(counts[0] == 1, counts[1] == 3, counts[2] == 1),
        And(counts[0] == 3, counts[1] == 1, counts[2] == 1)
    ))
    
    # Enforce s1 and s2 are in different rugs with count 1
    # Already handled above implicitly
    
    # Now add the rules for the multicolored rug (the one with 3 colors)
    
    # Rule 1: If white is used in a rug, two other colors are also used
    # Since the multicolored rug has exactly 3 colors, if white is in it, this rule is satisfied
    # For solid rugs: s1 and s2 are single colors, so white cannot be in a solid rug unless it's alone
    # But if white is s1 or s2, then the rule would require two other colors in that rug — impossible
    # So white cannot be one of the solid rugs unless it's in a multicolored rug
    # Since we have exactly two solid rugs and they are s1 and s2, if either is white, it's invalid
    idx_white = color_idx["white"]
    
    # If s1 or s2 is white, then the rule "if white is used, two other colors are also used" would be violated
    # because a solid rug with white has only one color
    if s1 == "white" or s2 == "white":
        solver.add(False)  # UNSAT
    
    # Rule 2: If olive is used in a rug, peach is also used
    idx_olive = color_idx["olive"]
    idx_peach = color_idx["peach"]
    
    # For each rug r, if olive is in rug r, then peach must be in rug r
    for r in range(3):
        solver.add(Implies(in_rug[idx_olive][r], in_rug[idx_peach][r]))
    
    # Rule 3: Forest and turquoise are not used together in a rug
    idx_forest = color_idx["forest"]
    idx_turquoise = color_idx["turquoise"]
    
    for r in range(3):
        solver.add(Not(And(in_rug[idx_forest][r], in_rug[idx_turquoise][r])))
    
    # Rule 4: Peach and turquoise are not used together in a rug
    for r in range(3):
        solver.add(Not(And(in_rug[idx_peach][r], in_rug[idx_turquoise][r])))
    
    # Rule 5: Peach and yellow are not used together in a rug
    idx_yellow = color_idx["yellow"]
    
    for r in range(3):
        solver.add(Not(And(in_rug[idx_peach][r], in_rug[idx_yellow][r])))
    
    # Check if this configuration is possible
    result = solver.check()
    if result == unsat:
        impossible_indices.append(idx)

print(impossible_indices)