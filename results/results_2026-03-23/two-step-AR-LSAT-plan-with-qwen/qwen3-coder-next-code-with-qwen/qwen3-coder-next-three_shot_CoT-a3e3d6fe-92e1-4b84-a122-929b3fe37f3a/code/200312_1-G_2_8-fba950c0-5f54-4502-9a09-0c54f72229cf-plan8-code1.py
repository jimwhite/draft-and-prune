from z3 import *

# Cargo types: 0=fuel, 1=grain, 2=livestock, 3=machinery, 4=produce, 5=textiles
cargo_types = ["fuel", "grain", "livestock", "machinery", "produce", "textiles"]
pos = {ct: Int(f"pos_{ct}") for ct in cargo_types}

solver = Solver()

# Domain constraints: positions 1-6, all distinct
for ct in cargo_types:
    solver.add(pos[ct] >= 1, pos[ct] <= 6)
solver.add(Distinct(*pos.values()))

# Ordering constraints
solver.add(pos["grain"] > pos["livestock"])
solver.add(pos["livestock"] > pos["textiles"])
solver.add(pos["produce"] > pos["fuel"])

# Textiles adjacent to produce: |pos[textiles] - pos[produce]| = 1
solver.add(Or(
    pos["textiles"] == pos["produce"] + 1,
    pos["produce"] == pos["textiles"] + 1
))

# Extra condition: exactly one bay between machinery and grain → |pos[machinery] - pos[grain]| = 2
solver.add(Or(
    pos["machinery"] == pos["grain"] + 2,
    pos["grain"] == pos["machinery"] + 2
))

# To find how many positions are fixed across all solutions:
# We'll collect all satisfying assignments and check which bay positions have consistent cargo

def get_model():
    s = Solver()
    s.add(solver.assertions())
    if s.check() == sat:
        return s.model()
    else:
        return None

# First, get one model to see possible assignments
model = get_model()
if model is None:
    print(0)  # No solution exists
else:
    # For each bay position (1-6), determine if the cargo type is fixed
    fixed_count = 0
    
    for bay in range(1, 7):
        # Collect all possible cargoes at this bay across solutions
        possible_cargoes = set()
        
        # We'll enumerate all solutions (up to 720, but constraints should limit this)
        s = Solver()
        s.add(solver.assertions())
        
        while s.check() == sat:
            m = s.model()
            # Get cargo at this bay
            for ct in cargo_types:
                if m.eval(pos[ct]).as_long() == bay:
                    possible_cargoes.add(ct)
                    break
            
            # Add constraint to exclude this assignment
            s.add(Or(*[pos[ct] != m.eval(pos[ct]).as_long() for ct in cargo_types]))
        
        # If only one possible cargo at this bay, it's fixed
        if len(possible_cargoes) == 1:
            fixed_count += 1
    
    print(fixed_count)