from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the seven fruits as variables
fruits = ["kiwis", "plums", "mangoes", "watermelons", "pears", "peaches", "oranges"]

# Define the domain: integers 1 to 7, where 1 = cheapest, 7 = most expensive
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add constraints based on the problem description
# 1. All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The pears are the third-cheapest" → pears == 3
problem.addConstraint(lambda pears: pears == 3, ["pears"])

# 3. "The kiwis are the second-most expensive" → kiwis == 6
problem.addConstraint(lambda kiwis: kiwis == 6, ["kiwis"])

# 4. "The pears are more expensive than the plums" → plums < pears
problem.addConstraint(lambda plums, pears: plums < pears, ["plums", "pears"])

# 5. "The oranges are less expensive than the kiwis" → oranges < kiwis
problem.addConstraint(lambda oranges, kiwis: oranges < kiwis, ["oranges", "kiwis"])

# 6. "The mangoes are the third-most expensive" → mangoes == 5
problem.addConstraint(lambda mangoes: mangoes == 5, ["mangoes"])

# 7. "The peaches are the second-cheapest" → peaches == 2
problem.addConstraint(lambda peaches: peaches == 2, ["peaches"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "kiwis",
    "B": "plums",
    "C": "mangoes",
    "D": "watermelons",
    "E": "pears",
    "F": "peaches",
    "G": "oranges"
}

# Find the cheapest fruit (rank 1) and print the corresponding choice letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 1:
            print(letter)