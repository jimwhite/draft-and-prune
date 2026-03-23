from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks 1=cheapest, 7=most expensive)
fruits = ["oranges", "loquats", "apples", "kiwis", "mangoes", "plums", "peaches"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add explicit rank constraints based on the problem statement:
# "The peaches are the cheapest" → peach rank = 1
problem.addConstraint(lambda peaches: peaches == 1, ["peaches"])

# "The apples are the second-cheapest" → apple rank = 2
problem.addConstraint(lambda apples: apples == 2, ["apples"])

# "The loquats are the third-cheapest" → loquat rank = 3
problem.addConstraint(lambda loquats: loquats == 3, ["loquats"])

# "The plums are the fourth-most expensive" → rank = 4 (since 7-4+1=4)
problem.addConstraint(lambda plums: plums == 4, ["plums"])

# Add comparative rank constraints:
# "The kiwis are more expensive than the mangoes" → kiwi rank > mango rank
problem.addConstraint(lambda kiwis, mangoes: kiwis > mangoes, ["kiwis", "mangoes"])

# "The oranges are less expensive than the mangoes" → orange rank < mango rank
problem.addConstraint(lambda oranges, mangoes: oranges < mangoes, ["oranges", "mangoes"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "oranges",
    "B": "loquats",
    "C": "apples",
    "D": "kiwis",
    "E": "mangoes",
    "F": "plums",
    "G": "peaches"
}

# Find the fruit with rank 7 (most expensive) and print corresponding choice letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 7:
            print(letter)