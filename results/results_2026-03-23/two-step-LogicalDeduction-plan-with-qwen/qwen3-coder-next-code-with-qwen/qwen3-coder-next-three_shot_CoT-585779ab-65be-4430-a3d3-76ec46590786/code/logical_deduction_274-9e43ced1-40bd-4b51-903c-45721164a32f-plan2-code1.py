from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the three fruits) and domain (price ranks)
fruits = ["peaches", "pears", "mangoes"]
ranks = range(1, 4)  # 1=cheapest, 3=most expensive
problem.addVariables(fruits, ranks)

# Add constraints based on the problem description
# 1. All fruits must have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The peaches are the cheapest" means peach's rank is 1
problem.addConstraint(lambda peaches: peaches == 1, ["peaches"])

# 3. "The mangoes are less expensive than the pears" means mango's rank < pear's rank
problem.addConstraint(lambda mangoes, pears: mangoes < pears, ["mangoes", "pears"])

# Solve for the unique solution
solutions = problem.getSolutions()

# The question asks which statement is true, and the choices directly state the cheapest fruit
# Since we know from constraint 2 that peaches are the cheapest (rank 1), choice A is correct
# We'll verify this by checking the solution
for solution in solutions:
    if solution["peaches"] == 1:
        print("A")
        break