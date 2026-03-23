from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the three fruits) and domain (price ranks: 1=least expensive, 2=second-most expensive, 3=most expensive)
fruits = ["mangoes", "watermelons", "kiwis"]
ranks = range(1, 4)
problem.addVariables(fruits, ranks)

# Add constraints based on the puzzle's statements
# 1. All fruits must have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The watermelons are less expensive than the kiwis" (watermelons rank < kiwis rank)
problem.addConstraint(lambda watermelons, kiwis: watermelons < kiwis, ("watermelons", "kiwis"))

# 3. "The kiwis are the second-most expensive" (kiwis rank == 2)
problem.addConstraint(lambda kiwis: kiwis == 2, ("kiwis",))

# Solve for the arrangement
solutions = problem.getSolutions()

# The question asks which statement is true, and choice C directly states "The kiwis are the second-most expensive"
# Since we have a constraint that kiwis == 2, and this is consistent with all other constraints,
# choice C must be true. We can verify by checking the solution.
for solution in solutions:
    if solution["kiwis"] == 2:
        print("C")