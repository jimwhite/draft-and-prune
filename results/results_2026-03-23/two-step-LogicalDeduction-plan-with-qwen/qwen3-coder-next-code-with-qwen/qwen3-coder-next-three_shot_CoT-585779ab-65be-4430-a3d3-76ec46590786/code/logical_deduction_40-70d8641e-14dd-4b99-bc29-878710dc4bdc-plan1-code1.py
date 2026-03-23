from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 5=most expensive)
fruits = ["cantaloupes", "kiwis", "oranges", "mangoes", "peaches"]
ranks = range(1, 6)
problem.addVariables(fruits, ranks)

# Add constraints based on the problem statements
# 1. All fruits have distinct price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The kiwis are less expensive than the mangoes" → kiwis < mangoes
problem.addConstraint(lambda kiwis, mangoes: kiwis < mangoes, ("kiwis", "mangoes"))

# 3. "The peaches are less expensive than the oranges" → peaches < oranges
problem.addConstraint(lambda peaches, oranges: peaches < oranges, ("peaches", "oranges"))

# 4. "The oranges are the second-most expensive" → oranges == 4
problem.addConstraint(lambda oranges: oranges == 4, ("oranges",))

# 5. "The mangoes are the second-cheapest" → mangoes == 2
problem.addConstraint(lambda mangoes: mangoes == 2, ("mangoes",))

# Solve the problem
solutions = problem.getSolutions()

# The question asks which fruit is the second-cheapest (rank 2)
# According to constraint #5, mangoes == 2, so the answer is D
# Let's verify by checking the solution
for solution in solutions:
    # Check which fruit has rank 2 and match with choices
    if solution["mangoes"] == 2:
        print("D")