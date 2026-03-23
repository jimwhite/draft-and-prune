from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the variables (the seven fruits) and the domain (price ranks)
# 1 = cheapest, 7 = most expensive
fruits = ["watermelons", "mangoes", "kiwis", "pears", "cantaloupes", "oranges", "peaches"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add constraints based on the puzzle's statements
# 1. All fruits must have a unique price rank
problem.addConstraint(AllDifferentConstraint())

# 2. "The oranges are more expensive than the peaches" → peaches > oranges
problem.addConstraint(lambda oranges, peaches: peaches > oranges, ("oranges", "peaches"))

# 3. "The cantaloupes are the fourth-most expensive" → rank 4
problem.addConstraint(lambda cantaloupes: cantaloupes == 4, ("cantaloupes",))

# 4. "The pears are less expensive than the cantaloupes" → pears < cantaloupes
problem.addConstraint(lambda pears, cantaloupes: pears < cantaloupes, ("pears", "cantaloupes"))

# 5. "The peaches are the second-most expensive" → rank 6
problem.addConstraint(lambda peaches: peaches == 6, ("peaches",))

# 6. "The mangoes are the cheapest" → rank 1
problem.addConstraint(lambda mangoes: mangoes == 1, ("mangoes",))

# 7. "The kiwis are the third-cheapest" → rank 3
problem.addConstraint(lambda kiwis: kiwis == 3, ("kiwis",))

# Find the solution(s)
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "watermelons",
    "B": "mangoes",
    "C": "kiwis",
    "D": "pears",
    "E": "cantaloupes",
    "F": "oranges",
    "G": "peaches"
}

# Find which fruit is the cheapest (rank 1) and print its corresponding letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 1:
            print(letter)