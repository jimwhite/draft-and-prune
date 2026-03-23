from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the seven fruits) and domain (price ranks 1-7, where 1=cheapest, 7=most expensive)
fruits = ["oranges", "plums", "loquats", "apples", "kiwis", "cantaloupes", "peaches"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add constraints based on the puzzle's statements
# 1. All fruits must have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The loquats are less expensive than the kiwis" → loquats < kiwis
problem.addConstraint(lambda loquats, kiwis: loquats < kiwis, ("loquats", "kiwis"))

# 3. "The plums are the cheapest" → plums == 1
problem.addConstraint(lambda plums: plums == 1, ("plums",))

# 4. "The loquats are the fourth-most expensive" → in ascending order (1=cheapest, 7=most expensive), 
#    fourth-most expensive = rank 4 (since most expensive=7, second=6, third=5, fourth=4)
problem.addConstraint(lambda loquats: loquats == 4, ("loquats",))

# 5. "The peaches are less expensive than the oranges" → peaches < oranges
problem.addConstraint(lambda peaches, oranges: peaches < oranges, ("peaches", "oranges"))

# 6. "The peaches are more expensive than the kiwis" → kiwis < peaches
problem.addConstraint(lambda kiwis, peaches: kiwis < peaches, ("kiwis", "peaches"))

# 7. "The apples are the second-cheapest" → apples == 2
problem.addConstraint(lambda apples: apples == 2, ("apples",))

# Solve for the arrangement
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "oranges",
    "B": "plums",
    "C": "loquats",
    "D": "apples",
    "E": "kiwis",
    "F": "cantaloupes",
    "G": "peaches"
}

# Find the fruit that is third-most expensive (rank 5 in our system: 7=most, 6=second, 5=third)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 5:
            print(letter)