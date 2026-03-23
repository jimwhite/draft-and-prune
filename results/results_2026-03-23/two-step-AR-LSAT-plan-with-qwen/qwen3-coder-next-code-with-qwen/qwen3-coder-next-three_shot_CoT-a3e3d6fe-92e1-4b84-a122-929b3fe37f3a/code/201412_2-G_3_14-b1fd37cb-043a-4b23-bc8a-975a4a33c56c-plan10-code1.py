from z3 import *
import itertools

# Color indices: 0=forest, 1=olive, 2=peach, 3=turquoise, 4=white, 5=yellow
colors = ["forest", "olive", "peach", "turquoise", "white", "yellow"]
color_indices = {c: i for i, c in enumerate(colors)}

# Generate all subsets of 5 colors from the 6 available
all_color_sets = list(itertools.combinations(range(6), 5))

# Store all possible pairs of solid rug colors that can occur
valid_solid_pairs = set()

for color_set in all_color_sets:
    # For each subset of 5 colors, generate all ways to partition into exactly two solid rugs and one multicolored rug
    # Since we need exactly 2 solid rugs, the partition must be of sizes (1, 1, 3)
    # Choose which two colors are solid (size-1 rugs), the remaining 3 go to the multicolored rug
    
    for solid_colors in itertools.combinations(color_set, 2):
        # The multicolored rug gets the remaining 3 colors
        multi_colors = tuple(c for c in color_set if c not in solid_colors)
        
        # Check rules for each rug
        valid = True
        
        # Rule 1: If white is used in a rug, two other colors must also be used (rug size >= 3)
        # Since solid rugs have size 1, white cannot be in a solid rug
        if color_indices["white"] in solid_colors:
            valid = False
        
        # Rule 2: If olive is used, peach must also be used in the same rug
        # So if olive is in a solid rug, it's invalid (needs peach too)
        if color_indices["olive"] in solid_colors and color_indices["peach"] not in solid_colors:
            valid = False
        if color_indices["olive"] in multi_colors and color_indices["peach"] not in multi_colors:
            valid = False
        # Also, if olive and peach are split (one solid, one in multi), invalid
        if color_indices["olive"] in solid_colors and color_indices["peach"] in multi_colors:
            valid = False
        if color_indices["olive"] in multi_colors and color_indices["peach"] in solid_colors:
            valid = False
        
        # Rule 3: Forest and turquoise not used together in same rug
        if color_indices["forest"] in multi_colors and color_indices["turquoise"] in multi_colors:
            valid = False
        # They can't be split either since they're in different rugs, but the rule says "not used together"
        # So only check same rug
        if color_indices["forest"] in solid_colors and color_indices["turquoise"] in solid_colors:
            valid = False
        
        # Rule 4: Peach and turquoise not used together in same rug
        if color_indices["peach"] in multi_colors and color_indices["turquoise"] in multi_colors:
            valid = False
        if color_indices["peach"] in solid_colors and color_indices["turquoise"] in solid_colors:
            valid = False
        
        # Rule 5: Peach and yellow not used together in same rug
        if color_indices["peach"] in multi_colors and color_indices["yellow"] in multi_colors:
            valid = False
        if color_indices["peach"] in solid_colors and color_indices["yellow"] in solid_colors:
            valid = False
        
        if valid:
            # Record the pair of solid rug colors (as a sorted tuple to avoid ordering issues)
            valid_solid_pairs.add(tuple(sorted(solid_colors)))

# Answer choices (pairs of colors to check if they can be the two solid rugs)
answer_choices = [
    ("forest", "peach"),      # indices (0, 2)
    ("forest", "yellow"),     # indices (0, 5)
    ("peach", "turquoise"),   # indices (2, 3)
    ("peach", "yellow"),      # indices (2, 5)
    ("turquoise", "yellow")   # indices (3, 5)
]

# Convert answer choices to index pairs
answer_pairs = [tuple(sorted((color_indices[c1], color_indices[c2]))) for c1, c2 in answer_choices]

# Find which pairs are impossible (not in valid_solid_pairs)
answer_index_list = []
for idx, pair in enumerate(answer_pairs):
    if pair not in valid_solid_pairs:
        answer_index_list.append(idx)

print(answer_index_list)