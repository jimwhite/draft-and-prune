from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the three fruits) and domain (price ranks)
fruits = ["mangoes", "watermelons", "kiwis"]
ranks = range(1, 4)  # 1=cheapest, 3=most expensive
problem.addVariables(fruits, ranks)

# Add constraints based on the puzzle's statements
# 1. All fruits must have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The watermelons are less expensive than the kiwis"
# (watermelons have a lower rank number than kiwis)
problem.addConstraint(lambda watermelons, kiwis: watermelons < kiwis, ("watermelons", "kiwis"))

# 3. "The kiwis are the second-most expensive"
# (second-most expensive among three items means rank 2)
problem.addConstraint(lambda kiwis: kiwis == 2, ("kiwis",))

# Solve for the unique arrangement
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "mangoes",
    "B": "watermelons",
    "C": "kiwis"
}

# Find which fruit is the cheapest (rank 1) and print corresponding letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 1:
            print(letter)