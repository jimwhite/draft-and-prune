from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (1=most expensive, 7=cheapest)
fruits = ["cantaloupes", "plums", "mangoes", "apples", "loquats", "pears", "peaches"]
domain = range(1, 8)
problem.addVariables(fruits, domain)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The apples are less expensive than the cantaloupes" 
# → apples is cheaper ⇒ higher rank number
problem.addConstraint(lambda apples, cantaloupes: apples > cantaloupes, ("apples", "cantaloupes"))

# "The apples are more expensive than the peaches"
# → apples is more expensive ⇒ lower rank number
problem.addConstraint(lambda apples, peaches: apples < peaches, ("apples", "peaches"))

# "The mangoes are the fourth-most expensive"
problem.addConstraint(lambda mangoes: mangoes == 4, ("mangoes",))

# "The peaches are more expensive than the plums"
problem.addConstraint(lambda peaches, plums: peaches < plums, ("peaches", "plums"))

# "The pears are the third-most expensive"
problem.addConstraint(lambda pears: pears == 3, ("pears",))

# "The loquats are the third-cheapest"
# → third from cheapest end: cheapest=7, second-cheapest=6, third-cheapest=5
problem.addConstraint(lambda loquats: loquats == 5, ("loquats",))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to fruits
choices = {
    "A": "cantaloupes",
    "B": "plums",
    "C": "mangoes",
    "D": "apples",
    "E": "loquats",
    "F": "pears",
    "G": "peaches"
}

# Find which fruit has rank 2 (second-most expensive)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 2:
            print(letter)