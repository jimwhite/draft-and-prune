from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 7=most expensive)
fruits = ["oranges", "loquats", "apples", "kiwis", "mangoes", "plums", "peaches"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add constraints
# All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# "The apples are the second-cheapest"
problem.addConstraint(lambda apples: apples == 2, ["apples"])

# "The peaches are the cheapest"
problem.addConstraint(lambda peaches: peaches == 1, ["peaches"])

# "The plums are the fourth-most expensive"
# Since most expensive is 7, fourth-most expensive = 7 - 3 = 4
problem.addConstraint(lambda plums: plums == 4, ["plums"])

# "The loquats are the third-cheapest"
problem.addConstraint(lambda loquats: loquats == 3, ["loquats"])

# "The kiwis are more expensive than the mangoes"
problem.addConstraint(lambda kiwis, mangoes: kiwis > mangoes, ["kiwis", "mangoes"])

# "The oranges are less expensive than the mangoes"
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

# Find which fruit is the most expensive (rank 7)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 7:
            print(letter)