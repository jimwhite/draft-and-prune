from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 5=most expensive)
fruits = ["watermelons", "oranges", "loquats", "plums", "kiwis"]
ranks = range(1, 6)
problem.addVariables(fruits, ranks)

# Add constraints based on the problem description
# 1. All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The plums are less expensive than the kiwis" → plums < kiwis
problem.addConstraint(lambda plums, kiwis: plums < kiwis, ("plums", "kiwis"))

# 3. "The plums are more expensive than the watermelons" → watermelons < plums
problem.addConstraint(lambda watermelons, plums: watermelons < plums, ("watermelons", "plums"))

# 4. "The loquats are more expensive than the kiwis" → kiwis < loquats
problem.addConstraint(lambda kiwis, loquats: kiwis < loquats, ("kiwis", "loquats"))

# 5. "The oranges are the most expensive" → oranges == 5
problem.addConstraint(lambda oranges: oranges == 5, ("oranges",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "watermelons",
    "B": "oranges",
    "C": "loquats",
    "D": "plums",
    "E": "kiwis"
}

# Find the fruit with rank 2 (second-cheapest) and print corresponding letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 2:
            print(letter)