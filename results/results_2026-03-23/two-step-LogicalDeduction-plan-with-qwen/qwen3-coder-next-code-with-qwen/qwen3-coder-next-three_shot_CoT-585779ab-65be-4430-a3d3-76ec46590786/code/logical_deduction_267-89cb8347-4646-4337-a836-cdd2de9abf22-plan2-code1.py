from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the three fruits) and domain (price ranks: 1=cheapest, 3=most expensive)
fruits = ["kiwis", "oranges", "watermelons"]
ranks = range(1, 4)
problem.addVariables(fruits, ranks)

# Add constraints based on the puzzle's statements
# 1. All fruits must have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The oranges are more expensive than the kiwis" (oranges rank > kiwis rank)
problem.addConstraint(lambda kiwis, oranges: oranges > kiwis, ("kiwis", "oranges"))

# 3. "The oranges are less expensive than the watermelons" (oranges rank < watermelons rank)
problem.addConstraint(lambda oranges, watermelons: oranges < watermelons, ("oranges", "watermelons"))

# Solve for the arrangement
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "kiwis",
    "B": "oranges",
    "C": "watermelons"
}

# Find the cheapest fruit (rank 1) and print the corresponding letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 1:
            print(letter)