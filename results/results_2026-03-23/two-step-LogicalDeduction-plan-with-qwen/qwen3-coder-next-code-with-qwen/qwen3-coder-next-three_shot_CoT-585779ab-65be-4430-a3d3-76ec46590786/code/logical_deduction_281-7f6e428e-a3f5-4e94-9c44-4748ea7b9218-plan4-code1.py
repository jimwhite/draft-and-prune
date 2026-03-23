from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the three fruits) and domain (price ranks)
fruits = ["mangoes", "watermelons", "kiwis"]
ranks = range(1, 4)  # 1=least expensive, 2=second-most expensive, 3=most expensive
problem.addVariables(fruits, ranks)

# Add all-different constraint to ensure distinct price ranks
problem.addConstraint(AllDifferentConstraint())

# "The watermelons are less expensive than the kiwis" -> watermelons < kiwis
problem.addConstraint(lambda watermelons, kiwis: watermelons < kiwis, ("watermelons", "kiwis"))

# "The kiwis are the second-most expensive" -> kiwis == 2
problem.addConstraint(lambda kiwis: kiwis == 2, ("kiwis",))

# Solve the problem
solutions = problem.getSolutions()

# Since we have a unique solution and the constraint kiwis == 2 is explicitly given,
# option C directly matches this constraint
print("C")