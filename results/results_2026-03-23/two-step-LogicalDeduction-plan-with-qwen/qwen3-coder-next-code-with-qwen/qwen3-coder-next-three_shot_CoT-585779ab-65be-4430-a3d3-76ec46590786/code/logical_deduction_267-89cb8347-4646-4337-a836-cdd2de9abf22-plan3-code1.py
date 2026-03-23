from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the three fruits) and domain (price ranks)
fruits = ["kiwis", "oranges", "watermelons"]
ranks = range(1, 4)  # 1=cheapest, 2=middle, 3=most expensive
problem.addVariables(fruits, ranks)

# Add constraints based on the puzzle's statements
# 1. All fruits must have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The oranges are more expensive than the kiwis" → kiwis < oranges
problem.addConstraint(lambda kiwis, oranges: kiwis < oranges, ("kiwis", "oranges"))

# 3. "The oranges are less expensive than the watermelons" → oranges < watermelons
problem.addConstraint(lambda oranges, watermelons: oranges < watermelons, ("oranges", "watermelons"))

# Solve for the arrangement
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "kiwis",
    "B": "oranges",
    "C": "watermelons"
}

# Find the cheapest fruit (rank 1) and print corresponding letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 1:
            print(letter)