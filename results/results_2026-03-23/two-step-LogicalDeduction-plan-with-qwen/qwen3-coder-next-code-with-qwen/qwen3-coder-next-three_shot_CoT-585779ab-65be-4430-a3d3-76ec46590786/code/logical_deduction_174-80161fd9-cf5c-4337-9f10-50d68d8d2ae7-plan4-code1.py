from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the seven fruits as variables
fruits = ["loquats", "cantaloupes", "watermelons", "apples", "oranges", "pears", "mangoes"]

# Define the domain: positions 1 to 7, where 1 = cheapest and 7 = most expensive
positions = range(1, 8)
problem.addVariables(fruits, positions)

# Add constraints based on the problem description
# 1. All fruits must have unique price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The oranges are the second-cheapest" → position of oranges = 2
problem.addConstraint(lambda oranges: oranges == 2, ["oranges"])

# 3. "The apples are less expensive than the pears" → apples < pears
problem.addConstraint(lambda apples, pears: apples < pears, ["apples", "pears"])

# 4. "The mangoes are more expensive than the cantaloupes" → cantaloupes < mangoes
problem.addConstraint(lambda cantaloupes, mangoes: cantaloupes < mangoes, ["cantaloupes", "mangoes"])

# 5. "The mangoes are the third-cheapest" → position of mangoes = 3
problem.addConstraint(lambda mangoes: mangoes == 3, ["mangoes"])

# 6. "The watermelons are the second-most expensive" → position of watermelons = 6
problem.addConstraint(lambda watermelons: watermelons == 6, ["watermelons"])

# 7. "The loquats are the third-most expensive" → position of loquats = 5
problem.addConstraint(lambda loquats: loquats == 5, ["loquats"])

# Solve the problem
solutions = problem.getSolutions()

# Since there's a unique solution, get the first one
solution = solutions[0]

# The question asks which statement is true, and option A states "The loquats are the third-most expensive."
# Based on our constraint, loquats should be at position 5 (third-most expensive: 7=most, 6=second-most, 5=third-most)
# Verify that loquats is indeed at position 5 (which it should be due to the constraint)
if solution["loquats"] == 5:
    print("A")