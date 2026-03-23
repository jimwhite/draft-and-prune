from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the three fruits) and domain (price ranks)
fruits = ["mangoes", "watermelons", "kiwis"]
ranks = range(1, 4)  # 1=least expensive, 2=second-most expensive, 3=most expensive
problem.addVariables(fruits, ranks)

# Add constraints based on the puzzle's statements
# 1. All fruits must have a unique price rank.
problem.addConstraint(AllDifferentConstraint())

# 2. "The watermelons are less expensive than the kiwis."
problem.addConstraint(lambda watermelons, kiwis: watermelons < kiwis, ("watermelons", "kiwis"))

# 3. "The kiwis are the second-most expensive."
problem.addConstraint(lambda kiwis: kiwis == 2, ("kiwis",))

# Solve for the arrangement
solutions = problem.getSolutions()

# The question asks which statement is true.
# Since the constraint directly states kiwis == 2, choice C must be correct.
# We'll verify by checking the solution as per the plan.

for solution in solutions:
    # Check which fruit has rank 2 (second-most expensive)
    for fruit, rank in solution.items():
        if rank == 2:
            # The choice that matches this fruit is the answer
            if fruit == "kiwis":
                print("C")