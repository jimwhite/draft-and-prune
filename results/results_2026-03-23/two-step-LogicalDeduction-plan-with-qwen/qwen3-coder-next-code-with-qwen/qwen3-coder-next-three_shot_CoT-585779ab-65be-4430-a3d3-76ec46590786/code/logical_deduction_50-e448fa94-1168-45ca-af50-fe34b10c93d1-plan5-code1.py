from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5, where 1 is leftmost)
birds = ["crow", "falcon", "hawk", "robin", "quail"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints based on the problem statements
# 1. All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The robin is the second from the left" → robin == 2
problem.addConstraint(lambda robin: robin == 2, ["robin"])

# 3. "The hawk is the second from the right" → hawk == 4
problem.addConstraint(lambda hawk: hawk == 4, ["hawk"])

# 4. "The robin is to the right of the falcon" → falcon < robin (i.e., falcon < 2)
problem.addConstraint(lambda falcon, robin: falcon < robin, ["falcon", "robin"])

# 5. "The quail is to the left of the hawk" → quail < hawk (i.e., quail < 4)
problem.addConstraint(lambda quail, hawk: quail < hawk, ["quail", "hawk"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to birds for the question: "Which bird is third from the left?"
choices = {
    "A": "crow",
    "B": "falcon",
    "C": "hawk",
    "D": "robin",
    "E": "quail"
}

# Find which bird is at position 3 (third from the left)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 3:
            print(letter)