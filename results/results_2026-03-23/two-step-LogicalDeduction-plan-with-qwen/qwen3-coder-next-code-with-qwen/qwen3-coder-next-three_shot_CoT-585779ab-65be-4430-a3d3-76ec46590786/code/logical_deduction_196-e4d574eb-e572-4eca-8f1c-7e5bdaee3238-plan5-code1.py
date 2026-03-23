from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the seven fruits) and domain (price ranks 1 to 7, where 1=cheapest, 7=most expensive)
fruits = ["oranges", "loquats", "apples", "kiwis", "mangoes", "plums", "peaches"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add constraints based on the puzzle's statements
# 1. All fruits must have a unique price rank
problem.addConstraint(AllDifferentConstraint())

# 2. "The apples are the second-cheapest" → rank 2
problem.addConstraint(lambda apples: apples == 2, ["apples"])

# 3. "The peaches are the cheapest" → rank 1
problem.addConstraint(lambda peaches: peaches == 1, ["peaches"])

# 4. "The plums are the fourth-most expensive" → rank 4 (since 7-4+1=4 in ascending order)
problem.addConstraint(lambda plums: plums == 4, ["plums"])

# 5. "The loquats are the third-cheapest" → rank 3
problem.addConstraint(lambda loquats: loquats == 3, ["loquats"])

# 6. "The kiwis are more expensive than the mangoes" → mangoes < kiwis (lower rank = cheaper)
problem.addConstraint(lambda mangoes, kiwis: mangoes < kiwis, ["mangoes", "kiwis"])

# 7. "The oranges are less expensive than the mangoes" → oranges < mangoes
problem.addConstraint(lambda oranges, mangoes: oranges < mangoes, ["oranges", "mangoes"])

# Solve the problem
solutions = problem.getSolutions()

# In our ranking system (1=cheapest, 7=most expensive), third-most expensive = rank 5
# (since 1=cheapest, 2, 3, 4, 5=third-most expensive, 6, 7=most expensive)
# Create mapping from choice letters to fruit names
choices = {
    "A": "oranges",
    "B": "loquats",
    "C": "apples",
    "D": "kiwis",
    "E": "mangoes",
    "F": "plums",
    "G": "peaches"
}

# Find which fruit has rank 5 (third-most expensive) and print the corresponding letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 5:
            print(letter)