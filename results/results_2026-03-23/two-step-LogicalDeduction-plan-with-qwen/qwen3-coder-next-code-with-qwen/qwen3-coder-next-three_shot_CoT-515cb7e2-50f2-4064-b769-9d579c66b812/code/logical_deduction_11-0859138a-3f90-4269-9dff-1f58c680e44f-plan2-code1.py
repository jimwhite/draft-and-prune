from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 5=newest)
vehicles = ["convertible", "truck", "bus", "sedan", "motorcyle"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints based on the problem description
# 1. All vehicles have different age ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The bus is newer than the truck" → bus > truck
problem.addConstraint(lambda bus, truck: bus > truck, ("bus", "truck"))

# 3. "The truck is newer than the convertible" → truck > convertible
problem.addConstraint(lambda truck, convertible: truck > convertible, ("truck", "convertible"))

# 4. "The sedan is the second-oldest" → sedan == 2
problem.addConstraint(lambda sedan: sedan == 2, ("sedan",))

# 5. "The motorcyle is newer than the bus" → motorcyle > bus
problem.addConstraint(lambda motorcyle, bus: motorcyle > bus, ("motorcyle", "bus"))

# Get the solution(s)
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