from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the seven fruits) and domain (price ranks 1-7, where 1=cheapest, 7=most expensive)
fruits = ["watermelons", "cantaloupes", "pears", "peaches", "mangoes", "kiwis", "oranges"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add constraints based on the puzzle's statements
# 1. All fruits must have a different price rank.
problem.addConstraint(AllDifferentConstraint())

# 2. "The oranges are more expensive than the cantaloupes."
problem.addConstraint(lambda oranges, cantaloupes: oranges > cantaloupes, ("oranges", "cantaloupes"))

# 3. "The pears are less expensive than the kiwis."
problem.addConstraint(lambda pears, kiwis: pears < kiwis, ("pears", "kiwis"))

# 4. "The kiwis are the fourth-most expensive."
problem.addConstraint(lambda kiwis: kiwis == 4, ("kiwis",))

# 5. "The mangoes are less expensive than the pears."
problem.addConstraint(lambda mangoes, pears: mangoes < pears, ("mangoes", "pears"))

# 6. "The peaches are the cheapest."
problem.addConstraint(lambda peaches: peaches == 1, ("peaches",))

# 7. "The cantaloupes are more expensive than the watermelons."
problem.addConstraint(lambda cantaloupes, watermelons: cantaloupes > watermelons, ("cantaloupes", "watermelons"))

# Find the solution(s)
solutions = problem.getSolutions()

# The question asks which fruit is the most expensive (rank 7)
choices = {
    "A": "watermelons",
    "B": "cantaloupes",
    "C": "pears",
    "D": "peaches",
    "E": "mangoes",
    "F": "kiwis",
    "G": "oranges"
}

# Find the fruit with rank 7 and print its corresponding choice letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 7:
            print(letter)