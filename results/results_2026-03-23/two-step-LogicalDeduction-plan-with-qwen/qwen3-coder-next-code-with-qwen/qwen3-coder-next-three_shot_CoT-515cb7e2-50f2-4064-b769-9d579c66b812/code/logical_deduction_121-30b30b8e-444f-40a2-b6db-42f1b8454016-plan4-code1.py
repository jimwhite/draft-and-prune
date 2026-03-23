from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 7=most expensive)
fruits = ["loquats", "peaches", "watermelons", "plums", "kiwis", "mangoes", "pears"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "The pears are more expensive than the kiwis" → kiwis < pears
problem.addConstraint(lambda kiwis, pears: kiwis < pears, ("kiwis", "pears"))

# "The watermelons are less expensive than the peaches" → watermelons < peaches
problem.addConstraint(lambda watermelons, peaches: watermelons < peaches, ("watermelons", "peaches"))

# "The mangoes are the third-cheapest" → mangoes == 3
problem.addConstraint(lambda mangoes: mangoes == 3, ("mangoes",))

# "The watermelons are the third-most expensive" → rank = 5 (7-3+1=5)
problem.addConstraint(lambda watermelons: watermelons == 5, ("watermelons",))

# "The plums are the second-most expensive" → rank = 6
problem.addConstraint(lambda plums: plums == 6, ("plums",))

# "The loquats are the second-cheapest" → loquats == 2
problem.addConstraint(lambda loquats: loquats == 2, ("loquats",))

# Solve the problem
solutions = problem.getSolutions()

# The question asks which fruit is third-cheapest (rank 3)
# According to constraints, mangoes should be rank 3
# Let's verify and output the correct choice

# Map choices to fruits
choices = {
    "A": "loquats",
    "B": "peaches",
    "C": "watermelons",
    "D": "plums",
    "E": "kiwis",
    "F": "mangoes",
    "G": "pears"
}

# Find which fruit has rank 3
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 3:
            print(letter)