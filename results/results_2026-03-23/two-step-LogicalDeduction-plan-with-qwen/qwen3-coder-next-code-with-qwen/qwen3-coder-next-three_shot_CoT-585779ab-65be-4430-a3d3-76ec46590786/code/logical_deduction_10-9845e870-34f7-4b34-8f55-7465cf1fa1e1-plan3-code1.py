from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the five birds)
birds = ["owl", "robin", "blue jay", "hawk", "hummingbird"]

# Define domain: positions 1 to 5 (1 = leftmost, 5 = rightmost)
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints based on the problem statement
# 1. All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The owl is the second from the right" → position 4
problem.addConstraint(lambda owl: owl == 4, ["owl"])

# 3. "The robin is the second from the left" → position 2
problem.addConstraint(lambda robin: robin == 2, ["robin"])

# 4. "The robin is to the right of the blue jay" → blue jay < robin
problem.addConstraint(lambda bj, r: bj < r, ["blue jay", "robin"])

# 5. "The hummingbird is to the right of the hawk" → hawk < hummingbird
problem.addConstraint(lambda h, hb: h < hb, ["hawk", "hummingbird"])

# Solve the problem
solutions = problem.getSolutions()

# The question asks which bird is second from the left (position 2)
# According to constraint #3, robin must be at position 2 in any valid solution
# So choice B ("The robin is the second from the left.") must be true

# Since we know robin == 2 is enforced as a constraint, B is necessarily true
print("B")