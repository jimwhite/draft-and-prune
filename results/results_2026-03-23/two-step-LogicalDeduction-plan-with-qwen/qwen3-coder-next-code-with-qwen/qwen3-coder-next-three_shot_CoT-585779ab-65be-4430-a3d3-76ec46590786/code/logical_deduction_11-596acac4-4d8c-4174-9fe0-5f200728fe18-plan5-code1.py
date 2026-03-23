from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 5=newest)
vehicles = ["convertible", "truck", "bus", "sedan", "motorcyle"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints based on the puzzle statements
# 1. All vehicles have different age ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The bus is newer than the truck" → bus > truck
problem.addConstraint(lambda truck, bus: truck < bus, ("truck", "bus"))

# 3. "The truck is newer than the convertible" → truck > convertible
problem.addConstraint(lambda convertible, truck: convertible < truck, ("convertible", "truck"))

# 4. "The sedan is the second-oldest" → sedan == 2
problem.addConstraint(lambda sedan: sedan == 2, ("sedan",))

# 5. "The motorcyle is newer than the bus" → motorcyle > bus
problem.addConstraint(lambda bus, motorcyle: bus < motorcyle, ("bus", "motorcyle"))

# Solve for the arrangement
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    "A": "convertible",
    "B": "truck",
    "C": "bus",
    "D": "sedan",
    "E": "motorcyle"
}

# Find which vehicle is the newest (rank 5) and print corresponding letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 5:
            print(letter)