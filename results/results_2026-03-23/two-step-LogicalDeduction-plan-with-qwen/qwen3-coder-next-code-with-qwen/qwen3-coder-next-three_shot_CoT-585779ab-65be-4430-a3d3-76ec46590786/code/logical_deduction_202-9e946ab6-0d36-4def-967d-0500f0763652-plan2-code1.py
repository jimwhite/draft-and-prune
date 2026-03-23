from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 7=most expensive)
fruits = ["watermelons", "mangoes", "kiwis", "pears", "cantaloupes", "oranges", "peaches"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem description:
# 1. "The oranges are more expensive than the peaches" → oranges > peaches
problem.addConstraint(lambda oranges, peaches: oranges > peaches, ("oranges", "peaches"))

# 2. "The cantaloupes are the fourth-most expensive" → cantaloupes == 4
problem.addConstraint(lambda cantaloupes: cantaloupes == 4, ("cantaloupes",))

# 3. "The pears are less expensive than the cantaloupes" → pears < 4
problem.addConstraint(lambda pears: pears < 4, ("pears",))

# 4. "The peaches are the second-most expensive" → peaches == 6
problem.addConstraint(lambda peaches: peaches == 6, ("peaches",))

# 5. "The mangoes are the cheapest" → mangoes == 1
problem.addConstraint(lambda mangoes: mangoes == 1, ("mangoes",))

# 6. "The kiwis are the third-cheapest" → kiwis == 3
problem.addConstraint(lambda kiwis: kiwis == 3, ("kiwis",))

# Solve the problem
solutions = problem.getSolutions()

# The question asks which fruit is the cheapest (rank 1)
# Based on constraints, mangoes must be rank 1
# Let's verify by checking the solution (though it's directly constrained)
for solution in solutions:
    # Find which fruit has rank 1
    for fruit, rank in solution.items():
        if rank == 1:
            # Map to the correct choice letter
            if fruit == "mangoes":
                print("B")
            break