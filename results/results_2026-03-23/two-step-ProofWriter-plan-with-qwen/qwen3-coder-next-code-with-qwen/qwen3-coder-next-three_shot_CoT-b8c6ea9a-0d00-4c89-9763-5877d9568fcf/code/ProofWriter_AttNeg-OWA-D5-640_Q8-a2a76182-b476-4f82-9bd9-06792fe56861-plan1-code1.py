# Facts
facts = [
    ("is_rough", "Bob", True),
    ("is_furry", "Dave", True),
    ("is_nice", "Dave", True),
    ("is_red", "Dave", False),
    ("is_smart", "Dave", True),
    ("is_green", "Fiona", True),
    ("is_nice", "Fiona", True),
    ("is_blue", "Harry", True),
    ("is_furry", "Harry", True),
    ("is_green", "Harry", True),
    ("is_nice", "Harry", True),
    ("is_red", "Harry", False),
    ("is_rough", "Harry", True),
    ("is_smart", "Harry", True)
]

# Rules (as logical implications)
rules = [
    # Smart things are green
    lambda x: ("is_smart", x, True) >> ("is_green", x, True),
    
    # If something is nice and not rough then it is red
    lambda x: ("is_nice", x, True) & ~("is_rough", x, True) >> ("is_red", x, True),
    
    # If something is nice then it is smart
    lambda x: ("is_nice", x, True) >> ("is_smart", x, True),
    
    # If something is rough then it is nice
    lambda x: ("is_rough", x, True) >> ("is_nice", x, True),
    
    # If something is blue then it is furry
    lambda x: ("is_blue", x, True) >> ("is_furry", x, True),
    
    # All blue, smart things are furry
    lambda x: ("is_blue", x, True) & ("is_smart", x, True) >> ("is_furry", x, True),
    
    # If Bob is furry and Bob is not rough then Bob is green
    lambda: ("is_furry", "Bob", True) & ~("is_rough", "Bob", True) >> ("is_green", "Bob", True),
    
    # If something is green then it is blue
    lambda x: ("is_green", x, True) >> ("is_blue", x, True),
    
    # If something is red and not nice then it is not blue
    lambda x: ("is_red", x, True) & ~("is_nice", x, True) >> ("is_blue", x, False)
]

# Query: Bob is not green
query = ~("is_green", "Bob", True)