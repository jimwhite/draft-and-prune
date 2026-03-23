from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the variables (the seven fruits) and the domain (their cost rank)
# Let's use ranks 1 to 7, where 1 is the cheapest and 7 is the most expensive.
fruits = ["loquats", "peaches", "watermelons", "plums", "kiwis", "mangoes", "pears"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add constraints based on the puzzle's statements
# 1. All fruits must have a different cost rank.
problem.addConstraint(AllDifferentConstraint())

# 2. "The pears are more expensive than the kiwis." (kiwis < pears)
problem.addConstraint(lambda kiwis, pears: kiwis < pears, ("kiwis", "pears"))

# 3. "The watermelons are less expensive than the peaches." (watermelons < peaches)
problem.addConstraint(lambda watermelons, peaches: watermelons < peaches, ("watermelons", "peaches"))

# 4. "The mangoes are the third-cheapest." (rank 3)
problem.addConstraint(lambda mangoes: mangoes == 3, ("mangoes",))

# 5. "The watermelons are the third-most expensive." (rank 5: 7=most, 6=2nd most, 5=3rd most)
problem.addConstraint(lambda watermelons: watermelons == 5, ("watermelons",))

# 6. "The plums are the second-most expensive." (rank 6)
problem.addConstraint(lambda plums: plums == 6, ("plums",))

# 7. "The loquats are the second-cheapest." (rank 2)
problem.addConstraint(lambda loquats: loquats == 2, ("loquats",))

# Find the unique solution to the problem
solutions = problem.getSolutions()

# The question asks which fruit is the cheapest (rank 1)
choices = {
    "A": "loquats",
    "B": "peaches",
    "C": "watermelons",
    "D": "plums",
    "E": "kiwis",
    "F": "mangoes",
    "G": "pears"
}

# Check the solution to find which fruit has rank 1 and print its corresponding letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 1:
            print(letter)