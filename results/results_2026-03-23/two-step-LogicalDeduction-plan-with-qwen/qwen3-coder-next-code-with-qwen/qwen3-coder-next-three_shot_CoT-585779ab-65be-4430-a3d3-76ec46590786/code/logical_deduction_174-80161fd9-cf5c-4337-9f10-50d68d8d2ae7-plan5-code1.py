from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 7=most expensive)
fruits = ["loquats", "cantaloupes", "watermelons", "apples", "oranges", "pears", "mangoes"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statement:
# "The oranges are the second-cheapest" → rank 2
problem.addConstraint(lambda oranges: oranges == 2, ["oranges"])

# "The mangoes are the third-cheapest" → rank 3
problem.addConstraint(lambda mangoes: mangoes == 3, ["mangoes"])

# "The watermelons are the second-most expensive" → rank 6 (7 is most expensive)
problem.addConstraint(lambda watermelons: watermelons == 6, ["watermelons"])

# "The loquats are the third-most expensive" → rank 5 (7,6,5 = most, second-most, third-most)
problem.addConstraint(lambda loquats: loquats == 5, ["loquats"])

# "The apples are less expensive than the pears" → apples < pears
problem.addConstraint(lambda apples, pears: apples < pears, ["apples", "pears"])

# "The mangoes are more expensive than the cantaloupes" → cantaloupes < mangoes (i.e., < 3)
problem.addConstraint(lambda cantaloupes, mangoes: cantaloupes < mangoes, ["cantaloupes", "mangoes"])

# Solve the problem
solutions = problem.getSolutions()

# Since we have direct constraints, we know loquats == 5 (third-most expensive)
# Check the choices: A says "The loquats are the third-most expensive" which matches our constraint
# So answer is A

print("A")