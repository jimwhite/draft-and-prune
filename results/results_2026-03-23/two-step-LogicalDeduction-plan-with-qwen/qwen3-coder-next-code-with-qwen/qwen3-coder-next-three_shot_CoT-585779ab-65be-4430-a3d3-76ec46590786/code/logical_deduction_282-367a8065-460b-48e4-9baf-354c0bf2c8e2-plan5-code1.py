from constraint import *

problem = Problem()

birds = ["quail", "owl", "hummingbird"]
positions = range(1, 4)
problem.addVariables(birds, positions)

problem.addConstraint(AllDifferentConstraint())

problem.addConstraint(lambda quail, owl: quail < owl, ["quail", "owl"])

problem.addConstraint(lambda owl, hummingbird: owl < hummingbird, ["owl", "hummingbird"])

solutions = problem.getSolutions()

choices = {
    "A": "quail",
    "B": "owl",
    "C": "hummingbird"
}

for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 3:
            print(letter)