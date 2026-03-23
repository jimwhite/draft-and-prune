# --- Facts ---
facts:
needs("cat", "dog")
is_kind("dog")
needs("dog", "rabbit")
eats("rabbit", "dog")
is_green("rabbit")
chases("tiger", "rabbit")
is_big("tiger")

# --- Rules ---
defrules:
    # Rule 1: If something is nice and it eats the tiger then it needs the dog
    (nice(?x) and eats(?x, "tiger")) -> needs(?x, "dog")
    
    # Rule 2: If something chases the cat then it eats the cat
    (chases(?x, "cat")) -> eats(?x, "cat")
    
    # Rule 3: If the dog chases the tiger then the tiger needs the rabbit
    (chases("dog", "tiger")) -> needs("tiger", "rabbit")
    
    # Rule 4: If the rabbit chases the tiger then the rabbit chases the cat
    (chases("rabbit", "tiger")) -> chases("rabbit", "cat")
    
    # Rule 5: If something chases the cat then the cat is kind
    (chases(?x, "cat")) -> is_kind("cat")
    
    # Rule 6: If something eats the dog then it chases the cat
    (eats(?x, "dog")) -> chases(?x, "cat")
    
    # Rule 7: If something is rough then it eats the dog
    (is_rough(?x)) -> eats(?x, "dog")
    
    # Rule 8: If something is kind then it is rough
    (is_kind(?x)) -> is_rough(?x)
    
    # Rule 9: If something eats the rabbit and the rabbit is big then it is kind
    (eats(?x, "rabbit") and is_big("rabbit")) -> is_kind(?x)

# --- Query ---
goals:
not(is_rough("cat"))